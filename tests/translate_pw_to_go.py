#!/usr/bin/env python3
"""
Translate PW DSL to Go Code

This script demonstrates the complete PW DSL → IR → Go workflow:
1. Read PW DSL file
2. Parse PW DSL → IR using pw_parser
3. Generate Go code from IR using go_generator_v2
4. Save Go output
5. Attempt to compile with Go
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dsl.pw_parser import parse_pw
from language.go_generator_v2 import generate_go


def main():
    # Input: PW DSL file
    pw_file = project_root / "test_sentient_maze.al"

    # Output: Go file
    go_file = project_root / "test_sentient_maze.go"

    print("=" * 80)
    print("PW DSL → Go Translation")
    print("=" * 80)
    print()

    # Step 1: Read PW DSL
    print(f"📖 Reading PW DSL from: {pw_file}")
    with open(pw_file, 'r') as f:
        pw_text = f.read()
    print(f"   Lines: {len(pw_text.splitlines())}")
    print()

    # Step 2: Parse PW DSL → IR
    print("🔄 Parsing PW DSL → IR...")
    try:
        ir_module = parse_pw(pw_text)
        print(f"   ✅ Module: {ir_module.name}")
        print(f"   ✅ Version: {ir_module.version}")
        print(f"   ✅ Imports: {len(ir_module.imports)}")
        print(f"   ✅ Functions: {len(ir_module.functions)}")
        print(f"   ✅ Classes: {len(ir_module.classes)}")
        print(f"   ✅ Module vars: {len(ir_module.module_vars)}")
    except Exception as e:
        print(f"   ❌ Parse error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    print()

    # Step 3: Generate Go code from IR
    print("🔧 Generating Go code from IR...")
    try:
        go_code = generate_go(ir_module)
        print(f"   ✅ Generated {len(go_code)} characters")
        print(f"   ✅ Lines: {len(go_code.splitlines())}")
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    print()

    # Step 4: Save Go code
    print(f"💾 Saving Go code to: {go_file}")
    with open(go_file, 'w') as f:
        f.write(go_code)
    print(f"   ✅ Saved")
    print()

    # Step 5: Display preview
    print("📝 Preview (first 50 lines):")
    print("-" * 80)
    lines = go_code.splitlines()
    for i, line in enumerate(lines[:50], 1):
        print(f"{i:3d} | {line}")
    if len(lines) > 50:
        print(f"... ({len(lines) - 50} more lines)")
    print("-" * 80)
    print()

    # Step 6: Attempt compilation check
    print("🔨 Checking Go syntax...")
    import subprocess
    try:
        result = subprocess.run(
            ['go', 'fmt', str(go_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("   ✅ Go fmt succeeded - syntax is valid!")
        else:
            print(f"   ⚠️  Go fmt reported issues:")
            if result.stderr:
                print(f"      {result.stderr}")
    except FileNotFoundError:
        print("   ⚠️  Go not found in PATH - skipping syntax check")
    except subprocess.TimeoutExpired:
        print("   ⚠️  Go fmt timed out")
    except Exception as e:
        print(f"   ⚠️  Could not run go fmt: {e}")
    print()

    # Summary
    print("=" * 80)
    print("✅ Translation Complete!")
    print("=" * 80)
    print(f"Input:  {pw_file}")
    print(f"Output: {go_file}")
    print(f"IR Functions: {len(ir_module.functions)}")
    print(f"Go Lines: {len(go_code.splitlines())}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
