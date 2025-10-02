from __future__ import annotations

import argparse
import importlib.util
import inspect
import shutil
import sys
import tempfile
import traceback
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple

from . import GLOBAL_FIXTURES, SkipTest, iter_parametrization


def main() -> None:
    parser = argparse.ArgumentParser(prog="pytest", add_help=False)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--", dest="ignored", nargs="*")
    args = parser.parse_args()

    targets = args.paths or ["tests"]
    files: List[Path] = []
    for target in targets:
        path = Path(target)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("test_*.py") if p.is_file()))
        elif path.is_file():
            files.append(path)
        else:
            print(f"pytest: warning: path not found: {target}", file=sys.stderr)

    if not files:
        print("pytest: no test files found", file=sys.stderr)
        sys.exit(1)

    failures = 0
    total = 0
    for index, file_path in enumerate(files):
        module = _load_module(file_path, index)
        tests, fixtures = _collect_tests(module)
        merged_fixtures = dict(GLOBAL_FIXTURES)
        merged_fixtures.update(fixtures)
        if not tests:
            continue
        fixture_cache: Dict[str, tuple[Any, Optional[Any]]] = {}

        def get_fixture(name: str):
            if name not in fixture_cache:
                fn = merged_fixtures[name]
                value = fn()
                if inspect.isgenerator(value):
                    gen = value
                    try:
                        produced = next(gen)
                    except StopIteration:
                        produced = None
                    fixture_cache[name] = (produced, gen)
                else:
                    fixture_cache[name] = (value, None)
            return fixture_cache[name][0]

        for name, func in tests.items():
            for params, case_id in iter_parametrization(func):
                case_label = f"{file_path}:{name}" if not case_id else f"{file_path}:{case_id}"
                total += 1
                injected = {}
                signature = inspect.signature(func)
                for param_name in signature.parameters:
                    if param_name in params:
                        continue
                    if param_name == "tmp_path":
                        tmp_dir = Path(tempfile.mkdtemp(prefix="pytest_tmp_"))
                        injected[param_name] = tmp_dir
                        continue
                    if param_name in merged_fixtures:
                        injected[param_name] = get_fixture(param_name)
                        continue
                try:
                    func(**{**params, **injected})
                except SkipTest as exc:  # pragma: no cover - optional
                    print(f"SKIPPED: {case_label} - {exc}")
                except Exception:  # noqa: BLE001
                    failures += 1
                    print(f"FAILED: {case_label}")
                    traceback.print_exc()
                finally:
                    if "tmp_path" in injected:
                        shutil.rmtree(injected["tmp_path"], ignore_errors=True)
        for _name, (_value, gen) in fixture_cache.items():
            if gen:
                try:
                    gen.close()
                except Exception:
                    pass
        # remove module to avoid cross-test state
        sys.modules.pop(module.__name__, None)

    if failures:
        print(f"=== {failures} FAILED, {total - failures} passed ===")
        sys.exit(1)
    print(f"=== {total} passed ===")
    sys.exit(0)


def _load_module(path: Path, index: int) -> ModuleType:
    module_name = f"_pytest_module_{index}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _collect_tests(module: ModuleType) -> Tuple[Dict[str, Callable], Dict[str, Callable]]:
    tests: Dict[str, Callable] = {}
    fixtures: Dict[str, Callable] = {}
    for attr_name in dir(module):
        obj = getattr(module, attr_name)
        if inspect.isfunction(obj):
            if attr_name.startswith("test_"):
                tests[attr_name] = obj
            elif getattr(obj, "__pytest_fixture__", False):
                fixtures[attr_name] = obj
    return tests, fixtures


if __name__ == "__main__":
    main()
