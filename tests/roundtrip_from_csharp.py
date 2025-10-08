# C# → Python reverse translation
# Note: C# parser timed out during execution
# Manual fallback translation based on C# source structure

from __future__ import annotations

def clear():
    """Clear the console screen."""
    os.system("cls" if (os.name == "nt") else "clear")


def galaxy(width: float = 120, height: float = 40, t: int = 0, arms: int = 3) -> str:
    """Generate galaxy visualization."""
    output = []

    for y in range(height):
        row = ""
        for x in range(width):
            dx = (x - (width / 2)) / (width / 4)
            dy = (y - (height / 2)) / (height / 4)
            r = math.sqrt(((dx ** 2) + (dy ** 2)))
            a = math.atan2(dy, dx)
            swirl = (((a * arms) + (r * 12)) - (t * 2))
            noise = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5) + 0.5)
            bright = ((math.cos(swirl) * noise) ** 2)

            if (bright > (0.5 - (r * 0.5))):
                color = COLORS[(int(((bright + (random.random() * 0.1)) * (len(COLORS) - 1))) % len(COLORS))]
                char = random.choice(["*", "·", "✦", ".", "•"])
                row = (row + f"{color}{char}{RESET}")
            else:
                row = (row + " ")

        output.append(row)

    return "\n".join(output)


def animate(frames = 99999):
    """Animate the galaxy visualization."""
    t = 0

    try:
        while True:
            clear()
            print(galaxy(120, 40, t))
            print(f"\n✨ Cosmic Drift t={t} ✨   (Ctrl+C to exit)")
            t = (t + 0.1)
            time.sleep(0.08)
    except KeyboardInterrupt:
        clear()
        print("🌀 Galaxy collapsed. Goodbye.\n")


# Note: This is a manual translation as the C# parser encountered timeout issues
# The structure follows the C# source in test_code_from_python.cs
