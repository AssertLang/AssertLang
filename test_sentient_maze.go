package testsentientmazeoriginal

import (
	"encoding/json"
	"errors"
	"fmt"
	"math/rand"
	"os"
	"time"
)

// ============================================================================
// Helper Functions (auto-generated)
// ============================================================================

// contains checks if a slice contains an element
func contains(slice []interface{}, elem interface{}) bool {
	for _, item := range slice {
		if item == elem {
			return true
		}
	}
	return false
}

const MemoryFile string = "sentient_memory.json"
const SIZE int = 15
var START []int = []interface{}{0, 0}
var END []int = []interface{}{(SIZE - 1), (SIZE - 1)}

func LoadMemory() (map[string][]interface{}, error) {
	if os.Path.Exists(MEMORY_FILE) {
	}
	return map[string]interface{}{"deaths": []interface{}{}, "successes": 0}, nil
}

func SaveMemory(mem interface{}) {
}

func MakeMaze(size interface{}) {
	var maze interface{} = func() []interface{} {
	result := []interface{}{}
	for _, _ := range make([]int, size) {
		result = append(result, func() []interface{} {
	result := []interface{}{}
	for _, _ := range make([]int, size) {
		result = append(result, func() interface{} { if (rand.Float64() < 0.2) { return 1 } else { return 0 } }())
	}
	return result
}())
	}
	return result
}()
	var  int = 0
	return maze, nil
}

func Neighbors(x int, y int) {
	return func() []interface{} {
	result := []interface{}{}
	for _, _item := range []interface{}{[]interface{}{1, 0}, []interface{}{-1, 0}, []interface{}{0, 1}, []interface{}{0, -1}} {
		result = append(result, []interface{}{(x + dx), (y + dy)})
	}
	return result
}(), nil
}

func PrintMaze(maze interface{}, pos interface{}, path interface{}) {
	exec.Command(...).Run(func() interface{} { if (os.Name == "nt") { return "cls" } else { return "clear" } }())
	for _, _iter := range /* for i, item := range arr */(maze) {
		var line string = ""
		for _, _iter := range /* for i, item := range arr */(row) {
			if (pos == []interface{}{x, y}) {
				line = (line + "[93m@[0m")
			} else {
				if (path && contains(path, []interface{}{x, y})  // TODO: implement contains() helper) {
					line = (line + "[92m·[0m")
				} else {
					if (c == 1) {
						line = (line + "█")
					} else {
						line = (line + " ")
					}
				}
			}
		}
		fmt.Println(line)
	}
	time.Sleep(0.05)
}

func SolveMaze(maze interface{}, memory interface{}) {
	var stack []array<int> = []interface{}{START}
	var visited interface{} = make(map[T]bool)()
	var deaths interface{} = make(map[T]bool)(func() []interface{} {
	result := []interface{}{}
	for _, d := range memory["deaths"] {
		result = append(result, struct(d))
	}
	return result
}())
	var path []interface{} = []interface{}{}
	for stack {
		var x interface{} = stack[-1][0]
		var y interface{} = stack[-1][1]
		print_maze(maze, []interface{}{x, y}, path)
		if ([]interface{}{x, y} == END) {
			 = ( + 1)
			fmt.Println("
🏁 Escaped successfully! Memory improving...")
			return true, path
		}
		visited.Add([]interface{}{x, y})
		var choices interface{} = func() []interface{} {
	result := []interface{}{}
	for _, n := range neighbors(x, y) {
		if (((((0 <= n[0]) && (0 <= n[1])) && (maze[n[1]][n[0]] == 0)) && !contains(visited, n)  // TODO: implement contains() helper) && !contains(deaths, n)  // TODO: implement contains() helper) {
			result = append(result, n)
		}
	}
	return result
}()
		if choices {
			var nxt interface{} = (arr) => arr[rand.Intn(len(arr))](choices)
			path.Append(nxt)
			stack.Append(nxt)
		} else {
			var dead interface{} = stack.Pop()
			if !contains(deaths, dead)  // TODO: implement contains() helper {
				memory["deaths"].Append(dead)
			}
		}
	}
	fmt.Println("
💀 Dead end! Learning for next time...")
	return false, path
}

func Main() {
	var memory interface{} = load_memory()
	var maze interface{} = make_maze(SIZE)
	var success interface{} = solve_maze(maze, memory)[0]
	var _ interface{} = solve_maze(maze, memory)[1]
	save_memory(memory)
	fmt.Println(fmt.Sprintf("
📚 Memory contains %v learned dead ends, %v successful escapes.", len(memory["deaths"]), memory["successes"]))
	fmt.Println("Run again to see it improve!")
}
