"""
Test Bug #14: NOT operator `!` support

This test verifies that the PW parser correctly handles the `!` operator
for boolean negation and that all code generators emit correct NOT syntax.

Bug Report: Bugs/v2.1.0b8/PW_BUG_REPORT_BATCH_8.md
"""

import pytest
from dsl.al_parser import parse_al
from dsl.ir import UnaryOperator, IRUnaryOp
from language.python_generator_v2 import PythonGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


class TestNotOperatorParsing:
    """Test that the parser correctly handles `!` operator."""

    def test_simple_not(self):
        """Test simple NOT: !flag"""
        code = """
function test() -> bool {
    let flag = true;
    return !flag;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]
        return_stmt = func.body[1]

        # Check that return value is a UnaryOp with NOT operator
        assert isinstance(return_stmt.value, IRUnaryOp)
        assert return_stmt.value.op == UnaryOperator.NOT

    def test_not_with_function_call(self):
        """Test NOT with function call: !check()"""
        code = """
function check() -> bool {
    return true;
}

function test() -> bool {
    return !check();
}
"""
        ir = parse_al(code)
        func = ir.functions[1]
        return_stmt = func.body[0]

        # Check that return value is a UnaryOp with NOT operator
        assert isinstance(return_stmt.value, IRUnaryOp)
        assert return_stmt.value.op == UnaryOperator.NOT

    def test_not_with_expression(self):
        """Test NOT with expression: !(a == b)"""
        code = """
function test(a: int, b: int) -> bool {
    return !(a == b);
}
"""
        ir = parse_al(code)
        func = ir.functions[0]
        return_stmt = func.body[0]

        # Check that return value is a UnaryOp with NOT operator
        assert isinstance(return_stmt.value, IRUnaryOp)
        assert return_stmt.value.op == UnaryOperator.NOT

    def test_double_negation(self):
        """Test double negation: !!value"""
        code = """
function test(value: bool) -> bool {
    return !!value;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]
        return_stmt = func.body[0]

        # Check that return value is a UnaryOp with NOT operator
        assert isinstance(return_stmt.value, IRUnaryOp)
        assert return_stmt.value.op == UnaryOperator.NOT
        # Check that operand is also a UnaryOp with NOT
        assert isinstance(return_stmt.value.operand, IRUnaryOp)
        assert return_stmt.value.operand.op == UnaryOperator.NOT

    def test_not_in_if_condition(self):
        """Test NOT in if condition: if (!flag) { }"""
        code = """
function test(flag: bool) -> string {
    if (!flag) {
        return "not true";
    }
    return "true";
}
"""
        ir = parse_al(code)
        func = ir.functions[0]
        if_stmt = func.body[0]

        # Check that if condition is a UnaryOp with NOT operator
        assert isinstance(if_stmt.condition, IRUnaryOp)
        assert if_stmt.condition.op == UnaryOperator.NOT

    def test_not_with_property_access(self):
        """Test NOT with property access: !obj.is_valid"""
        code = """
function test() -> bool {
    let obj = {is_valid: false};
    return !obj.is_valid;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]
        return_stmt = func.body[1]

        # Check that return value is a UnaryOp with NOT operator
        assert isinstance(return_stmt.value, IRUnaryOp)
        assert return_stmt.value.op == UnaryOperator.NOT


class TestNotOperatorCodeGeneration:
    """Test that all code generators emit correct NOT syntax."""

    def test_python_generator(self):
        """Python should emit: not value"""
        code = """
function test(flag: bool) -> bool {
    return !flag;
}
"""
        ir = parse_al(code)
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Python uses 'not' keyword
        assert 'not flag' in python_code or 'not (flag)' in python_code

    def test_go_generator(self):
        """Go should emit: !value"""
        code = """
function test(flag: bool) -> bool {
    return !flag;
}
"""
        ir = parse_al(code)
        generator = GoGeneratorV2()
        go_code = generator.generate(ir)

        # Go uses ! operator
        assert '!flag' in go_code

    def test_rust_generator(self):
        """Rust should emit: !value"""
        code = """
function test(flag: bool) -> bool {
    return !flag;
}
"""
        ir = parse_al(code)
        generator = RustGeneratorV2()
        rust_code = generator.generate(ir)

        # Rust uses ! operator
        assert '!flag' in rust_code

    def test_nodejs_generator(self):
        """TypeScript/Node.js should emit: !value"""
        code = """
