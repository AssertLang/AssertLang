"""
Tests for Go Parser V2 - Arbitrary Go Code → IR

Tests cover:
- Functions and methods
- Structs and interfaces
- Goroutines (abstracted as async)
- Error handling patterns
- Control flow
- Type mapping
"""

import pytest
from language.go_parser_v2 import GoParserV2, parse_go_source
from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRTypeDefinition,
    IRProperty,
    IRType,
    IRReturn,
    IRAssignment,
    IRIf,
    IRFor,
    IRCall,
    IRIdentifier,
    IRLiteral,
    IRBinaryOp,
    BinaryOperator,
    LiteralType,
)


class TestGoParserV2Basic:
    """Test basic Go parsing functionality."""

    def test_package_extraction(self):
        """Test package name extraction."""
        source = "package main\n\nfunc main() {}"
        module = parse_go_source(source)
        assert module.name == "main"

    def test_package_non_main(self):
        """Test non-main package extraction."""
        source = "package utils\n\nfunc Helper() {}"
        module = parse_go_source(source)
        assert module.name == "utils"

    def test_import_single(self):
        """Test single import extraction."""
        source = '''package main
import "fmt"
'''
        module = parse_go_source(source)
        assert len(module.imports) == 1
        assert module.imports[0].module == "fmt"
        assert module.imports[0].alias is None

    def test_import_multiple(self):
        """Test multiple imports extraction."""
        source = '''package main
import (
    "fmt"
    "strings"
    "net/http"
)
'''
        module = parse_go_source(source)
        assert len(module.imports) == 3
        assert module.imports[0].module == "fmt"
        assert module.imports[1].module == "strings"
        assert module.imports[2].module == "net/http"

    def test_import_with_alias(self):
        """Test import with alias."""
        source = '''package main
import (
    f "fmt"
    json "encoding/json"
)
'''
        module = parse_go_source(source)
        assert len(module.imports) == 2
        assert module.imports[0].alias == "f"
        assert module.imports[0].module == "fmt"
        assert module.imports[1].alias == "json"


class TestGoParserV2Functions:
    """Test function parsing."""

    def test_simple_function(self):
        """Test simple function with no params or return."""
        source = '''package main

func main() {
}
'''
        module = parse_go_source(source)
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "main"
        assert len(func.params) == 0
        assert func.return_type is None

    def test_function_with_params(self):
        """Test function with parameters."""
        source = '''package main

func Add(a int, b int) {
}
'''
        module = parse_go_source(source)
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "Add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[0].param_type.name == "int"
        assert func.params[1].name == "b"
        assert func.params[1].param_type.name == "int"

    def test_function_with_return_type(self):
        """Test function with return type."""
        source = '''package main

func GetName() string {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.name == "GetName"
        assert func.return_type is not None
        assert func.return_type.name == "string"

    def test_function_with_multiple_returns(self):
        """Test function with multiple return values."""
        source = '''package main

func GetUser() (string, error) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.name == "GetUser"
        # Should return first non-error type
        assert func.return_type is not None
        assert func.return_type.name == "string"

    def test_function_with_error_only(self):
        """Test function that returns only error."""
        source = '''package main

func Validate() error {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.return_type is not None
        assert func.return_type.name == "string"  # error maps to string

    def test_function_with_pointer_params(self):
        """Test function with pointer parameters."""
        source = '''package main

func Process(user *User) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert len(func.params) == 1
        assert func.params[0].name == "user"
        assert func.params[0].param_type.name == "User"
        assert func.params[0].param_type.is_optional is True  # *Type → Type?

    def test_function_with_slice_params(self):
        """Test function with slice parameters."""
        source = '''package main

func ProcessItems(items []string) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        param = func.params[0]
        assert param.param_type.name == "array"
        assert len(param.param_type.generic_args) == 1
        assert param.param_type.generic_args[0].name == "string"

    def test_function_with_map_params(self):
        """Test function with map parameters."""
        source = '''package main

func ProcessMap(data map[string]int) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        param = func.params[0]
        assert param.param_type.name == "map"
        assert len(param.param_type.generic_args) == 2
        assert param.param_type.generic_args[0].name == "string"
        assert param.param_type.generic_args[1].name == "int"

    def test_function_with_variadic_params(self):
        """Test function with variadic parameters."""
        source = '''package main

func Printf(format string, args ...interface{}) {
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert len(func.params) == 2
        assert func.params[1].is_variadic is True


class TestGoParserV2Structs:
    """Test struct type parsing."""

    def test_simple_struct(self):
        """Test simple struct definition."""
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
        assert type_def.fields[0].name == "ID"
        assert type_def.fields[0].prop_type.name == "string"
        assert type_def.fields[1].name == "Name"

    def test_struct_with_tags(self):
        """Test struct with JSON tags."""
        source = '''package main

