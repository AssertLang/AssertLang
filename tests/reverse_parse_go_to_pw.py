#!/usr/bin/env python3
"""
Reverse Parse Go → IR → PW DSL

This script demonstrates the reverse parsing capability:
1. Parse Go code → IR using GoParserV2
2. Generate PW DSL from IR using PWGenerator

Author: Promptware Translation Agent
Date: 2025-10-05
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from language.go_parser_v2 import GoParserV2
from dsl.pw_generator import PWGenerator


def reverse_parse_go_to_pw(go_file: str, output_file: str) -> dict:
    """
    Reverse parse Go file to PW DSL.

    Args:
        go_file: Path to Go source file
        output_file: Path to output PW DSL file

    Returns:
        Dictionary with statistics and results
    """
    print("=" * 80)
    print("REVERSE PARSING: Go → IR → PW DSL")
    print("=" * 80)
    print(f"Input:  {go_file}")
    print(f"Output: {output_file}")
    print()

    # Step 1: Parse Go → IR
    print("Step 1: Parsing Go code → IR...")
    try:
        parser = GoParserV2()
        ir_module = parser.parse_file(go_file)
        print(f"✅ Successfully parsed Go code")
        print(f"   - Module: {ir_module.name}")
        print(f"   - Version: {ir_module.version}")
        print(f"   - Imports: {len(ir_module.imports)}")
        print(f"   - Functions: {len(ir_module.functions)}")
        print(f"   - Types: {len(ir_module.types)}")
        print(f"   - Module vars: {len(ir_module.module_vars)}")
        print()
    except Exception as e:
        print(f"❌ Failed to parse Go code: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

    # Step 2: Generate PW DSL from IR
    print("Step 2: Generating PW DSL from IR...")
    try:
        generator = PWGenerator(indent_size=2)
        pw_code = generator.generate(ir_module)
        print(f"✅ Successfully generated PW DSL")
        print(f"   - Lines: {len(pw_code.splitlines())}")
        print(f"   - Characters: {len(pw_code)}")
        print()
    except Exception as e:
        print(f"❌ Failed to generate PW DSL: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e), "ir_module": ir_module}

    # Step 3: Write output
    print("Step 3: Writing PW DSL to file...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pw_code)
        print(f"✅ Successfully wrote PW DSL to {output_file}")
        print()
    except Exception as e:
        print(f"❌ Failed to write output: {e}")
        return {"success": False, "error": str(e), "ir_module": ir_module, "pw_code": pw_code}

    # Step 4: Show preview
    print("=" * 80)
    print("PREVIEW: First 50 lines of generated PW DSL")
    print("=" * 80)
    lines = pw_code.splitlines()
    for i, line in enumerate(lines[:50], 1):
        print(f"{i:3d} | {line}")

    if len(lines) > 50:
        print(f"... ({len(lines) - 50} more lines)")
    print()

    # Step 5: Statistics
    print("=" * 80)
    print("STATISTICS")
    print("=" * 80)

    # Count different constructs
    function_names = [f.name for f in ir_module.functions]
    import_names = [imp.module for imp in ir_module.imports]
    type_names = [t.name for t in ir_module.types]
    module_var_names = [v.target if hasattr(v, 'target') else str(v) for v in ir_module.module_vars]

    print(f"Functions parsed ({len(function_names)}):")
    for name in function_names:
        print(f"  - {name}")
    print()

    print(f"Imports parsed ({len(import_names)}):")
    for name in import_names:
        print(f"  - {name}")
    print()

    print(f"Types parsed ({len(type_names)}):")
    for name in type_names:
        print(f"  - {name}")
    print()

    print(f"Module variables parsed ({len(module_var_names)}):")
    for name in module_var_names:
        print(f"  - {name}")
    print()

    # Step 6: Issues encountered
    print("=" * 80)
    print("ISSUES ENCOUNTERED")
    print("=" * 80)

    issues = []

    # Check for empty function bodies
    for func in ir_module.functions:
        if not func.body:
            issues.append(f"Function '{func.name}' has empty body (may have failed to parse)")

    # Check for parse failures in module vars
    for var in ir_module.module_vars:
        if hasattr(var, 'value') and var.value is None:
            if hasattr(var, 'target'):
                issues.append(f"Module variable '{var.target}' has no value (may have failed to parse)")

    if issues:
        print("Found issues during parsing:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("✅ No issues detected during parsing")
    print()

    # Return results
    return {
        "success": True,
        "ir_module": ir_module,
        "pw_code": pw_code,
        "functions_parsed": len(function_names),
        "imports_parsed": len(import_names),
        "types_parsed": len(type_names),
        "module_vars_parsed": len(module_var_names),
        "issues": issues,
        "output_lines": len(lines),
    }


def main():
    """Main entry point."""
    # File paths
    go_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_sentient_maze.go"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/test_sentient_maze_from_go.pw"

    # Run reverse parsing
    results = reverse_parse_go_to_pw(go_file, output_file)

    # Final summary
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    if results["success"]:
        print("✅ Reverse parsing completed successfully!")
        print(f"   - Functions: {results['functions_parsed']}")
        print(f"   - Imports: {results['imports_parsed']}")
        print(f"   - Types: {results['types_parsed']}")
        print(f"   - Module vars: {results['module_vars_parsed']}")
        print(f"   - Output lines: {results['output_lines']}")
        print(f"   - Issues: {len(results['issues'])}")
        print()
        print(f"Output saved to: {output_file}")
    else:
        print("❌ Reverse parsing failed")
        print(f"   Error: {results.get('error', 'Unknown error')}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
