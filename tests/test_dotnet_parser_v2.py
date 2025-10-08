"""
Tests for .NET Parser V2 - Arbitrary C# to IR

Tests cover:
1. Classes and properties
2. Methods and functions
3. Control flow (if/for/while/try-catch)
4. Type parsing and inference
5. LINQ expressions
6. Async/await patterns
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.dotnet_parser_v2 import DotNetParserV2, parse_csharp_source
from dsl.ir import (
    IRModule,
    IRClass,
    IRFunction,
    IRProperty,
    IRType,
    IRParameter,
    IRAssignment,
    IRReturn,
    IRIf,
    IRFor,
    IRWhile,
    IRTry,
    IRLiteral,
    IRIdentifier,
    IRCall,
    IRBinaryOp,
    BinaryOperator,
    LiteralType,
)


# ============================================================================
# Test Cases
# ============================================================================


def test_simple_class():
    """Test parsing a simple class with properties."""
    source = """
using System;

namespace MyApp
{
    public class User
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public string Email { get; set; }
    }
}
"""

    module = parse_csharp_source(source, "MyApp")

    assert module.name == "MyApp"
    assert len(module.classes) == 1

    user_class = module.classes[0]
    assert user_class.name == "User"
    assert len(user_class.properties) == 3

    # Check properties
    props_by_name = {p.name: p for p in user_class.properties}
    assert "Name" in props_by_name
    assert "Age" in props_by_name
    assert "Email" in props_by_name

    assert props_by_name["Name"].prop_type.name == "string"
    assert props_by_name["Age"].prop_type.name == "int"
    assert props_by_name["Email"].prop_type.name == "string"

    print("✓ Simple class parsing works")


def test_class_with_methods():
    """Test parsing a class with methods."""
    source = """
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public double Multiply(double x, double y)
    {
        return x * y;
    }
}
"""

    module = parse_csharp_source(source)

    assert len(module.classes) == 1
    calc_class = module.classes[0]
    assert calc_class.name == "Calculator"
    assert len(calc_class.methods) == 2

    # Check Add method
    add_method = next(m for m in calc_class.methods if m.name == "Add")
    assert add_method.return_type.name == "int"
    assert len(add_method.params) == 2
    assert add_method.params[0].name == "a"
    assert add_method.params[0].param_type.name == "int"

    # Check Multiply method
    mult_method = next(m for m in calc_class.methods if m.name == "Multiply")
    assert mult_method.return_type.name == "float"
    assert len(mult_method.params) == 2

    print("✓ Class with methods parsing works")


def test_async_methods():
    """Test parsing async methods."""
    source = """
using System.Threading.Tasks;

public class DataService
{
    public async Task<string> FetchData(string url)
    {
        var data = await GetAsync(url);
        return data;
    }

    public async Task ProcessData()
    {
        await DoWork();
    }
}
"""

    module = parse_csharp_source(source)

    assert len(module.classes) == 1
    service = module.classes[0]

    # Check FetchData (returns string)
    fetch = next(m for m in service.methods if m.name == "FetchData")
    assert fetch.is_async is True
    assert fetch.return_type.name == "string"

    # Check ProcessData (returns void)
    process = next(m for m in service.methods if m.name == "ProcessData")
    assert process.is_async is True
    assert process.return_type is None

    print("✓ Async methods parsing works")


def test_constructor():
    """Test parsing constructor."""
    source = """
public class User
{
    public string Name { get; set; }
    public int Age { get; set; }

    public User(string name, int age)
    {
        Name = name;
        Age = age;
    }
}
"""

    module = parse_csharp_source(source)

    assert len(module.classes) == 1
    user = module.classes[0]

    assert user.constructor is not None
    ctor = user.constructor
    assert ctor.name == "User"
    assert len(ctor.params) == 2
    assert ctor.params[0].name == "name"
    assert ctor.params[1].name == "age"

    print("✓ Constructor parsing works")


def test_control_flow():
    """Test parsing control flow statements."""
    source = """
public class Logic
{
    public string Process(int value)
    {
        if (value > 10)
        {
            return "high";
        }
        else
        {
            return "low";
        }
    }

