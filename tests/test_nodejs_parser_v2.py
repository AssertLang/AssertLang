"""
Tests for Node.js Parser V2: JavaScript/TypeScript → IR

Tests cover:
- JavaScript function parsing
- TypeScript function parsing with type annotations
- Arrow functions (regular and async)
- Class parsing (properties, methods, constructor)
- Async/await patterns
- Type inference for JavaScript
- Type extraction for TypeScript
- Module imports/exports
"""

import pytest
from dsl.ir import (
    BinaryOperator,
    IRArray,
    IRAssignment,
    IRBinaryOp,
    IRCall,
    IRClass,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRImport,
    IRLiteral,
    IRMap,
    IRModule,
    IRParameter,
    IRProperty,
    IRPropertyAccess,
    IRReturn,
    IRType,
    IRWhile,
    LiteralType,
)
from language.nodejs_parser_v2 import NodeJSParserV2


class TestBasicFunctions:
    """Test parsing of basic function declarations."""

    def test_parse_simple_function(self):
        """Test parsing simple JavaScript function."""
        source = """
        function add(a, b) {
            return a + b;
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[1].name == "b"
        assert len(func.body) == 1
        assert isinstance(func.body[0], IRReturn)

    def test_parse_typescript_function(self):
        """Test parsing TypeScript function with type annotations."""
        source = """
        function add(a: number, b: number): number {
            return a + b;
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.params[0].param_type.name == "int"  # number → int
        assert func.params[1].param_type.name == "int"
        assert func.return_type.name == "int"

    def test_parse_async_function(self):
        """Test parsing async function."""
        source = """
        async function fetchData(url) {
            const response = await fetch(url);
            return response;
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "fetchData"
        assert func.is_async is True
        assert len(func.params) == 1
        assert func.params[0].name == "url"


class TestArrowFunctions:
    """Test parsing of arrow functions."""

    def test_parse_arrow_function_expression(self):
        """Test parsing arrow function with single expression."""
        source = """
        const add = (a, b) => a + b;
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert len(func.body) == 1
        assert isinstance(func.body[0], IRReturn)

    def test_parse_arrow_function_block(self):
        """Test parsing arrow function with block body."""
        source = """
        const multiply = (a, b) => {
            const result = a * b;
            return result;
        };
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "multiply"
        assert len(func.body) == 2
        assert isinstance(func.body[0], IRAssignment)
        assert isinstance(func.body[1], IRReturn)

    def test_parse_typescript_arrow_function(self):
        """Test parsing TypeScript arrow function with types."""
        source = """
        const add = (a: number, b: number): number => a + b;
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.params[0].param_type.name == "int"
        assert func.return_type.name == "int"

    def test_parse_async_arrow_function(self):
        """Test parsing async arrow function."""
        source = """
        const fetchData = async (url) => {
            const response = await fetch(url);
            return response.json();
        };
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "fetchData"
        assert func.is_async is True


class TestClasses:
    """Test parsing of class definitions."""

    def test_parse_simple_class(self):
        """Test parsing simple JavaScript class."""
        source = """
        class User {
            constructor(name, email) {
                this.name = name;
                this.email = email;
            }

            greet() {
                return "Hello";
            }
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "User"
        assert cls.constructor is not None
        assert len(cls.constructor.params) == 2
        assert len(cls.methods) == 1
        assert cls.methods[0].name == "greet"

    def test_parse_typescript_class(self):
        """Test parsing TypeScript class with property declarations."""
        source = """
        class User {
            name: string;
            email: string;
            age: number;

            constructor(name: string, email: string) {
                this.name = name;
                this.email = email;
            }

            greet(): string {
                return `Hello, ${this.name}`;
            }
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "User"

        # Check properties
        assert len(cls.properties) == 3
        prop_names = [p.name for p in cls.properties]
        assert "name" in prop_names
        assert "email" in prop_names
        assert "age" in prop_names

        # Check types
        name_prop = next(p for p in cls.properties if p.name == "name")
        assert name_prop.prop_type.name == "string"

        age_prop = next(p for p in cls.properties if p.name == "age")
        assert age_prop.prop_type.name == "int"

        # Check constructor
        assert cls.constructor is not None
        assert len(cls.constructor.params) == 2
        assert cls.constructor.params[0].param_type.name == "string"

        # Check methods
        assert len(cls.methods) == 1
        assert cls.methods[0].return_type.name == "string"

    def test_parse_class_with_async_method(self):
        """Test parsing class with async method."""
        source = """
        class DataService {
            async fetchUser(id) {
                const user = await api.get(id);
                return user;
            }
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.classes) == 1
        cls = module.classes[0]
        assert len(cls.methods) == 1
        assert cls.methods[0].is_async is True


class TestExpressions:
    """Test parsing of various expressions."""

    def test_parse_literals(self):
        """Test parsing literal values."""
        parser = NodeJSParserV2()

        # String literals
        expr = parser._parse_expression('"hello"')
        assert isinstance(expr, IRLiteral)
        assert expr.value == "hello"
        assert expr.literal_type == LiteralType.STRING

        # Number literals
        expr = parser._parse_expression('42')
        assert isinstance(expr, IRLiteral)
        assert expr.value == 42
        assert expr.literal_type == LiteralType.INTEGER

        expr = parser._parse_expression('3.14')
        assert isinstance(expr, IRLiteral)
        assert expr.value == 3.14
        assert expr.literal_type == LiteralType.FLOAT

        # Boolean literals
        expr = parser._parse_expression('true')
        assert isinstance(expr, IRLiteral)
        assert expr.value is True

        expr = parser._parse_expression('false')
        assert isinstance(expr, IRLiteral)
        assert expr.value is False

        # Null
        expr = parser._parse_expression('null')
        assert isinstance(expr, IRLiteral)
        assert expr.value is None

    def test_parse_array_literal(self):
        """Test parsing array literals."""
        parser = NodeJSParserV2()

        expr = parser._parse_expression('[1, 2, 3]')
        assert isinstance(expr, IRArray)
        assert len(expr.elements) == 3
        assert all(isinstance(e, IRLiteral) for e in expr.elements)

    def test_parse_object_literal(self):
        """Test parsing object literals."""
        parser = NodeJSParserV2()

        expr = parser._parse_expression('{name: "John", age: 30}')
        assert isinstance(expr, IRMap)
        assert len(expr.entries) == 2
        assert "name" in expr.entries
        assert "age" in expr.entries

    def test_parse_function_call(self):
        """Test parsing function calls."""
        parser = NodeJSParserV2()

        expr = parser._parse_expression('add(1, 2)')
        assert isinstance(expr, IRCall)
        assert isinstance(expr.function, IRIdentifier)
        assert expr.function.name == "add"
        assert len(expr.args) == 2

    def test_parse_property_access(self):
        """Test parsing property access."""
        parser = NodeJSParserV2()

        expr = parser._parse_expression('user.name')
        assert isinstance(expr, IRPropertyAccess)
        assert isinstance(expr.object, IRIdentifier)
        assert expr.property == "name"

        # Chained property access
        expr = parser._parse_expression('user.address.city')
        assert isinstance(expr, IRPropertyAccess)
        assert expr.property == "city"
        assert isinstance(expr.object, IRPropertyAccess)

    def test_parse_binary_operations(self):
        """Test parsing binary operations."""
        parser = NodeJSParserV2()

        # Arithmetic
        expr = parser._parse_expression('a + b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.ADD

        expr = parser._parse_expression('x * y')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.MULTIPLY

        # Comparison
        expr = parser._parse_expression('a === b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.EQUAL

        expr = parser._parse_expression('x < y')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.LESS_THAN

        # Logical
        expr = parser._parse_expression('a && b')
        assert isinstance(expr, IRBinaryOp)
        assert expr.op == BinaryOperator.AND


class TestStatements:
    """Test parsing of various statements."""

    def test_parse_variable_assignment(self):
        """Test parsing variable assignments."""
        parser = NodeJSParserV2()

        stmt = parser._parse_assignment('const x = 42;')
        assert isinstance(stmt, IRAssignment)
        assert stmt.target == "x"
        assert isinstance(stmt.value, IRLiteral)
        assert stmt.is_declaration is True

    def test_parse_if_statement(self):
        """Test parsing if statements."""
        source = """
        if (x > 0) {
            return x;
        } else {
            return 0;
        }
        """

        parser = NodeJSParserV2()
        stmt, _ = parser._parse_if_statement(source.strip())

        assert isinstance(stmt, IRIf)
        assert isinstance(stmt.condition, IRBinaryOp)
        assert len(stmt.then_body) == 1
        assert len(stmt.else_body) == 1

    def test_parse_while_loop(self):
        """Test parsing while loops."""
        source = """
        while (count > 0) {
            count = count - 1;
        }
        """

        parser = NodeJSParserV2()
        stmt, _ = parser._parse_while_statement(source.strip())

        assert isinstance(stmt, IRWhile)
        assert isinstance(stmt.condition, IRBinaryOp)
        assert len(stmt.body) >= 1

    def test_parse_return_statement(self):
        """Test parsing return statements."""
        parser = NodeJSParserV2()

        # Return with value
        stmt = parser._parse_return('return 42;')
        assert isinstance(stmt, IRReturn)
        assert isinstance(stmt.value, IRLiteral)

        # Return without value
        stmt = parser._parse_return('return;')
        assert isinstance(stmt, IRReturn)
        assert stmt.value is None


class TestImports:
    """Test parsing of import/export statements."""

    def test_parse_es6_imports(self):
        """Test parsing ES6 import statements."""
        source = """
        import { add, subtract } from 'math';
        import Calculator from 'calculator';
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.imports) == 2

        # Named imports
        assert module.imports[0].module == "math"
        assert "add" in module.imports[0].items
        assert "subtract" in module.imports[0].items

        # Default import
        assert module.imports[1].module == "calculator"
        assert module.imports[1].alias == "Calculator"

    def test_parse_commonjs_require(self):
        """Test parsing CommonJS require statements."""
        source = """
        const express = require('express');
        const http = require('http');
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        assert len(module.imports) == 2
        assert module.imports[0].module == "express"
        assert module.imports[0].alias == "express"


class TestTypeSystem:
    """Test TypeScript type parsing and inference."""

    def test_parse_primitive_types(self):
        """Test parsing primitive TypeScript types."""
        parser = NodeJSParserV2()

        type_str = "string"
        ir_type = parser._parse_type(type_str)
        assert ir_type.name == "string"

        type_str = "number"
        ir_type = parser._parse_type(type_str)
        assert ir_type.name == "int"

        type_str = "boolean"
        ir_type = parser._parse_type(type_str)
        assert ir_type.name == "bool"

    def test_parse_array_types(self):
        """Test parsing array types."""
        parser = NodeJSParserV2()

        # Array<T> syntax
        type_str = "Array<string>"
        ir_type = parser._parse_type(type_str)
        assert ir_type.name == "array"
        assert len(ir_type.generic_args) == 1
        assert ir_type.generic_args[0].name == "string"

        # T[] syntax
        type_str = "number[]"
        ir_type = parser._parse_type(type_str)
        assert ir_type.name == "array"
        assert ir_type.generic_args[0].name == "int"

    def test_parse_promise_types(self):
        """Test parsing Promise types."""
        parser = NodeJSParserV2()

        type_str = "Promise<string>"
        ir_type = parser._parse_type(type_str)
        # Promise<T> unwraps to T
        assert ir_type.name == "string"

    def test_infer_type_from_default_value(self):
        """Test type inference from default parameter values."""
        source = """
        function greet(name = "World") {
            return "Hello";
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "test")

        func = module.functions[0]
        param = func.params[0]
        assert param.name == "name"
        # Type inferred from default value
        assert param.param_type.name == "string"


class TestComplexScenarios:
    """Test parsing of complex, real-world scenarios."""

    def test_parse_complete_module(self):
        """Test parsing a complete JavaScript module."""
        source = """
        import { fetch } from 'node-fetch';

        class UserService {
            constructor(apiUrl) {
                this.apiUrl = apiUrl;
            }

            async getUser(id) {
                const response = await fetch(this.apiUrl + '/users/' + id);
                return response.json();
            }

            async createUser(userData) {
                const response = await fetch(this.apiUrl + '/users', {
                    method: 'POST',
                    body: JSON.stringify(userData)
                });
                return response.json();
            }
        }

        const formatUser = (user) => {
            return `${user.name} (${user.email})`;
        };

        module.exports = { UserService, formatUser };
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "user_service")

        # Check imports
        assert len(module.imports) >= 1

        # Check class
        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "UserService"
        assert cls.constructor is not None
        assert len(cls.methods) == 2
        assert all(m.is_async for m in cls.methods)

        # Check standalone function
        assert len(module.functions) >= 1
        func_names = [f.name for f in module.functions]
        assert "formatUser" in func_names

    def test_parse_typescript_module(self):
        """Test parsing a complete TypeScript module."""
        source = """
        export interface User {
            id: string;
            name: string;
            email: string;
        }

        export class UserRepository {
            private users: Map<string, User>;

            constructor() {
                this.users = new Map();
            }

            addUser(user: User): void {
                this.users.set(user.id, user);
            }

            getUser(id: string): User | null {
                return this.users.get(id) || null;
            }

            getAllUsers(): User[] {
                return Array.from(this.users.values());
            }
        }
        """

        parser = NodeJSParserV2()
        module = parser.parse_source(source, "user_repository")

        # Check class
        assert len(module.classes) >= 1
        cls = next(c for c in module.classes if c.name == "UserRepository")

        # Check properties
        assert len(cls.properties) >= 1

        # Check methods
        assert len(cls.methods) >= 3
        method_names = [m.name for m in cls.methods]
        assert "addUser" in method_names
        assert "getUser" in method_names
        assert "getAllUsers" in method_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
