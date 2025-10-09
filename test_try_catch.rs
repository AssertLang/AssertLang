pub fn safe_divide(a: i32, b: i32) -> i32 {
    // try-catch block
    if (b == 0) {
        return Err("Division by zero");
    }
    return (a / b);
    // catch all
    return 0;
}

pub fn complex_error_handling(x: i32) -> String {
    // try-catch block
    if (x < 0) {
        return Err("Negative value not allowed");
    }
    if (x == 0) {
        return Err("Zero is invalid");
    }
    return ("Valid: " + x);
    // catch all
    return ("Error: " + e);
}

pub fn nested_try_catch(value: i32) -> bool {
    // try-catch block
    // try-catch block
    if (value > 100) {
        return Err("Value too large");
    }
    return true;
    // catch all
    return Err(("Inner error: " + inner));
    // catch all
    return false;
}
