#!/usr/bin/env python3
"""Parse the manually-fixed PW DSL and generate Python"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dsl.pw_parser import parse_pw
from language.python_generator_v2 import generate_python

def main():
    pw_file = Path("test_sentient_maze_from_go_fixed.al")
    output_file = Path("test_sentient_maze_final.py")

    print(f"📥 Reading: {pw_file}")
    with open(pw_file) as f:
        pw_code = f.read()
    print(f"   {len(pw_code)} bytes, {len(pw_code.splitlines())} lines")

    print("\n🔄 Parsing PW DSL → IR...")
    try:
        ir_module = parse_pw(pw_code)
        print(f"   ✅ Module: {ir_module.name}")
        print(f"   - Functions: {len(ir_module.functions)}")
        print(f"   - Imports: {len(ir_module.imports)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n🔄 Generating Python...")
    try:
        python_code = generate_python(ir_module)
        print(f"   ✅ {len(python_code.splitlines())} lines")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print(f"\n💾 Saving: {output_file}")
    with open(output_file, "w") as f:
        f.write(python_code)

    print(f"\n📄 First 60 lines:")
    print("-" * 80)
    for i, line in enumerate(python_code.splitlines()[:60], 1):
        print(f"{i:3d} | {line}")
    print("-" * 80)

    print("\n✅ Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
