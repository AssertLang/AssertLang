module test_sentient_maze_original
version 1.0.0

import json
import os
import random
import time

function load_memory:
  returns:
    result map<string, array<any>>
  body:
    if os.path.exists(MEMORY_FILE):
    return {deaths: [], successes: 0}

function save_memory:
  params:
    mem any

function make_maze:
  params:
    size any
  body:
    let maze = [[1 if (random.random() < 0.2) else 0 for _ in range(size)] for _ in range(size)]
    let  = 0
    return maze

function neighbors:
  params:
    x int
    y int
  body:
    return [[(x + dx), (y + dy)] for _item in [[1, 0], [-1, 0], [0, 1], [0, -1]]]

function print_maze:
  params:
    maze any
    pos any = null
    path any = null
  body:
    os.system("cls" if (os.name == "nt") else "clear")
    for _iter in enumerate(maze):
      let line = ""
      for _iter in enumerate(row):
        if (pos == [x, y]):
          line = (line + "[93m@[0m")
        else:
          if (path and ([x, y] in path)):
            line = (line + "[92m·[0m")
          else:
            if (c == 1):
              line = (line + "█")
            else:
              line = (line + " ")
      print(line)
    time.sleep(0.05)

function solve_maze:
  params:
    maze any
    memory any
  body:
    let stack = [START]
    let visited = set()
    let deaths = set((tuple(d) for d in memory["deaths"]))
    let path = []
    while stack:
      let x = stack[-1][0]
      let y = stack[-1][1]
      print_maze(maze, [x, y], path)
      if ([x, y] == END):
         = ( + 1)
        print("
🏁 Escaped successfully! Memory improving...")
        return [true, path]
      visited.add([x, y])
      let choices = [n for n in neighbors(x, y) if (((((0 <= n[0]) and (0 <= n[1])) and (maze[n[1]][n[0]] == 0)) and (n not in visited)) and (n not in deaths))]
      if choices:
        let nxt = random.choice(choices)
        path.append(nxt)
        stack.append(nxt)
      else:
        let dead = stack.pop()
        if (dead not in deaths):
          memory["deaths"].append(dead)
    print("
💀 Dead end! Learning for next time...")
    return [false, path]

function main:
  body:
    let memory = load_memory()
    let maze = make_maze(SIZE)
    let success = solve_maze(maze, memory)[0]
    let _ = solve_maze(maze, memory)[1]
    save_memory(memory)
    print(f"
📚 Memory contains {len(memory["deaths"])} learned dead ends, {memory["successes"]} successful escapes.")
    print("Run again to see it improve!")
