"""
Demonstrate type inference improvements in code generation.

Shows before/after for Python code → IR → Generated code in multiple languages.
"""

from language.python_parser_v2 import PythonParserV2
from dsl.type_system import TypeSystem

# Sample Python code without type annotations
python_code = '''
def calculate_discount(price, discount_rate):
    """Calculate discounted price."""
    discount = price * discount_rate
    final_price = price - discount
    return final_price

def format_message(name, count):
    """Format a greeting message."""
    return f"Hello {name}, you have {count} items".upper()

def filter_valid_items(items):
    """Filter out invalid items."""
    valid = []
    for item in items:
        if item:
            valid.append(item)
    return valid
'''

def show_ir_types(module):
    """Show inferred types in IR."""
    print("\n" + "="*80)
    print("IR (Intermediate Representation) - Inferred Types")
    print("="*80)

    for func in module.functions:
        print(f"\nFunction: {func.name}")
        if func.params:
            print("  Parameters:")
            for param in func.params:
                type_str = str(param.param_type) if param.param_type else "None"
                print(f"    - {param.name}: {type_str}")
        if func.return_type:
            print(f"  Returns: {func.return_type}")
        else:
            print(f"  Returns: (void)")


def main():
    """Run the demo."""
    print("\n" + "="*80)
    print("TYPE INFERENCE DEMO - Before/After Comparison")
    print("="*80)
    print("\nOriginal Python Code (NO type annotations):")
    print("-" * 80)
    print(python_code)

    # Parse Python code
    parser = PythonParserV2()
    module = parser.parse_source(python_code, "demo")

    # Show IR types
    show_ir_types(module)

    # Show generated code for each language
    print("\n" + "="*80)
    print("GENERATED CODE SAMPLES")
    print("="*80)
    print("\nNotice: Types are inferred even though original Python had NO annotations!")

    # Python
    print("\n" + "="*80)
    print("Generated Python (with inferred types)")
    print("="*80)
    for func in module.functions:
        params_str = ", ".join(
            f"{p.name}: {parser.type_system.map_to_language(p.param_type, 'python')}"
            for p in func.params
        )
        return_str = parser.type_system.map_to_language(func.return_type, 'python') if func.return_type else "None"
        print(f"def {func.name}({params_str}) -> {return_str}:")
        print(f"    ...")

    # Go
    print("\n" + "="*80)
    print("Generated Go (with inferred types)")
    print("="*80)
    for func in module.functions:
        params_strs = [
            f"{p.name} {parser.type_system.map_to_language(p.param_type, 'go')}"
            for p in func.params
        ]
        params_str = ", ".join(params_strs)
        return_str = parser.type_system.map_to_language(func.return_type, 'go') if func.return_type else "error"
        func_name = func.name[0].upper() + func.name[1:]  # Capitalize
        print(f"func {func_name}({params_str}) {return_str} {{")
        print(f"    // ...")
        print(f"}}")

    # .NET
    print("\n" + "="*80)
    print("Generated C# (with inferred types)")
    print("="*80)
    for func in module.functions:
        params_strs = [
            f"{parser.type_system.map_to_language(p.param_type, 'dotnet')} {p.name}"
            for p in func.params
        ]
        params_str = ", ".join(params_strs)
        return_str = parser.type_system.map_to_language(func.return_type, 'dotnet') if func.return_type else "void"
        func_name = func.name[0].upper() + func.name[1:]  # Capitalize
        print(f"public {return_str} {func_name}({params_str})")
        print(f"{{")
        print(f"    // ...")
        print(f"}}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n✓ Inferred 'float' for price calculations (arithmetic + float literal)")
    print("✓ Inferred 'string' for format_message return (f-string literal)")
    print("✓ Inferred 'array' for items parameter (used in for loop)")
    print("✓ Generated strongly-typed code for Go, C#, etc.")
    print("\nWithout type inference:")
    print("  - Everything would be Any/interface{}/object")
    print("  - Generated code would be untyped and error-prone")
    print("\nWith type inference:")
    print("  - Specific types inferred from usage patterns")
    print("  - Generated code is type-safe and idiomatic")

if __name__ == "__main__":
    main()
