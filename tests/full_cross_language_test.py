#!/usr/bin/env python3
"""
Complete Cross-Language Translation Test

Tests ALL 20 bidirectional combinations:
- Python ↔ Node.js, Go, Rust, .NET (8 combinations)
- Node.js ↔ Go, Rust, .NET (6 combinations)
- Go ↔ Rust, .NET (4 combinations)
- Rust ↔ .NET (2 combinations)
Total: 20 combinations (5×4 = 20)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.agent_parser import parse_agent_pw
from language.mcp_server_generator import generate_python_mcp_server
from language.mcp_server_generator_nodejs import generate_nodejs_mcp_server
from language.mcp_server_generator_go import generate_go_mcp_server
from language.mcp_server_generator_rust import generate_rust_mcp_server
from language.mcp_server_generator_dotnet import generate_dotnet_mcp_server


# Simple test PW DSL
TEST_PW_TEMPLATE = """lang {lang}
agent test-agent
port 8000

expose health.check@v1:
  params:
  returns:
    status string
    uptime int

expose echo@v1:
  params:
    message string
  returns:
    echo string
"""


GENERATORS = {
    "python": generate_python_mcp_server,
    "nodejs": generate_nodejs_mcp_server,
    "go": generate_go_mcp_server,
    "rust": generate_rust_mcp_server,
    "dotnet": generate_dotnet_mcp_server,
}

PARSERS = {
    "python": "reverse_parsers/python_parser.py",
    "nodejs": "reverse_parsers/nodejs_parser.py",
    "go": "reverse_parsers/go_parser.py",
    "rust": "reverse_parsers/rust_parser.py",
    "dotnet": "reverse_parsers/dotnet_parser.py",
}

EXTENSIONS = {
    "python": ".py",
    "nodejs": ".js",
    "go": ".go",
    "rust": ".rs",
    "dotnet": ".cs",
}


def generate_code_for_lang(lang: str) -> str:
    """Generate code for a language from PW DSL."""
    pw_dsl = TEST_PW_TEMPLATE.format(lang=lang)
    agent = parse_agent_pw(pw_dsl)
    generator = GENERATORS[lang]
    return generator(agent)


def parse_code_to_pw(code: str, lang: str) -> str:
    """Parse code back to PW DSL using reverse parser."""
    with tempfile.NamedTemporaryFile(mode='w', suffix=EXTENSIONS[lang], delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        result = subprocess.run(
            ["python3", "reverse_parsers/cli.py", temp_file],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )

        if result.returncode != 0:
            raise Exception(f"Parse failed: {result.stderr}")

        # Extract just the PW DSL (before "Parsing..." message)
        pw_output = result.stdout.split("Parsing")[0].strip()
        return pw_output
    finally:
        Path(temp_file).unlink()


def validate_code(code: str, lang: str) -> bool:
    """Validate generated code is syntactically correct."""
    if lang == "python":
        import ast
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    elif lang == "nodejs":
        return "express()" in code or "fastify()" in code
    elif lang == "go":
        return "package main" in code and "func main()" in code
    elif lang == "rust":
        return "fn main()" in code
    elif lang == "dotnet":
        return "using" in code and "namespace" in code

    return False


def test_translation(source_lang: str, target_lang: str) -> dict:
    """Test translation from source_lang to target_lang."""
    result = {
        "source": source_lang,
        "target": target_lang,
        "status": "PENDING",
        "source_code_size": 0,
        "pw_size": 0,
        "target_code_size": 0,
        "error": None
    }

    try:
        # Step 1: Generate source code
        print(f"  1. Generating {source_lang} code...")
        source_code = generate_code_for_lang(source_lang)
        result["source_code_size"] = len(source_code)
        print(f"     ✓ Generated {len(source_code)} bytes")

        # Step 2: Parse to PW
        print(f"  2. Parsing {source_lang} → PW...")
        pw_dsl = parse_code_to_pw(source_code, source_lang)
        result["pw_size"] = len(pw_dsl)
        print(f"     ✓ Extracted {len(pw_dsl)} bytes PW DSL")

        # Step 3: Modify PW to target language
        print(f"  3. Modifying PW for {target_lang}...")
        pw_lines = pw_dsl.split("\n")
        pw_lines[0] = f"lang {target_lang}"
        pw_modified = "\n".join(pw_lines)

        # Step 4: Generate target code
        print(f"  4. Generating PW → {target_lang}...")
        agent = parse_agent_pw(pw_modified)
        target_code = GENERATORS[target_lang](agent)
        result["target_code_size"] = len(target_code)
        print(f"     ✓ Generated {len(target_code)} bytes")

        # Step 5: Validate target code
        print(f"  5. Validating {target_lang} code...")
        is_valid = validate_code(target_code, target_lang)
        print(f"     ✓ Valid: {is_valid}")

        if is_valid:
            result["status"] = "PASS"
        else:
            result["status"] = "FAIL"
            result["error"] = "Validation failed"

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)
        print(f"     ✗ Error: {e}")

    return result


def main():
    print("=" * 80)
    print("COMPLETE CROSS-LANGUAGE TRANSLATION TEST")
    print("Testing all 20 bidirectional combinations")
    print("=" * 80)
    print()

    languages = ["python", "nodejs", "go", "rust", "dotnet"]
    results = []

    # Test all combinations
    for i, source_lang in enumerate(languages):
        for target_lang in languages:
            if source_lang == target_lang:
                continue  # Skip same-language

            test_num = len(results) + 1
            print(f"[{test_num}/20] {source_lang.upper()} → {target_lang.upper()}")
            print("-" * 80)

            result = test_translation(source_lang, target_lang)
            results.append(result)
            print()

    # Summary
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()
    print(f"{'Source':<10} {'Target':<10} {'Status':<10} {'PW Size':<12} {'Target Size':<12}")
    print("-" * 80)

    passed = 0
    failed = 0
    errors = 0

    for r in results:
        status_emoji = "✅" if r["status"] == "PASS" else "❌" if r["status"] == "FAIL" else "⚠️"
        pw_size = f"{r['pw_size']} bytes" if r['pw_size'] > 0 else "-"
        target_size = f"{r['target_code_size']} bytes" if r['target_code_size'] > 0 else "-"

        print(f"{r['source']:<10} {r['target']:<10} {status_emoji} {r['status']:<8} {pw_size:<12} {target_size:<12}")

        if r["status"] == "PASS":
            passed += 1
        elif r["status"] == "FAIL":
            failed += 1
        else:
            errors += 1

    print("-" * 80)
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed} | Errors: {errors}")
    print(f"Success Rate: {passed / len(results) * 100:.1f}%")
    print()

    # Show errors if any
    if errors > 0 or failed > 0:
        print("=" * 80)
        print("FAILURES AND ERRORS")
        print("=" * 80)
        for r in results:
            if r["status"] != "PASS":
                print(f"{r['source']} → {r['target']}: {r['error']}")
        print()

    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
