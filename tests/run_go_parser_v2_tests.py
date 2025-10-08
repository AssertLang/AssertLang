#!/usr/bin/env python3
"""
Test runner for Go Parser V2 (without pytest dependency)
"""

import sys
import traceback
from language.go_parser_v2 import GoParserV2, parse_go_source
from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRTypeDefinition,
    IRReturn,
    IRAssignment,
    IRCall,
    IRIdentifier,
    IRLiteral,
    IRBinaryOp,
    IRPropertyAccess,
    BinaryOperator,
    LiteralType,
)


class TestRunner:
    """Simple test runner."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, test_name, test_func):
        """Run a single test."""
        try:
            test_func()
            self.passed += 1
            print(f"✓ {test_name}")
        except AssertionError as e:
            self.failed += 1
            error_msg = f"✗ {test_name}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
        except Exception as e:
            self.failed += 1
            error_msg = f"✗ {test_name}: {type(e).__name__}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
            traceback.print_exc()

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print(f"Tests: {self.passed + self.failed} total, {self.passed} passed, {self.failed} failed")

        if self.errors:
            print("\nFailed tests:")
            for error in self.errors:
                print(f"  {error}")

        return 0 if self.failed == 0 else 1


def main():
    runner = TestRunner()

    # Basic tests
    def test_package_extraction():
        source = "package main\n\nfunc main() {}"
        module = parse_go_source(source)
        assert module.name == "main", f"Expected 'main', got '{module.name}'"

    def test_import_single():
        source = 'package main\nimport "fmt"\n'
        module = parse_go_source(source)
        assert len(module.imports) == 1, f"Expected 1 import, got {len(module.imports)}"
        assert module.imports[0].module == "fmt"

    def test_import_multiple():
        source = '''package main
import (
    "fmt"
    "strings"
)
'''
        module = parse_go_source(source)
        assert len(module.imports) == 2

    # Function tests
    def test_simple_function():
        source = '''package main

func main() {
}
'''
        module = parse_go_source(source)
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "main"

    def test_function_with_params():
        source = '''package main

func Add(a int, b int) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.name == "Add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[0].param_type.name == "int"

    def test_function_with_return():
        source = '''package main

func GetName() string {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.return_type is not None
        assert func.return_type.name == "string"

    # Struct tests
    def test_simple_struct():
        source = '''package main

type User struct {
    ID string
    Name string
}
'''
        module = parse_go_source(source)
        assert len(module.types) == 1
        type_def = module.types[0]
        assert type_def.name == "User"
        assert len(type_def.fields) == 2

    def test_struct_with_tags():
        source = '''package main

type User struct {
    ID string `json:"id"`
    Name string `json:"name"`
}
'''
        module = parse_go_source(source)
        type_def = module.types[0]
        assert len(type_def.fields) == 2

    # Type mapping tests
    def test_primitive_types():
        parser = GoParserV2()
        assert parser._go_type_to_ir("string").name == "string"
        assert parser._go_type_to_ir("int").name == "int"
        assert parser._go_type_to_ir("float64").name == "float"
        assert parser._go_type_to_ir("bool").name == "bool"

    def test_pointer_types():
        parser = GoParserV2()
        ir_type = parser._go_type_to_ir("*string")
        assert ir_type.name == "string"
        assert ir_type.is_optional is True

    def test_slice_types():
        parser = GoParserV2()
        ir_type = parser._go_type_to_ir("[]string")
        assert ir_type.name == "array"
        assert len(ir_type.generic_args) == 1
        assert ir_type.generic_args[0].name == "string"

    def test_map_types():
        parser = GoParserV2()
        ir_type = parser._go_type_to_ir("map[string]int")
        assert ir_type.name == "map"
        assert len(ir_type.generic_args) == 2

    # Statement tests
    def test_return_statement():
        source = '''package main

func GetValue() int {
    return 42
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert len(func.body) == 1
        stmt = func.body[0]
        assert isinstance(stmt, IRReturn)

    def test_assignment_var():
        source = '''package main

func Test() {
    var x int = 10
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert len(func.body) == 1
        stmt = func.body[0]
        assert isinstance(stmt, IRAssignment)
        assert stmt.target == "x"

    def test_assignment_short():
        source = '''package main

func Test() {
    x := 42
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        stmt = func.body[0]
        assert isinstance(stmt, IRAssignment)
        assert stmt.is_declaration is True

    # Expression tests
    def test_literal_string():
        parser = GoParserV2()
        expr = parser._parse_expression('"hello"')
        assert isinstance(expr, IRLiteral)
        assert expr.value == "hello"

    def test_literal_integer():
        parser = GoParserV2()
        expr = parser._parse_expression('42')
        assert isinstance(expr, IRLiteral)
        assert expr.value == 42

    def test_literal_boolean():
        parser = GoParserV2()
        expr = parser._parse_expression('true')
        assert isinstance(expr, IRLiteral)
        assert expr.value is True

    def test_binary_operation():
        parser = GoParserV2()
        expr = parser._parse_expression('a + b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.ADD

    def test_function_call():
        parser = GoParserV2()
        expr = parser._parse_expression('doSomething()')
        assert isinstance(expr, IRCall)
        assert isinstance(expr.function, IRIdentifier)

    def test_property_access():
        parser = GoParserV2()
        expr = parser._parse_expression('user.name')
        assert isinstance(expr, IRPropertyAccess)

    # Async detection
    def test_goroutine_detected():
        source = '''package main

func Process() {
    go doWork()
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.is_async is True

    # Integration test
    def test_complete_program():
        source = '''package main

import "fmt"

type User struct {
    ID string
    Name string
}

func GetUser(id string) *User {
    return nil
}
'''
        module = parse_go_source(source)
        assert module.name == "main"
        assert len(module.imports) == 1
        assert len(module.types) == 1
        assert len(module.functions) == 1

    # Run all tests
    print("Running Go Parser V2 Tests...\n")

    runner.run_test("Package extraction", test_package_extraction)
    runner.run_test("Single import", test_import_single)
    runner.run_test("Multiple imports", test_import_multiple)
    runner.run_test("Simple function", test_simple_function)
    runner.run_test("Function with params", test_function_with_params)
    runner.run_test("Function with return", test_function_with_return)
    runner.run_test("Simple struct", test_simple_struct)
    runner.run_test("Struct with tags", test_struct_with_tags)
    runner.run_test("Primitive types", test_primitive_types)
    runner.run_test("Pointer types", test_pointer_types)
    runner.run_test("Slice types", test_slice_types)
    runner.run_test("Map types", test_map_types)
    runner.run_test("Return statement", test_return_statement)
    runner.run_test("Var assignment", test_assignment_var)
    runner.run_test("Short assignment", test_assignment_short)
    runner.run_test("Literal string", test_literal_string)
    runner.run_test("Literal integer", test_literal_integer)
    runner.run_test("Literal boolean", test_literal_boolean)
    runner.run_test("Binary operation", test_binary_operation)
    runner.run_test("Function call", test_function_call)
    runner.run_test("Property access", test_property_access)
    runner.run_test("Goroutine detection", test_goroutine_detected)
    runner.run_test("Complete program", test_complete_program)

    return runner.print_summary()


if __name__ == "__main__":
    sys.exit(main())
