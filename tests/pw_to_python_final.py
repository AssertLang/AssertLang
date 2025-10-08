#!/usr/bin/env python3
"""
PW DSL → Python Final Translation
Agent 4: Complete the bidirectional translation chain

Translation Chain:
1. Python → IR → PW DSL (Agent 1) ✅
2. PW DSL → IR → Go (Agent 2) ✅
3. Go → IR → PW DSL (Agent 3) ✅
4. PW DSL → IR → Python (Agent 4) ← YOU ARE HERE

Input: test_sentient_maze_from_go.pw (40% quality, malformed)
Output: test_sentient_maze_final.py (best effort Python)
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dsl.pw_parser import parse_pw, PWParseError
from language.python_generator_v2 import generate_python

def main():
    print("=" * 80)
    print("PW DSL → Python Translation (Agent 4)")
    print("=" * 80)

    # Input/output paths
    pw_file = Path("test_sentient_maze_from_go.pw")
    output_file = Path("test_sentient_maze_final.py")

    print(f"\n📥 Reading PW DSL: {pw_file}")

    # Read PW DSL
    with open(pw_file, "r") as f:
        pw_code = f.read()

    print(f"   ✅ Read {len(pw_code)} bytes, {len(pw_code.splitlines())} lines")

    # Parse PW DSL → IR
    print("\n🔄 Parsing PW DSL → IR...")
    try:
        ir_module = parse_pw(pw_code)
        print(f"   ✅ Parsed successfully!")
        print(f"   - Module: {ir_module.name} v{ir_module.version}")
        print(f"   - Imports: {len(ir_module.imports)}")
        print(f"   - Functions: {len(ir_module.functions)}")
        print(f"   - Classes: {len(ir_module.classes)}")
        print(f"   - Types: {len(ir_module.types)}")
        print(f"   - Enums: {len(ir_module.enums)}")

    except PWParseError as e:
        print(f"   ❌ Parse error: {e}")
        print(f"\n⚠️  WARNING: PW DSL is malformed (from Go translation)")
        print(f"   Will attempt to parse what we can...")

        # Try to parse line by line and skip errors
        lines = pw_code.splitlines()
        print(f"\n   Attempting partial parse of {len(lines)} lines...")

        # For now, just fail gracefully
        print(f"\n❌ Cannot continue without valid IR. Exiting.")
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
    print(f"\n💾 Saving Python code: {output_file}")
    with open(output_file, "w") as f:
        f.write(python_code)
    print(f"   ✅ Saved successfully")

    # Preview first 50 lines
    lines = python_code.splitlines()
    preview_count = min(50, len(lines))
    print(f"\n📄 Preview (first {preview_count} lines):")
    print("-" * 80)
    for i, line in enumerate(lines[:preview_count], 1):
        print(f"{i:3d} | {line}")
    print("-" * 80)

    # Summary
    print("\n" + "=" * 80)
    print("✅ Translation Complete!")
    print("=" * 80)
    print(f"\nInput:  {pw_file} ({len(pw_code.splitlines())} lines)")
    print(f"Output: {output_file} ({len(lines)} lines)")
    print(f"\nTranslation chain complete:")
    print("  Python → PW DSL → Go → PW DSL → Python ✅")

    return 0

if __name__ == "__main__":
    sys.exit(main())