type User struct {
    ID string `json:"id"`
    Name string `json:"name"`
    Age int `json:"age"`
}
'''
        module = parse_go_source(source)
        type_def = module.types[0]
        assert len(type_def.fields) == 3
        # Tags are ignored in IR, but fields are extracted
        assert type_def.fields[0].name == "ID"
        assert type_def.fields[2].prop_type.name == "int"

    def test_struct_with_complex_types(self):
        """Test struct with complex field types."""
        source = '''package main

type Order struct {
    Items []string
    Metadata map[string]interface{}
    User *User
}
'''
        module = parse_go_source(source)
        type_def = module.types[0]
        assert len(type_def.fields) == 3

        # Array field
        items_field = type_def.fields[0]
        assert items_field.prop_type.name == "array"
        assert items_field.prop_type.generic_args[0].name == "string"

        # Map field
        meta_field = type_def.fields[1]
        assert meta_field.prop_type.name == "map"
        assert meta_field.prop_type.generic_args[0].name == "string"

        # Pointer field (optional)
        user_field = type_def.fields[2]
        assert user_field.prop_type.name == "User"
        assert user_field.prop_type.is_optional is True


class TestGoParserV2Statements:
    """Test statement parsing in function bodies."""

    def test_return_statement_simple(self):
        """Test simple return statement."""
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
        assert isinstance(stmt.value, IRLiteral)
        assert stmt.value.value == 42

    def test_return_statement_string(self):
        """Test return with string literal."""
        source = '''package main

