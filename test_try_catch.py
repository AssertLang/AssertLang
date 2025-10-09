from __future__ import annotations

from __future__ import annotations

def safe_divide(a: int, b: int) -> int:
    try:
        if (b == 0):
            raise "Division by zero"
        return (a / b)
    except:
        return 0


def complex_error_handling(x: int) -> str:
    try:
        if (x < 0):
            raise "Negative value not allowed"
        if (x == 0):
            raise "Zero is invalid"
        return ("Valid: " + x)
    except:
        return ("Error: " + e)


def nested_try_catch(value: int) -> bool:
    try:
        try:
            if (value > 100):
                raise "Value too large"
            return True
        except:
            raise ("Inner error: " + inner)
    except:
        return False
