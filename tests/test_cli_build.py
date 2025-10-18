"""
Test CLI build command

Tests the `asl build` command for compiling PW to target languages.
"""

import sys
import subprocess
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_cli_command(args):
    """Run assertlang CLI command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["python3", "-m", "assertlang.cli"] + args,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.returncode, result.stdout, result.stderr


def test_build_help():
    """Test that build command has help."""
    print(f"\n{'='*60}")
    print("Testing: asl build --help")
    print(f"{'='*60}")

    returncode, stdout, stderr = run_cli_command(["build", "--help"])

    assert returncode == 0, f"Expected exit code 0, got {returncode}"

    output = stdout + stderr
    assert "Compile PW" in output or "compile" in output.lower(), f"Missing compile text in help\n{output}"
    assert ".al" in output, f"Missing .al reference in help\n{output}"

    print("✅ Build help works")
    return True


def test_build_python():
    """Test building PW to Python."""
    print(f"\n{'='*60}")
    print("Testing: asl build (Python)")
    print(f"{'='*60}")

    # Create temporary PW file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("""
function add(x: int, y: int) -> int {
    return x + y;
}

function main() -> int {
    let result = add(10, 20);
    return result;
}
""")
        temp_pw = f.name

    try:
        # Build to Python
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_py = f.name

        returncode, stdout, stderr = run_cli_command([
            "build", temp_pw, "--lang", "python", "-o", temp_py
        ])

        assert returncode == 0, f"Build failed with code {returncode}\n{stderr}"

        # Check output file exists and has content
        output_path = Path(temp_py)
        assert output_path.exists(), f"Output file not created: {temp_py}"

        python_code = output_path.read_text()
        assert "def add(" in python_code, "Generated Python missing add function"
        assert "def main(" in python_code, "Generated Python missing main function"

        print(f"  ✅ Generated {len(python_code)} chars of Python")
        print(f"  ✅ Contains add() and main() functions")
        print("✅ Build to Python works")

        # Cleanup
        output_path.unlink()
        return True

    finally:
        Path(temp_pw).unlink()


def test_build_to_stdout():
    """Test building to stdout (no output file)."""
    print(f"\n{'='*60}")
    print("Testing: asl build (stdout)")
    print(f"{'='*60}")

    # Create temporary PW file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("""
function hello() -> string {
    return "Hello";
}
""")
        temp_pw = f.name

    try:
        returncode, stdout, stderr = run_cli_command([
            "build", temp_pw, "--lang", "python"
        ])

        assert returncode == 0, f"Build failed with code {returncode}\n{stderr}"
        assert "def hello(" in stdout, "Generated Python not in stdout"

        print(f"  ✅ Generated {len(stdout)} chars to stdout")
        print("✅ Build to stdout works")
        return True

    finally:
        Path(temp_pw).unlink()


def test_build_verbose():
    """Test build with verbose output."""
    print(f"\n{'='*60}")
    print("Testing: asl build --verbose")
    print(f"{'='*60}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.al', delete=False) as f:
        f.write("function test() -> int { return 42; }")
        temp_pw = f.name

    try:
        returncode, stdout, stderr = run_cli_command([
            "build", temp_pw, "--lang", "python", "--verbose"
        ])

        assert returncode == 0, f"Build failed with code {returncode}"

        # Check for verbose messages (in stderr since that's where info() prints)
        output = stdout + stderr
        assert "Parsing" in output or "parsing" in output.lower(), "Missing verbose parsing message"

        print("  ✅ Verbose output present")
        print("✅ Build verbose mode works")
        return True

    finally:
        Path(temp_pw).unlink()


def test_build_nonexistent_file():
    """Test build with nonexistent file."""
    print(f"\n{'='*60}")
    print("Testing: asl build (nonexistent file)")
    print(f"{'='*60}")

    returncode, stdout, stderr = run_cli_command([
        "build", "/tmp/doesnotexist12345.al", "--lang", "python"
    ])

    assert returncode != 0, "Expected non-zero exit code for missing file"

    output = stdout + stderr
    assert "not found" in output.lower() or "error" in output.lower(), "Missing error message"

    print("  ✅ Fails with appropriate error")
    print("✅ Error handling works")
    return True


def run_all_tests():
    """Run all CLI build tests."""
    print("\n" + "="*60)
    print("CLI BUILD COMMAND TESTS")
    print("="*60)

    tests = [
        ("Build help", test_build_help),
        ("Build to Python", test_build_python),
        ("Build to stdout", test_build_to_stdout),
        ("Build verbose", test_build_verbose),
        ("Build error handling", test_build_nonexistent_file),
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