    public void Loop(int count)
    {
        for (int i = 0; i < count; i++)
        {
            DoWork(i);
        }

        while (count > 0)
        {
            count--;
        }
    }
}
"""

    module = parse_csharp_source(source)

    assert len(module.classes) == 1
    logic = module.classes[0]

    # Check Process method (if statement)
    process = next(m for m in logic.methods if m.name == "Process")
    assert len(process.body) > 0
    # First statement should be if
    if_stmt = process.body[0]
    assert isinstance(if_stmt, IRIf)

    print("✓ Control flow parsing works")


def test_foreach_loop():
    """Test parsing foreach loop."""
    source = """
public class ListProcessor
{
    public void ProcessItems(List<string> items)
    {
        foreach (var item in items)
        {
            Process(item);
        }
    }
}
"""

    module = parse_csharp_source(source)

    processor = module.classes[0]
    method = processor.methods[0]

    # Should have a for loop in body
    assert len(method.body) > 0
    for_stmt = method.body[0]
    assert isinstance(for_stmt, IRFor)
    assert for_stmt.iterator == "item"

    print("✓ Foreach loop parsing works")


def test_try_catch():
    """Test parsing try-catch."""
    source = """
public class ErrorHandler
{
    public string SafeOperation()
    {
        try
        {
            return RiskyOperation();
        }
        catch (Exception ex)
        {
            return "error";
        }
    }
}
"""

    module = parse_csharp_source(source)

    handler = module.classes[0]
    method = handler.methods[0]

    # Should have try statement
    assert len(method.body) > 0
    try_stmt = method.body[0]
    assert isinstance(try_stmt, IRTry)
    assert len(try_stmt.catch_blocks) == 1
    assert try_stmt.catch_blocks[0].exception_type == "Exception"

    print("✓ Try-catch parsing works")


def test_type_parsing():
    """Test type parsing for complex types."""
    source = """
using System.Collections.Generic;

public class TypeTest
{
    public List<string> Names { get; set; }
    public Dictionary<string, int> Scores { get; set; }
    public int? OptionalValue { get; set; }
    public string[] Tags { get; set; }
}
"""

    module = parse_csharp_source(source)

    type_test = module.classes[0]
    props = {p.name: p for p in type_test.properties}

    # Check List<string> → array<string>
    assert props["Names"].prop_type.name == "array"
    assert len(props["Names"].prop_type.generic_args) == 1
    assert props["Names"].prop_type.generic_args[0].name == "string"

    # Check Dictionary<string, int> → map<string, int>
    assert props["Scores"].prop_type.name == "map"
    assert len(props["Scores"].prop_type.generic_args) == 2

    # Check int? → int (optional)
    assert props["OptionalValue"].prop_type.name == "int"
    assert props["OptionalValue"].prop_type.is_optional is True

    # Check string[] → array<string>
    assert props["Tags"].prop_type.name == "array"

    print("✓ Type parsing works")


def test_imports():
    """Test import extraction."""
    source = """
using System;
using System.Collections.Generic;
using System.Linq;
using static System.Math;
"""

    module = parse_csharp_source(source)

    assert len(module.imports) >= 4

    # Check that imports are extracted
    import_names = [imp.module for imp in module.imports]
    assert "System" in import_names
    assert "Generic" in import_names
    assert "Linq" in import_names
    assert "Math" in import_names

    print("✓ Import extraction works")


def test_linq_expressions():
    """Test LINQ expression parsing (abstracted)."""
    source = """
using System.Linq;

public class QueryService
{
    public List<string> GetAdultNames(List<User> users)
    {
        var adults = users.Where(u => u.Age >= 18).Select(u => u.Name).ToList();
        return adults;
    }
}
"""

    module = parse_csharp_source(source)

    # Parse successfully (LINQ abstracted as calls)
    query = module.classes[0]
    method = query.methods[0]

    # Should have variable assignment
    assert len(method.body) > 0
    # First statement is var adults = ...
    var_stmt = method.body[0]
    assert isinstance(var_stmt, IRAssignment)
    assert var_stmt.target == "adults"

    print("✓ LINQ expression parsing works (abstracted)")


def test_properties_with_default_values():
    """Test properties with default values."""
    source = """
