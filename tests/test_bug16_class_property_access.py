"""
Test Bug #16: Class Property Access Regression

This test ensures that class property access generates correct attribute access
syntax (obj.property) instead of incorrectly using dictionary access (obj["property"]).

Bug Report: Bugs/v2.1.0b9/PW_BUG_REPORT_BATCH_9.md
Priority: CRITICAL - Regression from Bug #15 fix
Status: This bug was introduced when fixing Bug #15 (map access)

The Bug #15 fix over-corrected and started treating ALL property access as map access,
breaking class-based code. This test ensures classes work correctly while Bug #15 tests
ensure maps still work.
"""

import pytest
from pathlib import Path
import tempfile
import subprocess
import sys


def compile_pw_to_python(pw_code: str) -> str:
    """Compile PW code to Python and return the generated code."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pw', delete=False) as f:
        f.write(pw_code)
        pw_file = f.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        py_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'promptware.cli', 'build', pw_file, '--lang', 'python', '-o', py_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {result.stderr}")

        with open(py_file, 'r') as f:
            return f.read()
    finally:
        Path(pw_file).unlink(missing_ok=True)
        Path(py_file).unlink(missing_ok=True)


class TestBug16ClassPropertyAccess:
    """Test that class property access generates correct attribute access syntax."""

    def test_basic_class_property_access(self):
        """Test basic class property access uses dot notation."""
        pw_code = '''
class User {
    name: string;
    age: int;

    constructor(name: string, age: int) {
        self.name = name;
        self.age = age;
    }
}

function test_user() -> string {
    let user = User("Alice", 30);
    return user.name;
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Should use dot notation for class properties
        assert 'user.name' in python_code, "Class property access should use dot notation"
        assert 'self.name' in python_code, "Class self access should use dot notation"

        # Should NOT use bracket notation for classes
        assert 'user["name"]' not in python_code, "Should not use bracket notation for class instances"
        assert 'self["name"]' not in python_code, "Should not use bracket notation for self"

    def test_function_parameter_class_type(self):
        """Test that function parameters with class types use dot notation."""
        pw_code = '''
class Config {
    port: int;
    host: string;

    constructor(port: int, host: string) {
        self.port = port;
        self.host = host;
    }
}

function get_port(config: Config) -> int {
    return config.port;
}

function get_host(config: Config) -> string {
    return config.host;
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Parameters with class types should use dot notation
        assert 'config.port' in python_code, "Class parameter property access should use dot notation"
        assert 'config.host' in python_code, "Class parameter property access should use dot notation"

        # Should NOT use bracket notation
        assert 'config["port"]' not in python_code, "Should not use bracket notation for class parameter"
        assert 'config["host"]' not in python_code, "Should not use bracket notation for class parameter"

    def test_rate_limiter_bug_reproduction(self):
        """
        Test the exact pattern from pw_rate_limiter.pw that triggers Bug #16.

        This is the core case from the bug report:
        function register_tier(tier: RateLimitTier) -> bool {
            self.tiers[tier.name] = tier;  // tier.name should be tier.name, not tier["name"]
        }
        """
        pw_code = '''
class RateLimitTier {
    name: string;
    requests_per_second: int;
    burst_size: int;

    constructor(name: string, rps: int, burst: int) {
        self.name = name;
        self.requests_per_second = rps;
        self.burst_size = burst;
    }
}

class DistributedRateLimiter {
    tiers: map;

    constructor() {
        self.tiers = {};
    }

    function register_tier(tier: RateLimitTier) -> bool {
        self.tiers[tier.name] = tier;
        return true;
    }

    function get_tier(name: string) -> RateLimitTier {
        return self.tiers[name];
    }
}
'''
        python_code = compile_pw_to_python(pw_code)

        # The critical fix: tier is a RateLimitTier class, so tier.name should use dot notation
        assert 'tier.name' in python_code, \
            "BUG #16 FIX: Class parameter property access should use dot notation"

        # Should NOT use bracket notation for class instances
        assert 'tier["name"]' not in python_code, \
            "Should not use bracket notation for class instance property"

        # self.tiers is a map, so bracket notation is correct for map assignment
        assert 'self.tiers[' in python_code, "Map indexing should use brackets"

    def test_class_vs_map_mixed(self):
        """Test that classes use dot notation and maps use brackets in same function."""
        pw_code = '''
class Person {
    name: string;
    age: int;

    constructor(name: string, age: int) {
        self.name = name;
        self.age = age;
    }
}

function test_mixed(person: Person, data: map) -> bool {
    let person_name = person.name;
    let data_value = data.value;
    return true;
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Class should use dot notation
        assert 'person.name' in python_code, "Class parameter should use dot notation"

        # Map should use bracket notation
        assert 'data["value"]' in python_code, "Map parameter should use bracket notation"

    def test_nested_class_property_access(self):
        """Test accessing properties through nested class instances."""
        pw_code = '''
class Address {
    city: string;
    street: string;

    constructor(city: string, street: string) {
        self.city = city;
        self.street = street;
    }
}

class Person {
    name: string;
    address: Address;

    constructor(name: string, address: Address) {
        self.name = name;
        self.address = address;
    }
}

function get_city(person: Person) -> string {
    return person.address.city;
}
'''
        python_code = compile_pw_to_python(pw_code)

        # All levels should use dot notation
        assert 'person.address' in python_code, "Nested class access should use dot notation"
        # Note: person.address.city might be on same line or split
        assert '.city' in python_code, "Nested property access should use dot notation"

    def test_method_parameter_class_type(self):
        """Test that method parameters with class types use dot notation."""
        pw_code = '''
class Item {
    id: string;
    quantity: int;

    constructor(id: string, quantity: int) {
        self.id = id;
        self.quantity = quantity;
    }
}

class Cart {
    items: array;

    constructor() {
        self.items = [];
    }

    function add_item(item: Item) -> bool {
        if (item.quantity > 0) {
            return true;
        }
        return false;
    }

    function get_item_id(item: Item) -> string {
        return item.id;
    }
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Method parameters with class types should use dot notation
        assert 'item.quantity' in python_code, "Method parameter class property should use dot notation"
        assert 'item.id' in python_code, "Method parameter class property should use dot notation"

        # Should NOT use bracket notation
        assert 'item["quantity"]' not in python_code, "Should not use bracket notation for class parameter"
        assert 'item["id"]' not in python_code, "Should not use bracket notation for class parameter"

    def test_runtime_execution_no_type_error(self):
        """Test that generated code runs without TypeError: object is not subscriptable."""
        pw_code = '''
class Config {
    port: int;
    host: string;

    constructor(port: int, host: string) {
        self.port = port;
        self.host = host;
    }
}

function get_port(config: Config) -> int {
    return config.port;
}

function main() -> int {
    let config = Config(8080, "localhost");
    return get_port(config);
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Execute the generated Python code
        namespace = {}
        try:
            exec(python_code, namespace)
            # Call the main function
            result = namespace['main']()
            assert result == 8080, f"Expected 8080, got {result}"
        except TypeError as e:
            if "not subscriptable" in str(e):
                pytest.fail(f"Generated code raised TypeError: object is not subscriptable (Bug #16 not fixed): {e}")
            else:
                raise
        except Exception as e:
            pytest.fail(f"Generated code raised unexpected error: {e}")

    def test_class_with_map_property(self):
        """Test a class that has a map-typed property (should use bracket for map, dot for class)."""
        pw_code = '''
class Database {
    connections: map;
    max_connections: int;

    constructor(max_conn: int) {
        self.connections = {};
        self.max_connections = max_conn;
    }

    function add_connection(name: string) -> bool {
        self.connections[name] = true;
        return true;
    }

    function has_connection(name: string) -> bool {
        return self.connections[name] == true;
    }
}

function test_db(db: Database) -> int {
    return db.max_connections;
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Class property access should use dot notation
        assert 'db.max_connections' in python_code, "Class property should use dot notation"
        assert 'self.max_connections' in python_code, "Class self property should use dot notation"

        # Map property (self.connections) should use bracket notation for indexing
        assert 'self.connections[' in python_code, "Map property indexing should use brackets"

        # Should NOT use bracket for class property
        assert 'db["max_connections"]' not in python_code, "Should not use bracket for class property"

    def test_ensure_no_regression_from_bug15(self):
        """
        Ensure that fixing Bug #16 doesn't break Bug #15.

        Both classes and maps should work correctly:
        - Classes: use dot notation
        - Maps: use bracket notation
        """
        pw_code = '''
class User {
    name: string;

    constructor(name: string) {
        self.name = name;
    }
}

function test_both() -> bool {
    // Class instance
    let user = User("Alice");
    let user_name = user.name;

    // Map
    let data = {"status": "ok"};
    let status = data.status;

    // Function returning map
    let result = get_result();
    let success = result.success;

    return true;
}

function get_result() -> map {
    return {"success": true};
}
'''
        python_code = compile_pw_to_python(pw_code)

        # Class should use dot notation (Bug #16 fix)
        assert 'user.name' in python_code, "Class property should use dot notation"

        # Maps should use bracket notation (Bug #15 should still work)
        assert 'data["status"]' in python_code, "Map literal should use bracket notation"
        assert 'result["success"]' in python_code, "Map from function should use bracket notation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
