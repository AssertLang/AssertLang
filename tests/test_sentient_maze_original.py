#!/usr/bin/env python3
"""
🧠 The Sentient Maze
-------------------
Each time you run it, the maze 'remembers' where it got stuck last time.

- A grid-based maze is generated randomly.
- The AI 'walker' uses a basic memory-based exploration algorithm.
- Progress is saved to sentient_memory.json.
- On the next run, it will recall dead ends and try smarter paths.

Run a few times — you'll see it get faster.
"""

import json, os, random, time

MEMORY_FILE = "sentient_memory.json"

SIZE = 15
START = (0, 0)
END = (SIZE - 1, SIZE - 1)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"deaths": [], "successes": 0}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def make_maze(size):
    maze = [[1 if random.random() < 0.2 else 0 for _ in range(size)] for _ in range(size)]
    maze[0][0] = maze[-1][-1] = 0
    return maze

def neighbors(x, y):
    return [(x+dx, y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]]

def print_maze(maze, pos=None, path=None):
    os.system("cls" if os.name == "nt" else "clear")
    for y, row in enumerate(maze):
        line = ""
        for x, c in enumerate(row):
            if pos == (x, y):
                line += "\033[93m@\033[0m"
            elif path and (x, y) in path:
                line += "\033[92m·\033[0m"
            elif c == 1:
                line += "█"
            else:
                line += " "
        print(line)
    time.sleep(0.05)

def solve_maze(maze, memory):
    stack = [START]
    visited = set()
    deaths = set(tuple(d) for d in memory["deaths"])
    path = []
    while stack:
        x, y = stack[-1]
        print_maze(maze, (x, y), path)
        if (x, y) == END:
            memory["successes"] += 1
            print("\n🏁 Escaped successfully! Memory improving...")
            return True, path
        visited.add((x, y))
        choices = [n for n in neighbors(x, y)
                   if 0 <= n[0] < SIZE and 0 <= n[1] < SIZE
                   and maze[n[1]][n[0]] == 0
                   and n not in visited
                   and n not in deaths]
        if choices:
            nxt = random.choice(choices)
            path.append(nxt)
            stack.append(nxt)
        else:
            # Dead end, learn from mistake
            dead = stack.pop()
            if dead not in deaths:
                memory["deaths"].append(dead)
    print("\n💀 Dead end! Learning for next time...")
    return False, path

def main():
    memory = load_memory()
    maze = make_maze(SIZE)
    success, _ = solve_maze(maze, memory)
    save_memory(memory)
    print(f"\n📚 Memory contains {len(memory['deaths'])} learned dead ends, {memory['successes']} successful escapes.")
    print("Run again to see it improve!")

if __name__ == "__main__":
    main()
