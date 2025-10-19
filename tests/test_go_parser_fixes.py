#!/usr/bin/env python3
"""Test Go parser fixes: closures and module-level vars."""

from language.go_parser_v2 import GoParserV2
from dsl.al_generator import PWGenerator


# Test Go code with closures and module vars
GO_CODE = """
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
	fmt.Printf("Generated %dx%d maze\\\\n", len(maze), len(maze[0]))
}
"""


def test_go_parser_module_vars():
    """Test that Go parser extracts module-level variables correctly."""
    parser = GoParserV2()
    ir_module = parser.parse_source(GO_CODE, "test.go")

    # Should extract 4 module vars: SIZE, MEMORY_FILE, START, END
    assert len(ir_module.module_vars) == 4, (
        f"Expected 4 module vars (SIZE, MEMORY_FILE, START, END), got {len(ir_module.module_vars)}"
    )

    # Check that module has correct basic structure
    assert ir_module.name == "main"
    assert len(ir_module.imports) == 2  # fmt, math/rand
    assert len(ir_module.functions) >= 1  # At least MakeMaze


def test_go_parser_closures_in_pw_dsl():
    """Test that Go parser handles closures and doesn't leak 'func()' to PW DSL."""
    parser = GoParserV2()
    ir_module = parser.parse_source(GO_CODE, "test.go")

    # Generate PW DSL
    pw_gen = PWGenerator()
    pw_dsl = pw_gen.generate(ir_module)

    # Should not have malformed 'func()' in output (closures should be extracted)
    assert "func()" not in pw_dsl, (
        "Found 'func()' in PW DSL - closures not properly handled"
    )

    # Should have MakeMaze function
    assert "function MakeMaze" in pw_dsl or "function makeMaze" in pw_dsl.lower(), (
        "MakeMaze function not found in PW DSL"
    )
