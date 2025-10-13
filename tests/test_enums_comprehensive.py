"""
Comprehensive test suite for PW enum syntax.

Tests the YAML-style enum syntax (colon + dashes) and verifies that
C-style brace syntax is rejected with a helpful error message.

Bug #19: Enum syntax unclear - comprehensive test coverage
"""

import pytest
from dsl.pw_parser import parse_pw, PWParseError


def test_simple_enum_basic():
    """Test basic enum with 3 variants."""
    pw_code = """
enum Status:
    - Pending
    - Active
    - Completed
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Status"
    assert len(ir.enums[0].variants) == 3
    assert ir.enums[0].variants[0].name == "Pending"
    assert ir.enums[0].variants[1].name == "Active"
    assert ir.enums[0].variants[2].name == "Completed"


def test_simple_enum_single_variant():
    """Test enum with single variant."""
    pw_code = """
enum Result:
    - Ok
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Result"
    assert len(ir.enums[0].variants) == 1
    assert ir.enums[0].variants[0].name == "Ok"


def test_simple_enum_many_variants():
    """Test enum with many variants (7)."""
    pw_code = """
enum DayOfWeek:
    - Monday
    - Tuesday
    - Wednesday
    - Thursday
    - Friday
    - Saturday
    - Sunday
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "DayOfWeek"
    assert len(ir.enums[0].variants) == 7
    assert ir.enums[0].variants[0].name == "Monday"
    assert ir.enums[0].variants[6].name == "Sunday"


def test_enum_with_associated_type_single():
    """Test enum with single associated type (Rust-style)."""
    pw_code = """
enum Option:
    - Some(int)
    - None
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Option"
    assert len(ir.enums[0].variants) == 2

    # Some variant has associated type
    some_variant = ir.enums[0].variants[0]
    assert some_variant.name == "Some"
    assert len(some_variant.associated_types) == 1
    assert some_variant.associated_types[0].name == "int"

    # None variant has no associated type
    none_variant = ir.enums[0].variants[1]
    assert none_variant.name == "None"
    assert len(none_variant.associated_types) == 0


def test_enum_with_multiple_associated_types():
    """Test enum with multiple associated types."""
    pw_code = """
enum Event:
    - Click(int, int)
    - KeyPress(string)
    - Scroll(float)
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Event"

    # Click has 2 associated types
    click = ir.enums[0].variants[0]
    assert click.name == "Click"
    assert len(click.associated_types) == 2
    assert click.associated_types[0].name == "int"
    assert click.associated_types[1].name == "int"

    # KeyPress has 1 associated type
    keypress = ir.enums[0].variants[1]
    assert keypress.name == "KeyPress"
    assert len(keypress.associated_types) == 1
    assert keypress.associated_types[0].name == "string"

    # Scroll has 1 associated type
    scroll = ir.enums[0].variants[2]
    assert scroll.name == "Scroll"
    assert len(scroll.associated_types) == 1
    assert scroll.associated_types[0].name == "float"


def test_enum_result_pattern():
    """Test Result<T, E> enum pattern."""
    pw_code = """
enum Result:
    - Ok(int)
    - Error(string)
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Result"

    ok_variant = ir.enums[0].variants[0]
    assert ok_variant.name == "Ok"
    assert len(ok_variant.associated_types) == 1
    assert ok_variant.associated_types[0].name == "int"

    error_variant = ir.enums[0].variants[1]
    assert error_variant.name == "Error"
    assert len(error_variant.associated_types) == 1
    assert error_variant.associated_types[0].name == "string"


def test_multiple_enums_in_module():
    """Test multiple enum definitions in same module."""
    pw_code = """
enum Color:
    - Red
    - Green
    - Blue

enum Status:
    - Pending
    - Active

enum Priority:
    - Low
    - Medium
    - High
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 3
    assert ir.enums[0].name == "Color"
    assert ir.enums[1].name == "Status"
    assert ir.enums[2].name == "Priority"


def test_enum_in_module_with_other_constructs():
    """Test enum alongside functions and classes."""
    pw_code = """
enum Status:
    - Active
    - Inactive

function get_status() -> string {
    return "Active";
}

class User {
    status: string;

    constructor(status: string) {
        self.status = status;
    }
}
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert len(ir.functions) == 1
    assert len(ir.classes) == 1
    assert ir.enums[0].name == "Status"


def test_c_style_enum_fails_with_brace():
    """Test that C-style brace enum syntax is rejected."""
    pw_code = """
enum OperationType {
    QUERY,
    MUTATION
}
"""
    with pytest.raises(PWParseError) as exc_info:
        parse_pw(pw_code)

    error_msg = str(exc_info.value)
    assert "Expected :, got {" in error_msg or "Expected COLON" in error_msg


