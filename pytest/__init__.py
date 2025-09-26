from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Sequence, Tuple

__all__ = ["mark", "raises", "fixture", "skip", "SkipTest", "MonkeyPatch", "GLOBAL_FIXTURES"]


def _normalize_argnames(argnames: Any) -> List[str]:
    if isinstance(argnames, str):
        return [segment.strip() for segment in argnames.split(",") if segment.strip()]
    return list(argnames)


def _ensure_sequence(values: Any) -> Sequence[Any]:
    if isinstance(values, (list, tuple)):
        return values
    return list(values)


@dataclass
class _Parametrization:
    argnames: List[str]
    values: Sequence[Any]
    ids: Any


class _Mark:
    def parametrize(self, argnames: Any, values: Iterable[Any], ids: Any = None):
        arg_list = _normalize_argnames(argnames)
        values_seq = _ensure_sequence(values)

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            stack: List[_Parametrization] = getattr(func, "__pytest_parametrize__", [])
            stack.append(_Parametrization(arg_list, values_seq, ids))
            setattr(func, "__pytest_parametrize__", stack)
            return func

        return decorator


mark = _Mark()


class _RaisesContext:
    def __init__(self, expected: type[BaseException]) -> None:
        self.expected = expected

    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        if exc_type is None:
            raise AssertionError(f"Did not raise {self.expected.__name__}")
        if not issubclass(exc_type, self.expected):
            return False
        return True


def raises(expected: type[BaseException]) -> _RaisesContext:
    return _RaisesContext(expected)


def iter_parametrization(func: Callable[..., Any]):
    specs: List[_Parametrization] = getattr(func, "__pytest_parametrize__", [])
    if not specs:
        yield {}, func.__name__
        return

    def expand(index: int, current: dict[str, Any], id_parts: List[str]):
        if index >= len(specs):
            case_id = "::".join(id_parts) if id_parts else func.__name__
            yield current, case_id
            return
        spec = specs[index]
        for idx, value in enumerate(spec.values):
            if len(spec.argnames) == 1:
                values = [value]
            else:
                if not isinstance(value, (list, tuple)):
                    raise TypeError("Parametrized values must be sequences for multiple arguments")
                values = list(value)
            next_mapping = current.copy()
            for name, item in zip(spec.argnames, values):
                next_mapping[name] = item
            if callable(spec.ids):
                ident = str(spec.ids(value))
            elif spec.ids is not None:
                ident = str(spec.ids[idx])
            else:
                ident = "-".join(str(v) for v in values)
            expand(index + 1, next_mapping, id_parts + [ident])

    yield from expand(0, {}, [])
def fixture(func=None, **_kwargs):
    def decorator(fn):
        setattr(fn, "__pytest_fixture__", True)
        return fn

    if func is not None:
        return decorator(func)
    return decorator


@fixture
def monkeypatch():
    mp = MonkeyPatch()
    try:
        yield mp
    finally:
        mp.undo()


GLOBAL_FIXTURES = {"monkeypatch": monkeypatch}
class SkipTest(Exception):
    pass


def skip(message: str = "") -> None:
    raise SkipTest(message)


class MonkeyPatch:
    def __init__(self) -> None:
        self._setattrs: list[tuple[Any, str, Any, bool]] = []
        self._delenvs: list[tuple[str, Optional[str]]] = []

    def setattr(self, target: Any, name: str, value: Any, raising: bool = True) -> None:
        has_attr = hasattr(target, name)
        if not has_attr and raising:
            raise AttributeError(f"{target} has no attribute {name}")
        original = getattr(target, name, None)
        setattr(target, name, value)
        self._setattrs.append((target, name, original, has_attr))

    def setenv(self, name: str, value: str) -> None:
        import os

        original = os.environ.get(name)
        os.environ[name] = value
        self._delenvs.append((name, original))

    def undo(self) -> None:
        import os

        while self._setattrs:
            target, name, original, existed = self._setattrs.pop()
            if existed:
                setattr(target, name, original)
            else:
                delattr(target, name)
        while self._delenvs:
            name, original = self._delenvs.pop()
            if original is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = original
