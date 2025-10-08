"""
Master test runner for Production Readiness Plan

Runs all test suites and reports overall progress.
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_test_file(test_file: Path) -> tuple[bool, str]:
    """Run a test file and return (success, output)."""
    try:
        # Run from project root, not from tests/
        project_root = test_file.parent.parent
        result = subprocess.run(
            ["python3", str(test_file.relative_to(project_root))],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, f"ERROR: {e}"


def main():
    """Run all production tests."""
    print("\n" + "="*70)
    print("PRODUCTION READINESS TEST SUITE - MASTER RUNNER")
    print("="*70)

    # Define test suites
    test_suites = [
        ("Week 1: Type Validation", "test_type_validation.py", 20),
        ("Week 1: Whitespace Handling", "test_parser_whitespace.py", 8),
        ("Week 1: Multi-line Syntax", "test_multiline_syntax.py", 10),
        ("Week 2: For Loops", "test_for_loops.py", 7),
        ("Week 2: While Loops", "test_while_loops.py", 6),
        ("Week 3: Arrays", "test_arrays.py", 9),
        ("Week 3: Maps", "test_maps.py", 9),
        ("Week 4: Classes", "test_classes.py", 8),
        ("Week 4: Real Programs", "test_all_real_world.py", 3),
    ]

    results = []
    total_tests = 0
    total_passed = 0

    for suite_name, test_file, test_count in test_suites:
        test_path = Path(__file__).parent / test_file

        print(f"\n{'─'*70}")
        print(f"Running: {suite_name}")
        print(f"File: {test_file}")
        print(f"Expected: {test_count} tests")
        print(f"{'─'*70}")

        success, output = run_test_file(test_path)

        if success:
            print(f"✅ PASS - All {test_count} tests passed")
            results.append((suite_name, True, test_count, test_count))
            total_passed += test_count
        else:
            # Try to extract pass count from output
            passed = 0
            if "tests passed" in output:
                for line in output.split("\n"):
                    if "tests passed" in line:
                        parts = line.split("/")
                        if len(parts) >= 2:
                            passed = int(parts[0].split()[-1])

            print(f"❌ FAIL - {passed}/{test_count} tests passed")
            results.append((suite_name, False, passed, test_count))
            total_passed += passed

        total_tests += test_count

    # Overall summary
    print("\n" + "="*70)
    print("OVERALL SUMMARY")
    print("="*70)

    for suite_name, success, passed, expected in results:
        status = "✅" if success else "❌"
        print(f"{status} {suite_name}: {passed}/{expected} ({100*passed//expected}%)")

    print("\n" + "─"*70)
    percentage = (100 * total_passed) // total_tests if total_tests > 0 else 0
    print(f"TOTAL: {total_passed}/{total_tests} tests passing ({percentage}%)")
    print("─"*70)

    # Week summary
    print("\n" + "="*70)
    print("WEEK-BY-WEEK PROGRESS")
    print("="*70)

    weeks = {
        "Week 1 (Critical Fixes)": [(r[0], r[2], r[3]) for r in results if r[0].startswith("Week 1")],
        "Week 2 (Control Flow)": [(r[0], r[2], r[3]) for r in results if r[0].startswith("Week 2")],
        "Week 3 (Data Structures)": [(r[0], r[2], r[3]) for r in results if r[0].startswith("Week 3")],
        "Week 4 (Classes & Programs)": [(r[0], r[2], r[3]) for r in results if r[0].startswith("Week 4")],
    }

    for week_name, week_results in weeks.items():
        week_passed = sum(r[1] for r in week_results)
        week_total = sum(r[2] for r in week_results)
        week_pct = (100 * week_passed) // week_total if week_total > 0 else 0
        status = "✅" if week_passed == week_total else "🟡"
        print(f"{status} {week_name}: {week_passed}/{week_total} ({week_pct}%)")

    print("\n" + "="*70)

    # Success criteria
    all_passed = total_passed == total_tests
    if all_passed:
        print("🎉 ALL TESTS PASSING - PRODUCTION READY!")
    else:
        print(f"⚠️  {total_tests - total_passed} tests still failing")

    print("="*70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
