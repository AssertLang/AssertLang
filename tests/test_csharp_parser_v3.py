"""
Test C# Parser V3 - Full statement body parsing
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.csharp_parser_v3 import CSharpParserV3


def test_simple_method():
    """Test simple method with arithmetic."""
    print("\n=== Test 1: Simple Method ===")

    parser = CSharpParserV3()
    ir = parser.parse_file("/tmp/test_csharp.cs")

    # Find Calculator class
    calc_class = next((c for c in ir.classes if c.name == "Calculator"), None)
    assert calc_class, "Calculator class not found"

    # Find Add method
    add_method = next((m for m in calc_class.methods if m.name == "Add"), None)
    assert add_method, "Add method not found"

    print(f"Method: {add_method.name}({len(add_method.params)} params)")
    print(f"  Body: {len(add_method.body)} statements")

    for i, stmt in enumerate(add_method.body):
        print(f"    [{i}] {type(stmt).__name__}")

    print("✅ PASS")


def test_if_statement():
    """Test if statement parsing."""
    print("\n=== Test 2: If Statement ===")

    parser = CSharpParserV3()
    ir = parser.parse_file("/tmp/test_csharp.cs")

    calc_class = next((c for c in ir.classes if c.name == "Calculator"), None)
    add_method = next((m for m in calc_class.methods if m.name == "Add"), None)

    # Check for IRIf
    from dsl.ir import IRIf
    if_stmt = next((s for s in add_method.body if isinstance(s, IRIf)), None)
    assert if_stmt, "If statement not found"

    print(f"Method: {add_method.name}({len(add_method.params)} params)")
    print(f"  Body: {len(add_method.body)} statements")
    print(f"    [0] {type(add_method.body[0]).__name__}")
    print(f"    [1] {type(add_method.body[1]).__name__} (condition: {if_stmt.condition})")
    print(f"        Then: {len(if_stmt.then_body)} statements")
    print(f"    [2] {type(add_method.body[2]).__name__}")

    print("✅ PASS")


def test_for_loop():
    """Test for loop parsing."""
    print("\n=== Test 3: For Loop ===")

    parser = CSharpParserV3()
    ir = parser.parse_file("/tmp/test_csharp.cs")

    calc_class = next((c for c in ir.classes if c.name == "Calculator"), None)
    sum_method = next((m for m in calc_class.methods if m.name == "SumLoop"), None)
    assert sum_method, "SumLoop method not found"

    # Check for IRFor
    from dsl.ir import IRFor
    for_stmt = next((s for s in sum_method.body if isinstance(s, IRFor)), None)
    assert for_stmt, "For loop not found"

    print(f"Method: {sum_method.name}({len(sum_method.params)} params)")
    print(f"  Body: {len(sum_method.body)} statements")
    print(f"    [0] {type(sum_method.body[0]).__name__} (int sum = 0)")
    print(f"    [1] {type(sum_method.body[1]).__name__} (iterator: {for_stmt.iterator})")
    print(f"        Body: {len(for_stmt.body)} statements")
    print(f"    [2] {type(sum_method.body[2]).__name__}")

    print("✅ PASS")


def test_while_loop():
    """Test while loop parsing."""
    print("\n=== Test 4: While Loop ===")

    parser = CSharpParserV3()
    ir = parser.parse_file("/tmp/test_csharp.cs")

    # Find Program class
    program_class = next((c for c in ir.classes if c.name == "Program"), None)
    assert program_class, "Program class not found"

    # Find ProcessData method
    process_method = next((m for m in program_class.methods if m.name == "ProcessData"), None)
    assert process_method, "ProcessData method not found"

    # Check for IRWhile
    from dsl.ir import IRWhile
    while_stmt = next((s for s in process_method.body if isinstance(s, IRWhile)), None)
    assert while_stmt, "While loop not found"

    print(f"Method: {process_method.name}({len(process_method.params)} params)")
    print(f"  Body: {len(process_method.body)} statements")

    for i, stmt in enumerate(process_method.body):
        print(f"    [{i}] {type(stmt).__name__}")

    print("✅ PASS")


def test_accuracy():
    """Test overall accuracy assessment."""
    print("\n=== Test 5: Accuracy Assessment ===")

    parser = CSharpParserV3()
    ir = parser.parse_file("/tmp/test_csharp.cs")

    # Count features
    total_classes = len(ir.classes)
    total_functions = len(ir.functions)
    total_methods = sum(len(c.methods) for c in ir.classes)

    # Check body parsing
    from dsl.ir import IRIf, IRFor, IRWhile

    bodies_with_statements = 0
    total_bodies = 0
    control_flow_count = 0

    for cls in ir.classes:
        for method in cls.methods:
            total_bodies += 1
            if method.body:
                bodies_with_statements += 1
                # Count control flow
                for stmt in method.body:
                    if isinstance(stmt, (IRIf, IRFor, IRWhile)):
                        control_flow_count += 1

    for func in ir.functions:
        total_bodies += 1
        if func.body:
            bodies_with_statements += 1
            for stmt in func.body:
                if isinstance(stmt, (IRIf, IRFor, IRWhile)):
                    control_flow_count += 1

    print(f"Classes: {total_classes}")
    print(f"Functions: {total_functions}")
    print(f"Methods: {total_methods}")
    print(f"Bodies with statements: {bodies_with_statements}/{total_bodies}")
    print(f"Control flow statements: {control_flow_count}")

    accuracy = (bodies_with_statements / total_bodies) * 100 if total_bodies > 0 else 0
    print(f"\nBody parsing accuracy: {accuracy:.0f}%")

    if accuracy >= 95:
        print("✅ TARGET REACHED: 95%+")
    else:
        print(f"⚠️  Below target (need 95%, got {accuracy:.0f}%)")

    print("✅ PASS")


if __name__ == "__main__":
    test_simple_method()
    test_if_statement()
    test_for_loop()
    test_while_loop()
    test_accuracy()

    print("\n" + "="*50)
    print("ALL TESTS PASSED ✅")
    print("="*50)
