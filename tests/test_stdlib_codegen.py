"""
Test that stdlib files successfully generate Python code.

This test verifies the code generation for stdlib types:
1. Create IR for stdlib types (Option<T>, Result<T,E>, etc.)
2. Generate Python code
3. Verify Python code is syntactically valid
"""

import ast
from pathlib import Path

import pytest

from dsl.pw_parser import parse_pw
from language.python_generator_v2 import PythonGeneratorV2


def test_parse_and_generate_core_option():
    """Test that Option<T> from stdlib/core.al generates valid Python."""
    generator = PythonGeneratorV2()

    # Parse stdlib/core.al (or at least the Option<T> enum)
    code = """
enum Option<T>:
    - Some(T)
    - None
"""

    try:
        module = parse_pw(code)
        print("\n=== Parsed IR ===")
        print(f"Enums: {len(module.enums)}")
        if module.enums:
            enum = module.enums[0]
            print(f"  Name: {enum.name}")
            print(f"  Generic params: {enum.generic_params}")
            print(f"  Variants: {[v.name for v in enum.variants]}")

        # Generate Python
        python_code = generator.generate(module)
        print("\n=== Generated Python ===")
        print(python_code)
        print("=" * 60)

        # Verify syntactically valid
        ast.parse(python_code)

        # Verify key components
        assert "T = TypeVar('T')" in python_code
        assert "class Some(Generic[T]):" in python_code
        assert "class None_:" in python_code
        assert "Option = Union[Some[T], None_]" in python_code

    except Exception as e:
        print(f"\n=== Error ===")
        print(f"Failed to parse or generate: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_parse_and_generate_core_result():
    """Test that Result<T, E> from stdlib/core.al generates valid Python."""
    generator = PythonGeneratorV2()

    code = """
enum Result<T, E>:
    - Ok(T)
    - Err(E)
"""

    try:
        module = parse_pw(code)
        print("\n=== Parsed IR ===")
        print(f"Enums: {len(module.enums)}")
        if module.enums:
            enum = module.enums[0]
            print(f"  Name: {enum.name}")
            print(f"  Generic params: {enum.generic_params}")
            print(f"  Variants: {[v.name for v in enum.variants]}")

        # Generate Python
        python_code = generator.generate(module)
        print("\n=== Generated Python ===")
        print(python_code)
        print("=" * 60)

        # Verify syntactically valid
        ast.parse(python_code)

        # Verify key components
        assert "T = TypeVar('T')" in python_code
        assert "E = TypeVar('E')" in python_code
        assert "class Ok(Generic[T, E]):" in python_code
        assert "class Err(Generic[T, E]):" in python_code
        assert "Result = Union[Ok[T, E], Err[T, E]]" in python_code

    except Exception as e:
        print(f"\n=== Error ===")
        print(f"Failed to parse or generate: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_parse_and_generate_generic_function():
    """Test that generic functions from stdlib generate valid Python."""
    generator = PythonGeneratorV2()

    code = """
function option_some<T>(value: T) -> Option<T>:
    return Some(value)
"""

    try:
        module = parse_pw(code)
        print("\n=== Parsed IR ===")
        print(f"Functions: {len(module.functions)}")
        if module.functions:
            func = module.functions[0]
            print(f"  Name: {func.name}")
            print(f"  Generic params: {func.generic_params}")
            print(f"  Params: {[(p.name, p.param_type.name) for p in func.params]}")
            print(f"  Return type: {func.return_type}")

        # Generate Python
        python_code = generator.generate(module)
        print("\n=== Generated Python ===")
        print(python_code)
        print("=" * 60)

        # Verify syntactically valid
        ast.parse(python_code)

        # Verify key components
        assert "T = TypeVar('T')" in python_code
        assert "def option_some(value: T) -> Option[T]:" in python_code

    except Exception as e:
        print(f"\n=== Error ===")
        print(f"Failed to parse or generate: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_full_stdlib_core_file():
    """Test parsing and generating the full stdlib/core.al file."""
    generator = PythonGeneratorV2()

    stdlib_path = Path(__file__).parent.parent / "stdlib" / "core.al"

    if not stdlib_path.exists():
        pytest.skip(f"stdlib/core.al not found at {stdlib_path}")

    try:
        with open(stdlib_path) as f:
            code = f.read()

        print(f"\n=== Parsing {stdlib_path} ===")
        print(f"File size: {len(code)} characters")

        module = parse_pw(code)
        print(f"Parsed successfully!")
        print(f"  Enums: {len(module.enums)}")
        print(f"  Functions: {len(module.functions)}")

        # Generate Python
        python_code = generator.generate(module)
        print(f"\n=== Generated Python ===")
        print(f"Generated {len(python_code)} characters of Python code")
        print("\nFirst 500 characters:")
        print(python_code[:500])
        print("...")
        print("\nLast 500 characters:")
        print(python_code[-500:])
        print("=" * 60)

        # Verify syntactically valid
        ast.parse(python_code)
        print("\n✓ Generated code is syntactically valid Python!")

        # Save to file for inspection
        output_path = Path(__file__).parent.parent / "generated_stdlib_core.py"
        with open(output_path, "w") as f:
            f.write(python_code)
        print(f"\n✓ Saved generated code to {output_path}")

    except Exception as e:
        print(f"\n=== Error ===")
        print(f"Failed to parse or generate: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
