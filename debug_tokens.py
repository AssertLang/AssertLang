from dsl.pw_parser import Lexer

code = """class Test:
    x: int"""

print(f"Code:\n{code}\n")
print("Tokens:")

lexer = Lexer(code)
tokens = lexer.tokenize()

for i, tok in enumerate(tokens):
    print(f"  {i:3}: {tok}")
