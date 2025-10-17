"""
Test for Bug #7 - Safe map access through CLI path

This test verifies that property type information (like `users: map`) is preserved
through the full CLI code path:
1. PW text → IR (via parse_al)
2. IR → MCP tree (via ir_to_mcp)
3. MCP tree → IR (via mcp_to_ir)
4. IR → Python (via PythonGeneratorV2)
"""

import sys
from pathlib import Path

# Add pw-syntax-mcp-server to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp, mcp_to_ir
from language.python_generator_v2 import PythonGeneratorV2


def test_bug7_cli_path_preserves_property_types():
    """Test that property types survive the IR → MCP → IR roundtrip"""

    pw_code = """
class AuthManager {
    users: map;

    function has_user(username: string) -> bool {
        if (self.users[username] != null) {
            return true;
        }
        return false;
    }
}
"""

    # Step 1: Parse PW → IR
    ir = parse_al(pw_code)

    # Step 2: IR → MCP
    mcp_tree = ir_to_mcp(ir)

    # Step 3: MCP → IR
    ir_restored = mcp_to_ir(mcp_tree)

    # Step 4: IR → Python
    gen = PythonGeneratorV2()
    python_code = gen.generate(ir_restored)

    # Verify safe map access
    assert 'self.users.get(username)' in python_code, \
        f"Expected safe map access using .get(), got:\n{python_code}"

    # Verify property type is preserved
    assert 'users: Dict' in python_code or 'users:Dict' in python_code, \
        f"Expected property type annotation, got:\n{python_code}"

    # Ensure unsafe access is NOT present
    assert 'self.users[username]' not in python_code, \
        f"Found unsafe map access with [], got:\n{python_code}"


def test_bug7_property_roundtrip():
    """Test that IRProperty survives MCP roundtrip with type info"""

    from dsl.ir import IRProperty, IRType

    # Create a property with a map type
    original_prop = IRProperty(
        name="users",
        prop_type=IRType(name="map"),
        default_value=None
    )

    # Convert to MCP
    mcp = ir_to_mcp(original_prop)

    # Verify MCP structure
    assert mcp["tool"] == "pw_property"
    assert mcp["params"]["name"] == "users"
    assert mcp["params"]["prop_type"]["tool"] == "pw_type"
    assert mcp["params"]["prop_type"]["params"]["name"] == "map"

    # Convert back to IR
    restored_prop = mcp_to_ir(mcp)

    # Verify restoration
    assert restored_prop.name == "users"
    assert restored_prop.prop_type is not None
    assert restored_prop.prop_type.name == "map"


def test_bug7_class_properties_roundtrip():
    """Test that class properties with types survive MCP roundtrip"""

    from dsl.ir import IRClass, IRProperty, IRType

    # Create a class with properties
    original_class = IRClass(
        name="AuthManager",
        properties=[
            IRProperty(name="users", prop_type=IRType(name="map")),
            IRProperty(name="admin", prop_type=IRType(name="bool")),
        ],
        methods=[],
        base_classes=[]
    )

    # Convert to MCP and back
    mcp = ir_to_mcp(original_class)
    restored_class = mcp_to_ir(mcp)

    # Verify properties are restored correctly
    assert len(restored_class.properties) == 2

    users_prop = restored_class.properties[0]
    assert users_prop.name == "users"
    assert users_prop.prop_type is not None
    assert users_prop.prop_type.name == "map"

    admin_prop = restored_class.properties[1]
    assert admin_prop.name == "admin"
    assert admin_prop.prop_type is not None
    assert admin_prop.prop_type.name == "bool"


if __name__ == "__main__":
    test_bug7_cli_path_preserves_property_types()
    test_bug7_property_roundtrip()
    test_bug7_class_properties_roundtrip()
    print("✅ All Bug #7 CLI path tests passed!")
