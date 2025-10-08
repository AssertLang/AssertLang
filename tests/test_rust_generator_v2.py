"""
Test Suite for Rust Generator V2

Tests IR → Rust code generation with comprehensive coverage of:
- Basic constructs (functions, structs, enums)
- Type system (primitives, collections, Option, Result)
- Control flow (if/for/while/match)
- Ownership patterns
- Async/await
- Error handling
- Round-trip preservation

Target: 95%+ test pass rate
"""

import pytest
from language.rust_generator_v2 import RustGeneratorV2, generate_rust
from language.rust_parser_v2 import RustParserV2, parse_rust_code
from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRType,
    IRReturn,
    IRLiteral,
    IRIdentifier,
    IRAssignment,
    IRCall,
    IRBinaryOp,
    IRIf,
    IRFor,
    IRWhile,
    IRArray,
    IRMap,
    IRTypeDefinition,
    IRProperty,
    IREnum,
    IREnumVariant,
    IRClass,
    IRTry,
    IRCatch,
    IRThrow,
    BinaryOperator,
    LiteralType,
)


class TestBasicConstructs:
    """Test basic Rust constructs."""

    def test_empty_module(self):
        """Test generating an empty module."""
        module = IRModule(name="test", version="1.0.0")
        code = generate_rust(module)

        assert "pub" in code or code == "\n"  # May have no public items

    def test_simple_function(self):
        """Test generating a simple function."""
        func = IRFunction(
            name="greet",
            params=[IRParameter(name="name", param_type=IRType(name="string"))],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRLiteral(value="Hello", literal_type=LiteralType.STRING)
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "pub fn greet" in code
        assert "-> String" in code
        assert "return" in code

    def test_function_with_multiple_params(self):
        """Test function with multiple parameters."""
        func = IRFunction(
            name="add",
            params=[
                IRParameter(name="a", param_type=IRType(name="int")),
                IRParameter(name="b", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="int"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.ADD,
                        left=IRIdentifier(name="a"),
                        right=IRIdentifier(name="b")
                    )
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "pub fn add(a: i32, b: i32) -> i32" in code
        assert "a + b" in code

    def test_async_function(self):
        """Test async function generation."""
        func = IRFunction(
            name="fetch_data",
            params=[IRParameter(name="url", param_type=IRType(name="string"))],
            return_type=IRType(name="string"),
            is_async=True,
            body=[
                IRReturn(
                    value=IRLiteral(value="data", literal_type=LiteralType.STRING)
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "pub async fn fetch_data" in code


class TestTypeSystem:
    """Test type system and type mappings."""

    def test_primitive_types(self):
        """Test primitive type mappings."""
        func = IRFunction(
            name="types_demo",
            params=[
                IRParameter(name="s", param_type=IRType(name="string")),
                IRParameter(name="i", param_type=IRType(name="int")),
                IRParameter(name="f", param_type=IRType(name="float")),
                IRParameter(name="b", param_type=IRType(name="bool")),
            ],
            return_type=IRType(name="bool"),
            body=[IRReturn(value=IRIdentifier(name="b"))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Check parameter types (should be borrowed where appropriate)
        assert "s: &str" in code or "s: String" in code
        assert "i: i32" in code
        assert "f: f64" in code
        assert "b: bool" in code
        assert "-> bool" in code

    def test_array_type(self):
        """Test array type generation."""
        func = IRFunction(
            name="process_items",
            params=[
                IRParameter(
                    name="items",
                    param_type=IRType(
                        name="array",
                        generic_args=[IRType(name="string")]
                    )
                )
            ],
            return_type=IRType(name="int"),
            body=[IRReturn(value=IRLiteral(value=0, literal_type=LiteralType.INTEGER))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "Vec<String>" in code

    def test_map_type(self):
        """Test map type generation."""
        func = IRFunction(
            name="process_map",
            params=[
                IRParameter(
                    name="data",
                    param_type=IRType(
                        name="map",
                        generic_args=[
                            IRType(name="string"),
                            IRType(name="int")
                        ]
                    )
                )
            ],
            return_type=IRType(name="int"),
            body=[IRReturn(value=IRLiteral(value=0, literal_type=LiteralType.INTEGER))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "HashMap<String, i32>" in code
        assert "use std::collections::HashMap;" in code

    def test_optional_type(self):
        """Test optional type (T?) → Option<T>."""
        func = IRFunction(
            name="find_user",
            params=[IRParameter(name="id", param_type=IRType(name="string"))],
            return_type=IRType(name="string", is_optional=True),
            body=[IRReturn(value=IRLiteral(value=None, literal_type=LiteralType.NULL))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "Option<String>" in code

    def test_result_type(self):
        """Test function with throws → Result<T, E>."""
        func = IRFunction(
            name="risky_operation",
            params=[IRParameter(name="value", param_type=IRType(name="int"))],
            return_type=IRType(name="string"),
            throws=["Box<dyn Error>"],
            body=[
                IRReturn(
                    value=IRLiteral(value="success", literal_type=LiteralType.STRING)
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "Result<String, Box<dyn Error>>" in code
        assert "use std::error::Error;" in code


class TestStructGeneration:
    """Test struct generation."""

    def test_simple_struct(self):
        """Test simple struct generation."""
        struct = IRTypeDefinition(
            name="User",
            fields=[
                IRProperty(name="id", prop_type=IRType(name="string")),
                IRProperty(name="name", prop_type=IRType(name="string")),
                IRProperty(name="age", prop_type=IRType(name="int")),
            ]
        )

        module = IRModule(name="test", version="1.0.0", types=[struct])
        code = generate_rust(module)

        assert "#[derive(Debug, Clone)]" in code
        assert "pub struct User {" in code
        assert "pub id: String," in code
        assert "pub name: String," in code
        assert "pub age: i32," in code

    def test_struct_with_optional_fields(self):
        """Test struct with optional fields."""
        struct = IRTypeDefinition(
            name="Person",
            fields=[
                IRProperty(name="name", prop_type=IRType(name="string")),
                IRProperty(
                    name="email",
                    prop_type=IRType(name="string", is_optional=True)
                ),
            ]
        )

        module = IRModule(name="test", version="1.0.0", types=[struct])
        code = generate_rust(module)

        assert "pub name: String," in code
        assert "pub email: Option<String>," in code

    def test_nested_struct_types(self):
        """Test struct with nested collection types."""
        struct = IRTypeDefinition(
            name="Library",
            fields=[
                IRProperty(
                    name="books",
                    prop_type=IRType(
                        name="array",
                        generic_args=[IRType(name="string")]
                    )
                ),
                IRProperty(
                    name="metadata",
                    prop_type=IRType(
                        name="map",
                        generic_args=[
                            IRType(name="string"),
                            IRType(name="string")
                        ]
                    )
                ),
            ]
        )

        module = IRModule(name="test", version="1.0.0", types=[struct])
        code = generate_rust(module)

        assert "pub books: Vec<String>," in code
        assert "pub metadata: HashMap<String, String>," in code


class TestEnumGeneration:
    """Test enum generation."""

    def test_simple_enum(self):
        """Test simple enum without associated data."""
        enum = IREnum(
            name="Status",
            variants=[
                IREnumVariant(name="Pending"),
                IREnumVariant(name="Completed"),
                IREnumVariant(name="Failed"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        assert "#[derive(Debug, Clone, PartialEq)]" in code
        assert "pub enum Status {" in code
        assert "Pending," in code
        assert "Completed," in code
        assert "Failed," in code

    def test_enum_with_associated_types(self):
        """Test enum with associated data."""
        enum = IREnum(
            name="Message",
            variants=[
                IREnumVariant(name="Text", associated_types=[IRType(name="string")]),
                IREnumVariant(
                    name="Image",
                    associated_types=[
                        IRType(name="string"),
                        IRType(name="int")
                    ]
                ),
                IREnumVariant(name="Disconnect"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        assert "Text(String)," in code
        assert "Image(String, i32)," in code
        assert "Disconnect," in code


class TestControlFlow:
    """Test control flow statements."""

    def test_if_statement(self):
        """Test if statement generation."""
        func = IRFunction(
            name="check_value",
            params=[IRParameter(name="x", param_type=IRType(name="int"))],
            return_type=IRType(name="string"),
            body=[
                IRIf(
                    condition=IRBinaryOp(
                        op=BinaryOperator.GREATER_THAN,
                        left=IRIdentifier(name="x"),
                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                    ),
                    then_body=[
                        IRReturn(
                            value=IRLiteral(value="positive", literal_type=LiteralType.STRING)
                        )
                    ],
                    else_body=[
                        IRReturn(
                            value=IRLiteral(value="negative", literal_type=LiteralType.STRING)
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "if (x > 0) {" in code
        assert "} else {" in code

    def test_for_loop(self):
        """Test for loop generation."""
        func = IRFunction(
            name="sum_items",
            params=[
                IRParameter(
                    name="items",
                    param_type=IRType(
                        name="array",
                        generic_args=[IRType(name="int")]
                    )
                )
            ],
            return_type=IRType(name="int"),
            body=[
                IRFor(
                    iterator="item",
                    iterable=IRIdentifier(name="items"),
                    body=[
                        IRCall(
                            function=IRIdentifier(name="println"),
                            args=[IRIdentifier(name="item")]
                        )
                    ]
                ),
                IRReturn(value=IRLiteral(value=0, literal_type=LiteralType.INTEGER))
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "for item in items {" in code

    def test_while_loop(self):
        """Test while loop generation."""
        func = IRFunction(
            name="countdown",
            params=[IRParameter(name="n", param_type=IRType(name="int"))],
            return_type=IRType(name="null"),
            body=[
                IRWhile(
                    condition=IRBinaryOp(
                        op=BinaryOperator.GREATER_THAN,
                        left=IRIdentifier(name="n"),
                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                    ),
                    body=[
                        IRAssignment(
                            target="n",
                            value=IRBinaryOp(
                                op=BinaryOperator.SUBTRACT,
                                left=IRIdentifier(name="n"),
                                right=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
                            ),
                            is_declaration=False
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "while (n > 0) {" in code


class TestExpressions:
    """Test expression generation."""

    def test_literals(self):
        """Test literal value generation."""
        func = IRFunction(
            name="literals",
            params=[],
            return_type=IRType(name="string"),
            body=[
                IRAssignment(
                    target="s",
                    value=IRLiteral(value="hello", literal_type=LiteralType.STRING),
                    is_declaration=True
                ),
                IRAssignment(
                    target="i",
                    value=IRLiteral(value=42, literal_type=LiteralType.INTEGER),
                    is_declaration=True
                ),
                IRAssignment(
                    target="f",
                    value=IRLiteral(value=3.14, literal_type=LiteralType.FLOAT),
                    is_declaration=True
                ),
                IRAssignment(
                    target="b",
                    value=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                    is_declaration=True
                ),
                IRReturn(value=IRIdentifier(name="s"))
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert 'let s = "hello";' in code
        assert 'let i = 42;' in code
        assert 'let f = 3.14;' in code
        assert 'let b = true;' in code

    def test_binary_operations(self):
        """Test binary operations."""
        func = IRFunction(
            name="math_ops",
            params=[
                IRParameter(name="a", param_type=IRType(name="int")),
                IRParameter(name="b", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="int"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.ADD,
                        left=IRBinaryOp(
                            op=BinaryOperator.MULTIPLY,
                            left=IRIdentifier(name="a"),
                            right=IRLiteral(value=2, literal_type=LiteralType.INTEGER)
                        ),
                        right=IRIdentifier(name="b")
                    )
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "a * 2" in code or "(a * 2)" in code
        assert "+" in code

    def test_array_literal(self):
        """Test array literal generation."""
        func = IRFunction(
            name="create_array",
            params=[],
            return_type=IRType(
                name="array",
                generic_args=[IRType(name="int")]
            ),
            body=[
                IRReturn(
                    value=IRArray(
                        elements=[
                            IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                            IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                            IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                        ]
                    )
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "vec![1, 2, 3]" in code

    def test_function_call(self):
        """Test function call generation."""
        func = IRFunction(
            name="caller",
            params=[],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRCall(
                        function=IRIdentifier(name="helper"),
                        args=[
                            IRLiteral(value="test", literal_type=LiteralType.STRING)
                        ]
                    )
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert 'helper("test")' in code


class TestClassAndImpl:
    """Test class and impl block generation."""

    def test_impl_block_with_methods(self):
        """Test impl block with methods."""
        cls = IRClass(
            name="Calculator",
            methods=[
                IRFunction(
                    name="add",
                    params=[
                        IRParameter(name="a", param_type=IRType(name="int")),
                        IRParameter(name="b", param_type=IRType(name="int")),
                    ],
                    return_type=IRType(name="int"),
                    body=[
                        IRReturn(
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRIdentifier(name="a"),
                                right=IRIdentifier(name="b")
                            )
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        assert "impl Calculator {" in code
        assert "pub fn add(a: i32, b: i32) -> i32 {" in code

    def test_constructor_generation(self):
        """Test constructor as 'new' method."""
        cls = IRClass(
            name="User",
            constructor=IRFunction(
                name="new",
                params=[
                    IRParameter(name="id", param_type=IRType(name="string")),
                    IRParameter(name="name", param_type=IRType(name="string")),
                ],
                return_type=IRType(name="User"),
                body=[]
            ),
            methods=[]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        assert "impl User {" in code
        assert "pub fn new(id: &str, name: &str) -> Self {" in code

    def test_trait_generation(self):
        """Test trait generation."""
        trait = IRClass(
            name="Drawable",
            methods=[
                IRFunction(
                    name="draw",
                    params=[],
                    return_type=IRType(name="null"),
                    body=[]
                )
            ]
        )
        trait.metadata['rust_trait'] = True

        module = IRModule(name="test", version="1.0.0", classes=[trait])
        code = generate_rust(module)

        assert "pub trait Drawable {" in code
        assert "fn draw() -> ();" in code


class TestErrorHandling:
    """Test error handling patterns."""

    def test_throw_statement(self):
        """Test throw as return Err."""
        func = IRFunction(
            name="validate",
            params=[IRParameter(name="value", param_type=IRType(name="int"))],
            return_type=IRType(name="null"),
            throws=["ValidationError"],
            body=[
                IRIf(
                    condition=IRBinaryOp(
                        op=BinaryOperator.LESS_THAN,
                        left=IRIdentifier(name="value"),
                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                    ),
                    then_body=[
                        IRThrow(
                            exception=IRCall(
                                function=IRIdentifier(name="ValidationError"),
                                args=[
                                    IRLiteral(
                                        value="Invalid value",
                                        literal_type=LiteralType.STRING
                                    )
                                ]
                            )
                        )
                    ],
                    else_body=[]
                ),
                IRReturn(value=None)
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "Result<(), ValidationError>" in code
        assert "return Err" in code

    def test_try_catch(self):
        """Test try-catch conversion."""
        func = IRFunction(
            name="safe_operation",
            params=[],
            return_type=IRType(name="string"),
            body=[
                IRTry(
                    try_body=[
                        IRCall(
                            function=IRIdentifier(name="risky_operation"),
                            args=[]
                        )
                    ],
                    catch_blocks=[
                        IRCatch(
                            exception_type="Error",
                            exception_var="e",
                            body=[
                                IRReturn(
                                    value=IRLiteral(
                                        value="fallback",
                                        literal_type=LiteralType.STRING
                                    )
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should generate comments about try-catch
        assert "// try-catch" in code or "risky_operation" in code


class TestRoundTrip:
    """Test round-trip conversion: Rust → IR → Rust."""

    def test_simple_function_roundtrip(self):
        """Test round-trip for simple function."""
        original_code = '''
pub fn greet(name: &str) -> String {
    return "Hello".to_string();
}
'''

        # Parse to IR
        parser = RustParserV2()
        ir_module = parse_rust_code(original_code, "test")

        # Generate back to Rust
        generator = RustGeneratorV2()
        generated_code = generator.generate(ir_module)

        # Should contain function signature
        assert "fn greet" in generated_code
        assert "-> String" in generated_code

    def test_struct_roundtrip(self):
        """Test round-trip for struct."""
        original_code = '''
pub struct User {
    pub id: String,
    pub name: String,
    pub age: i32,
}
'''

        parser = RustParserV2()
        ir_module = parse_rust_code(original_code, "test")

        generator = RustGeneratorV2()
        generated_code = generator.generate(ir_module)

        assert "struct User" in generated_code
        assert "id: String" in generated_code
        assert "name: String" in generated_code
        assert "age: i32" in generated_code

    def test_enum_roundtrip(self):
        """Test round-trip for enum."""
        original_code = '''
pub enum Status {
    Pending,
    Completed,
    Failed,
}
'''

        parser = RustParserV2()
        ir_module = parse_rust_code(original_code, "test")

        generator = RustGeneratorV2()
        generated_code = generator.generate(ir_module)

        assert "enum Status" in generated_code
        assert "Pending" in generated_code
        assert "Completed" in generated_code
        assert "Failed" in generated_code

    def test_semantic_preservation(self):
        """Test that semantics are preserved in round-trip."""
        original_code = '''
pub fn add(a: i32, b: i32) -> i32 {
    return a + b;
}
'''

        parser = RustParserV2()
        ir_module = parse_rust_code(original_code, "test")

        # Check IR has correct structure
        assert len(ir_module.functions) == 1
        func = ir_module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2

        # Generate back
        generator = RustGeneratorV2()
        generated_code = generator.generate(ir_module)

        # Should preserve semantics
        assert "fn add" in generated_code
        assert "a: i32" in generated_code
        assert "b: i32" in generated_code
        assert "i32" in generated_code  # Return type


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_function_body(self):
        """Test function with no body."""
        func = IRFunction(
            name="empty",
            params=[],
            return_type=IRType(name="null"),
            body=[]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "fn empty" in code
        assert "todo!()" in code

    def test_nested_types(self):
        """Test deeply nested types."""
        func = IRFunction(
            name="complex_type",
            params=[],
            return_type=IRType(
                name="array",
                generic_args=[
                    IRType(
                        name="map",
                        generic_args=[
                            IRType(name="string"),
                            IRType(
                                name="array",
                                generic_args=[IRType(name="int")]
                            )
                        ]
                    )
                ]
            ),
            body=[
                IRReturn(
                    value=IRArray(elements=[])
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should handle nested types
        assert "Vec<HashMap<String, Vec<i32>>>" in code

    def test_snake_case_conversion(self):
        """Test camelCase to snake_case conversion."""
        func = IRFunction(
            name="getUserById",
            params=[IRParameter(name="userId", param_type=IRType(name="string"))],
            return_type=IRType(name="string"),
            body=[IRReturn(value=IRIdentifier(name="userId"))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "get_user_by_id" in code
        assert "user_id" in code


class TestCodeQuality:
    """Test generated code quality."""

    def test_derives_on_structs(self):
        """Test that structs have proper derives."""
        struct = IRTypeDefinition(
            name="Point",
            fields=[
                IRProperty(name="x", prop_type=IRType(name="int")),
                IRProperty(name="y", prop_type=IRType(name="int")),
            ]
        )

        module = IRModule(name="test", version="1.0.0", types=[struct])
        code = generate_rust(module)

        assert "#[derive(Debug, Clone)]" in code

    def test_derives_on_enums(self):
        """Test that enums have proper derives."""
        enum = IREnum(
            name="Color",
            variants=[
                IREnumVariant(name="Red"),
                IREnumVariant(name="Green"),
                IREnumVariant(name="Blue"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        assert "#[derive(Debug, Clone, PartialEq)]" in code

    def test_proper_indentation(self):
        """Test that generated code uses 4-space indentation."""
        func = IRFunction(
            name="test",
            params=[],
            return_type=IRType(name="int"),
            body=[
                IRIf(
                    condition=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                    then_body=[
                        IRReturn(
                            value=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
                        )
                    ],
                    else_body=[
                        IRReturn(
                            value=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Check for 4-space indentation
        lines = code.split('\n')
        for line in lines:
            if line.startswith('    '):
                # Should be multiples of 4 spaces
                leading_spaces = len(line) - len(line.lstrip(' '))
                assert leading_spaces % 4 == 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
