from __future__ import annotations

from typing import List

from __future__ import annotations

def find_first_even(numbers: List[int]) -> int:
    for num in numbers:
        if ((num % 2) == 0):
            return num
    return -1
