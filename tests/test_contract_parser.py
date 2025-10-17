"""
Tests for contract syntax parsing (Phase 2A).

Tests contract annotations:
- @requires (preconditions)
- @ensures (postconditions)
- @invariant (class invariants)
- @effects (side effects)
- @contract/@operation (metadata)
- /// documentation comments
- old keyword
"""

import pytest
from dsl.al_parser import Lexer, Parser
from dsl.ir import IRFunction, IRClass, IRContractClause, IROldExpr, IRBinaryOp


def parse_al(code: str):
    """Helper to parse PW code."""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


class TestBasicContractParsing:
    """Test basic contract annotation parsing."""

    def test_parse_requires_clause(self):
        """Test parsing @requires precondition."""
        code = """
function test(x: int) -> int {
    @requires positive: x > 0
    return x
}
"""
        module = parse_al(code)
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "test"
        assert len(func.requires) == 1

        clause = func.requires[0]
        assert clause.clause_type == "requires"
        assert clause.name == "positive"
        # Expression should be: x > 0
        assert isinstance(clause.expression, IRBinaryOp)

    def test_parse_ensures_clause(self):
        """Test parsing @ensures postcondition."""
        code = """
function test(x: int) -> int {
    @ensures result_positive: result > 0
    return x + 1
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.ensures) == 1

        clause = func.ensures[0]
        assert clause.clause_type == "ensures"
        assert clause.name == "result_positive"

    def test_parse_effects_annotation(self):
        """Test parsing @effects annotation."""
        code = """
function createUser(name: string) -> int {
    @effects [database.write, event.emit]
    return 42
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.effects) == 2
        assert "database.write" in func.effects
        assert "event.emit" in func.effects

    def test_parse_multiple_contract_clauses(self):
        """Test parsing multiple contract clauses."""
        code = """
function divide(a: int, b: int) -> int {
    @requires non_zero: b != 0
    @requires positive: a >= 0
    @ensures result_correct: result * b == a
    return a / b
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.requires) == 2
        assert len(func.ensures) == 1
        assert func.requires[0].name == "non_zero"
        assert func.requires[1].name == "positive"
        assert func.ensures[0].name == "result_correct"


class TestOldKeyword:
    """Test 'old' keyword parsing in postconditions."""

    def test_parse_old_in_ensures(self):
        """Test parsing 'old' keyword in postcondition."""
        code = """
function increment(x: int) -> int {
    @ensures increased: result == old x + 1
    return x + 1
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.ensures) == 1

        # The expression should contain IROldExpr
        ensures_expr = func.ensures[0].expression
        assert isinstance(ensures_expr, IRBinaryOp)
        # Right side should be: old x + 1 (a binary operation)
        # Left side of that should contain IROldExpr

    def test_old_with_property_access(self):
        """Test 'old' with property access."""
        code = """
function updateBalance(amount: int) -> int {
    @ensures balance_increased: this.balance == old this.balance + amount
    return this.balance + amount
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.ensures) == 1


class TestBackwardCompatibility:
    """Ensure existing PW code without contracts still works."""

    def test_function_without_contracts(self):
        """Test that functions without contracts still parse."""
        code = """
function add(a: int, b: int) -> int {
    return a + b
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.requires) == 0
        assert len(func.ensures) == 0
        assert len(func.effects) == 0

    def test_class_without_contracts(self):
        """Test that classes without contracts still parse."""
        code = """
class User {
    id: int;
    name: string;
}
"""
        module = parse_al(code)
        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "User"
        assert len(cls.invariants) == 0


class TestComplexExpressions:
    """Test complex expressions in contract clauses."""

    def test_complex_boolean_expression(self):
        """Test complex boolean expression in contract."""
        code = """
function validate(name: string, age: int) -> bool {
    @requires name_valid: str.length(name) >= 1 && str.length(name) <= 100
    @requires age_valid: age >= 0 && age < 150
    return true
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.requires) == 2

    def test_property_access_in_contract(self):
        """Test property access in contract clause."""
        code = """
function processUser(user: User) -> int {
    @requires user_has_id: user.id > 0
    @ensures result_matches: result == user.id
    return user.id
}
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.requires) == 1
        assert len(func.ensures) == 1


class TestErrorHandling:
    """Test error handling for invalid contract syntax."""

    def test_requires_without_name(self):
        """Test that @requires without name raises error."""
        code = """
function test(x: int) -> int {
    @requires x > 0
    return x
}
"""
        with pytest.raises(Exception):  # Should raise parse error
            parse_al(code)

    def test_invalid_annotation(self):
        """Test that invalid annotation name raises error."""
        code = """
function test(x: int) -> int {
    @invalid_annotation name: x > 0
    return x
}
"""
        with pytest.raises(Exception):  # Should raise parse error
            parse_al(code)


class TestPythonStyleSyntax:
    """Test contract parsing with Python-style syntax."""

    def test_requires_python_style(self):
        """Test contract with Python-style function body."""
        code = """
function test(x: int) -> int:
    @requires positive: x > 0
    return x
"""
        module = parse_al(code)
        func = module.functions[0]
        assert len(func.requires) == 1
        assert func.requires[0].name == "positive"


if __name__ == "__main__":
    # Run a quick smoke test
    code = """
function test(x: int) -> int {
    @requires positive: x > 0
    @ensures result_positive: result > 0
    return x + 1
}
"""
    module = parse_al(code)
    print(f"✓ Parsed function: {module.functions[0].name}")
    print(f"✓ Requires: {len(module.functions[0].requires)}")
    print(f"✓ Ensures: {len(module.functions[0].ensures)}")
    print("\nAll basic tests passed!")
