# Promptware Standard Library - Core Types
# Option<T> and Result<T,E> for safe error handling

# ============================================================================
# Option<T> - Represents an optional value (Some or None)
# ============================================================================

enum Option<T>:
    - Some(T)
    - None


# Constructors
function option_some<T>(value: T) -> Option<T>:
    """
    Create an Option with a value.

    Args:
        value: The value to wrap

    Returns:
        Option<T> containing the value

    Example:
        let num = option_some(42)  # Some(42)
    """
    return Option.Some(value)


function option_none<T>() -> Option<T>:
    """
    Create an empty Option.

    Returns:
        Option<T> with no value

    Example:
        let nothing = option_none()  # None
    """
    return Option.None


# Core methods
function option_map<T, U>(opt: Option<T>, fn: function(T) -> U) -> Option<U>:
    """
    Transform the value inside Some, or return None if empty.

    Args:
        opt: The Option to map over
        fn: Function to apply to the value

    Returns:
        Option<U> with transformed value, or None

    Example:
        let num = option_some(5)
        let doubled = option_map(num, fn(x) -> x * 2)  # Some(10)

        let empty = option_none()
        let result = option_map(empty, fn(x) -> x * 2)  # None
    """
    if opt is Some(val):
        return Some(fn(val))
    else:
        return None


function option_and_then<T, U>(opt: Option<T>, fn: function(T) -> Option<U>) -> Option<U>:
    """
    Chain operations that return Option (flatMap).
    Returns None if either the input is None or the function returns None.

    Args:
        opt: The Option to chain from
        fn: Function that returns an Option

    Returns:
        Result of fn if opt is Some, otherwise None

    Example:
        function safe_divide(a: int, b: int) -> Option<int>:
            if b == 0:
                return None
            else:
                return Some(a / b)

        let num = option_some(10)
        let result = option_and_then(num, fn(x) -> safe_divide(x, 2))  # Some(5)
        let bad = option_and_then(num, fn(x) -> safe_divide(x, 0))  # None
    """
    if opt is Some(val):
        return fn(val)
    else:
        return None


function option_unwrap_or<T>(opt: Option<T>, default: T) -> T:
    """
    Return the value or a default if None.

    Args:
        opt: The Option to unwrap
        default: Default value to return if None

    Returns:
        The wrapped value or the default

    Example:
        let num = option_some(42)
        let value = option_unwrap_or(num, 0)  # 42

        let empty = option_none()
        let value2 = option_unwrap_or(empty, 0)  # 0
    """
    if opt is Some(val):
        return val
    else:
        return default


function option_unwrap_or_else<T>(opt: Option<T>, fn: function() -> T) -> T:
    """
    Return the value or compute a default lazily.
    The function is only called if opt is None.

    Args:
        opt: The Option to unwrap
        fn: Function to compute default value

    Returns:
        The wrapped value or the computed default

    Example:
        let num = option_some(42)
        let value = option_unwrap_or_else(num, fn() -> 0)  # 42, fn not called

        let empty = option_none()
        let value2 = option_unwrap_or_else(empty, fn() -> 0)  # 0, fn called
    """
    if opt is Some(val):
        return val
    else:
        return fn()


function option_is_some<T>(opt: Option<T>) -> bool:
    """
    Check if Option contains a value.

    Args:
        opt: The Option to check

    Returns:
        true if Some, false if None

    Example:
        let num = option_some(42)
        let has_value = option_is_some(num)  # true

        let empty = option_none()
        let has_value2 = option_is_some(empty)  # false
    """
    if opt is Some(_):
        return true
    else:
        return false


function option_is_none<T>(opt: Option<T>) -> bool:
    """
    Check if Option is empty.

    Args:
        opt: The Option to check

    Returns:
        true if None, false if Some

    Example:
        let num = option_some(42)
        let is_empty = option_is_none(num)  # false

        let empty = option_none()
        let is_empty2 = option_is_none(empty)  # true
    """
    if opt is None:
        return true
    else:
        return false


function option_match<T, U>(
    opt: Option<T>,
    some_fn: function(T) -> U,
    none_fn: function() -> U
) -> U:
    """
    Pattern match on Option, calling the appropriate function.

    Args:
        opt: The Option to match
        some_fn: Function to call if Some
        none_fn: Function to call if None

    Returns:
        Result of the called function

    Example:
        let num = option_some(42)
        let msg = option_match(
            num,
            fn(x) -> "Got: " + str(x),
            fn() -> "Got nothing"
        )  # "Got: 42"
    """
    if opt is Some(val):
        return some_fn(val)
    else:
        return none_fn()


# ============================================================================
# Result<T,E> - Represents success (Ok) or failure (Err) with typed errors
# ============================================================================

enum Result<T, E>:
    - Ok(T)
    - Err(E)


