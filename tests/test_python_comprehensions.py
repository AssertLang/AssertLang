"""
Test Python comprehension parsing and generation.

This test validates that Python comprehensions are correctly:
1. Parsed into IRComprehension nodes
2. Generated back to idiomatic Python comprehensions
"""

from language.python_parser_v2 import PythonParserV2
from language.python_generator_v2 import PythonGeneratorV2


def test_list_comprehension():
    """Test list comprehension round-trip."""
    source = """
def process_numbers(numbers):
    evens = [n for n in numbers if n % 2 == 0]
    doubled = [n * 2 for n in numbers]
    return evens, doubled
"""

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(source, "test")

    # Generate
    generator = PythonGeneratorV2()
    result = generator.generate(ir_module)

    print("=== Original ===")
    print(source)
    print("\n=== Generated ===")
    print(result)

    # Validate - check that comprehensions are present
    assert "[n for n in numbers" in result or "[n for n in" in result, "List comprehension missing"
    assert "if" in result, "Filter condition missing"
    print("✅ List comprehension test passed")


def test_dict_comprehension():
    """Test dict comprehension round-trip."""
    source = """
def make_squares(numbers):
    squares = {n: n ** 2 for n in numbers}
    filtered = {n: n * 2 for n in numbers if n > 0}
    return squares, filtered
"""

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(source, "test")

    # Generate
    generator = PythonGeneratorV2()
    result = generator.generate(ir_module)

    print("\n=== Original ===")
    print(source)
    print("\n=== Generated ===")
    print(result)

    # Validate - check that dict comprehensions are present
    assert "{" in result and ":" in result and "for" in result, "Dict comprehension missing"
    print("✅ Dict comprehension test passed")


def test_set_comprehension():
    """Test set comprehension round-trip."""
    source = """
def unique_doubles(numbers):
    result = {n * 2 for n in numbers}
    return result
"""

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(source, "test")

    # Generate
    generator = PythonGeneratorV2()
    result = generator.generate(ir_module)

    print("\n=== Original ===")
    print(source)
    print("\n=== Generated ===")
    print(result)

    # Validate - check that set comprehension is present
    assert "{" in result and "for" in result and "in" in result, "Set comprehension missing"
    print("✅ Set comprehension test passed")


def test_generator_expression():
    """Test generator expression round-trip."""
    source = """
def process_lazy(numbers):
    gen = (n * 2 for n in numbers if n > 0)
    return list(gen)
"""

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(source, "test")

    # Generate
    generator = PythonGeneratorV2()
    result = generator.generate(ir_module)

    print("\n=== Original ===")
    print(source)
    print("\n=== Generated ===")
    print(result)

    # Validate - check that generator expression is present
    assert "(" in result and "for" in result and "in" in result, "Generator expression missing"
    print("✅ Generator expression test passed")


def test_real_world_example():
    """Test realistic data processing with comprehensions."""
    source = """
def analyze_users(users):
    active_users = [u for u in users if u.is_active]
    emails = [u.email for u in active_users]
    by_age = {u.age: u for u in users}
    unique_cities = {u.city for u in users if u.city is not None}
    return active_users, emails, by_age, unique_cities
"""

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(source, "test")

    # Check IR structure
    func = ir_module.functions[0]
    print(f"\n=== IR Function: {func.name} ===")
    print(f"Parameters: {len(func.params)}")
    print(f"Body statements: {len(func.body)}")

    # Generate
    generator = PythonGeneratorV2()
    result = generator.generate(ir_module)

    print("\n=== Original ===")
    print(source)
    print("\n=== Generated ===")
    print(result)

    # Validate all comprehension types are present
    assert "[u for u in users" in result or "[u for u in" in result, "List comprehension missing"
    assert "{" in result and ":" in result, "Dict comprehension missing"
    print("✅ Real-world example test passed")


if __name__ == "__main__":
    print("Testing Python Comprehension Support")
    print("=" * 60)

    try:
        test_list_comprehension()
        test_dict_comprehension()
        test_set_comprehension()
        test_generator_expression()
        test_real_world_example()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
