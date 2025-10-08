from language.python_parser_v2 import PythonParserV2
from dsl.type_inference import TypeInferenceEngine

python_code = '''
COLORS = ["red", "blue", "green"]
MAX_SIZE = 100

def test():
    x = COLORS[0]
    return x
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

engine = TypeInferenceEngine()
engine.infer_module_types(ir)

print("Type environment:")
for var_name, var_type in engine.type_env.items():
    print(f"  {var_name}: {var_type.name}", end="")
    if var_type.generic_args:
        print(f"<{', '.join(t.name for t in var_type.generic_args)}>", end="")
    print()
