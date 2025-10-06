#!/usr/bin/env python3
"""Trace with debug output."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Temporarily patch the method to add debug
original_generate_fstring = GoGeneratorV2._generate_fstring

def debug_generate_fstring(self, expr):
    print(f"\n[DEBUG] _generate_fstring called")
    print(f"[DEBUG] expr.parts: {expr.parts}")

    format_parts = []
    args = []

    for part in expr.parts:
        if isinstance(part, str):
            print(f"[DEBUG] Processing string part: {repr(part)}")
            escaped = part
            escaped = escaped.replace("\\", "\\\\")
            escaped = escaped.replace('"', '\\"')
            escaped = escaped.replace("\n", "\\n")
            escaped = escaped.replace("\t", "\\t")
            escaped = escaped.replace("\r", "\\r")
            print(f"[DEBUG] After escaping: {repr(escaped)}")
            format_parts.append(escaped)

    format_str = "".join(format_parts)
    print(f"[DEBUG] format_str: {repr(format_str)}")

    result = '"' + format_str + '"'
    print(f"[DEBUG] Final result: {repr(result)}")
    print(f"[DEBUG] Result value: {result}")

    return result

GoGeneratorV2._generate_fstring = debug_generate_fstring

python_code = '''
def test():
    msg = f"\\nHello\\n"
    return msg
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\n" + "=" * 80)
print("Generated Go:")
print("=" * 80)
print(go_code)
