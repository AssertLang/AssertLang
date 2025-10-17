"""
Test PW parser map/dictionary support.

Tests:
1. Map literal
2. Map access
3. Map assignment
4. Map with different types
5. Nested maps
6. Empty map
7. Map code generation
8. Multi-line map
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_map_literal():
    """Test map literal creation."""
    print(f"\n{'='*60}")
    print("Testing map literal")
    print(f"{'='*60}")

    pw_code = """function create_user() -> map {
    let user = {
        name: "Alice",
        age: 30,
        active: true
    };
    return user;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        # Check for map in body
        has_map = False
        for stmt in func.body:
            if hasattr(stmt, 'value') and hasattr(stmt.value, 'type'):
                if str(stmt.value.type) == 'NodeType.MAP':
                    has_map = True
                    print(f"  ✅ Map literal found with {len(stmt.value.entries)} entries")
                    break

        if has_map:
            print(f"\n✅ SUCCESS: Map literal works!")
            return True
        else:
            print(f"\n❌ FAILED: No map literal found")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_map_access():
    """Test map access."""
    print(f"\n{'='*60}")
    print("Testing map access")
    print(f"{'='*60}")

    pw_code = """function get_name(user: map) -> string {
    let name = user["name"];
    return name;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Map access works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_map_assignment():
    """Test map value assignment."""
    print(f"\n{'='*60}")
    print("Testing map value assignment")
    print(f"{'='*60}")

    pw_code = """function update_user(user: map, email: string) -> map {
    user["email"] = email;
    return user;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Map assignment works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_map_different_types():
    """Test maps with different value types."""
    print(f"\n{'='*60}")
    print("Testing maps with different types")
    print(f"{'='*60}")

    pw_code = """function create_config() -> map {
    let config = {
        host: "localhost",
        port: 8080,
        enabled: true,
        timeout: 30.5
    };
    return config;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Maps with different types work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_nested_maps():
    """Test nested maps."""
    print(f"\n{'='*60}")
    print("Testing nested maps")
    print(f"{'='*60}")

    pw_code = """function create_nested() -> map {
    let data = {
        user: {
            name: "Alice",
            age: 30
        },
        settings: {
            theme: "dark",
            notifications: true
        }
    };
    return data;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Nested maps work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_empty_map():
    """Test empty map."""
    print(f"\n{'='*60}")
    print("Testing empty map")
    print(f"{'='*60}")

    pw_code = """function create_empty() -> map {
    let empty = {};
    return empty;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Empty map works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_map_code_generation():
    """Test that maps generate correct Python code."""
    print(f"\n{'='*60}")
    print("Testing map code generation")
    print(f"{'='*60}")

    pw_code = """function get_user() -> map {
    let user = {
        name: "Bob",
        age: 25
    };
    return user;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has dict
        if "{" in python_code and "name" in python_code:
            print(f"\n✅ SUCCESS: Map generates correct Python!")
            print(f"\nGenerated Python:\n{python_code}")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't have map")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_map_multi_line():
    """Test multi-line map literal."""
    print(f"\n{'='*60}")
    print("Testing multi-line map literal")
    print(f"{'='*60}")

    pw_code = """function create_settings() -> map {
    let settings = {
        theme: "light",
        fontSize: 14,
        autoSave: true,
        tabSize: 4,
        wordWrap: false
    };
    return settings;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Multi-line map works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_string_keys():
    """Test map with string keys (quoted)."""
    print(f"\n{'='*60}")
    print("Testing map with string keys")
    print(f"{'='*60}")

    pw_code = """function create_api_response() -> map {
    let response = {
        "status": "success",
        "data": {
            "id": 123,
            "name": "Item"
        }
    };
    return response;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: String keys work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all map tests."""
    print("\n" + "="*60)
    print("PW PARSER MAP TESTS")
    print("="*60)

    tests = [
        ("Map literal", test_map_literal),
        ("Map access", test_map_access),
        ("Map assignment", test_map_assignment),
        ("Maps with different types", test_map_different_types),
        ("Nested maps", test_nested_maps),
        ("Empty map", test_empty_map),
        ("Map code generation", test_map_code_generation),
        ("Multi-line map", test_map_multi_line),
        ("String keys", test_string_keys),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print("\n" + "="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
