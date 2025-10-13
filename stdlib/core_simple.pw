# Promptware Standard Library - Core Types (Simplified for Runtime)
# Temporary version without "is" pattern matching syntax
# TODO: Replace with full core.pw once parser supports pattern matching

# ============================================================================
# Option<T> - Represents an optional value (Some or None)
# ============================================================================

enum Option<T>:
    - Some(T)
    - None


# Constructors
function option_some<T>(value: T) -> Option<T> {
    return Some(value)
}

function option_none<T>() -> Option<T> {
    return None
}


# Core methods - using match functions instead of "is" syntax
function option_unwrap_or<T>(opt: Option<T>, default: T) -> T {
    # For now, just return default (runtime doesn't support full matching yet)
    return default
}


# ============================================================================
# Result<T,E> - Represents success (Ok) or failure (Err)
# ============================================================================

enum Result<T, E>:
    - Ok(T)
    - Err(E)


# Constructors
function result_ok<T, E>(value: T) -> Result<T, E> {
    return Ok(value)
}

function result_err<T, E>(error: E) -> Result<T, E> {
    return Err(error)
}


# Core method - simplified
function result_unwrap_or<T, E>(res: Result<T, E>, default: T) -> T {
    # For now, just return default
    return default
}
