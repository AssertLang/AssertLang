"""
C# Exception Handling Tests

Tests try/catch/finally support in C# parser and generator.

Test Cases:
1. Simple try-catch
2. Try-catch with exception variable
3. Multiple catch blocks
4. Try-catch-finally
5. Try-finally (no catch)
6. Catch without variable
7. Round-trip C# → IR → C#
8. Cross-language: Python → C# exception translation
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.dotnet_parser_v2 import DotNetParserV2
from language.dotnet_generator_v2 import DotNetGeneratorV2
from language.python_parser_v2 import PythonParserV2
from dsl.ir import IRTry, IRCatch


def test_simple_try_catch():
    """Test simple try-catch parsing."""
    code = '''
public class Example {
    public int Divide(int a, int b) {
        try {
            return a / b;
        } catch (DivideByZeroException) {
            return 0;
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    # Verify try-catch parsed
    assert len(ir.classes) == 1
    method = ir.classes[0].methods[0]

    # Find try statement in body
    has_try = any(isinstance(stmt, IRTry) for stmt in method.body)
    assert has_try, "No IRTry found in method body"

    # Get the try statement
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))
    assert len(try_stmt.catch_blocks) == 1, "Expected 1 catch block"
    assert try_stmt.catch_blocks[0].exception_type.name == "DivideByZeroException"
    assert try_stmt.finally_body is None, "Should not have finally"

    print("✅ test_simple_try_catch PASSED")


def test_try_catch_with_variable():
    """Test try-catch with exception variable."""
    code = '''
public class Example {
    public int Process(string data) {
        try {
            return int.Parse(data);
        } catch (FormatException e) {
            Console.WriteLine(e.Message);
            return 0;
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    method = ir.classes[0].methods[0]
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))

    assert len(try_stmt.catch_blocks) == 1
    catch = try_stmt.catch_blocks[0]
    assert catch.exception_type.name == "FormatException"
    assert catch.exception_var == "e", f"Expected var 'e', got '{catch.exception_var}'"

    print("✅ test_try_catch_with_variable PASSED")


def test_multiple_catch_blocks():
    """Test multiple catch blocks."""
    code = '''
public class Example {
    public int FetchData(string url) {
        try {
            return DownloadInt(url);
        } catch (TimeoutException e) {
            Console.Error.WriteLine("Timeout");
            return -1;
        } catch (HttpRequestException e) {
            Console.Error.WriteLine("HTTP error");
            return -2;
        } catch (Exception e) {
            Console.Error.WriteLine("Unknown error");
            return -3;
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    method = ir.classes[0].methods[0]
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))

    assert len(try_stmt.catch_blocks) == 3, f"Expected 3 catch blocks, got {len(try_stmt.catch_blocks)}"

    # Verify each catch block
    assert try_stmt.catch_blocks[0].exception_type.name == "TimeoutException"
    assert try_stmt.catch_blocks[1].exception_type.name == "HttpRequestException"
    assert try_stmt.catch_blocks[2].exception_type.name == "Exception"

    print("✅ test_multiple_catch_blocks PASSED")


def test_try_catch_finally():
    """Test try-catch-finally."""
    code = '''
public class Example {
    public int Divide(int a, int b) {
        try {
            return a / b;
        } catch (DivideByZeroException e) {
            Console.WriteLine($"Error: {e.Message}");
            return 0;
        } finally {
            Console.WriteLine("Done");
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    method = ir.classes[0].methods[0]
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))

    assert len(try_stmt.catch_blocks) == 1
    assert try_stmt.finally_body is not None, "Expected finally block"
    assert len(try_stmt.finally_body) > 0, "Finally block should have statements"

    print("✅ test_try_catch_finally PASSED")


def test_catch_without_variable():
    """Test catch without variable name."""
    code = '''
public class Example {
    public void Process() {
        try {
            DoSomething();
        } catch (Exception) {
            Console.WriteLine("Error occurred");
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    method = ir.classes[0].methods[0]
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))

    assert len(try_stmt.catch_blocks) == 1
    catch = try_stmt.catch_blocks[0]
    assert catch.exception_type.name == "Exception"
    assert catch.exception_var is None, "Should not have exception variable"

    print("✅ test_catch_without_variable PASSED")


def test_round_trip_csharp():
    """Test C# → IR → C# round-trip."""
    original_code = '''
public class Example {
    public double Divide(double a, double b) {
        try {
            if (b == 0) {
                throw new DivideByZeroException();
            }
            return a / b;
        } catch (DivideByZeroException e) {
            Console.WriteLine($"Error: {e.Message}");
            return 0;
        } finally {
            Console.WriteLine("Done");
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(original_code, "test")

    generator = DotNetGeneratorV2()
    generated_code = generator.generate(ir)

    # Verify generated code contains exception handling
    assert "try" in generated_code, "Generated code missing 'try'"
    assert "catch" in generated_code, "Generated code missing 'catch'"
    assert "finally" in generated_code, "Generated code missing 'finally'"
    assert "DivideByZeroException" in generated_code, "Generated code missing exception type"

    print("✅ test_round_trip_csharp PASSED")
    print("\nGenerated C# code:")
    print(generated_code)


def test_python_to_csharp_translation():
    """Test Python try/except → C# try/catch translation."""
    python_code = '''
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return 0
    finally:
        print("Done")
'''
    # Parse Python
    python_parser = PythonParserV2()
    ir = python_parser.parse_source(python_code, "test")

    # Generate C#
    csharp_generator = DotNetGeneratorV2()
    csharp_code = csharp_generator.generate(ir)

    # Verify C# code has exception handling
    assert "try" in csharp_code, "C# code missing 'try'"
    assert "catch" in csharp_code, "C# code missing 'catch'"
    assert "finally" in csharp_code, "C# code missing 'finally'"

    print("✅ test_python_to_csharp_translation PASSED")
    print("\nTranslated C# code:")
    print(csharp_code)


def test_async_method_with_exceptions():
    """Test async method with exception handling."""
    code = '''
public class Example {
    public async Task<User> FetchUserAsync(string url) {
        try {
            var response = await httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsAsync<User>();
        } catch (HttpRequestException e) {
            logger.LogError($"HTTP error: {e.Message}");
            return null;
        } catch (JsonException e) {
            logger.LogError($"Parse error: {e.Message}");
            return null;
        } finally {
            logger.LogInfo("Request completed");
        }
    }
}
'''
    parser = DotNetParserV2()
    ir = parser.parse_source(code, "test")

    method = ir.classes[0].methods[0]

    # Verify async
    assert method.is_async, "Method should be async"

    # Verify exception handling
    try_stmt = next(stmt for stmt in method.body if isinstance(stmt, IRTry))
    assert len(try_stmt.catch_blocks) == 2, "Expected 2 catch blocks"
    assert try_stmt.finally_body is not None, "Expected finally block"

    print("✅ test_async_method_with_exceptions PASSED")


def run_all_tests():
    """Run all C# exception handling tests."""
    print("=" * 80)
    print("C# EXCEPTION HANDLING TEST SUITE")
    print("=" * 80)
    print()

    tests = [
        test_simple_try_catch,
        test_try_catch_with_variable,
        test_multiple_catch_blocks,
        test_try_catch_finally,
        test_catch_without_variable,
        test_round_trip_csharp,
        test_python_to_csharp_translation,
        test_async_method_with_exceptions,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1

    print()
    print("=" * 80)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 80)

    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    sys.exit(0 if failed == 0 else 1)
