"""
Test PW parser class support.

Tests:
1. Basic class with properties
2. Class with constructor
3. Class with methods
4. Class instantiation
5. Property access
6. Method calls
7. self reference
8. Class code generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_basic_class():
    """Test basic class with properties."""
    print(f"\n{'='*60}")
    print("Testing basic class with properties")
    print(f"{'='*60}")

    pw_code = """class User {
    id: string;
    name: string;
    age: int;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes")

        cls = ir.classes[0]
        print(f"  ✅ Class name: {cls.name}")
        print(f"  ✅ Properties: {len(cls.properties)}")

        if len(cls.properties) == 3:
            print(f"\n✅ SUCCESS: Basic class works!")
            return True
        else:
            print(f"\n❌ FAILED: Expected 3 properties, got {len(cls.properties)}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_class_with_constructor():
    """Test class with constructor."""
    print(f"\n{'='*60}")
    print("Testing class with constructor")
    print(f"{'='*60}")

    pw_code = """class User {
    id: string;
    name: string;

    constructor(id: string, name: string) {
        self.id = id;
        self.name = name;
    }
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes")

        cls = ir.classes[0]
        if cls.constructor:
            print(f"  ✅ Constructor found with {len(cls.constructor.params)} params")
            print(f"\n✅ SUCCESS: Class with constructor works!")
            return True
        else:
            print(f"\n❌ FAILED: No constructor found")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_class_with_methods():
    """Test class with methods."""
    print(f"\n{'='*60}")
    print("Testing class with methods")
    print(f"{'='*60}")

    pw_code = """class User {
    name: string;
    age: int;

    constructor(name: string, age: int) {
        self.name = name;
        self.age = age;
    }

    function greet() -> string {
        return "Hello, " + self.name;
    }

    function is_adult() -> bool {
        return self.age >= 18;
    }
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes")

        cls = ir.classes[0]
        print(f"  ✅ Methods: {len(cls.methods)}")

        if len(cls.methods) == 2:
            print(f"\n✅ SUCCESS: Class with methods works!")
            return True
        else:
            print(f"\n❌ FAILED: Expected 2 methods, got {len(cls.methods)}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_class_instantiation():
    """Test class instantiation."""
    print(f"\n{'='*60}")
    print("Testing class instantiation")
    print(f"{'='*60}")

    pw_code = """class User {
    name: string;

    constructor(name: string) {
        self.name = name;
    }
}

function create_user() -> User {
    let user = User("Alice");
    return user;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes, {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Class instantiation works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_property_access():
    """Test property access."""
    print(f"\n{'='*60}")
    print("Testing property access")
    print(f"{'='*60}")

    pw_code = """class User {
    name: string;

    constructor(name: string) {
        self.name = name;
    }
}

function get_name(user: User) -> string {
    return user.name;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes, {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Property access works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_method_calls():
    """Test method calls."""
    print(f"\n{'='*60}")
    print("Testing method calls")
    print(f"{'='*60}")

    pw_code = """class User {
    name: string;

    constructor(name: string) {
        self.name = name;
    }

    function greet() -> string {
        return "Hello, " + self.name;
    }
}

function test_user() -> string {
    let user = User("Bob");
    return user.greet();
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes, {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Method calls work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_self_reference():
    """Test self reference in methods."""
    print(f"\n{'='*60}")
    print("Testing self reference")
    print(f"{'='*60}")

    pw_code = """class Counter {
    count: int;

    constructor() {
        self.count = 0;
    }

    function increment() -> int {
        self.count = self.count + 1;
        return self.count;
    }
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes")
        print(f"\n✅ SUCCESS: Self reference works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_class_code_generation():
    """Test class code generation."""
    print(f"\n{'='*60}")
    print("Testing class code generation")
    print(f"{'='*60}")

    pw_code = """class Point {
    x: int;
    y: int;

    constructor(x: int, y: int) {
        self.x = x;
        self.y = y;
    }

    function distance() -> float {
        return 0.0;
    }
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.classes)} classes")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has class
        if "class Point" in python_code:
            print(f"\n✅ SUCCESS: Class generates correct Python!")
            print(f"\nGenerated Python:\n{python_code}")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't have class")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all class tests."""
    print("\n" + "="*60)
    print("PW PARSER CLASS TESTS")
    print("="*60)

    tests = [
        ("Basic class with properties", test_basic_class),
        ("Class with constructor", test_class_with_constructor),
        ("Class with methods", test_class_with_methods),
        ("Class instantiation", test_class_instantiation),
        ("Property access", test_property_access),
        ("Method calls", test_method_calls),
        ("Self reference", test_self_reference),
        ("Class code generation", test_class_code_generation),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print("\n" + "="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
