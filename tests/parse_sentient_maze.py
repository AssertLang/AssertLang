#!/usr/bin/env python3
"""
Parse sentient_maze Python file to PW DSL format.

This script demonstrates the Python Parser V2 → IR → PW DSL workflow.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from language.python_parser_v2 import PythonParserV2
from dsl.pw_generator import PWGenerator


def main():
    # Input and output paths
    input_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_sentient_maze_original.py"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_sentient_maze.pw"

    print(f"Parsing Python file: {input_file}")

    # Step 1: Parse Python → IR
    parser = PythonParserV2()
    ir_module = parser.parse_file(input_file)

    print(f"✓ Parsed to IR:")
    print(f"  - Module: {ir_module.name}")
    print(f"  - Imports: {len(ir_module.imports)}")
    print(f"  - Functions: {len(ir_module.functions)}")
    print(f"  - Classes: {len(ir_module.classes)}")
    print(f"  - Module variables: {len(ir_module.module_vars)}")

    # Step 2: Generate IR → PW DSL
    generator = PWGenerator()
    pw_code = generator.generate(ir_module)

    print(f"\n✓ Generated PW DSL ({len(pw_code)} characters)")

    # Step 3: Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pw_code)

    print(f"\n✓ Saved to: {output_file}")

    # Display first 50 lines
    lines = pw_code.split('\n')
    print(f"\n{'='*70}")
    print("First 50 lines of generated PW DSL:")
    print('='*70)
    for i, line in enumerate(lines[:50], 1):
        print(f"{i:3d} | {line}")

    if len(lines) > 50:
        print(f"... ({len(lines) - 50} more lines)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
