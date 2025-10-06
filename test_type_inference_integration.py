"""
Test type inference integration with Go generator.

This test verifies that the type inference engine improves generated Go code
by reducing interface{} usage in favor of specific types.
"""

from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRAssignment,
    IRReturn,
    IRIdentifier,
    IRLiteral,
    IRArray,
    IRMap,
    IRBinaryOp,
    IRType,
    LiteralType,
    BinaryOperator,
)
from language.go_generator_v2 import GoGeneratorV2


def test_literal_type_inference():
    """Test that literal assignments get proper types."""
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    # var name string = "Alice"
                    IRAssignment(
                        target=IRIdentifier(name="name"),
                        value=IRLiteral(value="Alice", literal_type=LiteralType.STRING),
                        is_declaration=True,
                    ),
                    # var age int = 30
                    IRAssignment(
                        target=IRIdentifier(name="age"),
                        value=IRLiteral(value=30, literal_type=LiteralType.INTEGER),
                        is_declaration=True,
                    ),
                    # var score float64 = 95.5
                    IRAssignment(
                        target=IRIdentifier(name="score"),
                        value=IRLiteral(value=95.5, literal_type=LiteralType.FLOAT),
                        is_declaration=True,
                    ),
                    # var active bool = true
                    IRAssignment(
                        target=IRIdentifier(name="active"),
                        value=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="name")),
                ],
                return_type=IRType(name="string"),
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("LITERAL TYPE INFERENCE TEST")
    print("=" * 80)
    print(code)
    print()

    # Verify specific types are used instead of interface{}
    assert "var name string" in code
    assert "var age int" in code
    assert "var score float64" in code
    assert "var active bool" in code

    # Verify we're NOT using interface{} for these simple literals
    lines = code.split("\n")
    var_lines = [l for l in lines if l.strip().startswith("var ")]
    for line in var_lines:
        if "name" in line or "age" in line or "score" in line or "active" in line:
            assert "interface{}" not in line, f"Found interface{{}} in: {line}"

    print("✅ Literal type inference working!")


def test_array_type_inference():
    """Test that array literals get proper element types."""
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    # numbers := []int{1, 2, 3}
                    IRAssignment(
                        target=IRIdentifier(name="numbers"),
                        value=IRArray(
                            elements=[
                                IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                                IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                                IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                            ]
                        ),
                        is_declaration=True,
                    ),
                    # names := []string{"Alice", "Bob"}
                    IRAssignment(
                        target=IRIdentifier(name="names"),
                        value=IRArray(
                            elements=[
                                IRLiteral(value="Alice", literal_type=LiteralType.STRING),
                                IRLiteral(value="Bob", literal_type=LiteralType.STRING),
                            ]
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="numbers")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("ARRAY TYPE INFERENCE TEST")
    print("=" * 80)
    print(code)
    print()

    # Verify specific array types
    assert "[]int{1, 2, 3}" in code
    assert "[]string{" in code and "Alice" in code

    print("✅ Array type inference working!")


def test_map_type_inference():
    """Test that map literals get proper value types."""
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    # scores := map[string]int{"Alice": 95, "Bob": 87}
                    IRAssignment(
                        target=IRIdentifier(name="scores"),
                        value=IRMap(
                            entries={
                                "Alice": IRLiteral(value=95, literal_type=LiteralType.INTEGER),
                                "Bob": IRLiteral(value=87, literal_type=LiteralType.INTEGER),
                            }
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="scores")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("MAP TYPE INFERENCE TEST")
    print("=" * 80)
    print(code)
    print()

    # Verify specific map type
    assert "map[string]int{" in code

    print("✅ Map type inference working!")


def test_binary_op_type_inference():
    """Test that binary operations infer proper types."""
    module = IRModule(
        name="test",
        version="1.0.0",
        functions=[
            IRFunction(
                name="example",
                params=[],
                body=[
                    # x := 5
                    IRAssignment(
                        target=IRIdentifier(name="x"),
                        value=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
                        is_declaration=True,
                    ),
                    # y := 3
                    IRAssignment(
                        target=IRIdentifier(name="y"),
                        value=IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                        is_declaration=True,
                    ),
                    # sum := x + y (should infer int)
                    IRAssignment(
                        target=IRIdentifier(name="sum"),
                        value=IRBinaryOp(
                            left=IRIdentifier(name="x"),
                            right=IRIdentifier(name="y"),
                            op=BinaryOperator.ADD,
                        ),
                        is_declaration=True,
                    ),
                    # result := x > y (should infer bool)
                    IRAssignment(
                        target=IRIdentifier(name="result"),
                        value=IRBinaryOp(
                            left=IRIdentifier(name="x"),
                            right=IRIdentifier(name="y"),
                            op=BinaryOperator.GREATER_THAN,
                        ),
                        is_declaration=True,
                    ),
                    IRReturn(value=IRIdentifier(name="sum")),
                ],
            )
        ],
    )

    generator = GoGeneratorV2()
    code = generator.generate(module)

    print("=" * 80)
    print("BINARY OP TYPE INFERENCE TEST")
    print("=" * 80)
    print(code)
    print()

    # Check that sum and result have inferred types
    assert "var sum int" in code
    assert "var result bool" in code

    print("✅ Binary operation type inference working!")


if __name__ == "__main__":
    test_literal_type_inference()
    test_array_type_inference()
    test_map_type_inference()
    test_binary_op_type_inference()

    print()
    print("=" * 80)
    print("ALL TYPE INFERENCE TESTS PASSED! ✅")
    print("=" * 80)
    print()
    print("Impact:")
    print("- Literals: string, int, float64, bool (instead of interface{})")
    print("- Arrays: []int, []string (instead of []interface{})")
    print("- Maps: map[string]int (instead of map[string]interface{})")
    print("- Binary ops: int for arithmetic, bool for comparisons")
