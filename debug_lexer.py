#!/usr/bin/env python3
"""Debug lexer to see what tokens are produced."""

from dsl.pw_parser import Lexer

code = "import x"

print(f"Code: {code!r}")
print("\nTokenizing...")

lexer = Lexer(code)
tokens = lexer.tokenize()

print("\nTokens:")
for i, tok in enumerate(tokens):
    print(f"  {i}: {tok}")
