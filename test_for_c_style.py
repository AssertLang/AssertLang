from __future__ import annotations

from __future__ import annotations

def count() -> int:
    x = 0
    i = 0
    while (i < 10):
        x = (x + 1)
        i = (i + 1)
    return x


def sum_range(n: int) -> int:
    total = 0
    i = 0
    while (i < n):
        total = (total + i)
        i = (i + 1)
    return total
