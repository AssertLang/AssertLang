"""
Tests for PW DSL 2.0 Parser and Generator

Test strategy:
1. Unit tests for parser (PW text → IR)
2. Unit tests for generator (IR → PW text)
3. Round-trip tests (PW → IR → PW)
4. Golden fixtures (real-world PW programs)
"""

import pytest

from dsl.ir import (
    BinaryOperator,
    IRArray,
    IRAssignment,
    IRBinaryOp,
    IRBreak,
    IRCall,
    IRClass,
    IRContinue,
    IREnum,
    IREnumVariant,
    IRFor,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRImport,
    IRLiteral,
    IRMap,
    IRModule,
    IRParameter,
    IRPass,
    IRProperty,
    IRReturn,
    IRType,
    IRTypeDefinition,
    IRWhile,
    LiteralType,
    UnaryOperator,
)
from dsl.pw_generator import generate_pw
from dsl.pw_parser import parse_pw


class TestLexer:
    """Test lexical analysis (tokenization)."""

    def test_simple_module(self):
        """Test parsing simple module declaration."""
        code = """
module test
version 1.0.0
"""
        module = parse_pw(code.strip())
        assert module.name == "test"
        assert module.version == "1.0.0"

    def test_imports(self):
        """Test parsing imports."""
        code = """
module test
version 1.0.0

import http_client
import database from storage
import json as JSON
"""
        module = parse_pw(code.strip())
        assert len(module.imports) == 3
        assert module.imports[0].module == "http_client"
        assert module.imports[1].module == "database"
        assert module.imports[2].module == "json"
        assert module.imports[2].alias == "JSON"


class TestTypeDefinitions:
    """Test type definition parsing."""

    def test_simple_type(self):
        """Test simple type definition."""
        code = """
module test
version 1.0.0

type User:
  id string
  name string
  age int
"""
        module = parse_pw(code.strip())
        assert len(module.types) == 1
        user_type = module.types[0]
        assert user_type.name == "User"
        assert len(user_type.fields) == 3
        assert user_type.fields[0].name == "id"
        assert user_type.fields[0].prop_type.name == "string"

    def test_optional_type(self):
        """Test optional type annotation."""
        code = """
module test
version 1.0.0

type User:
  id string
  email string?
"""
        module = parse_pw(code.strip())
        user_type = module.types[0]
        assert user_type.fields[1].prop_type.is_optional

    def test_generic_type(self):
        """Test generic type annotation."""
        code = """
module test
version 1.0.0

type Container:
  items array<string>
  metadata map<string, any>
"""
        module = parse_pw(code.strip())
        container_type = module.types[0]
        assert container_type.fields[0].prop_type.name == "array"
        assert len(container_type.fields[0].prop_type.generic_args) == 1
        assert container_type.fields[0].prop_type.generic_args[0].name == "string"


class TestEnums:
    """Test enum parsing."""

    def test_simple_enum(self):
        """Test simple enum."""
        code = """
module test
version 1.0.0

enum Status:
  - pending
  - completed
  - failed
"""
        module = parse_pw(code.strip())
        assert len(module.enums) == 1
        status_enum = module.enums[0]
        assert status_enum.name == "Status"
        assert len(status_enum.variants) == 3
        assert status_enum.variants[0].name == "pending"

    def test_enum_with_data(self):
        """Test enum with associated data."""
        code = """
module test
version 1.0.0

enum Result:
  - ok(value any)
  - error(message string, code int)
"""
        module = parse_pw(code.strip())
        result_enum = module.enums[0]
        assert len(result_enum.variants[1].associated_types) == 2


class TestFunctions:
    """Test function parsing."""

    def test_simple_function(self):
        """Test simple function."""
        code = """
module test
version 1.0.0

function greet:
  params:
    name string
  returns:
    greeting string
  body:
    return "Hello " + name
"""
        module = parse_pw(code.strip())
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "greet"
        assert len(func.params) == 1
        assert func.params[0].name == "name"
        assert func.return_type.name == "string"
        assert len(func.body) == 1

    def test_function_with_throws(self):
        """Test function with throws."""
        code = """
module test
version 1.0.0

function process:
  params:
    data string
  returns:
    result string
  throws:
    - ValidationError
    - ProcessError
  body:
    return data
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert len(func.throws) == 2
        assert func.throws[0] == "ValidationError"

    def test_async_function(self):
        """Test async function."""
        code = """
