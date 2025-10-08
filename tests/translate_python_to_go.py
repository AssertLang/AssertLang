#!/usr/bin/env python3
"""
Translate Python file to Go using Promptware V2 system.

This script demonstrates the complete translation pipeline:
Python → IR → Go
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

def translate_python_to_go(input_path: str, output_path: str):
    """
    Translate Python file to Go.

    Args:
        input_path: Path to input Python file
        output_path: Path to output Go file
    """
    print(f"=== Promptware Python → Go Translation ===")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print()

    # Step 1: Parse Python → IR
    print("Step 1: Parsing Python → IR...")
    parser = PythonParserV2()
    ir_module = parser.parse_file(input_path)

    print(f"  ✓ Module: {ir_module.name}")
    print(f"  ✓ Imports: {len(ir_module.imports)}")
    print(f"  ✓ Functions: {len(ir_module.functions)}")
    print(f"  ✓ Classes: {len(ir_module.classes)}")
    print(f"  ✓ Types: {len(ir_module.types)}")
    print(f"  ✓ Enums: {len(ir_module.enums)}")
    print()

    # Step 2: Generate Go from IR
    print("Step 2: Generating Go from IR...")
    generator = GoGeneratorV2()
    generator.source_language = "python"  # Set source for library mapping
    go_code = generator.generate(ir_module)

    print(f"  ✓ Generated {len(go_code)} characters of Go code")
    print()

    # Step 3: Write output
    print("Step 3: Writing output...")
    with open(output_path, 'w') as f:
        f.write(go_code)

    print(f"  ✓ Written to {output_path}")
    print()

    # Summary
    print("=== Translation Summary ===")
    print(f"Functions translated: {len(ir_module.functions)}")
    print(f"Classes translated: {len(ir_module.classes)}")

    # List function names
    if ir_module.functions:
        print("\nFunctions:")
        for func in ir_module.functions:
            print(f"  - {func.name}()")

    if ir_module.classes:
        print("\nClasses:")
        for cls in ir_module.classes:
            print(f"  - {cls.name}")
            if cls.constructor:
                print(f"    ✓ Constructor")
            if cls.methods:
                print(f"    ✓ {len(cls.methods)} methods")

    print("\n✓ Translation complete!")

if __name__ == "__main__":
    input_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_original.py"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.go"

    translate_python_to_go(input_file, output_file)
