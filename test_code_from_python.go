package testcodeoriginal

import (
	"errors"
	"fmt"
	"math"
	"math/rand"
	"os"
	"time"
)

// ============================================================================
// Helper Functions (auto-generated)
// ============================================================================

// Choice returns a random element from a slice
func Choice(slice []interface{}) interface{} {
    if len(slice) == 0 {
        return nil
    }
    return slice[rand.Intn(len(slice))]
}

// ChoiceString returns a random string from a slice
func ChoiceString(slice []string) string {
    if len(slice) == 0 {
        return ""
    }
    return slice[rand.Intn(len(slice))]
}

// ChoiceInt returns a random int from a slice
func ChoiceInt(slice []int) int {
    if len(slice) == 0 {
        return 0
    }
    return slice[rand.Intn(len(slice))]
}

var COLORS []string = []string{"\x1b[38;5;27m", "\x1b[38;5;33m", "\x1b[38;5;51m", "\x1b[38;5;93m", "\x1b[38;5;201m", "\x1b[38;5;220m", "\x1b[38;5;15m"}
const RESET string = "\x1b[0m"

func Clear() {
	exec.Command(...).Run(func() string { if (os.Name == "nt") { return "cls" } else { return "clear" } }())
}

func Galaxy(width float64, height float64, t int, arms int) (string, error) {
	var output []interface{} = []interface{}{}
	var cx float64 = (width / 2)
	var cy float64 = (height / 2)
	for y := 0; y < height; y++ {
		var row int = ""
		for x := 0; x < width; x++ {
			var dx float64 = ((x - cx) / cx)
			var dy float64 = ((y - cy) / cy)
			var r float64 = math.Sqrt((math.Pow(dx, 2) + math.Pow(dy, 2)))
			var a float64 = math.Atan2(dy, dx)
			var swirl float64 = (((a * arms) + (r * 12)) - (t * 2))
			var noise float64 = ((pnoise2((dx * 2), ((dy * 2) + t)) * 0.5) + 0.5)
			var bright interface{} = math.Pow((math.Cos(swirl) * noise), 2)
			if (bright > (0.5 - (r * 0.5))) {
				var color interface{} = COLORS[(int(((bright + (rand.Float64() * 0.1)) * (len(COLORS) - 1))) % len(COLORS))]
				var char interface{} = ChoiceString([]string{"*", "·", "✦", ".", "•"})
				row = (row + fmt.Sprintf("%v%v%v", color, char, RESET))
			} else {
				row = (row + " ")
			}
		}
		output = append(output, row)
	}
	return strings.Join(output, "\n"), nil
}

func Animate(frames interface{}) error {
	var t int = 0
	for true {
		clear()
		fmt.Println(galaxy(120, 40, t))
		fmt.Println(fmt.Sprintf("\n✨ Cosmic Drift t=%v ✨   (Ctrl+C to exit)", fmt.Sprintf("%.2f", t)))
		t = (t + 0.1)
		time.Sleep(0.08)
	}
	// catch KeyboardInterrupt
	clear()
	fmt.Println("🌀 Galaxy collapsed. Goodbye.\n")
}
