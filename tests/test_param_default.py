from language.python_parser_v2 import PythonParserV2

python_code = '''
def animate(frames=99999):
    return frames
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

func = ir.functions[0]
print(f"Function: {func.name}")
for param in func.params:
    print(f"  Param: {param.name}")
    print(f"    Type: {param.param_type}")
    print(f"    Default: {param.default_value}")
