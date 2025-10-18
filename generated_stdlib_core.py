from __future__ import annotations

from enum import Enum

from typing import Generic, TypeVar

E = TypeVar('E')
F = TypeVar('F')
T = TypeVar('T')
U = TypeVar('U')


@dataclass
class Some(Generic[T]):
    value: T

@dataclass
class None_:
    pass


Option = Union[Some[T], None_]


@dataclass
class Ok(Generic[T, E]):
    value: T

@dataclass
class Err(Generic[T, E]):
    value: E


Result = Union[Ok[T, E], Err[T, E]]


def option_some(value: T) -> Option[T]:
    # Unknown statement: IRLiteral
    return Option.Some(value)


def option_none() -> Option[T]:
    # Unknown statement: IRLiteral
    return None_()


def option_map(opt: Option[T], fn: function[T]) -> Option[U]:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        val = opt.value
        return Some(value=fn(val))
    else:
        return None_()


def option_and_then(opt: Option[T], fn: function[T]) -> Option[U]:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        val = opt.value
        return fn(val)
    else:
        return None_()


def option_unwrap_or(opt: Option[T], default: T) -> T:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        val = opt.value
        return val
    else:
        return default


def option_unwrap_or_else(opt: Option[T], fn: function) -> T:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        val = opt.value
        return val
    else:
        return fn()


def option_is_some(opt: Option[T]) -> bool:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        return True
    else:
        return False


def option_is_none(opt: Option[T]) -> bool:
    # Unknown statement: IRLiteral
    if isinstance(opt, None_):
        return True
    else:
        return False


def option_match(opt: Option[T], some_fn: function[T], none_fn: function) -> U:
    # Unknown statement: IRLiteral
    if isinstance(opt, Some):
        val = opt.value
        return some_fn(val)
    else:
        return none_fn()


def result_ok(value: T) -> Result[T, E]:
    # Unknown statement: IRLiteral
    return Result.Ok(value)


def result_err(error: E) -> Result[T, E]:
    # Unknown statement: IRLiteral
    return Result.Err(error)


def result_map(res: Result[T, E], fn: function[T]) -> Result[U, E]:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        val = res.value
        return Ok(value=fn(val))
    else:
        if isinstance(res, Err):
            e = res.value
            return Err(value=e)


def result_map_err(res: Result[T, E], fn: function[E]) -> Result[T, F]:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        val = res.value
        return Ok(value=val)
    else:
        if isinstance(res, Err):
            e = res.value
            return Err(value=fn(e))


def result_and_then(res: Result[T, E], fn: function[T]) -> Result[U, E]:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        val = res.value
        return fn(val)
    else:
        if isinstance(res, Err):
            e = res.value
            return Err(value=e)


def result_unwrap_or(res: Result[T, E], default: T) -> T:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        val = res.value
        return val
    else:
        return default


def result_is_ok(res: Result[T, E]) -> bool:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        return True
    else:
        return False


def result_is_err(res: Result[T, E]) -> bool:
    # Unknown statement: IRLiteral
    if isinstance(res, Err):
        return True
    else:
        return False


def result_match(res: Result[T, E], ok_fn: function[T], err_fn: function[E]) -> U:
    # Unknown statement: IRLiteral
    if isinstance(res, Ok):
        val = res.value
        return ok_fn(val)
    else:
        if isinstance(res, Err):
            e = res.value
            return err_fn(e)