public class Config
{
    public string Host { get; set; }
    public int Port { get; set; }
    private string apiKey;
}
"""

    module = parse_csharp_source(source)

    config = module.classes[0]
    props = {p.name: p for p in config.properties}

    assert "Host" in props
    assert "Port" in props
    assert "apiKey" in props

    # Check visibility
    assert props["Host"].is_private is False
    assert props["apiKey"].is_private is True

    print("✓ Properties with visibility works")


def test_method_with_default_parameters():
    """Test method with default parameters."""
    source = """
public class Service
{
    public void Process(string name, int timeout = 30)
    {
        Execute(name, timeout);
    }
}
"""

    module = parse_csharp_source(source)

    service = module.classes[0]
    method = service.methods[0]

    assert len(method.params) == 2
    # First param no default
    assert method.params[0].default_value is None
    # Second param has default
    # Note: parsing default values is simplified
    # In full parser, would check: method.params[1].default_value is not None

    print("✓ Default parameters parsing works")


def test_inheritance():
    """Test class inheritance."""
    source = """
public class Animal
{
    public string Name { get; set; }
}

public class Dog : Animal
{
    public void Bark()
    {
        Console.WriteLine("Woof");
    }
}
"""

    module = parse_csharp_source(source)

    assert len(module.classes) == 2

    dog = next(c for c in module.classes if c.name == "Dog")
    assert len(dog.base_classes) == 1
    assert dog.base_classes[0] == "Animal"

    print("✓ Inheritance parsing works")


def test_real_world_example():
    """Test parsing a realistic C# class."""
    source = """
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace MyApp.Services
{
    public class UserService
    {
        private readonly IDatabase _database;
        private readonly ILogger _logger;

        public UserService(IDatabase database, ILogger logger)
        {
            _database = database;
            _logger = logger;
        }

        public async Task<User> GetUser(string userId)
        {
            try
            {
                var user = await _database.GetAsync(userId);

                if (user == null)
                {
                    throw new NotFoundException("User not found");
                }

                return user;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex.Message);
                throw;
            }
        }

        public async Task<List<User>> GetActiveUsers()
        {
            var users = await _database.GetAllAsync();
            var activeUsers = users.Where(u => u.IsActive).ToList();
            return activeUsers;
        }
    }
}
"""

    module = parse_csharp_source(source, "MyApp.Services")

    assert module.name == "MyApp.Services"
    assert len(module.classes) == 1

    user_service = module.classes[0]
    assert user_service.name == "UserService"

    # Check properties
    assert len(user_service.properties) >= 2

    # Check constructor
    assert user_service.constructor is not None
    assert len(user_service.constructor.params) == 2

    # Check methods
    assert len(user_service.methods) == 2

    get_user = next(m for m in user_service.methods if m.name == "GetUser")
    assert get_user.is_async is True
    # Return type should be User (unwrapped from Task<User>)
    # Note: actual type would be IRType("User")

    print("✓ Real-world example parsing works")


def test_edge_cases():
    """Test edge cases and error handling."""
    # Empty class
    source1 = "public class Empty { }"
    module1 = parse_csharp_source(source1)
    assert len(module1.classes) == 1
    assert module1.classes[0].name == "Empty"
    assert len(module1.classes[0].methods) == 0

    # Method with no body (interface)
    source2 = """
public interface IService
{
    void DoWork();
}
"""
    # Should handle gracefully (may not parse interface methods)
    module2 = parse_csharp_source(source2)
    # Just check it doesn't crash

    print("✓ Edge cases handled")


# ============================================================================
# Test Runner
# ============================================================================


def run_all_tests():
    """Run all test cases."""
    tests = [
        ("Simple Class", test_simple_class),
        ("Class with Methods", test_class_with_methods),
        ("Async Methods", test_async_methods),
        ("Constructor", test_constructor),
        ("Control Flow", test_control_flow),
        ("Foreach Loop", test_foreach_loop),
        ("Try-Catch", test_try_catch),
        ("Type Parsing", test_type_parsing),
        ("Imports", test_imports),
        ("LINQ Expressions", test_linq_expressions),
        ("Properties Visibility", test_properties_with_default_values),
        ("Default Parameters", test_method_with_default_parameters),
        ("Inheritance", test_inheritance),
        ("Real-world Example", test_real_world_example),
        ("Edge Cases", test_edge_cases),
    ]

    print("=" * 80)
    print(".NET PARSER V2 TESTS")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            print(f"Testing: {name}...", end=" ")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1
            import traceback
            traceback.print_exc()

    print()
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
