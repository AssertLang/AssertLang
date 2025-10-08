#!/usr/bin/env python3
"""Debug IR structure to see how append is represented."""

from language.python_parser_v2 import PythonParserV2

python_code = '''
def test():
    output = []
    output.append("item")
    return output
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Print IR structure
func = ir.functions[0]
print(f"Function: {func.name}")
print(f"Body statements: {len(func.body)}")

for i, stmt in enumerate(func.body):
    print(f"\nStatement {i}: {type(stmt).__name__}")
    print(f"  {stmt}")

    # Check if it's assignment with IRCall
    if hasattr(stmt, 'value'):
        print(f"  Value: {type(stmt.value).__name__}")
        if hasattr(stmt.value, 'function'):
            print(f"  Function: {type(stmt.value.function).__name__}")
            print(f"  Function obj: {stmt.value.function}")
