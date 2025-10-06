import 'math';
import 'random';
import 'time';
import 'os';
import 'sys';

const COLORS = ["[38;5;27m", "[38;5;33m", "[38;5;51m", "[38;5;93m", "[38;5;201m", "[38;5;220m", "[38;5;15m"];
const RESET = "[0m";

/**
 */
export function clear() {
  os.system(((os.name === "nt") ? "cls" : "clear"));
}

/**
 * @param {number} width
 * @param {number} height
 * @param {number} t
 * @param {number} arms
 * @returns {string}
 */
export function galaxy(width = 120, height = 40, t = 0.0, arms = 3) {
  const output = [];
  const  = <unknown>;
  for (const y of range(height)) {
    const row = "";
    for (const x of range(width)) {
      const  = <unknown>;
      const r = math.sqrt(((dx ** 2) + (dy ** 2)));
      const a = math.atan2(dy, dx);
      let swirl = (((a * arms) + (r * 12)) - (t * 2));
      let noise = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5) + 0.5);
      const bright = ((math.cos(swirl) * noise) ** 2);
      if ((bright > (0.5 - (r * 0.5)))) {
        const color = COLORS[(int(((bright + (random.random() * 0.1)) * (len(COLORS) - 1))) % len(COLORS))];
        const char = random.choice(["*", "·", "✦", ".", "•"]);
        row = (row + `${color}${char}${RESET}`);
      } else {
        row = (row + " ");
      }
    }
    output.append(row);
  }
  return "
".join(output);
}

/**
 * @param {any} frames
 */
export function animate(frames = 99999) {
  let t = 0;
  try {
    while (true) {
      clear();
      print(galaxy(120, 40, t));
      print(`
✨ Cosmic Drift t=${t} ✨   (Ctrl+C to exit)`);
      t = (t + 0.1);
      time.sleep(0.08);
    }
  } catch (error) {
    clear();
    print("🌀 Galaxy collapsed. Goodbye.
");
  }
}
