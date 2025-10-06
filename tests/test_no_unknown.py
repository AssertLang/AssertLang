#!/usr/bin/env python3
"""
Test script to verify no <unknown> or comment placeholders in generated code.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dsl.ir import *
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


def create_comprehensive_module() -> IRModule:
    """Create a comprehensive IR module with all expression types."""

    module = IRModule(name="comprehensive_test", version="1.0.0")

    # Create a function that uses all expression types
    func = IRFunction(
        name="test_all_expressions",
        params=[
            IRParameter(name="x", param_type=IRType(name="int")),
            IRParameter(name="y", param_type=IRType(name="int")),
            IRParameter(name="items", param_type=IRType(name="array", generic_args=[IRType(name="int")])),
        ],
        return_type=IRType(name="map", generic_args=[IRType(name="string"), IRType(name="any")]),
        body=[
            # Literals
            IRAssignment(
                target="str_val",
                value=IRLiteral(value="test", literal_type=LiteralType.STRING),
                is_declaration=True,
            ),
            IRAssignment(
                target="int_val",
                value=IRLiteral(value=42, literal_type=LiteralType.INTEGER),
                is_declaration=True,
            ),
            IRAssignment(
                target="float_val",
                value=IRLiteral(value=3.14, literal_type=LiteralType.FLOAT),
                is_declaration=True,
            ),
            IRAssignment(
                target="bool_val",
                value=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                is_declaration=True,
            ),
            IRAssignment(
                target="null_val",
                value=IRLiteral(value=None, literal_type=LiteralType.NULL),
                is_declaration=True,
            ),

            # Binary operations
            IRAssignment(
                target="sum",
                value=IRBinaryOp(
                    left=IRIdentifier(name="x"),
                    op=BinaryOperator.ADD,
                    right=IRIdentifier(name="y"),
                ),
                is_declaration=True,
            ),
            IRAssignment(
                target="is_equal",
                value=IRBinaryOp(
                    left=IRIdentifier(name="x"),
                    op=BinaryOperator.EQUAL,
                    right=IRIdentifier(name="y"),
                ),
                is_declaration=True,
            ),

            # Unary operations
            IRAssignment(
                target="negated",
                value=IRUnaryOp(
                    op=UnaryOperator.NEGATE,
                    operand=IRIdentifier(name="x"),
                ),
                is_declaration=True,
            ),
            IRAssignment(
                target="not_val",
                value=IRUnaryOp(
                    op=UnaryOperator.NOT,
                    operand=IRIdentifier(name="bool_val"),
                ),
                is_declaration=True,
            ),

            # Arrays
            IRAssignment(
                target="arr",
                value=IRArray(elements=[
                    IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                    IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                    IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                ]),
                is_declaration=True,
            ),

            # Maps
            IRAssignment(
                target="map_val",
                value=IRMap(entries={
                    "key1": IRLiteral(value="value1", literal_type=LiteralType.STRING),
                    "key2": IRLiteral(value=123, literal_type=LiteralType.INTEGER),
                }),
                is_declaration=True,
            ),

            # Property access
            IRAssignment(
                target="prop",
                value=IRPropertyAccess(
                    object=IRIdentifier(name="map_val"),
                    property="key1",
                ),
                is_declaration=True,
            ),

            # Index access
            IRAssignment(
                target="first_item",
                value=IRIndex(
                    object=IRIdentifier(name="items"),
                    index=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
                ),
                is_declaration=True,
            ),

            # Function calls
            IRAssignment(
                target="result",
                value=IRCall(
                    function=IRIdentifier(name="some_function"),
                    args=[IRIdentifier(name="x"), IRIdentifier(name="y")],
                ),
                is_declaration=True,
            ),

            # Ternary
            IRAssignment(
                target="conditional",
                value=IRTernary(
                    condition=IRIdentifier(name="bool_val"),
                    true_value=IRLiteral(value="yes", literal_type=LiteralType.STRING),
                    false_value=IRLiteral(value="no", literal_type=LiteralType.STRING),
                ),
                is_declaration=True,
            ),

            # Lambda
            IRAssignment(
                target="double_func",
                value=IRLambda(
                    params=[IRParameter(name="n", param_type=IRType(name="int"))],
                    body=IRBinaryOp(
                        left=IRIdentifier(name="n"),
                        op=BinaryOperator.MULTIPLY,
                        right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                    ),
                ),
                is_declaration=True,
            ),

            # Return
            IRReturn(value=IRIdentifier(name="map_val")),
        ],
        doc="Test function with all expression types",
    )

    module.functions.append(func)
    return module


def check_for_unknown(code: str, language: str) -> tuple[bool, list[str]]:
    """Check if code contains unknown/placeholder patterns."""
    issues = []

    # Check for various unknown patterns
    patterns = [
        "<unknown>",
        "/* unknown",
        "/* Unknown",
        "// Unknown statement",
        "// unknown",
        "/* multi-statement",  # Incomplete lambdas
    ]

    for pattern in patterns:
        if pattern in code:
            # Find line numbers
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if pattern in line:
                    issues.append(f"Line {i}: {line.strip()}")

    return len(issues) == 0, issues


def main():
    """Run comprehensive test."""
    print("=" * 70)
    print("TESTING FOR <unknown> PLACEHOLDERS IN ALL GENERATORS")
    print("=" * 70)
    print()

    module = create_comprehensive_module()

    generators = [
        ("JavaScript/TypeScript", lambda: generate_nodejs(module, typescript=True)),
        ("JavaScript", lambda: generate_nodejs(module, typescript=False)),
        ("Go", lambda: generate_go(module)),
        ("Rust", lambda: generate_rust(module)),
        ("C#/.NET", lambda: generate_csharp(module)),
    ]

    all_passed = True

    for lang_name, generator_func in generators:
        print(f"\n{'=' * 70}")
        print(f"Testing: {lang_name}")
        print(f"{'=' * 70}\n")

        try:
            code = generator_func()
            passed, issues = check_for_unknown(code, lang_name)

            if passed:
                print(f"✅ {lang_name}: PASSED - No unknown placeholders found")
                print(f"   Generated {len(code)} characters, {len(code.splitlines())} lines")
            else:
                print(f"❌ {lang_name}: FAILED - Found {len(issues)} issues:")
                for issue in issues[:5]:  # Show first 5
                    print(f"   {issue}")
                if len(issues) > 5:
                    print(f"   ... and {len(issues) - 5} more")
                all_passed = False

        except Exception as e:
            print(f"❌ {lang_name}: ERROR - {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED - No unknown placeholders in any language")
    else:
        print("❌ SOME TESTS FAILED - See details above")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
