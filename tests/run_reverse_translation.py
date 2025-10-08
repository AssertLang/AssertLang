#!/usr/bin/env python3
"""
Reverse translation script: JS/Go/Rust/C# back to Python
Uses V2 parsers and Python generator to translate back
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2
from language.python_generator_v2 import PythonGeneratorV2

def reverse_translate_js():
    """JavaScript → Python"""
    print("=" * 80)
    print("REVERSE TRANSLATION: JavaScript → Python")
    print("=" * 80)

    js_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.js"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/roundtrip_from_js.py"

    try:
        # Parse JS → IR
        parser = NodeJSParserV2()

        print(f"\n📖 Reading: {js_file}")
        ir = parser.parse_file(js_file)
        print(f"✅ Parsed {len(ir.functions)} functions, {len(ir.classes)} classes")

        # Generate Python from IR
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Write output
        with open(output_file, 'w') as f:
            f.write(python_code)

        print(f"✅ Generated: {output_file}")
        print(f"📄 Output preview (first 20 lines):")
        print("-" * 80)
        print('\n'.join(python_code.split('\n')[:20]))
        print("-" * 80)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def reverse_translate_go():
    """Go → Python"""
    print("\n" + "=" * 80)
    print("REVERSE TRANSLATION: Go → Python")
    print("=" * 80)

    go_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.go"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/roundtrip_from_go.py"

    try:
        # Parse Go → IR
        parser = GoParserV2()

        print(f"\n📖 Reading: {go_file}")
        ir = parser.parse_file(go_file)
        print(f"✅ Parsed {len(ir.functions)} functions, {len(ir.classes)} classes")

        # Generate Python from IR
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Write output
        with open(output_file, 'w') as f:
            f.write(python_code)

        print(f"✅ Generated: {output_file}")
        print(f"📄 Output preview (first 20 lines):")
        print("-" * 80)
        print('\n'.join(python_code.split('\n')[:20]))
        print("-" * 80)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def reverse_translate_rust():
    """Rust → Python"""
    print("\n" + "=" * 80)
    print("REVERSE TRANSLATION: Rust → Python")
    print("=" * 80)

    rust_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.rs"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/roundtrip_from_rust.py"

    try:
        # Parse Rust → IR
        parser = RustParserV2()

        print(f"\n📖 Reading: {rust_file}")
        ir = parser.parse_file(rust_file)
        print(f"✅ Parsed {len(ir.functions)} functions, {len(ir.classes)} classes")

        # Generate Python from IR
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Write output
        with open(output_file, 'w') as f:
            f.write(python_code)

        print(f"✅ Generated: {output_file}")
        print(f"📄 Output preview (first 20 lines):")
        print("-" * 80)
        print('\n'.join(python_code.split('\n')[:20]))
        print("-" * 80)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def reverse_translate_csharp():
    """C# → Python"""
    print("\n" + "=" * 80)
    print("REVERSE TRANSLATION: C# → Python")
    print("=" * 80)

    cs_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_code_from_python.cs"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/roundtrip_from_csharp.py"

    try:
        # Parse C# → IR
        parser = DotNetParserV2()

        print(f"\n📖 Reading: {cs_file}")
        ir = parser.parse_file(cs_file)
        print(f"✅ Parsed {len(ir.functions)} functions, {len(ir.classes)} classes")

        # Generate Python from IR
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Write output
        with open(output_file, 'w') as f:
            f.write(python_code)

        print(f"✅ Generated: {output_file}")
        print(f"📄 Output preview (first 20 lines):")
        print("-" * 80)
        print('\n'.join(python_code.split('\n')[:20]))
        print("-" * 80)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all reverse translations"""
    print("\n🔄 PROMPTWARE REVERSE TRANSLATION TEST")
    print("Translating generated code back to Python")
    print("=" * 80)

    results = {}

    # Run all translations
    results['JavaScript'] = reverse_translate_js()
    results['Go'] = reverse_translate_go()
    results['Rust'] = reverse_translate_rust()
    results['C#'] = reverse_translate_csharp()

    # Summary
    print("\n" + "=" * 80)
    print("📊 REVERSE TRANSLATION SUMMARY")
    print("=" * 80)

    successful = sum(1 for v in results.values() if v)
    total = len(results)

    for lang, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{lang:15} → Python: {status}")

    print(f"\nTotal: {successful}/{total} translations successful ({successful/total*100:.0f}%)")

    if successful == total:
        print("\n🎉 All reverse translations completed successfully!")
    else:
        print(f"\n⚠️  {total - successful} translation(s) failed. See errors above.")

    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
