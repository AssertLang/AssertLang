from language.python_parser_v2 import PythonParserV2

python_code = '''
COLORS = ["red", "blue", "green"]
MAX_SIZE = 100

def test():
    x = COLORS[0]
    return x
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

print("Module variables:")
for var in ir.module_vars:
    print(f"  {var.target}: {var.value}")
    print(f"    Type: {type(var.value).__name__}")
