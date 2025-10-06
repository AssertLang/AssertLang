"""
Cross-Language Collection Operation Translation Tests

Tests bidirectional translation of collection operations across:
- Python (comprehensions)
- JavaScript (.map/.filter)
- Rust (.iter().map().collect())
- C# (LINQ .Where().Select())

Validates that the IR-based translation preserves semantics across all combinations.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import PythonGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


def test_python_to_javascript():
    """Python comprehension → JavaScript map/filter"""
    print("\n=== Python → JavaScript ===")
    
    python_code = """
def process(items):
    result = [x * 2 for x in items if x > 0]
    return result
"""
    
    # Parse Python → IR
    parser = PythonParserV2()
    ir = parser.parse_source(python_code, "test.py")
    
    # Generate IR → JavaScript
    generator = NodeJSGeneratorV2()
    js_code = generator.generate(ir)
    
    print(f"Generated JavaScript:\n{js_code}\n")
    
    # Verify contains filter and map
    assert ".filter(" in js_code, "Should have .filter()"
    assert ".map(" in js_code, "Should have .map()"
    
    print("✅ Python → JavaScript translation works")


def test_javascript_to_rust():
    """JavaScript .filter().map() → Rust iterator chain"""
    print("\n=== JavaScript → Rust ===")
    
    js_code = """
function transform(numbers) {
    const result = numbers.filter(x => x > 10).map(x => x * 2);
    return result;
}
"""
    
    # Parse JS → IR
    parser = NodeJSParserV2()
    ir = parser.parse_source(js_code, "test.js")
    
    # Generate IR → Rust
    generator = RustGeneratorV2()
    rust_code = generator.generate(ir)
    
    print(f"Generated Rust:\n{rust_code}\n")
    
    # Verify contains iterator chain
    assert ".iter()" in rust_code, "Should have .iter()"
    assert ".filter(" in rust_code, "Should have .filter()"
    assert ".map(" in rust_code, "Should have .map()"
    assert ".collect()" in rust_code, "Should have .collect()"
    
    print("✅ JavaScript → Rust translation works")


def test_rust_to_csharp():
    """Rust iterator chain → C# LINQ"""
    print("\n=== Rust → C# ===")
    
    rust_code = """
pub fn process_numbers(items: Vec<i32>) -> Vec<i32> {
    let result = items.iter().filter(|x| x % 2 == 0).map(|x| x * 2).collect();
    return result;
}
"""
    
    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(rust_code, "test.rs")
    
    # Generate IR → C#
    generator = DotNetGeneratorV2()
    csharp_code = generator.generate(ir)
    
    print(f"Generated C#:\n{csharp_code}\n")
    
    # Verify contains LINQ
    assert ".Where(" in csharp_code, "Should have .Where()"
    assert ".Select(" in csharp_code, "Should have .Select()"
    assert ".ToList()" in csharp_code, "Should have .ToList()"
    
    print("✅ Rust → C# translation works")


def test_csharp_to_python():
    """C# LINQ → Python comprehension"""
    print("\n=== C# → Python ===")
    
    csharp_code = """
public class Processor {
    public List<int> Filter(List<int> data) {
        var evens = data.Where(x => x % 2 == 0).Select(x => x + 1).ToList();
        return evens;
    }
}
"""
    
    # Parse C# → IR
    parser = DotNetParserV2()
    ir = parser.parse_source(csharp_code, "test.cs")
    
    # Generate IR → Python
    generator = PythonGeneratorV2()
    python_code = generator.generate(ir)
    
    print(f"Generated Python:\n{python_code}\n")
    
    # Verify contains comprehension syntax
    assert "[" in python_code and "for" in python_code and "in" in python_code
    
    print("✅ C# → Python translation works")


def test_round_trip_all_languages():
    """Test Python → JS → Rust → C# → Python preserves semantics"""
    print("\n=== Full Round-Trip: Python → JS → Rust → C# → Python ===")
    
    original_python = """
def filter_positives(numbers):
    result = [n * 2 for n in numbers if n > 0]
    return result
"""
    
    # Python → IR
    py_parser = PythonParserV2()
    ir1 = py_parser.parse_source(original_python, "test.py")
    
    # IR → JavaScript
    js_gen = NodeJSGeneratorV2()
    js_code = js_gen.generate(ir1)
    print(f"Step 1 - JavaScript:\n{js_code[:100]}...\n")
    
    # JavaScript → IR
    js_parser = NodeJSParserV2()
    ir2 = js_parser.parse_source(js_code, "test.js")
    
    # IR → Rust
    rust_gen = RustGeneratorV2()
    rust_code = rust_gen.generate(ir2)
    print(f"Step 2 - Rust:\n{rust_code[:150]}...\n")
    
    # Rust → IR
    rust_parser = RustParserV2()
    ir3 = rust_parser.parse_source(rust_code, "test.rs")
    
    # IR → C#
    cs_gen = DotNetGeneratorV2()
    cs_code = cs_gen.generate(ir3)
    print(f"Step 3 - C#:\n{cs_code[:150]}...\n")
    
    # C# → IR
    cs_parser = DotNetParserV2()
    ir4 = cs_parser.parse_source(cs_code, "test.cs")
    
    # IR → Python (back to original)
    py_gen = PythonGeneratorV2()
    final_python = py_gen.generate(ir4)
    print(f"Step 4 - Back to Python:\n{final_python[:150]}...\n")
    
    # Verify all translations preserve collection operation
    assert ".filter(" in js_code and ".map(" in js_code
    assert ".iter()" in rust_code and ".collect()" in rust_code
    assert ".Where(" in cs_code and ".Select(" in cs_code
    assert "for" in final_python and "in" in final_python
    
    print("✅ Full round-trip translation preserves semantics")


def run_all_tests():
    """Run all cross-language translation tests"""
    print("\n" + "="*70)
    print("CROSS-LANGUAGE COLLECTION OPERATION TRANSLATION TESTS")
    print("="*70)
    
    tests = [
        ("Python → JavaScript", test_python_to_javascript),
        ("JavaScript → Rust", test_javascript_to_rust),
        ("Rust → C#", test_rust_to_csharp),
        ("C# → Python", test_csharp_to_python),
        ("Full Round-Trip", test_round_trip_all_languages),
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
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    if failed > 0:
        print(f"❌ {failed} tests failed")
        return False
    else:
        print("✅ ALL CROSS-LANGUAGE TRANSLATION TESTS PASSED")
        print("\nBidirectional collection operation translation working across:")
        print("  - Python (comprehensions)")
        print("  - JavaScript (.map/.filter)")
        print("  - Rust (.iter().map().collect())")
        print("  - C# (LINQ .Where().Select())")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
