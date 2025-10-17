#!/usr/bin/env python3
"""
Test for Bug #11: Floor Division Operator vs Comment Ambiguity

Bug #11 was caused by the lexer treating `//` (floor division operator) as a C-style
comment start, causing tokens to be skipped and leading to parser confusion.

The fix uses context-aware tokenization: `//` is treated as FLOOR_DIV operator when it
appears after expression tokens (identifiers, numbers, closing parens/brackets), and
as a comment otherwise.
"""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

import pytest
from dsl.al_parser import Lexer, Parser, TokenType


class TestFloorDivisionOperator:
    """Test floor division operator tokenization and parsing."""

    def test_floor_division_in_simple_expression(self):
        """Test // as operator in simple arithmetic."""
        code = """
function test() -> int {
    let x = 10 // 3;
    return x;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Find the // token
        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1, "Should have exactly one FLOOR_DIV token"

        # Parse should succeed
        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_after_paren(self):
        """Test // as operator after closing parenthesis."""
        code = """
function test() -> int {
    let a = 10;
    let b = 5;
    let result = (a * b) // 100;
    return result;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_vs_comment_after_semicolon(self):
        """Test that // after semicolon is treated as comment."""
        code = """class Foo {
    name: string;  // This is a comment
}"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Should NOT have FLOOR_DIV token (it's a comment)
        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 0, "// after semicolon should be comment, not operator"

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_in_nested_if(self):
        """Test floor division in nested if blocks (Bug #11 reproduction)."""
        code = """
function test() -> int {
    if (100 < 200) {
        let x = (10 * 5) // 2;

        if (x > 10) {
            return x;
        }
    }
    return 0;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_multiple_occurrences(self):
        """Test multiple floor division operators in same function."""
        code = """
function calculate() -> int {
    let a = 100 // 10;
    let b = 50 // 5;
    let c = (a + b) // 3;
    return c;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 3, "Should have 3 FLOOR_DIV tokens"

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_comment_at_line_start(self):
        """Test // at line start is always a comment."""
        code = """
function test() -> int {
    // This is a comment
    let x = 10;
    return x;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Should NOT have FLOOR_DIV token
        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 0

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_after_identifier(self):
        """Test // after identifier is treated as operator."""
        code = """
function test() -> int {
    let count = 100;
    let divisor = 7;
    let result = count // divisor;
    return result;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_floor_division_in_complex_expression(self):
        """Test floor division in complex nested expression."""
        code = """
function test() -> int {
    let a = 5;
    let b = 4;
    let c = 3;
    let d = 2;
    let e = 1;
    let result = ((a * b) + c) // (d - e);
    return result;
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1

        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None

    def test_bug11_exact_reproduction(self):
        """Test exact Bug #11 scenario from database_query_optimizer.al."""
        code = """
class QueryPlan {
    plan_type: string;

    constructor(plan_type: string, name: string) {
        self.plan_type = plan_type;
    }
}

function optimize_query() -> QueryPlan {
    let row_count = 1000;
    let selectivity = 50;

    if (true) {
        let estimated_rows = (row_count * selectivity) // 100;

        if (estimated_rows > 100) {
            return QueryPlan("index_scan", "idx_test");
        } else {
            return QueryPlan("seq_scan", "none");
        }
    }

    return QueryPlan("default", "none");
}
"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # Should have exactly 1 FLOOR_DIV token
        floor_div_tokens = [t for t in tokens if t.type == TokenType.FLOOR_DIV]
        assert len(floor_div_tokens) == 1

        # Parser should succeed (Bug #11 would fail here with "Expected identifier or string as map key")
        parser = Parser(tokens)
        ir = parser.parse()
        assert ir is not None
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "optimize_query"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
