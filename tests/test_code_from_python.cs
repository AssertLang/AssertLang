using System;
using System.Math;  // from python: math
using System.Random;  // from python: random
using time;
using System.Environment;  // from python: os
using sys;

namespace testcodeoriginal
{
    public static class Functions
    {
        public static void Clear()
        {
            os.System(((os.Name == "nt") ? "cls" : "clear"));
        }

        public static string Galaxy(double width = 120, double height = 40, int t = 0.0d, int arms = 3)
        {
            object output = new[] {  };
            object  = <unknown>;
            foreach (var y in range(height))
            {
                string row = "";
                foreach (var x in range(width))
                {
                    object  = <unknown>;
                    object r = math.Sqrt((Math.Pow(dx, 2) + Math.Pow(dy, 2)));
                    object a = math.Atan2(dy, dx);
                    int swirl = (((a * arms) + (r * 12)) - (t * 2));
                    double noise = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5d) + 0.5d);
                    object bright = Math.Pow((math.Cos(swirl) * noise), 2);
                    if ((bright > (0.5d - (r * 0.5d))))
                    {
                        object color = cOLORS[(int(((bright + (random.Random() * 0.1d)) * (len(cOLORS) - 1))) % len(cOLORS))];
                        object char = random.Choice(new[] { "*", "·", "✦", ".", "•" });
                        row = (row + null);
                    }
                    else
                    {
                        row = (row + " ");
                    }
                }
                output.Append(row);
            }
            return "
".Join(output);
        }

        public static void Animate(object frames = 99999)
        {
            int t = 0;
            try
            {
                while (true)
                {
                    clear();
                    print(galaxy(120, 40, t));
                    print(null);
                    t = (t + 0.1d);
                    time.Sleep(0.08d);
                }
            }
            catch (KeyboardInterrupt)
            {
                clear();
                print("🌀 Galaxy collapsed. Goodbye.
");
            }
        }

    }

}
