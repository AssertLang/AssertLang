#!/usr/bin/env python3
"""
Translate Python code to Rust using AssertLang translation system.

This script:
1. Reads a Python file
2. Parses it to IR using PythonParserV2
3. Generates Rust code using RustGeneratorV2
4. Saves the output
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from language.python_parser_v2 import PythonParserV2
from language.rust_generator_v2 import RustGeneratorV2


def translate_python_to_rust(input_file: str, output_file: str) -> dict:
    """
    Translate Python file to Rust.

    Args:
        input_file: Path to Python source file
        output_file: Path to output Rust file

    Returns:
        Dictionary with translation stats
    """
    print(f"📖 Reading Python file: {input_file}")

    # Step 1: Parse Python → IR
    parser = PythonParserV2()
    ir_module = parser.parse_file(input_file)

    print(f"✅ Parsed Python to IR")
    print(f"   - Module: {ir_module.name}")
    print(f"   - Functions: {len(ir_module.functions)}")
    print(f"   - Classes: {len(ir_module.classes)}")
    print(f"   - Imports: {len(ir_module.imports)}")

    # Step 2: Generate Rust from IR
    generator = RustGeneratorV2()
    rust_code = generator.generate(ir_module)

    print(f"✅ Generated Rust code")

    # Step 3: Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rust_code)

    print(f"💾 Saved Rust code to: {output_file}")

    # Return stats
    return {
        'module_name': ir_module.name,
        'functions': len(ir_module.functions),
        'classes': len(ir_module.classes),
        'imports': len(ir_module.imports),
        'output_file': output_file,
        'lines': len(rust_code.splitlines())
    }


if __name__ == "__main__":
    # Translate test_code_original.py → test_code_from_python.rs
    input_path = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/test_code_original.py"
    output_path = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/test_code_from_python.rs"

    try:
        stats = translate_python_to_rust(input_path, output_path)

        print("\n" + "="*60)
        print("🎉 TRANSLATION COMPLETE")
        print("="*60)
        print(f"Module: {stats['module_name']}")
        print(f"Functions translated: {stats['functions']}")
        print(f"Classes translated: {stats['classes']}")
        print(f"Imports: {stats['imports']}")
        print(f"Output file: {stats['output_file']}")
        print(f"Lines of Rust code: {stats['lines']}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Translation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