func GetName() string {
    return "John"
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        stmt = func.body[0]
        assert isinstance(stmt, IRReturn)
        assert stmt.value.value == "John"

    def test_assignment_var(self):
        """Test variable declaration with var."""
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
        assert stmt.is_declaration is True
        assert stmt.var_type.name == "int"

    def test_assignment_short_declaration(self):
        """Test short variable declaration."""
        source = '''package main

func Test() {
    x := 42
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        stmt = func.body[0]
        assert isinstance(stmt, IRAssignment)
        assert stmt.target == "x"
        assert stmt.is_declaration is True

    def test_assignment_simple(self):
        """Test simple assignment."""
        source = '''package main

func Test() {
    x = 100
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        stmt = func.body[0]
        assert isinstance(stmt, IRAssignment)
        assert stmt.target == "x"
        assert stmt.is_declaration is False


class TestGoParserV2Expressions:
    """Test expression parsing."""

    def test_literal_expressions(self):
        """Test various literal expressions."""
        parser = GoParserV2()

        # String
        expr = parser._parse_expression('"hello"')
        assert isinstance(expr, IRLiteral)
        assert expr.value == "hello"
        assert expr.literal_type == LiteralType.STRING

        # Integer
        expr = parser._parse_expression('42')
        assert isinstance(expr, IRLiteral)
        assert expr.value == 42
        assert expr.literal_type == LiteralType.INTEGER

        # Float
        expr = parser._parse_expression('3.14')
        assert isinstance(expr, IRLiteral)
        assert expr.value == 3.14
        assert expr.literal_type == LiteralType.FLOAT

        # Boolean
        expr = parser._parse_expression('true')
        assert isinstance(expr, IRLiteral)
        assert expr.value is True
        assert expr.literal_type == LiteralType.BOOLEAN

        # Nil
        expr = parser._parse_expression('nil')
        assert isinstance(expr, IRLiteral)
        assert expr.value is None
        assert expr.literal_type == LiteralType.NULL

    def test_binary_operations(self):
        """Test binary operation parsing."""
        parser = GoParserV2()

        # Addition
        expr = parser._parse_expression('a + b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.ADD

        # Comparison
        expr = parser._parse_expression('x == y')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.EQUAL

        # Logical
        expr = parser._parse_expression('a && b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.AND

    def test_function_call(self):
        """Test function call parsing."""
        parser = GoParserV2()

        expr = parser._parse_expression('doSomething()')
        assert isinstance(expr, IRCall)
        assert isinstance(expr.function, IRIdentifier)
        assert expr.function.name == "doSomething"
        assert len(expr.args) == 0

    def test_function_call_with_args(self):
        """Test function call with arguments."""
        parser = GoParserV2()

        expr = parser._parse_expression('add(1, 2)')
        assert isinstance(expr, IRCall)
        assert len(expr.args) == 2
        assert isinstance(expr.args[0], IRLiteral)
        assert expr.args[0].value == 1

    def test_property_access(self):
        """Test property access parsing."""
        parser = GoParserV2()

        expr = parser._parse_expression('user.name')
        assert isinstance(expr, IRPropertyAccess)
        assert isinstance(expr.object, IRIdentifier)
        assert expr.object.name == "user"
        assert expr.property == "name"

    def test_nested_property_access(self):
        """Test nested property access."""
        parser = GoParserV2()

        expr = parser._parse_expression('order.user.name')
        assert isinstance(expr, IRPropertyAccess)
        assert expr.property == "name"
        assert isinstance(expr.object, IRPropertyAccess)
        assert expr.object.property == "user"

    def test_method_call(self):
        """Test method call (property access + call)."""
        parser = GoParserV2()

        expr = parser._parse_expression('user.GetName()')
        assert isinstance(expr, IRCall)
        assert isinstance(expr.function, IRPropertyAccess)


class TestGoParserV2TypeMapping:
    """Test Go type to IR type mapping."""

    def test_primitive_types(self):
        """Test primitive type mapping."""
        parser = GoParserV2()

        assert parser._go_type_to_ir("string").name == "string"
        assert parser._go_type_to_ir("int").name == "int"
        assert parser._go_type_to_ir("int64").name == "int"
        assert parser._go_type_to_ir("float64").name == "float"
        assert parser._go_type_to_ir("bool").name == "bool"

    def test_pointer_types(self):
        """Test pointer type mapping to optional."""
        parser = GoParserV2()

        ir_type = parser._go_type_to_ir("*string")
        assert ir_type.name == "string"
        assert ir_type.is_optional is True

    def test_slice_types(self):
        """Test slice type mapping to array."""
        parser = GoParserV2()

        ir_type = parser._go_type_to_ir("[]string")
        assert ir_type.name == "array"
        assert len(ir_type.generic_args) == 1
        assert ir_type.generic_args[0].name == "string"

    def test_map_types(self):
        """Test map type mapping."""
        parser = GoParserV2()

        ir_type = parser._go_type_to_ir("map[string]int")
        assert ir_type.name == "map"
        assert len(ir_type.generic_args) == 2
        assert ir_type.generic_args[0].name == "string"
        assert ir_type.generic_args[1].name == "int"

    def test_interface_types(self):
        """Test interface{} mapping to any."""
        parser = GoParserV2()

        assert parser._go_type_to_ir("interface{}").name == "any"
        assert parser._go_type_to_ir("any").name == "any"

    def test_error_type(self):
        """Test error type mapping to string."""
        parser = GoParserV2()

        assert parser._go_type_to_ir("error").name == "string"

    def test_custom_types(self):
        """Test custom type preservation."""
        parser = GoParserV2()

        assert parser._go_type_to_ir("User").name == "User"
        assert parser._go_type_to_ir("Payment").name == "Payment"


class TestGoParserV2AsyncDetection:
    """Test goroutine detection (async)."""

    def test_goroutine_detected(self):
        """Test that goroutines are detected as async."""
        source = '''package main

func Process() {
    go doWork()
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.is_async is True

    def test_no_goroutine_not_async(self):
        """Test function without goroutines is not async."""
        source = '''package main

func Process() {
    doWork()
}
'''
        module = parse_go_source(source)
        func = module.functions[0]
        assert func.is_async is False


class TestGoParserV2Integration:
    """Integration tests with complete Go programs."""

    def test_complete_http_handler(self):
        """Test parsing a complete HTTP handler."""
        source = '''package main

import (
    "fmt"
    "net/http"
)

type User struct {
    ID string
    Name string
}

func HandleUser(w http.ResponseWriter, r *http.Request) {
    user := User{ID: "123", Name: "John"}
    fmt.Fprintf(w, "User: %s", user.Name)
}
'''
        module = parse_go_source(source)

        # Check module structure
        assert module.name == "main"
        assert len(module.imports) == 2
        assert len(module.types) == 1
        assert len(module.functions) == 1

        # Check type
        user_type = module.types[0]
        assert user_type.name == "User"
        assert len(user_type.fields) == 2

        # Check function
        func = module.functions[0]
        assert func.name == "HandleUser"
        assert len(func.params) == 2

    def test_complete_business_logic(self):
        """Test parsing business logic function."""
        source = '''package main

type Order struct {
    ID string
    Total float64
}

func ProcessOrder(order *Order) error {
    if order.Total > 1000 {
        return fmt.Errorf("amount too high")
    }
    return nil
}
'''
        module = parse_go_source(source)

        assert len(module.types) == 1
        assert len(module.functions) == 1

        func = module.functions[0]
        assert func.name == "ProcessOrder"
        assert len(func.params) == 1
        assert func.params[0].param_type.name == "Order"
        assert func.params[0].param_type.is_optional is True
        assert func.return_type.name == "string"  # error → string


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
