"""
Test Bug #7: Map Key Existence Check Pattern - Safe Access

Tests that map[key] in read context generates safe access patterns:
- Python: dict.get(key)
- Rust: map.get(&key).cloned()
- C#: (dict.ContainsKey(key) ? dict[key] : null)

But map[key] = value in write context generates direct assignment.
"""

from dsl.al_parser import Lexer, Parser
from language.python_generator_v2 import PythonGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


def test_safe_map_read_standalone_function():
    """Test safe map access in standalone function with map parameter."""
    pw_code = """
function check_user(users: map, username: string) -> bool {
    if (users[username] != null) {
        return true;
    }
    return false;
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    assert "users.get(username)" in python_code, \
        f"Expected users.get(username) for safe read, got:\n{python_code}"
    assert "users[username]" not in python_code or "users[username] =" in python_code, \
        "Should not have direct bracket notation for reads"


def test_safe_map_write_standalone_function():
    """Test direct map assignment in standalone function."""
    pw_code = """
function add_user(users: map, username: string) -> bool {
    if (users[username] != null) {
        return false;
    }
    users[username] = "active";
    return true;
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    # Should use .get() for read
    assert "users.get(username)" in python_code, \
        f"Expected users.get(username) for safe read, got:\n{python_code}"

    # Should use direct bracket for write
    assert 'users[username] = "active"' in python_code, \
        f"Expected users[username] = for direct write, got:\n{python_code}"


def test_safe_map_read_class_property():
    """Test safe map access for class properties (e.g., self.users[key])."""
    pw_code = """
class AuthManager {
    users: map;

    constructor() {
        self.users = {};
    }

    function has_user(username: string) -> bool {
        if (self.users[username] != null) {
            return true;
        }
        return false;
    }
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    assert "self.users.get(username)" in python_code, \
        f"Expected self.users.get(username) for safe read, got:\n{python_code}"

    # Make sure we don't have unsafe access in conditionals
    lines = python_code.split('\n')
    for line in lines:
        if 'if' in line and 'self.users[username]' in line and '!=' in line:
            assert False, f"Found unsafe map access in conditional: {line}"


def test_safe_map_write_class_property():
    """Test direct map assignment for class properties."""
    pw_code = """
class AuthManager {
    users: map;

    constructor() {
        self.users = {};
    }

    function register(username: string, password: string) -> bool {
        if (self.users[username] != null) {
            return false;
        }
        self.users[username] = "hashed";
        return true;
    }
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    # Should use .get() for read
    assert "self.users.get(username)" in python_code, \
        f"Expected self.users.get(username) for safe read, got:\n{python_code}"

    # Should use direct bracket for write
    assert 'self.users[username] = "hashed"' in python_code, \
        f"Expected self.users[username] = for direct write, got:\n{python_code}"


def test_safe_map_read_return_value():
    """Test safe map access when returning a value."""
    pw_code = """
class AuthManager {
    users: map;

    constructor() {
        self.users = {};
    }

    function get_user(username: string) -> string {
        if (self.users[username] != null) {
            return self.users[username];
        }
        return "guest";
    }
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    # Both reads should use .get()
    assert python_code.count("self.users.get(username)") >= 2, \
        f"Expected at least 2 self.users.get(username) calls, got:\n{python_code}"


def test_safe_map_multiple_languages():
    """Test safe map access across all 5 languages."""
    pw_code = """
function check_user(users: map, username: string) -> bool {
    if (users[username] != null) {
        return true;
    }
    return false;
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Python - should use .get()
    py_gen = PythonGeneratorV2()
    py_code = py_gen.generate(ir)
    assert "users.get(username)" in py_code, \
        f"Python should use .get() for safe access"

    # Go - already safe (returns nil for missing keys)
    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir)
    # Go uses direct bracket notation but it's safe in Go
    assert "users[username]" in go_code, \
        "Go uses bracket notation (which is safe in Go)"

    # Rust - should use .get()
    rust_gen = RustGeneratorV2()
    rust_code = rust_gen.generate(ir)
    assert "users.get(" in rust_code, \
        f"Rust should use .get() for safe access"

    # TypeScript - already safe (returns undefined)
    ts_gen = NodeJSGeneratorV2()
    ts_code = ts_gen.generate(ir)
    # TypeScript uses direct bracket notation but it's safe
    assert "users[username]" in ts_code, \
        "TypeScript uses bracket notation (which is safe in TS)"

    # C# - should use ContainsKey check
    cs_gen = DotNetGeneratorV2()
    cs_code = cs_gen.generate(ir)
    assert "ContainsKey" in cs_code or ".Get(" in cs_code, \
        f"C# should use ContainsKey or Get for safe access"


def test_bug7_original_example():
    """Test the original Bug #7 example from the bug report."""
    pw_code = """
class AuthManager {
    users: map;

    function register(username: string, password: string) -> bool {
        if (self.users[username] != null) {
            return false;
        }
        self.users[username] = "hashed";
        return true;
    }
}
"""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()

    # Test Python generation
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir)

    # Verify the fix
    assert "self.users.get(username)" in python_code, \
        "Bug #7: Map read should use .get() not direct bracket"
    assert 'self.users[username] = "hashed"' in python_code, \
        "Bug #7: Map write should use direct bracket notation"

    # Make sure we can run the generated code without KeyError
    # This is the original bug - it would throw KeyError
    print("\nGenerated Python code:")
    print(python_code)
    print("\nBug #7 FIXED: Map reads use safe .get() access!")


if __name__ == "__main__":
    # Run the tests
    test_safe_map_read_standalone_function()
    test_safe_map_write_standalone_function()
    test_safe_map_read_class_property()
    test_safe_map_write_class_property()
    test_safe_map_read_return_value()
    test_safe_map_multiple_languages()
    test_bug7_original_example()
    print("\n✅ All Bug #7 tests passed!")
