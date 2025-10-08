#!/usr/bin/env python3
"""
Final comprehensive test: Verify NO placeholders in generated code.
Tests all generators with real-world complex IR structures.
"""

import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dsl.ir import *
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


def create_complex_demo() -> IRModule:
    """Create a complex real-world-like module."""

    module = IRModule(name="demo_app", version="2.0.0")

    # Type definition
    user_type = IRTypeDefinition(
        name="User",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="int")),
            IRProperty(name="name", prop_type=IRType(name="string")),
            IRProperty(name="email", prop_type=IRType(name="string", is_optional=True)),
            IRProperty(name="age", prop_type=IRType(name="int", is_optional=True)),
        ],
        doc="User data model",
    )
    module.types.append(user_type)

    # Enum
    status_enum = IREnum(
        name="Status",
        variants=[
            IREnumVariant(name="Active", value="active"),
            IREnumVariant(name="Inactive", value="inactive"),
            IREnumVariant(name="Pending", value="pending"),
        ],
        doc="User status",
    )
    module.enums.append(status_enum)

    # Complex function with all expression types
    process_users = IRFunction(
        name="process_users",
        params=[
            IRParameter(
                name="users",
                param_type=IRType(name="array", generic_args=[IRType(name="User")]),
            ),
            IRParameter(name="min_age", param_type=IRType(name="int")),
        ],
        return_type=IRType(name="map", generic_args=[IRType(name="string"), IRType(name="int")]),
        body=[
            # Variable declarations with different expressions
            IRAssignment(
                target="results",
                value=IRMap(entries={}),
                is_declaration=True,
                var_type=IRType(name="map", generic_args=[IRType(name="string"), IRType(name="int")]),
            ),

            # For loop with filtering logic
            IRFor(
                iterator="user",
                iterable=IRIdentifier(name="users"),
                body=[
                    # Access property
                    IRAssignment(
                        target="user_age",
                        value=IRPropertyAccess(
                            object=IRIdentifier(name="user"),
                            property="age",
                        ),
                        is_declaration=True,
                    ),

                    # Ternary expression
                    IRAssignment(
                        target="age_value",
                        value=IRTernary(
                            condition=IRBinaryOp(
                                left=IRIdentifier(name="user_age"),
                                op=BinaryOperator.NOT_EQUAL,
                                right=IRLiteral(value=None, literal_type=LiteralType.NULL),
                            ),
                            true_value=IRIdentifier(name="user_age"),
                            false_value=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
                        ),
                        is_declaration=True,
                    ),

                    # If statement with comparison
                    IRIf(
                        condition=IRBinaryOp(
                            left=IRIdentifier(name="age_value"),
                            op=BinaryOperator.GREATER_EQUAL,
                            right=IRIdentifier(name="min_age"),
                        ),
                        then_body=[
                            # Property access and function call
                            IRAssignment(
                                target="user_name",
                                value=IRPropertyAccess(
                                    object=IRIdentifier(name="user"),
                                    property="name",
                                ),
                                is_declaration=True,
                            ),

                            # Binary operation
                            IRAssignment(
                                target="count",
                                value=IRBinaryOp(
                                    left=IRIndex(
                                        object=IRIdentifier(name="results"),
                                        index=IRIdentifier(name="user_name"),
                                    ),
                                    op=BinaryOperator.ADD,
                                    right=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                                ),
                                is_declaration=False,
                            ),
                        ],
                        else_body=[],
                    ),
                ],
            ),

            # Return statement
            IRReturn(value=IRIdentifier(name="results")),
        ],
        doc="Process users based on age criteria",
    )
    module.functions.append(process_users)

    # Class with methods
    user_service = IRClass(
        name="UserService",
        properties=[
            IRProperty(
                name="api_key",
                prop_type=IRType(name="string"),
                is_private=True,
            ),
            IRProperty(
                name="cache",
                prop_type=IRType(name="map", generic_args=[IRType(name="string"), IRType(name="User")]),
            ),
        ],
        constructor=IRFunction(
            name="__init__",
            params=[
                IRParameter(name="api_key", param_type=IRType(name="string")),
            ],
            body=[
                IRAssignment(
                    target="api_key",
                    value=IRIdentifier(name="api_key"),
                    is_declaration=False,
                ),
                IRAssignment(
                    target="cache",
                    value=IRMap(entries={}),
                    is_declaration=False,
                ),
            ],
        ),
        methods=[
            IRFunction(
                name="get_user",
                params=[
                    IRParameter(name="user_id", param_type=IRType(name="int")),
                ],
                return_type=IRType(name="User", is_optional=True),
                body=[
                    # Lambda expression
                    IRAssignment(
                        target="formatter",
                        value=IRLambda(
                            params=[
                                IRParameter(name="id", param_type=IRType(name="int")),
                            ],
                            body=IRCall(
                                function=IRIdentifier(name="format"),
                                args=[
                                    IRLiteral(value="user_{}", literal_type=LiteralType.STRING),
                                    IRIdentifier(name="id"),
                                ],
                            ),
                        ),
                        is_declaration=True,
                    ),

                    # Call with lambda
                    IRAssignment(
                        target="cache_key",
                        value=IRCall(
                            function=IRIdentifier(name="formatter"),
                            args=[IRIdentifier(name="user_id")],
                        ),
                        is_declaration=True,
                    ),

                    # Array creation
                    IRAssignment(
                        target="headers",
                        value=IRArray(elements=[
                            IRLiteral(value="Authorization", literal_type=LiteralType.STRING),
                            IRIdentifier(name="api_key"),
                        ]),
                        is_declaration=True,
                    ),

                    # Return with ternary
                    IRReturn(
                        value=IRTernary(
                            condition=IRCall(
                                function=IRPropertyAccess(
                                    object=IRIdentifier(name="cache"),
                                    property="has_key",
                                ),
                                args=[IRIdentifier(name="cache_key")],
                            ),
                            true_value=IRIndex(
                                object=IRIdentifier(name="cache"),
                                index=IRIdentifier(name="cache_key"),
                            ),
                            false_value=IRLiteral(value=None, literal_type=LiteralType.NULL),
                        ),
                    ),
                ],
                doc="Get user by ID with caching",
            ),
        ],
        doc="Service for managing users",
    )
    module.classes.append(user_service)

    return module


