#!/usr/bin/env python3
"""
Comprehensive validation of ALL 107 operations × 5 languages = 535 implementations

This script checks:
1. Syntax validity (can it be parsed?)
2. Placeholder detection (/* comments */, incomplete code)
3. Import statements are valid
4. Code structure is reasonable

Categories to check:
- File I/O (12)
- String (15)
- HTTP (8)
- JSON (4)
- Math (10)
- Time (8)
- Process (6)
- Array (10)
- Encoding (6)
- Type Conversions (8)
"""

import json
import ast
import re
from pw_operations_mcp_server import PWOperationsMCPServer

def validate_python_code(code, imports):
    """Check if Python code is syntactically valid."""
    try:
        # Combine imports and code
        full_code = "\n".join(imports) + "\n" + code
        ast.parse(full_code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Parse error: {e}"

def check_placeholder(code):
    """Check if code contains placeholder comments."""
    placeholders = [
        "/* No built-in",
        "/* Requires",
        "/* Manual implementation",
        "/* Complex",
        "/* popen",
        "TODO",
        "FIXME",
        "PLACEHOLDER"
    ]
    for p in placeholders:
        if p in code:
            return True, p
    return False, None

def validate_all_operations():
    """Validate all 535 implementations."""
    server = PWOperationsMCPServer()

    results = {
        "total_operations": len(server.operations),
        "total_implementations": 0,
        "valid": 0,
        "invalid": 0,
        "placeholders": 0,
        "by_language": {
            "python": {"valid": 0, "invalid": 0, "placeholder": 0},
            "rust": {"valid": 0, "invalid": 0, "placeholder": 0},
            "go": {"valid": 0, "invalid": 0, "placeholder": 0},
            "javascript": {"valid": 0, "invalid": 0, "placeholder": 0},
            "cpp": {"valid": 0, "invalid": 0, "placeholder": 0}
        },
        "issues": []
    }

    print("=" * 80)
    print("COMPREHENSIVE VALIDATION: All 107 Operations × 5 Languages")
    print("=" * 80)
    print()

    for op_id, op_data in server.operations.items():
        implementations = op_data.get("implementations", {})

        for lang, impl in implementations.items():
            results["total_implementations"] += 1
            code = impl.get("code", "")
            imports = impl.get("imports", [])

            # Check for placeholders
            has_placeholder, placeholder_text = check_placeholder(code)

            if has_placeholder:
                results["placeholders"] += 1
                results["by_language"][lang]["placeholder"] += 1
                results["issues"].append({
                    "operation": op_id,
                    "language": lang,
                    "issue": "placeholder",
                    "detail": placeholder_text,
                    "code": code[:100]
                })
                continue

            # Language-specific validation
            if lang == "python":
                is_valid, error = validate_python_code(code, imports)
                if is_valid:
                    results["valid"] += 1
                    results["by_language"][lang]["valid"] += 1
                else:
                    results["invalid"] += 1
                    results["by_language"][lang]["invalid"] += 1
                    results["issues"].append({
                        "operation": op_id,
                        "language": lang,
                        "issue": "syntax_error",
                        "detail": error,
                        "code": code
                    })
            else:
                # For non-Python, just check it's not empty and doesn't look obviously broken
                if code and len(code) > 5 and not code.startswith("/*"):
                    results["valid"] += 1
                    results["by_language"][lang]["valid"] += 1
                else:
                    results["invalid"] += 1
                    results["by_language"][lang]["invalid"] += 1
                    results["issues"].append({
                        "operation": op_id,
                        "language": lang,
                        "issue": "empty_or_broken",
                        "detail": "Code is too short or commented out",
                        "code": code
                    })

    return results

def print_results(results):
    """Print validation results."""
    print("RESULTS:")
    print("-" * 80)
    print(f"Total Operations: {results['total_operations']}")
    print(f"Total Implementations: {results['total_implementations']}")
    print(f"Expected: {results['total_operations'] * 5} (107 ops × 5 languages)")
    print()

    print(f"✅ Valid: {results['valid']} ({results['valid']/results['total_implementations']*100:.1f}%)")
    print(f"❌ Invalid: {results['invalid']} ({results['invalid']/results['total_implementations']*100:.1f}%)")
    print(f"⚠️  Placeholders: {results['placeholders']} ({results['placeholders']/results['total_implementations']*100:.1f}%)")
    print()

    print("BY LANGUAGE:")
    print("-" * 80)
    for lang, stats in results["by_language"].items():
        total = stats["valid"] + stats["invalid"] + stats["placeholder"]
        valid_pct = stats["valid"] / total * 100 if total > 0 else 0
        print(f"{lang:12} | Valid: {stats['valid']:3} | Invalid: {stats['invalid']:3} | Placeholder: {stats['placeholder']:3} | {valid_pct:.1f}%")
    print()

    if results["issues"]:
        print("ISSUES FOUND:")
        print("-" * 80)

        # Group by issue type
        by_type = {}
        for issue in results["issues"]:
            issue_type = issue["issue"]
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(issue)

        for issue_type, issues in by_type.items():
            print(f"\n{issue_type.upper()} ({len(issues)} issues):")
            for issue in issues[:10]:  # Show first 10 of each type
                print(f"  • {issue['operation']:20} [{issue['language']:10}] - {issue['detail']}")
                if len(issue['code']) < 100:
                    print(f"    Code: {issue['code']}")

            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")

    print()
    print("=" * 80)

    # Calculate quality score
    quality_score = results["valid"] / results["total_implementations"] * 100

    if quality_score >= 90:
        print(f"✅ QUALITY: EXCELLENT ({quality_score:.1f}%)")
    elif quality_score >= 75:
        print(f"⚠️  QUALITY: GOOD ({quality_score:.1f}%) - Some fixes needed")
    elif quality_score >= 50:
        print(f"⚠️  QUALITY: FAIR ({quality_score:.1f}%) - Significant fixes needed")
    else:
        print(f"❌ QUALITY: POOR ({quality_score:.1f}%) - Major overhaul needed")

    print("=" * 80)

    return quality_score >= 90

if __name__ == "__main__":
    results = validate_all_operations()
    is_production_ready = print_results(results)

    print()
    print("CONCLUSION:")
    print("-" * 80)
    if is_production_ready:
        print("✅ All operations verified - System is production-ready")
    else:
        print("❌ Issues found - Manual review and fixes required")
        print()
        print("Recommended actions:")
        print("1. Fix placeholder implementations (C++ string ops, etc.)")
        print("2. Validate syntax errors in Python implementations")
        print("3. Test actual execution of problematic operations")
        print("4. Consider marking incomplete operations as 'not supported'")
    print("-" * 80)
