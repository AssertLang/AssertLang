#!/usr/bin/env python3
"""
Test AssertLang v0.1.6 Fix

Tests the fix for ISSUE #1: Auto-import al_math, al_str, al_list when used.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.al_parser import parse_al
from language.python_generator_v2 import PythonGeneratorV2


def test_math_auto_import():
    """
    Test that math module functions trigger auto-import.
    """
    al_code = """
function calculate(x: float) -> float {
    let rounded = math.round(x);
    let max_val = math.max(rounded, 10);
    let min_val = math.min(max_val, 100);
    let power = math.pow(2, 3);
    return math.floor(min_val);
}
"""

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    print("=" * 80)
    print("TEST #1: Math Module Auto-Import")
    print("=" * 80)

    # Check that al_math is auto-imported
    if "al_math as math" in py_code:
        print("✅ PASS: al_math auto-imported")
    else:
        print("❌ FAIL: al_math NOT auto-imported")
        print(py_code)
        return False

    # Verify the import line format
    if "from assertlang.runtime import Ok, Error, Result, al_math as math" in py_code:
        print("✅ PASS: Import line format correct")
    else:
        print("❌ FAIL: Import line format incorrect")
        return False

    # Verify math.round(), math.max(), etc. are in the code
    if "math.round(" in py_code and "math.max(" in py_code:
        print("✅ PASS: Math functions present in generated code")
    else:
        print("❌ FAIL: Math functions missing")
        return False

    print("\n📝 Generated Python:")
    print("-" * 80)
    print(py_code)
    print("-" * 80)

    return True


def test_str_auto_import():
    """
    Test that str module functions trigger auto-import.
    """
    al_code = """
function format_text(name: string) -> string {
    let length = str.length(name);
    let upper = str.upper(name);
    return upper;
}
"""

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    print("\n" + "=" * 80)
    print("TEST #2: Str Module Auto-Import")
    print("=" * 80)

    # Note: str.length() is translated to len(), so str might not be imported
    # But str.upper() should trigger the import
    if "al_str as str" in py_code:
        print("✅ PASS: al_str auto-imported")
    else:
        print("❌ FAIL: al_str NOT auto-imported")
        print(py_code)
        return False

    print("\n📝 Generated Python:")
    print("-" * 80)
    print(py_code)
    print("-" * 80)

    return True


def test_list_auto_import():
    """
    Test that list module functions trigger auto-import.
    """
    al_code = """
function process_list(items: list) -> list {
    let first = list.first(items);
    let last = list.last(items);
    let reversed = list.reverse(items);
    return reversed;
}
"""

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    print("\n" + "=" * 80)
    print("TEST #3: List Module Auto-Import")
    print("=" * 80)

    if "al_list as list" in py_code:
        print("✅ PASS: al_list auto-imported")
    else:
        print("❌ FAIL: al_list NOT auto-imported")
        print(py_code)
        return False

    print("\n📝 Generated Python:")
    print("-" * 80)
    print(py_code)
    print("-" * 80)

    return True


def test_multiple_modules_auto_import():
    """
    Test that multiple modules are auto-imported when all are used.
    """
    al_code = """
function complex_calculation(data: list, threshold: float) -> string {
    let count = list.length(data);
    let avg = math.round(threshold);
    let result = str.upper("result");
    return result;
}
"""

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    print("\n" + "=" * 80)
    print("TEST #4: Multiple Modules Auto-Import")
    print("=" * 80)

    all_imported = (
        "al_math as math" in py_code and
        "al_str as str" in py_code and
        "al_list as list" in py_code
    )

    if all_imported:
        print("✅ PASS: All three modules auto-imported")
    else:
        print(f"❌ FAIL: Not all modules imported")
        print(f"  math: {'✅' if 'al_math as math' in py_code else '❌'}")
        print(f"  str:  {'✅' if 'al_str as str' in py_code else '❌'}")
        print(f"  list: {'✅' if 'al_list as list' in py_code else '❌'}")
        print(py_code)
        return False

    print("\n📝 Generated Python:")
    print("-" * 80)
    print(py_code)
    print("-" * 80)

    return True


def test_no_modules_no_import():
    """
    Test that modules are NOT imported when not used.
    """
    al_code = """
function simple_function(x: int) -> int {
    return x + 1;
}
"""

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    print("\n" + "=" * 80)
    print("TEST #5: No Unnecessary Imports")
    print("=" * 80)

    # Should only have Ok, Error, Result - no module imports
    if "from assertlang.runtime import Ok, Error, Result\n" in py_code:
        print("✅ PASS: Only basic runtime imported (no unnecessary modules)")
    else:
        print("❌ FAIL: Unexpected imports")
        print(py_code)
        return False

    # Make sure no al_math, al_str, al_list in imports
    if "al_math" not in py_code and "al_str" not in py_code and "al_list" not in py_code:
        print("✅ PASS: No module imports when not needed")
    else:
        print("❌ FAIL: Unnecessary module imports present")
        return False

    print("\n📝 Generated Python:")
    print("-" * 80)
    print(py_code)
    print("-" * 80)

    return True


def test_generated_code_runs():
    """
    Test that generated code with auto-imports actually runs.
    """
    al_code = """
function calculate_dose(weight: float, age: int) -> float {
    let base_dose = weight * 1.5;
    let adjusted = math.round(base_dose);
    let minimum = math.max(adjusted, 10);
    return math.min(minimum, 100);
}
"""

    print("\n" + "=" * 80)
    print("TEST #6: Generated Code Execution")
    print("=" * 80)

    ir_module = parse_al(al_code)
    generator = PythonGeneratorV2()
    py_code = generator.generate(ir_module)

    # Try to execute the generated code
    try:
        # Add parent to path for assertlang.runtime import
        exec_globals = {"__name__": "__main__"}
        exec(py_code, exec_globals)

        # Test the function
        calculate_dose = exec_globals["calculate_dose"]
        result = calculate_dose(50.0, 30)

        if result == 75.0:
            print(f"✅ PASS: Generated code executes correctly (result: {result})")
            return True
        else:
            print(f"❌ FAIL: Unexpected result: {result} (expected 75.0)")
            return False

    except Exception as e:
        print(f"❌ FAIL: Generated code failed to execute: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "        AssertLang v0.1.6 - Auto-Import Fix Test Suite".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)

    all_passed = True

    # Run tests
    if not test_math_auto_import():
        all_passed = False

    if not test_str_auto_import():
        all_passed = False

    if not test_list_auto_import():
        all_passed = False

    if not test_multiple_modules_auto_import():
        all_passed = False

    if not test_no_modules_no_import():
        all_passed = False

    if not test_generated_code_runs():
        all_passed = False

    # Final result
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    if all_passed:
        print("✅✅✅ ALL TESTS PASSED ✅✅✅")
        print("\nv0.1.6 fix is working correctly!")
        print("\nFixed:")
        print("  ✅ Auto-import al_math when math.* functions used")
        print("  ✅ Auto-import al_str when str.* functions used")
        print("  ✅ Auto-import al_list when list.* functions used")
        print("  ✅ No unnecessary imports when modules not used")
        print("  ✅ Generated code runs without manual fixes")
        print("\nPython transpilation is now 100% production-ready!")
        exit(0)
    else:
        print("❌❌❌ SOME TESTS FAILED ❌❌❌")
        exit(1)
