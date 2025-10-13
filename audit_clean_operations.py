#!/usr/bin/env python3
"""
STRICT AUDIT: Remove ALL placeholders and broken code.

Only keep operations that have REAL, EXECUTABLE code in each language.
If a language has a placeholder, REMOVE that language from the operation.
"""

import json
from pw_operations_mcp_server import PWOperationsMCPServer

def is_placeholder_or_broken(code, imports):
    """Detect if code is a placeholder or broken."""

    # Explicit placeholder markers
    placeholder_markers = [
        "/* No built-in",
        "/* Requires",
        "/* Manual implementation",
        "/* Complex",
        "/* Compile-time",
        "/* popen",
        "TODO",
        "FIXME",
        "PLACEHOLDER"
    ]

    for marker in placeholder_markers:
        if marker in code:
            return True, f"Contains: {marker}"

    # Code that's just a comment
    if code.strip().startswith("/*") and code.strip().endswith("*/"):
        return True, "Just a comment"

    # Code that's too short to be real
    if len(code.strip()) < 10:
        return True, "Too short"

    # Empty or None
    if not code or code.strip() == "":
        return True, "Empty"

    return False, None

def audit_all_operations():
    """Audit all operations and classify them."""
    server = PWOperationsMCPServer()

    results = {
        "total_operations": len(server.operations),
        "by_operation": {},
        "summary": {
            "python": {"working": 0, "broken": 0},
            "rust": {"working": 0, "broken": 0},
            "go": {"working": 0, "broken": 0},
            "javascript": {"working": 0, "broken": 0},
            "cpp": {"working": 0, "broken": 0}
        },
        "operations_to_remove": [],
        "language_implementations_to_remove": []
    }

    print("=" * 80)
    print("STRICT AUDIT: Operations with REAL, WORKING Code Only")
    print("=" * 80)
    print()

    for op_id, op_data in server.operations.items():
        implementations = op_data.get("implementations", {})

        op_status = {
            "id": op_id,
            "syntax": op_data.get("pw_syntax", ""),
            "languages": {}
        }

        for lang, impl in implementations.items():
            code = impl.get("code", "")
            imports = impl.get("imports", [])

            is_broken, reason = is_placeholder_or_broken(code, imports)

            op_status["languages"][lang] = {
                "working": not is_broken,
                "code": code[:100] if len(code) <= 100 else code[:97] + "...",
                "reason": reason if is_broken else "OK"
            }

            if is_broken:
                results["summary"][lang]["broken"] += 1
                results["language_implementations_to_remove"].append({
                    "operation": op_id,
                    "language": lang,
                    "reason": reason
                })
            else:
                results["summary"][lang]["working"] += 1

        results["by_operation"][op_id] = op_status

        # If NO languages work, mark entire operation for removal
        working_langs = [l for l, s in op_status["languages"].items() if s["working"]]
        if len(working_langs) == 0:
            results["operations_to_remove"].append(op_id)

    return results

def print_audit_results(results):
    """Print detailed audit results."""

    print("SUMMARY BY LANGUAGE:")
    print("-" * 80)
    for lang, stats in results["summary"].items():
        total = stats["working"] + stats["broken"]
        pct = stats["working"] / total * 100 if total > 0 else 0
        print(f"{lang:12} | Working: {stats['working']:3} | Broken: {stats['broken']:3} | {pct:.1f}%")
    print()

    print("IMPLEMENTATIONS TO REMOVE:")
    print("-" * 80)

    # Group by language
    by_lang = {}
    for item in results["language_implementations_to_remove"]:
        lang = item["language"]
        if lang not in by_lang:
            by_lang[lang] = []
        by_lang[lang].append(item)

    for lang, items in sorted(by_lang.items()):
        print(f"\n{lang.upper()} ({len(items)} broken implementations):")
        for item in items:
            print(f"  • {item['operation']:25} - {item['reason']}")

    print()

    if results["operations_to_remove"]:
        print(f"OPERATIONS WITH NO WORKING IMPLEMENTATIONS ({len(results['operations_to_remove'])}):")
        print("-" * 80)
        for op_id in results["operations_to_remove"]:
            print(f"  • {op_id}")
        print()

    print("=" * 80)
    print("CLEAN OPERATION COUNT:")
    print("-" * 80)

    # Calculate operations that work in ALL 5 languages
    all_five = 0
    four_langs = 0
    three_langs = 0
    two_langs = 0
    one_lang = 0

    for op_id, op_status in results["by_operation"].items():
        working_count = sum(1 for l, s in op_status["languages"].items() if s["working"])

        if working_count == 5:
            all_five += 1
        elif working_count == 4:
            four_langs += 1
        elif working_count == 3:
            three_langs += 1
        elif working_count == 2:
            two_langs += 1
        elif working_count == 1:
            one_lang += 1

    print(f"Operations working in ALL 5 languages: {all_five}")
    print(f"Operations working in 4 languages: {four_langs}")
    print(f"Operations working in 3 languages: {three_langs}")
    print(f"Operations working in 2 languages: {two_langs}")
    print(f"Operations working in 1 language: {one_lang}")
    print(f"Operations working in 0 languages: {len(results['operations_to_remove'])}")
    print()
    print(f"Total clean operations (1+ language): {all_five + four_langs + three_langs + two_langs + one_lang}")
    print("=" * 80)

    return all_five, four_langs, three_langs

def generate_clean_operations_list(results):
    """Generate list of operations with only working implementations."""

    clean_ops = {}

    for op_id, op_status in results["by_operation"].items():
        working_langs = {}

        for lang, status in op_status["languages"].items():
            if status["working"]:
                working_langs[lang] = True

        if working_langs:
            clean_ops[op_id] = {
                "syntax": op_status["syntax"],
                "supported_languages": list(working_langs.keys()),
                "language_count": len(working_langs)
            }

    return clean_ops

if __name__ == "__main__":
    results = audit_all_operations()
    all_five, four_langs, three_langs = print_audit_results(results)

    clean_ops = generate_clean_operations_list(results)

    # Save clean list
    with open("CLEAN_OPERATIONS_LIST.json", "w") as f:
        json.dump(clean_ops, f, indent=2)

    print()
    print("RECOMMENDATION:")
    print("-" * 80)
    print(f"✅ Keep {len(clean_ops)} operations with working code")
    print(f"❌ Remove {len(results['language_implementations_to_remove'])} broken language implementations")
    print(f"❌ Remove {len(results['operations_to_remove'])} operations with no working code")
    print()
    print(f"Focus on {all_five} operations that work in ALL 5 languages")
    print(f"for production-ready multi-language support.")
    print()
    print("Clean operations list saved to: CLEAN_OPERATIONS_LIST.json")
    print("-" * 80)
