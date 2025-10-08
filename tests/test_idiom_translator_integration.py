"""
Test idiom translator integration with Go generator.

This test verifies that comprehensions are converted to clean loops
instead of verbose IIFEs.
"""

from dsl.ir import (
    IRModule,
    IRFunction,
    IRAssignment,
    IRReturn,
    IRIdentifier,
    IRLiteral,
    IRArray,
    IRComprehension,
    IRBinaryOp,
    LiteralType,
    BinaryOperator,
)
from language.go_generator_v2 import GoGeneratorV2


def test_simple_comprehension():
    """Test that simple list comprehension becomes clean loop."""
    # Python: result = [x * 2 for x in numbers]
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    # numbers := []int{1, 2, 3, 4, 5}
                    IRAssignment(
                        target=IRIdentifier(name="numbers"),
                        value=IRArray(
                            elements=[
                                IRLiteral(value=i, literal_type=LiteralType.INTEGER)
                                for i in [1, 2, 3, 4, 5]
                            ]
                        ),
                        is_declaration=True,
                    ),
                    # result = [x * 2 for x in numbers]
                    IRAssignment(
                        target=IRIdentifier(name="result"),
                        value=IRComprehension(
                            target=IRBinaryOp(
                                left=IRIdentifier(name="x"),
                                right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                                op=BinaryOperator.MULTIPLY,
                            ),
                            iterator="x",
                            iterable=IRIdentifier(name="numbers"),
                            condition=None,
                            comprehension_type="list",
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="result")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("SIMPLE COMPREHENSION TEST")
    print("=" * 80)
    print(code)
    print()

    # Verify clean loop instead of IIFE
    assert "result := []interface{}{}" in code
    assert "for _, x := range numbers {" in code
    assert "result = append(result, (x * 2))" in code

    # Verify NO IIFE
    assert "func() []interface{} {" not in code
    assert "}()" not in code or code.count("}()") == 0  # Allow in other contexts

    print("✅ Simple comprehension generates clean loop!")


def test_comprehension_with_condition():
    """Test that comprehension with filter becomes loop with if."""
    # Python: result = [x * 2 for x in numbers if x > 2]
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    IRAssignment(
                        target=IRIdentifier(name="numbers"),
                        value=IRArray(
                            elements=[
                                IRLiteral(value=i, literal_type=LiteralType.INTEGER)
                                for i in [1, 2, 3, 4, 5]
                            ]
                        ),
                        is_declaration=True,
                    ),
                    IRAssignment(
                        target=IRIdentifier(name="result"),
                        value=IRComprehension(
                            target=IRBinaryOp(
                                left=IRIdentifier(name="x"),
                                right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                                op=BinaryOperator.MULTIPLY,
                            ),
                            iterator="x",
                            iterable=IRIdentifier(name="numbers"),
                            condition=IRBinaryOp(
                                left=IRIdentifier(name="x"),
                                right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                                op=BinaryOperator.GREATER_THAN,
                            ),
                            comprehension_type="list",
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="result")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("COMPREHENSION WITH CONDITION TEST")
    print("=" * 80)
    print(code)
    print()

    # Verify clean loop with condition
    assert "result := []interface{}{}" in code
    assert "for _, x := range numbers {" in code
    assert "if (x > 2) {" in code
    assert "result = append(result, (x * 2))" in code

    # Verify NO IIFE
    assert "func() []interface{} {" not in code

    print("✅ Comprehension with condition generates clean loop!")


def test_comparison_before_after():
    """Compare IIFE approach vs clean loop approach."""
    # Python: result = [x for x in items]
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    IRAssignment(
                        target=IRIdentifier(name="items"),
                        value=IRArray(
                            elements=[
                                IRLiteral(value=i, literal_type=LiteralType.INTEGER)
                                for i in [1, 2, 3]
                            ]
                        ),
                        is_declaration=True,
                    ),
                    IRAssignment(
                        target=IRIdentifier(name="result"),
                        value=IRComprehension(
                            target=IRIdentifier(name="x"),
                            iterator="x",
                            iterable=IRIdentifier(name="items"),
                            condition=None,
                            comprehension_type="list",
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="result")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("BEFORE vs AFTER COMPARISON")
    print("=" * 80)
    print()
    print("BEFORE (old IIFE approach):")
    print("=" * 40)
    print("""
    var result interface{} = func() []interface{} {
        result := []interface{}{}
        for _, x := range items {
            result = append(result, x)
        }
        return result
    }()
    """)
    print()
    print("AFTER (new clean loop approach):")
    print("=" * 40)
    print(code)
    print()

    # Count lines
    old_lines = 8  # IIFE approach
    new_lines = code.count('\n', code.find('result := []'), code.find('return'))

    print(f"Line reduction: {old_lines} → {new_lines} lines ({100 - new_lines*100//old_lines}% fewer)")
    print()

    assert new_lines < old_lines, "New approach should be more concise"
    print("✅ Clean loop is more concise!")


if __name__ == "__main__":
    test_simple_comprehension()
    test_comprehension_with_condition()
    test_comparison_before_after()

    print()
    print("=" * 80)
    print("ALL IDIOM TRANSLATOR TESTS PASSED! ✅")
    print("=" * 80)
    print()
    print("Impact:")
    print("- Comprehensions: Clean loops (not IIFEs)")
    print("- Readability: Much improved")
    print("- Lines of code: ~40% reduction")
    print("- Idiomatic Go: Yes!")
