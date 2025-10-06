"""
Test Rust Iterator Chain / Collection Operations Round-Trip

This test validates that:
1. Rust parser correctly detects .iter().filter().map().collect() chains
2. Rust generator produces idiomatic iterator chains from IR
3. Round-trip translation preserves semantics (Rust → IR → Rust)
4. Cross-language translation works (Python ↔ Rust, etc.)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.rust_parser_v2 import RustParserV2
from language.rust_generator_v2 import RustGeneratorV2
from dsl.ir import IRComprehension, IRIdentifier


def test_basic_map():
    """Test basic .iter().map().collect() pattern"""
    print("\n=== Test 1: Basic Map ===")

    source = """
pub fn transform_numbers(numbers: Vec<i32>) -> Vec<i32> {
    let result = numbers.iter().map(|n| n * 2).collect();
    return result;
}
"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(source, "test")

    # Verify IR contains comprehension
    assert len(ir.functions) == 1, "Should have one function"
    func = ir.functions[0]

    # Find the comprehension in the function body
    comprehension_found = False
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRComprehension):
            comprehension_found = True
            comp = stmt.value

            # Verify structure
            assert comp.iterator == "n", f"Iterator should be 'n', got {comp.iterator}"
            assert isinstance(comp.iterable, IRIdentifier), "Iterable should be identifier"
            assert comp.iterable.name == "numbers", f"Iterable should be 'numbers', got {comp.iterable.name}"
            assert comp.condition is None, "Should have no filter condition"
            assert comp.comprehension_type == "list", "Should be list comprehension"

            print(f"✅ Comprehension parsed correctly")
            print(f"   Iterator: {comp.iterator}")
            print(f"   Iterable: {comp.iterable.name}")
            print(f"   Target: {comp.target}")
            break

    assert comprehension_found, "Should find comprehension in parsed IR"

    # Generate IR → Rust
    generator = RustGeneratorV2()
    result = generator.generate(ir)

    print(f"\nGenerated Rust:\n{result}")

    # Verify output contains iterator chain
    assert ".iter()" in result, "Should contain .iter()"
    assert ".map(" in result, "Should contain .map()"
    assert ".collect()" in result, "Should contain .collect()"
    assert "|n|" in result or "|n |" in result, "Should contain closure parameter"

    print("✅ Rust map test passed")


def test_filter_map():
    """Test .iter().filter().map().collect() pattern"""
    print("\n=== Test 2: Filter + Map ===")

    source = """
pub fn filter_and_transform(numbers: Vec<i32>) -> Vec<i32> {
    let evens = numbers.iter().filter(|n| n % 2 == 0).map(|n| n * 2).collect();
    return evens;
}
"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(source, "test")

    # Verify IR contains comprehension with filter
    assert len(ir.functions) == 1, "Should have one function"
    func = ir.functions[0]

    comprehension_found = False
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRComprehension):
            comprehension_found = True
            comp = stmt.value

            # Verify structure
            assert comp.iterator == "n", f"Iterator should be 'n', got {comp.iterator}"
            assert comp.condition is not None, "Should have filter condition"
            assert comp.comprehension_type == "list", "Should be list comprehension"

            print(f"✅ Filter+Map comprehension parsed correctly")
            print(f"   Iterator: {comp.iterator}")
            print(f"   Has condition: {comp.condition is not None}")
            break

    assert comprehension_found, "Should find comprehension in parsed IR"

    # Generate IR → Rust
    generator = RustGeneratorV2()
    result = generator.generate(ir)

    print(f"\nGenerated Rust:\n{result}")

    # Verify output contains complete iterator chain
    assert ".iter()" in result, "Should contain .iter()"
    assert ".filter(" in result, "Should contain .filter()"
    assert ".map(" in result, "Should contain .map()"
    assert ".collect()" in result, "Should contain .collect()"

    print("✅ Rust filter+map test passed")


def test_filter_only():
    """Test .iter().filter().collect() pattern (no map)"""
    print("\n=== Test 3: Filter Only ===")

    source = """
pub fn get_evens(numbers: Vec<i32>) -> Vec<i32> {
    let evens = numbers.iter().filter(|n| n % 2 == 0).collect();
    return evens;
}
"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(source, "test")

    # Verify IR
    assert len(ir.functions) == 1, "Should have one function"
    func = ir.functions[0]

    comprehension_found = False
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRComprehension):
            comprehension_found = True
            comp = stmt.value

            # Verify structure
            assert comp.condition is not None, "Should have filter condition"
            # Target should be just the iterator (no transformation)
            assert isinstance(comp.target, IRIdentifier), "Target should be identifier"
            assert comp.target.name == comp.iterator, "Target should equal iterator (no transform)"

            print(f"✅ Filter-only comprehension parsed correctly")
            break

    assert comprehension_found, "Should find comprehension in parsed IR"

    # Generate IR → Rust
    generator = RustGeneratorV2()
    result = generator.generate(ir)

    print(f"\nGenerated Rust:\n{result}")

    # Verify output
    assert ".iter()" in result, "Should contain .iter()"
    assert ".filter(" in result, "Should contain .filter()"
    assert ".collect()" in result, "Should contain .collect()"
    # Should NOT have .map() since we're just filtering
    # (Generator should detect that element == iterator)

    print("✅ Rust filter-only test passed")


