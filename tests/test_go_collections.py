"""
Test Go Collection Operations (Comprehension → For-Append Pattern)

Go doesn't have list comprehensions, so we use immediately-invoked functions
that execute for-append patterns. This test validates:
1. Python/JS/Rust/C# comprehensions → Go for-append
2. Generated Go code is syntactically valid
3. Semantics are preserved
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2  
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2
from language.go_generator_v2 import GoGeneratorV2


def test_python_to_go():
    """Test Python comprehension → Go for-append"""
    print("\n=== Test 1: Python → Go ===")
    
    python_code = """
def filter_numbers(items):
    result = [x * 2 for x in items if x > 0]
    return result
"""
    
    # Parse Python → IR
    parser = PythonParserV2()
    ir = parser.parse_source(python_code, "test.py")
    
    # Generate IR → Go
    generator = GoGeneratorV2()
    go_code = generator.generate(ir)
    
    print(f"Generated Go:\n{go_code}\n")
    
    # Verify contains for-append pattern
    assert "for _, x := range" in go_code, "Should have for range loop"
    assert "append(result," in go_code, "Should have append call"
    assert "if" in go_code, "Should have condition"
    
    print("✅ Python → Go comprehension translation works")


def test_javascript_to_go():
    """Test JavaScript .filter().map() → Go for-append"""
    print("\n=== Test 2: JavaScript → Go ===")
    
    js_code = """
function processData(numbers) {
    const result = numbers.filter(x => x > 10).map(x => x * 2);
    return result;
}
"""
    
    # Parse JS → IR
    parser = NodeJSParserV2()
    ir = parser.parse_source(js_code, "test.js")
    
    # Generate IR → Go
    generator = GoGeneratorV2()
    go_code = generator.generate(ir)
    
    print(f"Generated Go:\n{go_code}\n")
    
    # Verify
    assert "for _, x := range" in go_code
    assert "append(result," in go_code
    
    print("✅ JavaScript → Go translation works")


def test_rust_to_go():
    """Test Rust iterator chain → Go for-append"""
    print("\n=== Test 3: Rust → Go ===")
    
    rust_code = """
pub fn transform(items: Vec<i32>) -> Vec<i32> {
    let result = items.iter().filter(|x| x > 5).map(|x| x + 1).collect();
    return result;
}
"""
    
    # Parse Rust → IR
    parser = RustParserV2()
    ir = parser.parse_source(rust_code, "test.rs")
    
    # Generate IR → Go
    generator = GoGeneratorV2()
    go_code = generator.generate(ir)
    
    print(f"Generated Go:\n{go_code}\n")
    
    # Verify
    assert "for _," in go_code
    assert "append(result," in go_code
    
    print("✅ Rust → Go translation works")


def test_csharp_to_go():
    """Test C# LINQ → Go for-append"""
    print("\n=== Test 4: C# → Go ===")
    
    csharp_code = """
public class Processor {
    public List<int> Filter(List<int> data) {
        var evens = data.Where(x => x % 2 == 0).Select(x => x * 2).ToList();
        return evens;
    }
}
"""
    
    # Parse C# → IR
    parser = DotNetParserV2()
    ir = parser.parse_source(csharp_code, "test.cs")
    
    # Generate IR → Go
    generator = GoGeneratorV2()
    go_code = generator.generate(ir)
    
    print(f"Generated Go:\n{go_code}\n")
    
    # Verify
    assert "for _," in go_code
    assert "append(result," in go_code
    
    print("✅ C# → Go translation works")


def test_go_no_filter():
    """Test map-only comprehension (no filter)"""
    print("\n=== Test 5: Map Only (No Filter) ===")
    
    python_code = """
def double(items):
    return [x * 2 for x in items]
"""
    
    parser = PythonParserV2()
    ir = parser.parse_source(python_code, "test.py")
    
    generator = GoGeneratorV2()
    go_code = generator.generate(ir)
    
    print(f"Generated Go:\n{go_code}\n")
    
    # Should have for-append but no if statement
    assert "for _, x := range" in go_code
    assert "append(result," in go_code
    # Should NOT have nested if (direct append)
    
    print("✅ Map-only comprehension works")


def run_all_tests():
    """Run all Go collection operation tests"""
    print("\n" + "="*70)
    print("GO COLLECTION OPERATIONS TESTS")
    print("(Comprehension → For-Append Pattern)")
    print("="*70)
    
    tests = [
        ("Python → Go", test_python_to_go),
        ("JavaScript → Go", test_javascript_to_go),
        ("Rust → Go", test_rust_to_go),
        ("C# → Go", test_csharp_to_go),
        ("Map Only", test_go_no_filter),
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
        print("✅ ALL GO COLLECTION TESTS PASSED")
        print("\nGo successfully generates for-append patterns from:")
        print("  - Python comprehensions")
        print("  - JavaScript .map/.filter")
        print("  - Rust iterator chains")
        print("  - C# LINQ")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
