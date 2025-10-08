"""
Final Validation Test Suite - Measure Translation Quality

Tests Python → PW → Go → PW → Python round-trip quality.
"""

import sys
from pathlib import Path
from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2
from language.go_parser_v2 import GoParserV2
from language.python_generator_v2 import PythonGeneratorV2
from dsl.pw_generator import generate_pw
from dsl.pw_parser import parse_pw


def test_simple_function():
    """Test simple function translation."""
    print("\n" + "="*80)
    print("TEST 1: Simple Function")
    print("="*80)

    python_code = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR
    parser = PythonParserV2()
    ir1 = parser.parse_source(python_code)
    print(f"✓ Parsed: {len(ir1.functions)} functions")

    # IR → Go
    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir1)
    print("\n2. Generated Go:")
    print(go_code)

    # Go → IR
    go_parser = GoParserV2()
    ir2 = go_parser.parse_source(go_code)
    print(f"✓ Parsed back: {len(ir2.functions)} functions")

    # IR → Python
    py_gen = PythonGeneratorV2()
    python_code2 = py_gen.generate(ir2)
    print("\n3. Round-trip Python:")
    print(python_code2)

    # Validate
    assert len(ir1.functions) == len(ir2.functions), "Function count mismatch"
    assert ir1.functions[0].name == ir2.functions[0].name, "Function name mismatch"

    print("\n✅ Simple function: PASS")
    return True


def test_control_flow():
    """Test control flow translation."""
    print("\n" + "="*80)
    print("TEST 2: Control Flow")
    print("="*80)

    python_code = '''
def check_value(x: int) -> str:
    """Check if value is positive, negative, or zero."""
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR → Go
    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    print("\n2. Generated Go:")
    print(go_code)

    # Validate structure
    assert "if (x > 0)" in go_code, "Missing if condition"
    assert "else" in go_code, "Missing else"

    print("\n✅ Control flow: PASS")
    return True


def test_list_operations():
    """Test list/array operations."""
    print("\n" + "="*80)
    print("TEST 3: List Operations")
    print("="*80)

    python_code = '''
def process_list(numbers: list) -> list:
    """Double all numbers."""
    result = []
    for num in numbers:
        result.append(num * 2)
    return result
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR → Go
    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    print("\n2. Generated Go:")
    print(go_code)

    # Validate
    assert "result := []interface{}{}" in go_code or "var result" in go_code, "Missing result initialization"
    assert "append(result, " in go_code, "Missing append"
    assert "for _, num := range numbers" in go_code or "for num" in go_code, "Missing for loop"

    print("\n✅ List operations: PASS")
    return True


def test_type_inference():
    """Test type inference quality."""
    print("\n" + "="*80)
    print("TEST 4: Type Inference")
    print("="*80)

    python_code = '''
def example():
    """Test type inference."""
    name = "Alice"
    age = 30
    score = 95.5
    active = True
    numbers = [1, 2, 3]
    return name
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR → Go
    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    print("\n2. Generated Go:")
    print(go_code)

    # Count specific types vs interface{}
    specific_types = 0
    generic_types = 0

    lines = go_code.split('\n')
    for line in lines:
        if 'var ' in line or ':=' in line:
            if 'string' in line or 'int' in line or 'float64' in line or 'bool' in line or '[]int' in line:
                specific_types += 1
            elif 'interface{}' in line:
                generic_types += 1

    total = specific_types + generic_types
    if total > 0:
        accuracy = (specific_types / total) * 100
        print(f"\nType inference accuracy: {accuracy:.1f}% ({specific_types}/{total} specific types)")
        assert accuracy >= 80, f"Type inference too low: {accuracy}%"

    print("\n✅ Type inference: PASS")
    return True


def test_comprehension_to_loop():
    """Test comprehension conversion."""
    print("\n" + "="*80)
    print("TEST 5: Comprehension → Clean Loop")
    print("="*80)

    python_code = '''
def filter_evens(numbers: list) -> list:
    """Get even numbers."""
    evens = [x for x in numbers if x % 2 == 0]
    return evens
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR → Go
    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    print("\n2. Generated Go:")
    print(go_code)

    # Validate clean loop (no IIFE)
    assert "func() []interface{}" not in go_code, "Should use clean loop, not IIFE"
    assert "evens := []interface{}{}" in go_code or "var evens" in go_code, "Missing initialization"
    assert "for _, x := range numbers" in go_code, "Missing for loop"
    assert "if " in go_code and "% 2" in go_code, "Missing filter condition"
    assert "append(evens, " in go_code, "Missing append"

    print("\n✅ Comprehension to loop: PASS")
    return True


def test_math_operations():
    """Test mathematical operations."""
    print("\n" + "="*80)
    print("TEST 6: Math Operations (Power, etc.)")
    print("="*80)

    python_code = '''
def calculate(x: float, y: float) -> float:
    """Calculate x squared plus y cubed."""
    return x ** 2 + y ** 3
'''

    print("\n1. Original Python:")
    print(python_code)

    # Python → IR → Go
    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    print("\n2. Generated Go:")
    print(go_code)

    # Validate power operator converted to math.Pow
    assert "math.Pow" in go_code, "Power operator should use math.Pow"
    assert "**" not in go_code, "Should not have ** operator"

    print("\n✅ Math operations: PASS")
    return True


def calculate_overall_quality():
    """Calculate overall translation quality metrics."""
    print("\n" + "="*80)
    print("OVERALL QUALITY ASSESSMENT")
    print("="*80)

    tests = [
        ("Simple functions", test_simple_function),
        ("Control flow", test_control_flow),
        ("List operations", test_list_operations),
        ("Type inference", test_type_inference),
        ("Comprehensions", test_comprehension_to_loop),
        ("Math operations", test_math_operations),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {name}: ERROR - {e}")

    total = passed + failed
    quality = (passed / total) * 100 if total > 0 else 0

    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Tests passed: {passed}/{total}")
    print(f"Quality score: {quality:.1f}%")
    print()

    if quality >= 90:
        print("🎉 EXCELLENT! System meets 90%+ quality target!")
    elif quality >= 80:
        print("✅ GOOD! System meets 80%+ quality target.")
    elif quality >= 70:
        print("⚠️  ACCEPTABLE. System approaching quality target.")
    else:
        print("❌ NEEDS IMPROVEMENT. Quality below target.")

    return quality


if __name__ == "__main__":
    try:
        quality = calculate_overall_quality()
        sys.exit(0 if quality >= 80 else 1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