module test
version 1.0.0

async function fetch_data:
  params:
    url string
  returns:
    data any
  body:
    return null
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert func.is_async


class TestClasses:
    """Test class parsing."""

    def test_simple_class(self):
        """Test simple class."""
        code = """
module test
version 1.0.0

class Point:
  properties:
    x int
    y int
  constructor:
    params:
      x int
      y int
    body:
      self.x = x
      self.y = y
  method distance:
    params:
      other Point
    returns:
      dist float
    body:
      return 0.0
"""
        module = parse_pw(code.strip())
        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "Point"
        assert len(cls.properties) == 2
        assert cls.constructor is not None
        assert len(cls.methods) == 1


class TestStatements:
    """Test statement parsing."""

    def test_assignment(self):
        """Test assignment statement."""
        code = """
module test
version 1.0.0

function test:
  body:
    let x = 10
    let y = "hello"
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0], IRAssignment)
        assert func.body[0].target == "x"
        assert func.body[0].is_declaration

    def test_if_statement(self):
        """Test if statement."""
        code = """
module test
version 1.0.0

function test:
  body:
    if x > 0:
      return 1
    else:
      return 0
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0], IRIf)

    def test_for_loop(self):
        """Test for loop."""
        code = """
module test
version 1.0.0

function test:
  body:
    for item in items:
      pass
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0], IRFor)
        assert func.body[0].iterator == "item"

    def test_while_loop(self):
        """Test while loop."""
        code = """
module test
version 1.0.0

function test:
  body:
    while x > 0:
      x = x - 1
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0], IRWhile)


class TestExpressions:
    """Test expression parsing."""

    def test_literals(self):
        """Test literal expressions."""
        code = """
module test
version 1.0.0

function test:
  body:
    let a = 42
    let b = 3.14
    let c = "hello"
    let d = true
    let e = null
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0].value, IRLiteral)
        assert func.body[0].value.literal_type == LiteralType.INTEGER
        assert func.body[0].value.value == 42

    def test_binary_operations(self):
        """Test binary operations."""
        code = """
module test
version 1.0.0

function test:
  body:
    let a = 1 + 2
    let b = x == y
    let c = p and q
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0].value, IRBinaryOp)
        assert func.body[0].value.op == BinaryOperator.ADD

    def test_function_call(self):
        """Test function call."""
        code = """
module test
version 1.0.0

function test:
  body:
    let result = process(x, y, z: 10)
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        call = func.body[0].value
        assert isinstance(call, IRCall)
        assert len(call.args) == 2
        assert len(call.kwargs) == 1

    def test_property_access(self):
        """Test property access."""
        code = """
module test
version 1.0.0

function test:
  body:
    let name = user.name
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        from dsl.ir import IRPropertyAccess
        assert isinstance(func.body[0].value, IRPropertyAccess)

    def test_array_literal(self):
        """Test array literal."""
        code = """
module test
version 1.0.0

function test:
  body:
    let items = [1, 2, 3]
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0].value, IRArray)
        assert len(func.body[0].value.elements) == 3

    def test_map_literal(self):
        """Test map literal."""
        code = """
module test
version 1.0.0

function test:
  body:
    let obj = {name: "Alice", age: 30}
"""
        module = parse_pw(code.strip())
        func = module.functions[0]
        assert isinstance(func.body[0].value, IRMap)
        assert len(func.body[0].value.entries) == 2


class TestRoundTrip:
    """Test round-trip conversion (PW → IR → PW)."""

    def test_simple_roundtrip(self):
        """Test simple round-trip."""
        original = """module test
version 1.0.0

