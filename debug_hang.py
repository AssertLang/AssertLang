#!/usr/bin/env python3
"""Debug parser hang by tracing parser state."""

import signal
import sys
from dsl.pw_parser import Lexer, Parser

def timeout_handler(signum, frame):
    print("\n⏱️  TIMEOUT - Parser hung!")
    print(f"Current parser position: {parser.pos}/{len(parser.tokens)}")
    if parser.pos < len(parser.tokens):
        print(f"Current token: {parser.current()}")
        print(f"Next 5 tokens:")
        for i in range(5):
            if parser.pos + i < len(parser.tokens):
                print(f"  [{i}] {parser.tokens[parser.pos + i]}")
    sys.exit(1)

code = open('stdlib/types.pw').read()
print(f'Lexing {len(code)} chars...')
lexer = Lexer(code)
tokens = lexer.tokenize()
print(f'Lexed {len(tokens)} tokens')

print('Parsing (3 second timeout)...')
parser = Parser(tokens)

# Set 3 second timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(3)

try:
    ir = parser.parse()
    signal.alarm(0)  # Cancel alarm
    print('✅ Parsed successfully')
    print(f'Classes: {len(ir.classes)}')
    print(f'Functions: {len(ir.functions)}')
except Exception as e:
    signal.alarm(0)  # Cancel alarm
    print(f'❌ Parse error: {e}')
    print(f'Position: {parser.pos}/{len(parser.tokens)}')
    if parser.pos < len(parser.tokens):
        print(f'Current token: {parser.current()}')