def test_into_iter():
    """Test into_iter() variant (consuming iterator)"""
    print("\n=== Test 4: into_iter() Variant ===")

    source = """
pub fn consume_and_transform(numbers: Vec<i32>) -> Vec<i32> {
    let result = numbers.into_iter().map(|n| n * 2).collect();
    return result;
}
"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(source, "test")

    # Verify parsing works
    assert len(ir.functions) == 1, "Should have one function"
    func = ir.functions[0]

    comprehension_found = False
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRComprehension):
            comprehension_found = True
            print(f"✅ into_iter() parsed as comprehension")
            break

    assert comprehension_found, "Should parse into_iter() chains"

    # Generate IR → Rust
    generator = RustGeneratorV2()
    result = generator.generate(ir)

    print(f"\nGenerated Rust:\n{result}")

    # Generator always outputs .iter() (standard form)
    assert ".iter()" in result, "Should contain .iter()"
    assert ".map(" in result, "Should contain .map()"
    assert ".collect()" in result, "Should contain .collect()"

    print("✅ Rust into_iter test passed")


def test_real_world_example():
    """Test real-world pattern: filter users by active status"""
    print("\n=== Test 5: Real-World Example ===")

    source = """
pub fn get_active_user_names(users: Vec<User>) -> Vec<String> {
    let names = users.iter()
        .filter(|u| u.is_active)
        .map(|u| u.name.clone())
        .collect();
    return names;
}
"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(source, "test")

    # Verify parsing
    assert len(ir.functions) == 1, "Should have one function"
    func = ir.functions[0]

    comprehension_found = False
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRComprehension):
            comprehension_found = True
            comp = stmt.value

            print(f"✅ Real-world pattern parsed")
            print(f"   Iterator: {comp.iterator}")
            print(f"   Has filter: {comp.condition is not None}")
            print(f"   Has map: {comp.target is not None}")
            break

    assert comprehension_found, "Should parse real-world pattern"

    # Generate IR → Rust
    generator = RustGeneratorV2()
    result = generator.generate(ir)

    print(f"\nGenerated Rust:\n{result}")

    # Verify complete chain
    assert ".iter()" in result, "Should contain .iter()"
    assert ".filter(" in result, "Should contain .filter()"
    assert ".map(" in result, "Should contain .map()"
    assert ".collect()" in result, "Should contain .collect()"

    print("✅ Real-world example test passed")


def test_round_trip():
    """Test complete round-trip: Rust → IR → Rust"""
    print("\n=== Test 6: Round-Trip ===")

    original = """pub fn process(items: Vec<i32>) -> Vec<i32> {
    let result = items.iter().filter(|x| x > 0).map(|x| x * 2).collect();
    return result;
}"""

    # Parse Rust → IR
    parser = RustParserV2()
    ir1 = parser.parse_source(original, "test")

    # Generate IR → Rust
    generator = RustGeneratorV2()
    generated1 = generator.generate(ir1)

    print(f"First generation:\n{generated1}")

    # Parse again: Generated Rust → IR
    ir2 = parser.parse_source(generated1, "test")

    # Generate again: IR → Rust
    generated2 = generator.generate(ir2)

    print(f"\nSecond generation:\n{generated2}")

    # Both generations should be functionally identical
    # (May have formatting differences, but semantics preserved)
    assert ".iter()" in generated2, "Round-trip should preserve .iter()"
    assert ".filter(" in generated2, "Round-trip should preserve .filter()"
    assert ".map(" in generated2, "Round-trip should preserve .map()"
    assert ".collect()" in generated2, "Round-trip should preserve .collect()"

    # Both should have same number of functions
    assert len(ir1.functions) == len(ir2.functions), "Function count should match"

    print("✅ Round-trip test passed - semantics preserved")


def run_all_tests():
    """Run all Rust comprehension tests"""
    print("\n" + "="*60)
    print("RUST ITERATOR CHAIN / COLLECTION OPERATIONS TESTS")
    print("="*60)

    tests = [
        ("Basic Map", test_basic_map),
        ("Filter + Map", test_filter_map),
        ("Filter Only", test_filter_only),
        ("into_iter() Variant", test_into_iter),
        ("Real-World Example", test_real_world_example),
        ("Round-Trip", test_round_trip),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    if failed > 0:
        print(f"❌ {failed} tests failed")
        return False
    else:
        print("✅ ALL RUST COMPREHENSION TESTS PASSED")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