function greet:
  params:
    name string
  returns:
    result string
  body:
    return "Hello"
"""
        # Parse
        module = parse_pw(original)

        # Generate
        generated = generate_pw(module)

        # Parse again
        module2 = parse_pw(generated)

        # Compare
        assert module.name == module2.name
        assert module.version == module2.version
        assert len(module.functions) == len(module2.functions)

    def test_complex_roundtrip(self):
        """Test complex program round-trip."""
        original = """module payment_processor
version 1.0.0

import http_client
import database from storage

type User:
  id string
  name string
  email string?

enum Status:
  - pending
  - completed
  - failed

function process_payment:
  params:
    amount float
    user_id string
  returns:
    result Status
  throws:
    - ValidationError
  body:
    let user = database.get_user(user_id)
    if user == null:
      throw ValidationError("User not found")
    return Status.completed
"""
        # Parse
        module = parse_pw(original)

        # Generate
        generated = generate_pw(module)

        # Parse again
        module2 = parse_pw(generated)

        # Verify structure preserved
        assert module.name == module2.name
        assert len(module.imports) == len(module2.imports)
        assert len(module.types) == len(module2.types)
        assert len(module.enums) == len(module2.enums)
        assert len(module.functions) == len(module2.functions)


class TestGoldenFixtures:
    """Test with golden fixtures (real-world examples)."""

    def test_math_utils(self):
        """Test math utilities module."""
        code = """module math_utils
version 1.0.0

function factorial:
  params:
    n int
  returns:
    result int
  body:
    if n <= 1:
      return 1
    return n * factorial(n - 1)

function fibonacci:
  params:
    n int
  returns:
    result int
  body:
    if n <= 1:
      return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        module = parse_pw(code)
        assert len(module.functions) == 2
        assert module.functions[0].name == "factorial"
        assert module.functions[1].name == "fibonacci"

    def test_bank_account(self):
        """Test bank account class."""
        code = """module banking
version 1.0.0

class BankAccount:
  properties:
    balance float = 0.0
    owner string
  constructor:
    params:
      owner string
      initial_balance float = 0.0
    body:
      self.owner = owner
      self.balance = initial_balance
  method deposit:
    params:
      amount float
    returns:
      new_balance float
    body:
      self.balance = self.balance + amount
      return self.balance
  method withdraw:
    params:
      amount float
    returns:
      new_balance float
    throws:
      - InsufficientFunds
    body:
      if amount > self.balance:
        throw InsufficientFunds("Not enough funds")
      self.balance = self.balance - amount
      return self.balance
"""
        module = parse_pw(code)
        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "BankAccount"
        assert len(cls.properties) == 2
        assert len(cls.methods) == 2


class TestErrorHandling:
    """Test error handling."""

    def test_syntax_error_indentation(self):
        """Test indentation error."""
        code = """module test
version 1.0.0

function test:
   body:
    return 1
"""
        with pytest.raises(Exception):  # Should raise PWParseError
            parse_pw(code)

    def test_semantic_error_undefined(self):
        """Test undefined reference (future enhancement)."""
        # This would require semantic analysis phase
        pass


def test_full_system():
    """Integration test: full system."""
    code = """module data_processor
version 2.0.0

import json
import database from storage

type ProcessResult:
  success bool
  count int
  errors array<string>

enum ErrorType:
  - validation
  - database
  - network

function process_batch:
  params:
    items array<map<string, any>>
  returns:
    result ProcessResult
  throws:
    - ValidationError
  body:
    let errors = []
    let count = 0
    for item in items:
      count = count + 1
    return {success: true, count: count, errors: errors}
"""
    # Parse
    module = parse_pw(code)

    # Verify structure
    assert module.name == "data_processor"
    assert module.version == "2.0.0"
    assert len(module.imports) == 2
    assert len(module.types) == 1
    assert len(module.enums) == 1
    assert len(module.functions) == 1

    # Generate
    generated = generate_pw(module)

    # Round-trip
    module2 = parse_pw(generated)
    assert module.name == module2.name


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
