#!/usr/bin/env python3
"""
Translate Python file to JavaScript using Promptware translation system.

Translation path: Python → IR → JavaScript
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2


def translate_python_to_javascript(
    input_file: str,
    output_file: str,
    typescript: bool = False
) -> dict:
    """
    Translate Python file to JavaScript.

    Args:
        input_file: Path to input Python file
        output_file: Path to output JavaScript file
        typescript: Generate TypeScript instead of JavaScript

    Returns:
        Dictionary with translation stats and metadata
    """
    print(f"🔄 Translating Python → JavaScript")
    print(f"   Input:  {input_file}")
    print(f"   Output: {output_file}")
    print()

    # Step 1: Parse Python → IR
    print("📖 Step 1: Parsing Python code → IR...")
    parser = PythonParserV2()
    try:
        ir_module = parser.parse_file(input_file)
        print(f"   ✓ Parsed module: {ir_module.name}")
        print(f"   ✓ Functions: {len(ir_module.functions)}")
        print(f"   ✓ Classes: {len(ir_module.classes)}")
        print(f"   ✓ Imports: {len(ir_module.imports)}")
        print()
    except Exception as e:
        print(f"   ✗ Error parsing Python: {e}")
        raise

    # Step 2: Generate JavaScript from IR
    print("🔨 Step 2: Generating JavaScript from IR...")
    generator = NodeJSGeneratorV2(typescript=typescript)
    try:
        js_code = generator.generate(ir_module)
        print(f"   ✓ Generated {len(js_code.splitlines())} lines of JavaScript")
        print()
    except Exception as e:
        print(f"   ✗ Error generating JavaScript: {e}")
        raise

    # Step 3: Write output
    print(f"💾 Step 3: Writing output to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_code)
        print(f"   ✓ Successfully wrote {output_file}")
        print()
    except Exception as e:
        print(f"   ✗ Error writing output: {e}")
        raise

    # Return statistics
    stats = {
        "input_file": input_file,
        "output_file": output_file,
        "module_name": ir_module.name,
        "num_functions": len(ir_module.functions),
        "num_classes": len(ir_module.classes),
        "num_imports": len(ir_module.imports),
        "output_lines": len(js_code.splitlines()),
        "success": True
    }

    return stats


def main():
    """Main entry point."""
    # Configuration
    input_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_original.py"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.js"

    print("=" * 70)
    print("Promptware Universal Code Translation System")
    print("Python → JavaScript Translation")
    print("=" * 70)
    print()

    try:
        stats = translate_python_to_javascript(
            input_file=input_file,
            output_file=output_file,
            typescript=False  # Generate JavaScript, not TypeScript
        )

        print("=" * 70)
        print("✅ TRANSLATION SUCCESSFUL")
        print("=" * 70)
        print()
        print(f"Module: {stats['module_name']}")
        print(f"Functions translated: {stats['num_functions']}")
        print(f"Classes translated: {stats['num_classes']}")
        print(f"Imports translated: {stats['num_imports']}")
        print(f"Output lines: {stats['output_lines']}")
        print()
        print(f"Output saved to: {stats['output_file']}")
        print()

    except Exception as e:
        print("=" * 70)
        print("❌ TRANSLATION FAILED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
