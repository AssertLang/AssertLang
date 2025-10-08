from __future__ import annotations

from typing import Any

import json
import os
import random
import time

def load_memory() -> Any:
    if os.path.exists("memory.json"):
        f = open("memory.json", "r")
        data = json.load(f)
        return data
    return {"deaths": [], "successes": 0}


def save_memory(mem: Any):
    f = open("memory.json", "w")
    json.dump(mem, f)


def make_maze(size: int) -> Any:
    maze = []
    i = 0
    while (i < size):
        row = []
        j = 0
        while (j < size):
            if (random.random() < 0.2):
                row.append(1)
            row.append(0)
            j = (j + 1)
        maze.append(row)
        i = (i + 1)
    return maze


def neighbors(x: int, y: int) -> Any:
    result = []
    result.append([(x + 1), y])
    result.append([(x - 1), y])
    result.append([x, (y + 1)])
    result.append([x, (y - 1)])
    return result


def main():
    memory = load_memory()
    maze = make_maze(15)
    save_memory(memory)
