"""
Test CLI compile and run commands

Tests the `asl compile` and `promptware run` commands.
"""

import sys
import subprocess
import tempfile
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_cli_command(args):
    """Run promptware CLI command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["python3", "-m", "promptware.cli"] + args,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.returncode, result.stdout, result.stderr


def test_compile_to_json():
    """Test compiling PW to MCP JSON."""
    print(f"\n{'='*60}")
    print("Testing: asl compile")
    print(f"{'='*60}")

    # Create temporary PW file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("""
function multiply(a: int, b: int) -> int {
    return a * b;
}
""")
        temp_pw = f.name

    try:
        # Compile to JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_json = f.name

        returncode, stdout, stderr = run_cli_command([
            "compile", temp_pw, "-o", temp_json
        ])

        assert returncode == 0, f"Compile failed with code {returncode}\n{stderr}"

        # Check output file exists
        json_path = Path(temp_json)
        assert json_path.exists(), f"JSON file not created: {temp_json}"

        # Check JSON is valid
        json_content = json_path.read_text()
        parsed = json.loads(json_content)

        assert isinstance(parsed, dict), "JSON should be an object"

        print(f"  ✅ Generated {len(json_content)} chars of JSON")
        print(f"  ✅ JSON is valid")
        print("✅ Compile to JSON works")

        # Cleanup
        json_path.unlink()
        return True

    finally:
        Path(temp_pw).unlink()


def test_compile_default_output():
    """Test compile with default output name."""
    print(f"\n{'='*60}")
    print("Testing: asl compile (default output)")
    print(f"{'='*60}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("function test() -> int { return 1; }")
        temp_pw = f.name

    try:
        returncode, stdout, stderr = run_cli_command([
            "compile", temp_pw
        ])

        assert returncode == 0, f"Compile failed with code {returncode}\n{stderr}"

        # Default output should be <input>.json
        expected_json = temp_pw + '.json'
        json_path = Path(expected_json)

        assert json_path.exists(), f"Default JSON file not created: {expected_json}"

        print(f"  ✅ Created {expected_json}")
        print("✅ Default output name works")

        # Cleanup
        json_path.unlink()
        return True

    finally:
        Path(temp_pw).unlink()


def test_run_executes():
    """Test run command executes PW code."""
    print(f"\n{'='*60}")
    print("Testing: promptware run")
    print(f"{'='*60}")

    # Create PW file that prints output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        # Note: This won't actually print since we don't have print() in PW yet
        # But it should at least execute without error
        f.write("""
function calculate() -> int {
    let x = 5;
    let y = 10;
    return x + y;
}

function main() -> int {
    let result = calculate();
    return result;
}
""")
        temp_pw = f.name

    try:
        returncode, stdout, stderr = run_cli_command([
            "run", temp_pw
        ])

        # Should execute successfully (even if no output)
        assert returncode == 0, f"Run failed with code {returncode}\n{stderr}"

        print("  ✅ Code executed without errors")
        print("✅ Run command works")
        return True

    finally:
        Path(temp_pw).unlink()


def test_run_verbose():
    """Test run with verbose output."""
    print(f"\n{'='*60}")
    print("Testing: promptware run --verbose")
    print(f"{'='*60}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("function main() -> int { return 0; }")
        temp_pw = f.name

    try:
        returncode, stdout, stderr = run_cli_command([
            "run", temp_pw, "--verbose"
        ])

        assert returncode == 0, f"Run failed with code {returncode}"

        output = stdout + stderr
        assert "Parsing" in output or "parsing" in output.lower(), "Missing verbose output"

        print("  ✅ Verbose output present")
        print("✅ Run verbose mode works")
        return True

    finally:
        Path(temp_pw).unlink()


def run_all_tests():
    """Run all CLI compile/run tests."""
    print("\n" + "="*60)
    print("CLI COMPILE & RUN COMMAND TESTS")
    print("="*60)

    tests = [
        ("Compile to JSON", test_compile_to_json),
        ("Compile default output", test_compile_default_output),
        ("Run executes code", test_run_executes),
        ("Run verbose", test_run_verbose),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print("\n" + "="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
