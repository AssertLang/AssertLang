module sentient_maze
version 1.0.0

import json
import os
import random
import time

function load_memory:
  returns:
    result any
  body:
    if os.path.exists("sentient_memory.json"):
      let f = open("sentient_memory.json", "r")
      let data = json.load(f)
      return data
    return {"deaths": [], "successes": 0}

function save_memory:
  params:
    mem any
  body:
    let f = open("sentient_memory.json", "w")
    json.dump(mem, f)

function make_maze:
  params:
    size int
  returns:
    result any
  body:
    let maze = []
    let i = 0
    while i < size:
      let row = []
      let j = 0
      while j < size:
        if random.random() < 0.2:
          row.append(1)
        row.append(0)
        let j = j + 1
      maze.append(row)
      let i = i + 1
    return maze

function neighbors:
  params:
    x int
    y int
  returns:
    result any
  body:
    let result = []
    result.append([x + 1, y])
    result.append([x - 1, y])
    result.append([x, y + 1])
    result.append([x, y - 1])
    return result

function print_maze:
  params:
    maze any
    pos any
    path any
  body:
    os.system("clear")
    let y = 0
    while y < len(maze):
      let row = maze[y]
      let line = ""
      let x = 0
      while x < len(row):
        let c = row[x]
        if pos == [x, y]:
          line = line + "@"
        if c == 1:
          line = line + "█"
        line = line + " "
        let x = x + 1
      print(line)
      let y = y + 1
    time.sleep(0.05)

function solve_maze:
  params:
    maze any
    memory any
  returns:
    result any
  body:
    let stack = [[0, 0]]
    let visited = []
    let deaths = memory["deaths"]
    let path = []
    let SIZE = 15
    let END = [SIZE - 1, SIZE - 1]
    while len(stack) > 0:
      let x = stack[-1][0]
      let y = stack[-1][1]
      print_maze(maze, [x, y], path)
      if [x, y] == END:
        print("Escaped successfully!")
        return [true, path]
      visited.append([x, y])
      let nlist = neighbors(x, y)
      let choices = []
      let i = 0
      while i < len(nlist):
        let n = nlist[i]
        if n[0] >= 0 and n[0] < SIZE and n[1] >= 0 and n[1] < SIZE:
          if maze[n[1]][n[0]] == 0:
            if n not in visited:
              if n not in deaths:
                choices.append(n)
        let i = i + 1
      if len(choices) > 0:
        let nxt = choices[random.randint(0, len(choices) - 1)]
        path.append(nxt)
        stack.append(nxt)
      let dead = stack.pop()
      if dead not in deaths:
        memory["deaths"].append(dead)
    print("Dead end! Learning for next time...")
    return [false, path]

function main:
  body:
    let memory = load_memory()
    let maze = make_maze(15)
    let success = solve_maze(maze, memory)
    save_memory(memory)
    print("Run again to see it improve!")