function test(flag: bool) -> bool {
    return !flag;
}
"""
        ir = parse_al(code)
        generator = NodeJSGeneratorV2()
        ts_code = generator.generate(ir)

        # TypeScript uses ! operator
        assert '!flag' in ts_code

    def test_dotnet_generator(self):
        """C# should emit: !value"""
        code = """
function test(flag: bool) -> bool {
    return !flag;
}
"""
        ir = parse_al(code)
        generator = DotNetGeneratorV2()
        csharp_code = generator.generate(ir)

        # C# uses ! operator
        assert '!flag' in csharp_code


class TestNotOperatorComplexScenarios:
    """Test NOT operator in complex real-world scenarios."""

    def test_validation_pattern(self):
        """Test validation pattern from Bug #14 report"""
        code = """
function validate() -> bool {
    let base_validation = {is_valid: true};
    if (!base_validation.is_valid) {
        return false;
    }
    return true;
}
"""
        ir = parse_al(code)

        # Should parse successfully
        assert len(ir.functions) == 1

        # Test all generators
        for Generator in [PythonGeneratorV2, GoGeneratorV2, RustGeneratorV2, NodeJSGeneratorV2, DotNetGeneratorV2]:
            generator = Generator()
            code = generator.generate(ir)
            # Should generate code without errors
            assert code is not None
            assert len(code) > 0

    def test_combined_logical_operations(self):
        """Test NOT combined with AND/OR"""
        code = """
function test(a: bool, b: bool) -> bool {
    return !a && b;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]

        # Should parse successfully and have correct structure
        assert len(func.body) == 1

    def test_nested_not_in_complex_expression(self):
        """Test nested NOT in complex boolean expression"""
        code = """
function test(a: bool, b: bool, c: bool) -> bool {
    return !(a && b) || !c;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]

        # Should parse successfully
        assert len(func.body) == 1

    def test_not_in_while_loop(self):
        """Test NOT in while loop condition"""
        code = """
function test() -> int {
    let done = false;
    let count = 0;
    while (!done) {
        count = count + 1;
        if (count > 5) {
            done = true;
        }
    }
    return count;
}
"""
        ir = parse_al(code)
        func = ir.functions[0]

        # Should parse successfully
        assert len(func.body) == 4  # let done, let count, while loop, return count

    def test_not_with_array_check(self):
        """Test NOT with array/collection checks"""
        code = """
function test(items: array<int>) -> bool {
    return !(items == null);
}
"""
        ir = parse_al(code)

        # Should parse successfully
        assert len(ir.functions) == 1


class TestNotOperatorRoundtrip:
    """Test roundtrip compilation to all languages."""

    @pytest.fixture
    def sample_code(self):
        """Sample PW code using NOT operator in various contexts."""
        return """
function check_flags(is_valid: bool, is_complete: bool) -> string {
    if (!is_valid) {
        return "invalid";
    }

    if (!is_complete) {
        return "incomplete";
    }

    let both_true = !(!is_valid && !is_complete);
    if (both_true) {
        return "success";
    }

    return "unknown";
}
"""

    def test_python_roundtrip(self, sample_code):
        """Test Python code generation"""
        ir = parse_al(sample_code)
        generator = PythonGeneratorV2()
        python_code = generator.generate(ir)

        # Verify Python code contains 'not' keyword
        assert python_code is not None
        assert 'not is_valid' in python_code or 'not (is_valid)' in python_code

    def test_go_roundtrip(self, sample_code):
        """Test Go code generation"""
        ir = parse_al(sample_code)
        generator = GoGeneratorV2()
        go_code = generator.generate(ir)

        # Verify Go code contains ! operator
        assert go_code is not None
        assert '!isValid' in go_code or '!is_valid' in go_code

    def test_rust_roundtrip(self, sample_code):
        """Test Rust code generation"""
        ir = parse_al(sample_code)
        generator = RustGeneratorV2()
        rust_code = generator.generate(ir)

        # Verify Rust code contains ! operator
        assert rust_code is not None
        assert '!is_valid' in rust_code

    def test_nodejs_roundtrip(self, sample_code):
        """Test Node.js/TypeScript code generation"""
        ir = parse_al(sample_code)
        generator = NodeJSGeneratorV2()
        ts_code = generator.generate(ir)

        # Verify TypeScript code contains ! operator
        assert ts_code is not None
        assert '!isValid' in ts_code or '!is_valid' in ts_code

    def test_dotnet_roundtrip(self, sample_code):
        """Test C# code generation"""
        ir = parse_al(sample_code)
        generator = DotNetGeneratorV2()
        csharp_code = generator.generate(ir)

        # Verify C# code contains ! operator
        assert csharp_code is not None
        assert '!isValid' in csharp_code or '!is_valid' in csharp_code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
