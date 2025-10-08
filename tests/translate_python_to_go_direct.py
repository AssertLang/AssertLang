#!/usr/bin/env python3
"""
Direct Python → Go Translation (Bypassing PW DSL)

This script demonstrates the Python → IR → Go workflow:
1. Read Python source file
2. Parse Python → IR using python_parser_v2
3. Generate Go code from IR using go_generator_v2
4. Save Go output
5. Attempt to compile with Go
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import generate_go


def main():
    # Input: Python file
    py_file = project_root / "test_sentient_maze_original.py"

    # Output: Go file
    go_file = project_root / "test_sentient_maze.go"

    print("=" * 80)
    print("Python → Go Direct Translation")
    print("=" * 80)
    print()

    # Step 1: Read Python source
    print(f"📖 Reading Python from: {py_file}")
    with open(py_file, 'r') as f:
        py_code = f.read()
    print(f"   Lines: {len(py_code.splitlines())}")
    print()

    # Step 2: Parse Python → IR
    print("🔄 Parsing Python → IR...")
    try:
        parser = PythonParserV2()
        ir_module = parser.parse_file(str(py_file))
        print(f"   ✅ Module: {ir_module.name}")
        print(f"   ✅ Version: {ir_module.version}")
        print(f"   ✅ Imports: {len(ir_module.imports)}")
        print(f"   ✅ Functions: {len(ir_module.functions)}")
        print(f"   ✅ Classes: {len(ir_module.classes)}")
        print(f"   ✅ Module vars: {len(ir_module.module_vars)}")

        # Show function names
        if ir_module.functions:
            print("   📋 Functions found:")
            for func in ir_module.functions:
                print(f"      - {func.name}() with {len(func.params)} params")
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
        # First try go fmt
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

        # Try to build
        print()
        print("   Attempting go build...")
        result = subprocess.run(
            ['go', 'build', '-o', '/dev/null', str(go_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(project_root)
        )
        if result.returncode == 0:
            print("   ✅ Go build succeeded - code compiles!")
        else:
            print(f"   ⚠️  Go build reported issues:")
            if result.stderr:
                for line in result.stderr.splitlines()[:20]:
                    print(f"      {line}")
            if result.stdout:
                for line in result.stdout.splitlines()[:20]:
                    print(f"      {line}")
    except FileNotFoundError:
        print("   ⚠️  Go not found in PATH - skipping syntax check")
    except subprocess.TimeoutExpired:
        print("   ⚠️  Go timed out")
    except Exception as e:
        print(f"   ⚠️  Could not run go: {e}")
    print()

    # Summary
    print("=" * 80)
    print("✅ Translation Complete!")
    print("=" * 80)
    print(f"Input:  {py_file}")
    print(f"Output: {go_file}")
    print(f"Python Lines: {len(py_code.splitlines())}")
    print(f"Go Lines: {len(go_code.splitlines())}")
    print(f"Functions Translated: {len(ir_module.functions)}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
