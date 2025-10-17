#!/usr/bin/env python3
"""
Demonstrate PW DSL → Python Translation
(Using a manually created valid PW DSL as proof of concept)

Since the Go-generated PW DSL is too malformed (40% quality),
this demonstrates what the translation WOULD produce with valid input.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dsl.al_parser import parse_al
from language.python_generator_v2 import generate_python

# Create a simple, valid PW DSL example (subset of sentient maze logic)
VALID_PW_DSL = """
module sentient_maze
version 1.0.0

import json
import os
import random
import time

function load_memory:
  returns:
    result any
  body:
    if os.path.exists("memory.json"):
      let f = open("memory.json", "r")
      let data = json.load(f)
      return data
    return {"deaths": [], "successes": 0}

function save_memory:
  params:
    mem any
  body:
    let f = open("memory.json", "w")
    json.dump(mem, f)

function make_maze:
  params:
    size int
  returns:
    result any
  body:
    let maze = []
    let i = 0
    while i < size:
      let row = []
      let j = 0
      while j < size:
        if random.random() < 0.2:
          row.append(1)
        row.append(0)
        let j = j + 1
      maze.append(row)
      let i = i + 1
    return maze

function neighbors:
  params:
    x int
    y int
  returns:
    result any
  body:
    let result = []
    result.append([x + 1, y])
    result.append([x - 1, y])
    result.append([x, y + 1])
    result.append([x, y - 1])
    return result

function main:
  body:
    let memory = load_memory()
    let maze = make_maze(15)
    save_memory(memory)
"""

def main():
    print("=" * 80)
    print("PW DSL → Python Translation Demo")
    print("=" * 80)

    print("\n📝 Using manually created valid PW DSL (subset of sentient maze)")
    print(f"   Length: {len(VALID_PW_DSL)} bytes, {len(VALID_PW_DSL.splitlines())} lines")

    # Parse PW DSL → IR
    print("\n🔄 Parsing PW DSL → IR...")
    try:
        ir_module = parse_al(VALID_PW_DSL)
        print(f"   ✅ Parsed successfully!")
        print(f"   - Module: {ir_module.name} v{ir_module.version}")
        print(f"   - Imports: {len(ir_module.imports)}")
        print(f"   - Functions: {len(ir_module.functions)}")
        print(f"   - Classes: {len(ir_module.classes)}")

    except Exception as e:
        print(f"   ❌ Parse error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Generate Python from IR
    print("\n🔄 Generating Python from IR...")
    try:
        python_code = generate_python(ir_module)
        print(f"   ✅ Generated {len(python_code)} bytes, {len(python_code.splitlines())} lines")

    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Save output
    output_file = Path("test_sentient_maze_demo.py")
    print(f"\n💾 Saving Python code: {output_file}")
    with open(output_file, "w") as f:
        f.write(python_code)
    print(f"   ✅ Saved successfully")

    # Full output
    print(f"\n📄 Generated Python Code:")
    print("-" * 80)
    print(python_code)
    print("-" * 80)

    # Summary
    print("\n" + "=" * 80)
    print("✅ Demo Complete!")
    print("=" * 80)
    print(f"\nProof of concept: PW DSL → Python translation WORKS")
    print(f"Limitation: Go-generated PW DSL is too malformed to parse (40% quality)")
    print(f"\nWith valid PW DSL input, the system generates clean Python.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
