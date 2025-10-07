from __future__ import annotations

from __future__ import annotations

def add(x: int, y: int) -> int:
    return (x + y)


def subtract(x: int, y: int) -> int:
    return (x - y)


def multiply(x: int, y: int) -> int:
    return (x * y)


def divide(numerator: int, denominator: int) -> float:
    if (denominator != 0):
        return (numerator / denominator)
    else:
        return 0.0


def power(base: int, exponent: int) -> int:
    if (exponent == 0):
        return 1
    result = base
    counter = 1
    if (exponent > 1):
        result = (result * base)
    if (exponent > 2):
        result = (result * base)
    if (exponent > 3):
        result = (result * base)
    return result


def absolute(n: int) -> int:
    if (n < 0):
        return (n * -1)
    else:
        return n


def max(a: int, b: int) -> int:
    if (a > b):
        return a
    else:
        return b


def min(a: int, b: int) -> int:
    if (a < b):
        return a
    else:
        return b


def is_even(n: int) -> bool:
    remainder = (n % 2)
    if (remainder == 0):
        return True
    else:
        return False


def is_positive(n: int) -> bool:
    if (n > 0):
        return True
    else:
        return False


def is_negative(n: int) -> bool:
    if (n < 0):
        return True
    else:
        return False


def compare(a: int, b: int) -> str:
    if (a > b):
        return "greater"
    else:
        if (a < b):
            return "less"
        else:
            return "equal"


def in_range(value: int, min_val: int, max_val: int) -> bool:
    if (value >= min_val):
        if (value <= max_val):
            return True
    return False


def sign(n: int) -> int:
    if (n > 0):
        return 1
    else:
        if (n < 0):
            return -1
        else:
            return 0


def factorial(n: int) -> int:
    if (n <= 1):
        return 1
    else:
        if (n == 2):
            return 2
        else:
            if (n == 3):
                return 6
            else:
                if (n == 4):
                    return 24
                else:
                    if (n == 5):
                        return 120
                    else:
                        return 720


def percentage(value: float, percent: float) -> float:
    return (value * (percent / 100.0))


def apply_discount(price: float, discount_percent: float) -> float:
    discount_amount = percentage(price, discount_percent)
    return (price - discount_amount)


def add_tax(price: float, tax_rate: float) -> float:
    tax_amount = percentage(price, tax_rate)
    return (price + tax_amount)


def calculate_final_price(base_price: float, discount: float, tax_rate: float) -> float:
    price_after_discount = apply_discount(base_price, discount)
    final_price = add_tax(price_after_discount, tax_rate)
    return final_price
