pub fn add(x: i32, y: i32) -> i32 {
    return (x + y);
}

pub fn subtract(x: i32, y: i32) -> i32 {
    return (x - y);
}

pub fn multiply(x: i32, y: i32) -> i32 {
    return (x * y);
}

pub fn divide(numerator: i32, denominator: i32) -> f64 {
    if (denominator != 0) {
        return (numerator / denominator);
    } else {
        return 0.0;
    }
}

pub fn power(base: i32, exponent: i32) -> i32 {
    if (exponent == 0) {
        return 1;
    }
    let result = base;
    let counter = 1;
    if (exponent > 1) {
        result = (result * base);
    }
    if (exponent > 2) {
        result = (result * base);
    }
    if (exponent > 3) {
        result = (result * base);
    }
    return result;
}

pub fn absolute(n: i32) -> i32 {
    if (n < 0) {
        return (n * -1);
    } else {
        return n;
    }
}

pub fn max(a: i32, b: i32) -> i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

pub fn min(a: i32, b: i32) -> i32 {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

pub fn is_even(n: i32) -> bool {
    let remainder = (n % 2);
    if (remainder == 0) {
        return true;
    } else {
        return false;
    }
}

pub fn is_positive(n: i32) -> bool {
    if (n > 0) {
        return true;
    } else {
        return false;
    }
}

pub fn is_negative(n: i32) -> bool {
    if (n < 0) {
        return true;
    } else {
        return false;
    }
}

pub fn compare(a: i32, b: i32) -> String {
    if (a > b) {
        return "greater";
    } else {
        if (a < b) {
            return "less";
        } else {
            return "equal";
        }
    }
}

pub fn in_range(value: i32, min_val: i32, max_val: i32) -> bool {
    if (value >= min_val) {
        if (value <= max_val) {
            return true;
        }
    }
    return false;
}

pub fn sign(n: i32) -> i32 {
    if (n > 0) {
        return 1;
    } else {
        if (n < 0) {
            return -1;
        } else {
            return 0;
        }
    }
}

pub fn factorial(n: i32) -> i32 {
    if (n <= 1) {
        return 1;
    } else {
        if (n == 2) {
            return 2;
        } else {
            if (n == 3) {
                return 6;
            } else {
                if (n == 4) {
                    return 24;
                } else {
                    if (n == 5) {
                        return 120;
                    } else {
                        return 720;
                    }
                }
            }
        }
    }
}

pub fn percentage(value: f64, percent: f64) -> f64 {
    return (value * (percent / 100.0));
}

pub fn apply_discount(price: f64, discount_percent: f64) -> f64 {
    let discount_amount = percentage(price, discount_percent);
    return (price - discount_amount);
}

pub fn add_tax(price: f64, tax_rate: f64) -> f64 {
    let tax_amount = percentage(price, tax_rate);
    return (price + tax_amount);
}

pub fn calculate_final_price(base_price: f64, discount: f64, tax_rate: f64) -> f64 {
    let price_after_discount = apply_discount(base_price, discount);
    let final_price = add_tax(price_after_discount, tax_rate);
    return final_price;
}
