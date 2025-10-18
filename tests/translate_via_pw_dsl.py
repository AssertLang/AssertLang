#!/usr/bin/env python3
"""
CORRECT AssertLang Translation Pipeline using PW DSL as bridge.

This is the PROPER architecture:
1. Python → IR → PW DSL (text format)
2. PW DSL (text) → IR → Go

PW DSL is the universal intermediate language that:
- Agents can read/write (human-readable)
- Language-agnostic (no Python/Go bias)
- MCP servers exchange
- Enables universal translation
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2
from dsl.al_generator import PWGenerator
from dsl.al_parser import parse_al

def translate_python_to_go_via_pw(input_path: str, output_path: str, save_pw_dsl: bool = True):
    """
    Translate Python to Go using PW DSL as the bridge.

    Args:
        input_path: Path to input Python file
        output_path: Path to output Go file
        save_pw_dsl: If True, save intermediate PW DSL to file
    """
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  AssertLang Universal Translation: Python → PW DSL → Go     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print()

    # ========================================================================
    # PHASE 1: Python → PW DSL
    # ========================================================================
    print("📝 PHASE 1: Python → PW DSL")
    print("─" * 60)

    # Step 1.1: Parse Python to IR
    print("  Step 1.1: Parsing Python source → IR...")
    python_parser = PythonParserV2()
    ir_from_python = python_parser.parse_file(input_path)
    print(f"    ✓ Module: {ir_from_python.name}")
    print(f"    ✓ Functions: {len(ir_from_python.functions)}")
    print(f"    ✓ Classes: {len(ir_from_python.classes)}")
    print()

    # Step 1.2: Generate PW DSL from IR
    print("  Step 1.2: Generating PW DSL from IR...")
    pw_generator = PWGenerator()
    pw_dsl_text = pw_generator.generate(ir_from_python)
    print(f"    ✓ Generated {len(pw_dsl_text)} characters of PW DSL")
    print()

    # Step 1.3: Save PW DSL (optional, for inspection)
    if save_pw_dsl:
        pw_path = str(output_path).replace('.go', '.al')
        with open(pw_path, 'w') as f:
            f.write(pw_dsl_text)
        print(f"  Step 1.3: Saved PW DSL → {pw_path}")
        print()

    print("  ✅ Phase 1 Complete: Python → PW DSL")
    print()

    # ========================================================================
    # PHASE 2: PW DSL → Go
    # ========================================================================
    print("🔄 PHASE 2: PW DSL → Go")
    print("─" * 60)

    # Step 2.1: Parse PW DSL to IR
    print("  Step 2.1: Parsing PW DSL → IR...")
    ir_from_pw = parse_al(pw_dsl_text)
    print(f"    ✓ Module: {ir_from_pw.name}")
    print(f"    ✓ Functions: {len(ir_from_pw.functions)}")
    print(f"    ✓ Classes: {len(ir_from_pw.classes)}")
    print()

    # Step 2.2: Generate Go from IR
    print("  Step 2.2: Generating Go from IR...")
    go_generator = GoGeneratorV2()
    go_generator.source_language = "pw"  # Source is PW DSL, not Python!
    go_code = go_generator.generate(ir_from_pw)
    print(f"    ✓ Generated {len(go_code)} characters of Go code")
    print()

    # Step 2.3: Write Go output
    print("  Step 2.3: Writing Go output...")
    with open(output_path, 'w') as f:
        f.write(go_code)
    print(f"    ✓ Written to {output_path}")
    print()

    print("  ✅ Phase 2 Complete: PW DSL → Go")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                  ✅ TRANSLATION COMPLETE                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Translation Flow:")
    print(f"  1. Python ({Path(input_path).name})")
    print(f"     ↓ PythonParserV2")
    print(f"  2. IR (Intermediate Representation)")
    print(f"     ↓ PWGenerator")
    print(f"  3. PW DSL ({Path(pw_path).name if save_pw_dsl else 'in-memory'})")
    print(f"     ↓ PWParser")
    print(f"  4. IR (Intermediate Representation)")
    print(f"     ↓ GoGeneratorV2")
    print(f"  5. Go ({Path(output_path).name})")
    print()
    print("🔑 Key Points:")
    print("  • PW DSL is the universal bridge")
    print("  • Agents exchange PW DSL, not Python/Go")
    print("  • Language-agnostic intermediate format")
    print("  • Human-readable for debugging")
    print("  • Same flow works for ANY language pair!")
    print()

    # Show function mapping
    if ir_from_pw.functions:
        print("Functions Translated:")
        for func in ir_from_pw.functions:
            print(f"  • {func.name}()")

    if ir_from_pw.classes:
        print("\nClasses Translated:")
        for cls in ir_from_pw.classes:
            print(f"  • {cls.name}")

    print()
    print("✨ Universal Translation System: WORKING AS DESIGNED ✨")

if __name__ == "__main__":
    input_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/test_code_original.py"
    output_file = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/test_code_from_python_via_pw.go"

    translate_python_to_go_via_pw(input_file, output_file, save_pw_dsl=True)
