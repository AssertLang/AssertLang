#!/usr/bin/env python3
"""Debug lexer with trace to find infinite loop."""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

from dsl.pw_parser import Lexer

code = "import x"
lexer = Lexer(code)

# Monkey-patch advance to add tracing
original_advance = lexer.advance
call_count = 0

def traced_advance():
    global call_count
    call_count += 1
    result = original_advance()
    if call_count % 10 == 0:
        print(f"Advance called {call_count} times, pos={lexer.pos}/{len(lexer.text)}, char={result!r}", flush=True)
    if call_count > 100:
        print(f"INFINITE LOOP DETECTED at pos={lexer.pos}, line={lexer.line}", flush=True)
        print(f"Recent tokens: {lexer.tokens[-5:]}", flush=True)
        sys.exit(1)
    return result

lexer.advance = traced_advance

print(f"Tokenizing: {code!r}")
try:
    tokens = lexer.tokenize()
    print(f"Success! Got {len(tokens)} tokens")
    for tok in tokens:
        print(f"  {tok}")
except Exception as e:
    print(f"Error: {e}")