def check_for_bad_patterns(code: str, language: str) -> tuple[bool, list[str]]:
    """Check for any placeholder patterns that indicate incomplete generation."""

    bad_patterns = [
        r"<unknown>",
        r"/\*\s*unknown",
        r"/\*\s*Unknown",
        r"//\s*Unknown\s+statement",
        r"//\s*unknown\s+expression",
        r"TODO:\s*implement",  # Only if it's the main implementation
    ]

    issues = []

    for pattern in bad_patterns:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            # Find line number
            line_num = code[:match.start()].count('\n') + 1
            line = code.split('\n')[line_num - 1]
            issues.append(f"Line {line_num}: {line.strip()}")

    return len(issues) == 0, issues


def analyze_code_quality(code: str, language: str) -> dict:
    """Analyze generated code quality metrics."""

    lines = code.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]

    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty_lines),
        "avg_line_length": sum(len(l) for l in lines) / max(len(lines), 1),
        "has_functions": "func" in code or "function" in code or "def" in code,
        "has_classes": "class" in code or "struct" in code or "impl" in code,
    }


def main():
    """Run comprehensive final test."""

    print("=" * 80)
    print("FINAL COMPREHENSIVE TEST: NO PLACEHOLDERS IN GENERATED CODE")
    print("=" * 80)
    print()

    module = create_complex_demo()

    generators = [
        ("TypeScript", lambda: generate_nodejs(module, typescript=True)),
        ("JavaScript", lambda: generate_nodejs(module, typescript=False)),
        ("Go", lambda: generate_go(module)),
        ("Rust", lambda: generate_rust(module)),
        ("C#", lambda: generate_csharp(module)),
    ]

    results = {}
    all_passed = True

    for lang_name, generator_func in generators:
        print(f"\n{'=' * 80}")
        print(f"Testing: {lang_name}")
        print(f"{'=' * 80}\n")

        try:
            code = generator_func()
            passed, issues = check_for_bad_patterns(code, lang_name)
            metrics = analyze_code_quality(code, lang_name)

            if passed:
                print(f"✅ {lang_name}: PASSED")
                print(f"   Lines: {metrics['total_lines']} ({metrics['code_lines']} non-empty)")
                print(f"   Characters: {len(code)}")
                print(f"   Avg line length: {metrics['avg_line_length']:.1f}")
                print(f"   Has functions: {metrics['has_functions']}")
                print(f"   Has classes: {metrics['has_classes']}")

                results[lang_name] = {
                    "status": "PASS",
                    "code": code,
                    "metrics": metrics,
                }
            else:
                print(f"❌ {lang_name}: FAILED")
                print(f"   Found {len(issues)} placeholder issues:")
                for issue in issues[:10]:
                    print(f"   - {issue}")
                if len(issues) > 10:
                    print(f"   ... and {len(issues) - 10} more")

                results[lang_name] = {
                    "status": "FAIL",
                    "issues": issues,
                }
                all_passed = False

        except Exception as e:
            print(f"❌ {lang_name}: ERROR")
            print(f"   {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

            results[lang_name] = {
                "status": "ERROR",
                "error": str(e),
            }
            all_passed = False

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results.values() if r.get("status") == "PASS")
    failed = len(results) - passed

    print(f"\nResults: {passed}/{len(results)} passed")

    for lang, result in results.items():
        status = result.get("status", "UNKNOWN")
        if status == "PASS":
            print(f"  ✅ {lang}")
        else:
            print(f"  ❌ {lang} ({status})")

    print("\n" + "=" * 80)

    if all_passed:
        print("✅ SUCCESS: All generators produce valid code without placeholders!")
        print("=" * 80)
        return 0
    else:
        print("❌ FAILURE: Some generators still have placeholders or errors")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
