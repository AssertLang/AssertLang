from __future__ import annotations

def add(a: int, b: int) -> int:
    return (a + b)


def divide(a: int, b: int) -> int:
    return (a // b)


def increment(count: int) -> int:
    return (count + 1)


def main() -> int:
    print("=== Simple Math Contract Tests ===")
    print("")
    print("Test 1: add(5, 3) - should succeed")
    result1 = add(5, 3)
    print("Result:", result1)
    print("")
    print("Test 2: divide(10, 2) - should succeed")
    result2 = divide(10, 2)
    print("Result:", result2)
    print("")
    print("Test 3: increment(5) - should succeed")
    result3 = increment(5)
    print("Result:", result3)
    print("")
    print("=== All tests passed ===")
    return 0
