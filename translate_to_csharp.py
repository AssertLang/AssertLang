#!/usr/bin/env python3
"""
Translate Python code to C# using Promptware translation system.

This script:
1. Parses Python source using PythonParserV2
2. Converts to IR (Intermediate Representation)
3. Generates C# code using DotNetGeneratorV2
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from language.python_parser_v2 import PythonParserV2
from language.dotnet_generator_v2 import DotNetGeneratorV2

def translate_python_to_csharp(input_file: str, output_file: str) -> dict:
    """
    Translate Python file to C# using Promptware IR.

    Args:
        input_file: Path to Python source file
        output_file: Path to output C# file

    Returns:
        Dictionary with translation statistics
    """
    print(f"📖 Reading Python file: {input_file}")

    # Step 1: Parse Python to IR
    parser = PythonParserV2()
    ir_module = parser.parse_file(input_file)

    print(f"✅ Parsed to IR: {ir_module.name}")
    print(f"   - Functions: {len(ir_module.functions)}")
    print(f"   - Classes: {len(ir_module.classes)}")
    print(f"   - Imports: {len(ir_module.imports)}")

    # Step 2: Generate C# from IR
    print(f"🔄 Generating C# code...")
    generator = DotNetGeneratorV2(namespace=ir_module.name.replace("_", ""))
    generator.source_language = "python"  # Help with library mapping
    csharp_code = generator.generate(ir_module)

    # Step 3: Write output
    print(f"💾 Writing C# file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(csharp_code)

    # Statistics
    stats = {
        'input_file': input_file,
        'output_file': output_file,
        'module_name': ir_module.name,
        'functions_count': len(ir_module.functions),
        'classes_count': len(ir_module.classes),
        'imports_count': len(ir_module.imports),
        'output_lines': len(csharp_code.split('\n'))
    }

    print(f"✨ Translation complete!")
    print(f"   - Output: {output_file}")
    print(f"   - Lines: {stats['output_lines']}")

    return stats

if __name__ == "__main__":
    # File paths
    input_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_original.py"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.cs"

    # Run translation
    stats = translate_python_to_csharp(input_file, output_file)

    # Summary
    print("\n" + "="*60)
    print("TRANSLATION SUMMARY")
    print("="*60)
    print(f"Module Name: {stats['module_name']}")
    print(f"Functions Translated: {stats['functions_count']}")
    print(f"Classes Translated: {stats['classes_count']}")
    print(f"Imports Processed: {stats['imports_count']}")
    print(f"Output Lines: {stats['output_lines']}")
    print("="*60)
