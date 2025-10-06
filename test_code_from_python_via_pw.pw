module test_code_original
version 1.0.0

import math
import random
import time
import os
import sys

let <unknown: str> = ["[38;5;27m", "[38;5;33m", "[38;5;51m", "[38;5;93m", "[38;5;201m", "[38;5;220m", "[38;5;15m"]
let <unknown: str> = "[0m"

function clear:
  body:
    os.system("cls" if (os.name == "nt") else "clear")

function galaxy:
  params:
    width float = 120
    height float = 40
    t int = 0.0
    arms int = 3
  returns:
    result string
  body:
    let output = []
    let cx = (width / 2)
    let cy = (height / 2)
    for y in range(height):
      let row = ""
      for x in range(width):
        let dx = ((x - cx) / cx)
        let dy = ((y - cy) / cy)
        let r = math.sqrt(((dx ** 2) + (dy ** 2)))
        let a = math.atan2(dy, dx)
        let swirl = (((a * arms) + (r * 12)) - (t * 2))
        let noise = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5) + 0.5)
        let bright = ((math.cos(swirl) * noise) ** 2)
        if (bright > (0.5 - (r * 0.5))):
          let color = COLORS[(int(((bright + (random.random() * 0.1)) * (len(COLORS) - 1))) % len(COLORS))]
          let char = random.choice(["*", "·", "✦", ".", "•"])
          row = (row + f"{color}{char}{RESET}")
        else:
          row = (row + " ")
      output.append(row)
    return "
".join(output)

function animate:
  params:
    frames any = 99999
  body:
    let t = 0
    try:
      while true:
        clear()
        print(galaxy(120, 40, t))
        print(f"
✨ Cosmic Drift t={t.toFixed(2)} ✨   (Ctrl+C to exit)")
        t = (t + 0.1)
        time.sleep(0.08)
    catch KeyboardInterrupt:
      clear()
      print("🌀 Galaxy collapsed. Goodbye.
")
