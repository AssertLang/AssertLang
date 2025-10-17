#!/usr/bin/env python3
"""Test Go parser fixes: closures and module-level vars."""

from language.go_parser_v2 import GoParserV2
from dsl.al_generator import PWGenerator

# Test Go code with closures and module vars
go_code = """
package main

import (
	"fmt"
	"math/rand"
)

const SIZE int = 15
const MEMORY_FILE string = "memory.json"
var START []int = []int{0, 0}
var END []int = []int{SIZE - 1, SIZE - 1}

func MakeMaze(size int) [][]int {
	maze := func() [][]int {
		result := [][]int{}
		for i := 0; i < size; i++ {
			row := []int{}
			for j := 0; j < size; j++ {
				cell := func() int {
					if rand.Float64() < 0.2 {
						return 1
					} else {
						return 0
					}
				}()
				row = append(row, cell)
			}
			result = append(result, row)
		}
		return result
	}()
	maze[0][0] = 0
	maze[SIZE-1][SIZE-1] = 0
	return maze
}

func main() {
	fmt.Println("Testing closures and module vars")
	maze := MakeMaze(SIZE)
	fmt.Printf("Generated %dx%d maze\\n", len(maze), len(maze[0]))
}
"""

print("=" * 80)
print("Testing Go Parser V2 Fixes")
print("=" * 80)

# Parse Go code
parser = GoParserV2()
ir_module = parser.parse_source(go_code, "test.go")

print(f"\n✅ Parsed successfully!")
print(f"\nModule: {ir_module.name}")
print(f"Imports: {len(ir_module.imports)}")
print(f"Module vars: {len(ir_module.module_vars)}")
print(f"Functions: {len(ir_module.functions)}")

# Show module vars
print("\n" + "-" * 80)
print("Module Variables:")
print("-" * 80)
for var in ir_module.module_vars:
    print(f"  {var.target.name} = {var.value}")

# Generate PW DSL
pw_gen = PWGenerator()
pw_dsl = pw_gen.generate(ir_module)

print("\n" + "=" * 80)
print("Generated PW DSL (first 100 lines):")
print("=" * 80)
lines = pw_dsl.split('\n')
for i, line in enumerate(lines[:100], 1):
    print(f"{i:3d} | {line}")

# Save to file
with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_go_parser_fixes_output.al", "w") as f:
    f.write(pw_dsl)

print(f"\n✅ Saved to test_go_parser_fixes_output.al ({len(lines)} lines)")

# Check for improvements
print("\n" + "=" * 80)
print("Validation:")
print("=" * 80)

# Check module vars extracted
if len(ir_module.module_vars) == 4:
    print("✅ All 4 module vars extracted (SIZE, MEMORY_FILE, START, END)")
else:
    print(f"❌ Expected 4 module vars, got {len(ir_module.module_vars)}")

# Check if closures are in PW DSL
if "func()" not in pw_dsl:
    print("✅ No malformed 'func()' in PW DSL (closures properly extracted)")
else:
    print("⚠️  'func()' still appearing in PW DSL - needs more work")

# Check if MakeMaze was extracted
if "function MakeMaze" in pw_dsl or "function makeMaze" in pw_dsl.lower():
    print("✅ MakeMaze function extracted")
else:
    print("❌ MakeMaze function not found")

print("\n" + "=" * 80)
print("Test complete!")
print("=" * 80)
