#!/usr/bin/env python3
"""
Identify Exact Failure Patterns from Test Output

Analyzes test results to identify specific issues that need fixing.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2

from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


class FailureAnalyzer:
    """Analyzes test output to identify exact failure patterns."""

    def __init__(self):
        self.failures = []
        self.categories = {
            "type_inference": [],
            "syntax_errors": [],
            "semantic_errors": [],
            "library_mapping": [],
            "missing_features": [],
        }

    def analyze_go_struct_initialization(self):
        """Issue: User{\"Alice\", 30} instead of User{Name: \"Alice\", Age: 30}"""
        print("\n" + "="*70)
        print("FAILURE 1: Go Struct Initialization")
        print("="*70)

        code = '''
package main

type User struct {
    Name string
    Age  int
}

func GetUser(id int) (User, error) {
    user := User{Name: "Alice", Age: 30}
    return user, nil
}
'''
        parser = GoParserV2()
        ir = parser.parse_source(code, "main")
        generated = generate_go(ir)

        print("Expected: User{Name: \"Alice\", Age: 30}")
        if 'User("Alice", 30)' in generated:
            print("❌ FOUND: User(\"Alice\", 30)  [INCORRECT - tuple-style]")
            self.failures.append({
                "issue": "Go struct literals parsed as function calls",
                "category": "syntax_errors",
                "severity": "high",
                "location": "go_parser_v2.py - struct literal parsing",
                "expected": "User{Name: \"Alice\", Age: 30}",
                "actual": "User(\"Alice\", 30)",
            })
            return False
        else:
            print("✅ PASSED: Correct struct initialization")
            return True

    def analyze_go_multiple_returns(self):
        """Issue: return user, nil, nil - extra return value"""
        print("\n" + "="*70)
        print("FAILURE 2: Go Multiple Return Values")
        print("="*70)

        code = '''
package main

func GetUser(id int) (User, error) {
    user := User{Name: "Alice"}
    return user, nil
}
'''
        parser = GoParserV2()
        ir = parser.parse_source(code, "main")
        generated = generate_go(ir)

        print("Expected: return user, nil")
        if 'return user, nil, nil' in generated or generated.count(', nil') > 1:
            print("❌ FOUND: Extra return values")
            print(f"Generated:\n{generated[generated.find('return'):generated.find('return')+50]}")
            self.failures.append({
                "issue": "Go generator adds extra nil return",
                "category": "semantic_errors",
                "severity": "high",
                "location": "go_generator_v2.py - return statement generation",
                "expected": "2 return values",
                "actual": "3 return values",
            })
            return False
        else:
            print("✅ PASSED: Correct number of return values")
            return True

    def analyze_string_concatenation(self):
        """Issue: str() function called instead of template/interpolation"""
        print("\n" + "="*70)
        print("FAILURE 3: String Concatenation/Interpolation")
        print("="*70)

        python_code = '''
def greet(name):
    message = f"Hello, {name}!"
    return message
'''

        parser = PythonParserV2()
        ir = parser.parse_source(python_code, "test")
        js_code = generate_nodejs(ir, typescript=False)

        print("Expected: `Hello, ${name}!` or 'Hello, ' + name + '!'")
        if 'str(name)' in js_code:
            print(f"❌ FOUND: str() function call in JavaScript")
            print(f"Generated: {js_code[js_code.find('Hello'):js_code.find('Hello')+60] if 'Hello' in js_code else js_code[:100]}")
            self.failures.append({
                "issue": "F-strings not parsed, str() called in generated code",
                "category": "missing_features",
                "severity": "high",
                "location": "python_parser_v2.py - f-string parsing, nodejs_generator_v2.py - string interpolation",
                "expected": "Template literal or string concatenation",
                "actual": "str() function calls",
            })
            return False
        else:
            print("✅ PASSED: Proper string handling")
            return True

    def analyze_type_specificity(self):
        """Issue: Too many 'any' types instead of specific types"""
        print("\n" + "="*70)
        print("FAILURE 4: Type Specificity")
        print("="*70)

        python_code = '''
def calculate(a, b):
    return a + b

def get_name():
    return "Alice"

def get_age():
    return 30
'''

        parser = PythonParserV2()
        ir = parser.parse_source(python_code, "test")

        any_count = 0
        specific_count = 0

        for func in ir.functions:
            if func.return_type:
                if func.return_type.name == "any":
                    any_count += 1
                else:
                    specific_count += 1

        total = any_count + specific_count
        specificity = (specific_count / total * 100) if total > 0 else 0

        print(f"Type Specificity: {specificity:.1f}%")
        print(f"  Specific types: {specific_count}/{total}")
        print(f"  'any' types: {any_count}/{total}")

        if specificity < 50:
            print("❌ FAILED: Less than 50% type specificity")
            self.failures.append({
                "issue": "Low type specificity - too many 'any' fallbacks",
                "category": "type_inference",
                "severity": "medium",
                "location": "python_parser_v2.py - type inference",
                "expected": ">50% specific types",
                "actual": f"{specificity:.1f}% specific types",
            })
            return False
        else:
            print("✅ PASSED: Good type specificity")
            return True

    def analyze_library_usage_in_code(self):
        """Issue: Library names not translated in function calls"""
        print("\n" + "="*70)
        print("FAILURE 5: Library Function Calls")
        print("="*70)

        python_code = '''
import requests

def fetch_user(user_id):
    response = requests.get("https://api.example.com")
    return response.json()
'''

        parser = PythonParserV2()
        ir = parser.parse_source(python_code, "test")
        js_code = generate_nodejs(ir, typescript=False, source_language="python")

        print("Expected: axios.get() in JavaScript")
        if 'requests.get' in js_code or 'requests.Get' in js_code:
            print("❌ FOUND: requests.get() not translated to axios.get()")
            print(f"Generated: {js_code[js_code.find('function'):js_code.find('function')+200] if 'function' in js_code else js_code[:200]}")
            self.failures.append({
                "issue": "Library function calls not translated (requests.get stays as-is)",
                "category": "library_mapping",
                "severity": "high",
                "location": "generators - need to translate library.method() calls",
                "expected": "axios.get()",
                "actual": "requests.get()",
            })
            return False
        else:
            print("✅ PASSED: Library calls translated")
            return True

    def analyze_await_preservation(self):
        """Issue: await keyword not preserved in async functions"""
        print("\n" + "="*70)
        print("FAILURE 6: Await Keyword Preservation")
        print("="*70)

        js_code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''

        parser = NodeJSParserV2()
        ir = parser.parse_source(js_code, "test")
        python_code = generate_python(ir)

        print("Expected: 'await' keyword in Python")
        await_count = python_code.count('await ')

        if await_count < 2:
            print(f"❌ FOUND: Only {await_count} await keywords (expected 2)")
            print(f"Generated:\n{python_code[:300]}")
            self.failures.append({
                "issue": "Await keywords not preserved in async functions",
                "category": "missing_features",
                "severity": "medium",
                "location": "nodejs_parser_v2.py - await parsing, python_generator_v2.py - await generation",
                "expected": "2 await keywords",
                "actual": f"{await_count} await keywords",
            })
            return False
        else:
            print(f"✅ PASSED: {await_count} await keywords found")
            return True


def main():
    print("\n" + "="*70)
    print("ASSERTLANG V2 - EXACT FAILURE PATTERN IDENTIFICATION")
    print("="*70)
    print("\nAnalyzing test results to identify specific issues...\n")

    analyzer = FailureAnalyzer()

    tests = [
        ("Go Struct Initialization", analyzer.analyze_go_struct_initialization),
        ("Go Multiple Returns", analyzer.analyze_go_multiple_returns),
        ("String Concatenation", analyzer.analyze_string_concatenation),
        ("Type Specificity", analyzer.analyze_type_specificity),
        ("Library Function Calls", analyzer.analyze_library_usage_in_code),
        ("Await Preservation", analyzer.analyze_await_preservation),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "="*70)
    print("FAILURE ANALYSIS SUMMARY")
    print("="*70)

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for name, p in results:
        status = "✅ PASS" if p else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} patterns working ({100*passed//total}%)")
    print(f"Failures identified: {len(analyzer.failures)}")

    if analyzer.failures:
        print("\n" + "="*70)
        print("DETAILED FAILURE REPORT")
        print("="*70)

        # Group by category
        by_category = {}
        for failure in analyzer.failures:
            cat = failure['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(failure)

        for category, failures in by_category.items():
            print(f"\n📂 Category: {category.upper()}")
            print("-" * 70)
            for i, failure in enumerate(failures, 1):
                print(f"\n{i}. {failure['issue']}")
                print(f"   Severity: {failure['severity']}")
                print(f"   Location: {failure['location']}")
                print(f"   Expected: {failure['expected']}")
                print(f"   Actual: {failure['actual']}")

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)

    if analyzer.failures:
        print("\n1. Research best practices for each failure category")
        print("2. Implement targeted fixes based on research")
        print("3. Re-run tests to validate improvements")
        print("4. Measure accuracy delta")
    else:
        print("\n✅ No critical failures detected!")
        print("System is performing well. Consider:")
        print("  - Expanding test coverage")
        print("  - Testing on real-world GitHub repositories")
        print("  - Performance optimization")

    return 0 if not analyzer.failures else 1


if __name__ == "__main__":
    exit(main())
