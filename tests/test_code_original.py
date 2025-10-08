#!/usr/bin/env python3
"""
✨ Galactic ASCII Painter ✨

Generates a terminal galaxy made of swirling ASCII stars using:
 - Perlin noise (for chaotic swirls)
 - Polar coordinate warping (for galaxy arms)
 - ANSI color gradients (for cosmic vibes)

Run:
    python galaxy_art.py

Press Ctrl+C to exit.
"""

import math
import random
import time
import os
import sys

try:
    from noise import pnoise2
except ImportError:
    # Lightweight Perlin fallback
    def pnoise2(x, y, repeatx=1024, repeaty=1024, base=0):
        return math.sin(x * 3.1415 + y * 2.718) * 0.5

COLORS = [
    "\033[38;5;27m",   # deep blue
    "\033[38;5;33m",   # cyan
    "\033[38;5;51m",   # aqua
    "\033[38;5;93m",   # purple
    "\033[38;5;201m",  # magenta
    "\033[38;5;220m",  # yellow
    "\033[38;5;15m"    # white
]
RESET = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def galaxy(width=120, height=40, t=0.0, arms=3):
    output = []
    cx, cy = width / 2, height / 2
    for y in range(height):
        row = ""
        for x in range(width):
            dx, dy = (x - cx) / cx, (y - cy) / cy
            r = math.sqrt(dx**2 + dy**2)
            a = math.atan2(dy, dx)
            swirl = a * arms + r * 12 - t * 2
            noise = pnoise2(dx * 2, dy * 2 + t) * 0.5 + 0.5
            bright = (math.cos(swirl) * noise) ** 2
            if bright > 0.5 - (r * 0.5):
                color = COLORS[int((bright + random.random()*0.1) * (len(COLORS)-1)) % len(COLORS)]
                char = random.choice(["*", "·", "✦", ".", "•"])
                row += f"{color}{char}{RESET}"
            else:
                row += " "
        output.append(row)
    return "\n".join(output)

def animate(frames=99999):
    t = 0
    try:
        while True:
            clear()
            print(galaxy(120, 40, t))
            print(f"\n✨ Cosmic Drift t={t:.2f} ✨   (Ctrl+C to exit)")
            t += 0.1
            time.sleep(0.08)
    except KeyboardInterrupt:
        clear()
        print("🌀 Galaxy collapsed. Goodbye.\n")

if __name__ == "__main__":
    animate()