# Constructors
function result_ok<T, E>(value: T) -> Result<T, E>:
    """
    Create a successful Result.

    Args:
        value: The success value

    Returns:
        Result<T, E> containing the value

    Example:
        let success = result_ok(42)  # Ok(42)
    """
    return Result.Ok(value)


function result_err<T, E>(error: E) -> Result<T, E>:
    """
    Create a failed Result.

    Args:
        error: The error value

    Returns:
        Result<T, E> containing the error

    Example:
        let failure = result_err("something went wrong")  # Err("something went wrong")
    """
    return Result.Err(error)


# Core methods
function result_map<T, E, U>(res: Result<T, E>, fn: function(T) -> U) -> Result<U, E>:
    """
    Transform the Ok value, or pass through the Err.

    Args:
        res: The Result to map over
        fn: Function to apply to Ok value

    Returns:
        Result<U, E> with transformed value, or original Err

    Example:
        let success = result_ok(5)
        let doubled = result_map(success, fn(x) -> x * 2)  # Ok(10)

        let failure = result_err("error")
        let result = result_map(failure, fn(x) -> x * 2)  # Err("error")
    """
    if res is Ok(val):
        return Ok(fn(val))
    else if res is Err(e):
        return Err(e)


function result_map_err<T, E, F>(res: Result<T, E>, fn: function(E) -> F) -> Result<T, F>:
    """
    Transform the Err value, or pass through the Ok.

    Args:
        res: The Result to map over
        fn: Function to apply to Err value

    Returns:
        Result<T, F> with original value or transformed error

    Example:
        let success = result_ok(42)
        let result = result_map_err(success, fn(e) -> "Error: " + e)  # Ok(42)

        let failure = result_err("bad")
        let mapped = result_map_err(failure, fn(e) -> "Error: " + e)  # Err("Error: bad")
    """
    if res is Ok(val):
        return Ok(val)
    else if res is Err(e):
        return Err(fn(e))


function result_and_then<T, E, U>(
    res: Result<T, E>,
    fn: function(T) -> Result<U, E>
) -> Result<U, E>:
    """
    Chain operations that return Result.
    Short-circuits on first Err.

    Args:
        res: The Result to chain from
        fn: Function that returns a Result

    Returns:
        Result of fn if Ok, otherwise original Err

    Example:
        function safe_divide(a: int, b: int) -> Result<int, string>:
            if b == 0:
                return result_err("division by zero")
            else:
                return result_ok(a / b)

        let num = result_ok(10)
        let result = result_and_then(num, fn(x) -> safe_divide(x, 2))  # Ok(5)
        let bad = result_and_then(num, fn(x) -> safe_divide(x, 0))  # Err("division by zero")
    """
    if res is Ok(val):
        return fn(val)
    else if res is Err(e):
        return Err(e)


function result_unwrap_or<T, E>(res: Result<T, E>, default: T) -> T:
    """
    Return the Ok value or a default if Err.

    Args:
        res: The Result to unwrap
        default: Default value to return if Err

    Returns:
        The Ok value or the default

    Example:
        let success = result_ok(42)
        let value = result_unwrap_or(success, 0)  # 42

        let failure = result_err("error")
        let value2 = result_unwrap_or(failure, 0)  # 0
    """
    if res is Ok(val):
        return val
    else:
        return default


function result_is_ok<T, E>(res: Result<T, E>) -> bool:
    """
    Check if Result is Ok.

    Args:
        res: The Result to check

    Returns:
        true if Ok, false if Err

    Example:
        let success = result_ok(42)
        let is_success = result_is_ok(success)  # true

        let failure = result_err("error")
        let is_success2 = result_is_ok(failure)  # false
    """
    if res is Ok(_):
        return true
    else:
        return false


function result_is_err<T, E>(res: Result<T, E>) -> bool:
    """
    Check if Result is Err.

    Args:
        res: The Result to check

    Returns:
        true if Err, false if Ok

    Example:
        let success = result_ok(42)
        let is_error = result_is_err(success)  # false

        let failure = result_err("error")
        let is_error2 = result_is_err(failure)  # true
    """
    if res is Err(_):
        return true
    else:
        return false


function result_match<T, E, U>(
    res: Result<T, E>,
    ok_fn: function(T) -> U,
    err_fn: function(E) -> U
) -> U:
    """
    Pattern match on Result, calling the appropriate function.

    Args:
        res: The Result to match
        ok_fn: Function to call if Ok
        err_fn: Function to call if Err

    Returns:
        Result of the called function

    Example:
        let success = result_ok(42)
        let msg = result_match(
            success,
            fn(x) -> "Success: " + str(x),
            fn(e) -> "Error: " + e
        )  # "Success: 42"
    """
    if res is Ok(val):
        return ok_fn(val)
    else if res is Err(e):
        return err_fn(e)