def test_c_style_enum_fails_with_semicolons():
    """Test that enum with semicolons is rejected."""
    pw_code = """
enum Status {
    Pending;
    Active;
    Completed;
}
"""
    with pytest.raises(PWParseError) as exc_info:
        parse_pw(pw_code)

    error_msg = str(exc_info.value)
    # Should fail on the brace first
    assert "Expected :, got {" in error_msg or "Expected COLON" in error_msg


def test_enum_no_semicolons_after_variants():
    """Test that semicolons after variants are not needed."""
    pw_code = """
enum Status:
    - Pending
    - Active
    - Completed
"""
    # Should parse successfully without semicolons
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1


def test_enum_graphql_operation_type():
    """Test real-world GraphQL OperationType enum."""
    pw_code = """
enum OperationType:
    - QUERY
    - MUTATION
    - SUBSCRIPTION
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "OperationType"
    assert len(ir.enums[0].variants) == 3
    assert ir.enums[0].variants[0].name == "QUERY"
    assert ir.enums[0].variants[1].name == "MUTATION"
    assert ir.enums[0].variants[2].name == "SUBSCRIPTION"


def test_enum_graphql_type_kind():
    """Test real-world GraphQL TypeKind enum."""
    pw_code = """
enum TypeKind:
    - SCALAR
    - OBJECT
    - INTERFACE
    - UNION
    - ENUM
    - INPUT_OBJECT
    - LIST
    - NON_NULL
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "TypeKind"
    assert len(ir.enums[0].variants) == 8


def test_enum_cache_state():
    """Test real-world CacheState enum."""
    pw_code = """
enum CacheState:
    - Empty
    - Loading
    - Ready
    - Stale
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "CacheState"
    assert len(ir.enums[0].variants) == 4


def test_enum_workflow_node_type():
    """Test real-world workflow NodeType enum."""
    pw_code = """
enum NodeType:
    - Task
    - Decision
    - Parallel
    - Join
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "NodeType"
    assert len(ir.enums[0].variants) == 4


def test_enum_workflow_execution_status():
    """Test real-world ExecutionStatus enum."""
    pw_code = """
enum ExecutionStatus:
    - Pending
    - Running
    - Completed
    - Failed
    - Cancelled
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "ExecutionStatus"
    assert len(ir.enums[0].variants) == 5


def test_enum_empty_fails():
    """Test that enum with no variants fails."""
    pw_code = """
enum EmptyEnum:
"""
    # This should fail - enum must have at least one variant
    with pytest.raises(PWParseError):
        parse_pw(pw_code)


def test_enum_variant_names_case_sensitive():
    """Test that enum variant names are case-sensitive."""
    pw_code = """
enum Status:
    - active
    - Active
    - ACTIVE
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert len(ir.enums[0].variants) == 3
    assert ir.enums[0].variants[0].name == "active"
    assert ir.enums[0].variants[1].name == "Active"
    assert ir.enums[0].variants[2].name == "ACTIVE"


def test_enum_variant_names_with_underscores():
    """Test enum variant names with underscores."""
    pw_code = """
enum HttpMethod:
    - GET
    - POST
    - PUT
    - DELETE
    - PATCH
    - HEAD
    - OPTIONS
    - CONNECT
    - TRACE
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert len(ir.enums[0].variants) == 9


def test_enum_variant_names_snake_case():
    """Test enum variant names with snake_case."""
    pw_code = """
enum JobStatus:
    - not_started
    - in_progress
    - completed_successfully
    - failed_with_error
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    assert len(ir.enums[0].variants) == 4
    assert ir.enums[0].variants[2].name == "completed_successfully"


def test_enum_with_generic_associated_type():
    """Test enum with generic associated types."""
    pw_code = """
enum Container:
    - Some(array<int>)
    - None
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    some_variant = ir.enums[0].variants[0]
    assert some_variant.name == "Some"
    assert len(some_variant.associated_types) == 1
    assert some_variant.associated_types[0].name == "array"
    assert len(some_variant.associated_types[0].generic_args) == 1
    assert some_variant.associated_types[0].generic_args[0].name == "int"


def test_enum_with_map_associated_type():
    """Test enum with map associated type."""
    pw_code = """
enum Response:
    - Success(map<string, int>)
    - Error(string)
"""
    ir = parse_pw(pw_code)
    assert len(ir.enums) == 1
    success_variant = ir.enums[0].variants[0]
    assert success_variant.name == "Success"
    assert len(success_variant.associated_types) == 1
    assert success_variant.associated_types[0].name == "map"
    assert len(success_variant.associated_types[0].generic_args) == 2


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
