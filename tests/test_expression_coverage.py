#!/usr/bin/env python3
"""
Test that all IR expression types generate valid code without placeholders.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dsl.ir import *
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


def test_expression_type(expr_name: str, expr: IRExpression) -> dict:
    """Test a single expression type across all generators."""

    generators = {
        "nodejs": NodeJSGeneratorV2(typescript=True),
        "go": GoGeneratorV2(),
        "rust": RustGeneratorV2(),
        "dotnet": DotNetGeneratorV2(),
    }

    results = {}

    for lang, gen in generators.items():
        try:
            if lang == "nodejs":
                code = gen.generate_expression(expr)
            elif lang == "go":
                code = gen._generate_expression(expr)
            elif lang == "rust":
                code = gen._generate_expression(expr)
            elif lang == "dotnet":
                code = gen._generate_expression(expr)

            # Check for bad patterns
            bad_patterns = ["<unknown>", "/* unknown", "/* Unknown", "// Unknown"]
            has_placeholder = any(pattern in code for pattern in bad_patterns)

            results[lang] = {
                "code": code,
                "has_placeholder": has_placeholder,
                "length": len(code),
            }
        except Exception as e:
            results[lang] = {
                "code": None,
                "has_placeholder": True,
                "error": str(e),
            }

    return results


def main():
    """Test all expression types."""

    print("=" * 70)
    print("EXPRESSION TYPE COVERAGE TEST")
    print("=" * 70)
    print()

    # Test cases: (name, IR expression)
    test_cases = [
        ("Literal String", IRLiteral(value="hello", literal_type=LiteralType.STRING)),
        ("Literal Integer", IRLiteral(value=42, literal_type=LiteralType.INTEGER)),
        ("Literal Float", IRLiteral(value=3.14, literal_type=LiteralType.FLOAT)),
        ("Literal Boolean", IRLiteral(value=True, literal_type=LiteralType.BOOLEAN)),
        ("Literal Null", IRLiteral(value=None, literal_type=LiteralType.NULL)),

        ("Identifier", IRIdentifier(name="myVar")),

        ("Binary Add", IRBinaryOp(
            left=IRIdentifier(name="a"),
            op=BinaryOperator.ADD,
            right=IRIdentifier(name="b"),
        )),
        ("Binary Equal", IRBinaryOp(
            left=IRIdentifier(name="x"),
            op=BinaryOperator.EQUAL,
            right=IRIdentifier(name="y"),
        )),
        ("Binary AND", IRBinaryOp(
            left=IRIdentifier(name="a"),
            op=BinaryOperator.AND,
            right=IRIdentifier(name="b"),
        )),

        ("Unary NOT", IRUnaryOp(
            op=UnaryOperator.NOT,
            operand=IRIdentifier(name="flag"),
        )),
        ("Unary NEGATE", IRUnaryOp(
            op=UnaryOperator.NEGATE,
            operand=IRIdentifier(name="num"),
        )),

        ("Call Simple", IRCall(
            function=IRIdentifier(name="myFunc"),
            args=[],
        )),
        ("Call With Args", IRCall(
            function=IRIdentifier(name="myFunc"),
            args=[
                IRIdentifier(name="x"),
                IRLiteral(value=10, literal_type=LiteralType.INTEGER),
            ],
        )),

        ("Property Access", IRPropertyAccess(
            object=IRIdentifier(name="obj"),
            property="field",
        )),

        ("Index Access", IRIndex(
            object=IRIdentifier(name="arr"),
            index=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
        )),

        ("Array Empty", IRArray(elements=[])),
        ("Array With Elements", IRArray(elements=[
            IRLiteral(value=1, literal_type=LiteralType.INTEGER),
            IRLiteral(value=2, literal_type=LiteralType.INTEGER),
            IRLiteral(value=3, literal_type=LiteralType.INTEGER),
        ])),

        ("Map Empty", IRMap(entries={})),
        ("Map With Entries", IRMap(entries={
            "name": IRLiteral(value="John", literal_type=LiteralType.STRING),
            "age": IRLiteral(value=30, literal_type=LiteralType.INTEGER),
        })),

        ("Ternary", IRTernary(
            condition=IRIdentifier(name="flag"),
            true_value=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
            false_value=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
        )),

        ("Lambda Simple", IRLambda(
            params=[IRParameter(name="x", param_type=IRType(name="int"))],
            body=IRIdentifier(name="x"),
        )),
        ("Lambda Complex", IRLambda(
            params=[
                IRParameter(name="x", param_type=IRType(name="int")),
                IRParameter(name="y", param_type=IRType(name="int")),
            ],
            body=IRBinaryOp(
                left=IRIdentifier(name="x"),
                op=BinaryOperator.ADD,
                right=IRIdentifier(name="y"),
            ),
        )),
    ]

    all_passed = True
    failed_tests = []

    for test_name, expr in test_cases:
        results = test_expression_type(test_name, expr)

        # Check if any language has placeholders
        has_any_placeholder = any(r.get("has_placeholder", False) for r in results.values())

        if has_any_placeholder:
            print(f"❌ {test_name}")
            all_passed = False
            failed_tests.append(test_name)

            for lang, result in results.items():
                if result.get("has_placeholder", False):
                    print(f"   {lang}: {result.get('code', 'ERROR')}")
        else:
            print(f"✅ {test_name}")
            # Show generated code samples
            for lang, result in results.items():
                code = result.get("code", "")
                if code and len(code) < 80:
                    print(f"   {lang:8s}: {code}")

    print("\n" + "=" * 70)
    print(f"RESULTS: {len(test_cases) - len(failed_tests)}/{len(test_cases)} passed")

    if all_passed:
        print("✅ ALL EXPRESSION TYPES GENERATE VALID CODE")
    else:
        print(f"❌ {len(failed_tests)} FAILED:")
        for test in failed_tests:
            print(f"   - {test}")

    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
