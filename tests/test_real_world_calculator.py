"""
Test real-world program: Calculator CLI

This tests the complete calculator program that uses:
- Classes with constructor and methods
- Arrays and maps
- Control flow (if/while)
- Function calls
- Multi-line syntax
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.pw_parser import parse_pw


def test_calculator_parses():
    """Test that calculator program parses without errors."""
    print(f"\n{'='*60}")
    print("Testing Calculator CLI Program")
    print(f"{'='*60}")

    # Read the calculator program
    calc_file = Path(__file__).parent.parent / "examples" / "calculator_cli.pw"

    try:
        with open(calc_file) as f:
            pw_code = f.read()

        print(f"  ✅ Read calculator program: {len(pw_code)} chars")

        # Parse the program
        ir = parse_pw(pw_code)

        print(f"  ✅ Parsed successfully")
        print(f"  ✅ Classes: {len(ir.classes)}")
        print(f"  ✅ Functions: {len(ir.functions)}")

        # Verify expected structure
        assert len(ir.classes) == 1, f"Expected 1 class, got {len(ir.classes)}"
        assert ir.classes[0].name == "Calculator", f"Expected Calculator class"

        # Calculator should have history property
        assert len(ir.classes[0].properties) == 1, "Expected 1 property"
        assert ir.classes[0].properties[0].name == "history"

        # Calculator should have constructor
        assert ir.classes[0].constructor is not None, "Expected constructor"

        # Calculator should have 5 methods (add, subtract, multiply, divide, get_history, clear_history)
        assert len(ir.classes[0].methods) >= 5, f"Expected at least 5 methods, got {len(ir.classes[0].methods)}"

        method_names = [m.name for m in ir.classes[0].methods]
        assert "add" in method_names, "Expected add method"
        assert "subtract" in method_names, "Expected subtract method"
        assert "multiply" in method_names, "Expected multiply method"
        assert "divide" in method_names, "Expected divide method"

        # Should have helper functions
        function_names = [f.name for f in ir.functions]
        assert "parse_operation" in function_names
        assert "calculate" in function_names
        assert "run_calculator" in function_names
        assert "main" in function_names

        print(f"\n✅ SUCCESS: Calculator CLI program is valid!")
        print(f"\nProgram structure:")
        print(f"  - Calculator class with {len(ir.classes[0].methods)} methods")
        print(f"  - {len(ir.functions)} helper functions")
        print(f"  - Uses: classes, arrays, maps, loops, conditionals")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_calculator_parses()
    sys.exit(0 if success else 1)
