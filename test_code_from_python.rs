use math;
use random;
use time;
use os;
use sys;

pub fn clear() {
    os.system(if (os.name == "nt") { "cls" } else { "clear" });
}

pub fn galaxy(width: f64, height: f64, t: i32, arms: i32) -> String {
    let output: Box<dyn std::any::Any> = vec![];
    let : Box<dyn std::any::Any> = <unknown>;
    for y in range(height) {
        let row: String = "";
        for x in range(width) {
            let : Box<dyn std::any::Any> = <unknown>;
            let r: Box<dyn std::any::Any> = math.sqrt(((dx ** 2) + (dy ** 2)));
            let a: Box<dyn std::any::Any> = math.atan2(dy, dx);
            let swirl: i32 = (((a * arms) + (r * 12)) - (t * 2));
            let noise: f64 = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5) + 0.5);
            let bright: Box<dyn std::any::Any> = ((math.cos(swirl) * noise) ** 2);
            if (bright > (0.5 - (r * 0.5))) {
                let color: Box<dyn std::any::Any> = colors[(int(((bright + (random.random() * 0.1)) * (len(colors) - 1))) % len(colors))];
                let char: Box<dyn std::any::Any> = random.choice(vec!["*", "·", "✦", ".", "•"]);
                row = (row + None);
            } else {
                row = (row + " ");
            }
        }
        output.append(row);
    }
    return "
".join(output);
}

pub fn animate(frames: &Box<dyn std::any::Any>) {
    let t: i32 = 0;
    // try-catch block
    while true {
        clear();
        print(galaxy(120, 40, t));
        print(None);
        t = (t + 0.1);
        time.sleep(0.08);
    }
    // catch KeyboardInterrupt
    clear();
    print("🌀 Galaxy collapsed. Goodbye.
");
}
