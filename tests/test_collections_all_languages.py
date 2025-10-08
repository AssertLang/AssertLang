"""
Test collection operations across all 5 languages (25 combinations).

Based on Python comprehensions and JavaScript .map/.filter, test:
- Round-trip (5 tests): Code → IR → same language
- Cross-language (20 tests): Code → IR → different language

Measures improvement: 20% (Python only) → X%
"""

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import PythonGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2

# Test patterns
COLLECTION_PATTERNS = {
    "Python": """
def filter_and_map(items):
    filtered = [x for x in items if x > 0]
    mapped = [x * 2 for x in items]
    both = [x * 2 for x in items if x > 0]
    return both
""",
    "JavaScript": """
function filterAndMap(items) {
    const filtered = items.filter(x => x > 0);
    const mapped = items.map(x => x * 2);
    const both = items.filter(x => x > 0).map(x => x * 2);
    return both;
}
""",
    "Go": None,  # Not implemented yet
    "Rust": None,  # Not implemented yet
    "C#": None,  # Not implemented yet
}

PARSERS = {
    "Python": PythonParserV2(),
    "JavaScript": NodeJSParserV2(),
    "Go": GoParserV2(),
    "Rust": RustParserV2(),
    "C#": DotNetParserV2(),
}

GENERATORS = {
    "Python": PythonGeneratorV2(),
    "JavaScript": NodeJSGeneratorV2(typescript=False),
    "Go": GoGeneratorV2(),
    "Rust": RustGeneratorV2(),
    "C#": DotNetGeneratorV2(),
}

def test_round_trip(lang: str, code: str) -> dict:
    """Test: Code → IR → Same language."""
    parser = PARSERS[lang]
    generator = GENERATORS[lang]

    try:
        ir = parser.parse_source(code, "test")
        regenerated = generator.generate(ir)

        # Check for collection keywords
        has_collection = False
        if lang == "Python":
            has_collection = " for " in regenerated and " in " in regenerated
        elif lang == "JavaScript":
            has_collection = ".filter(" in regenerated or ".map(" in regenerated
        elif lang == "Go":
            has_collection = "for " in regenerated and "append(" in regenerated
        elif lang == "Rust":
            has_collection = ".iter()" in regenerated or ".filter(" in regenerated
        elif lang == "C#":
            has_collection = ".Where(" in regenerated or ".Select(" in regenerated

        return {
            "from": lang,
            "to": lang,
            "success": has_collection,
            "error": "" if has_collection else f"No collection operations in output"
        }
    except Exception as e:
        return {
            "from": lang,
            "to": lang,
            "success": False,
            "error": str(e)
        }

def test_translation(from_lang: str, to_lang: str, code: str) -> dict:
    """Test: From language → IR → To language."""
    parser = PARSERS[from_lang]
    generator = GENERATORS[to_lang]

    try:
        ir = parser.parse_source(code, "test")
        output = generator.generate(ir)

        # Check for collection keywords in target language
        has_collection = False
        if to_lang == "Python":
            has_collection = " for " in output and " in " in output
        elif to_lang == "JavaScript":
            has_collection = ".filter(" in output or ".map(" in output
        elif to_lang == "Go":
            has_collection = "for " in output and "append(" in output
        elif to_lang == "Rust":
            has_collection = ".iter()" in output or ".filter(" in output
        elif to_lang == "C#":
            has_collection = ".Where(" in output or ".Select(" in output

        return {
            "from": from_lang,
            "to": to_lang,
            "success": has_collection,
            "error": "" if has_collection else f"No collection operations in {to_lang} output"
        }
    except Exception as e:
        return {
            "from": from_lang,
            "to": to_lang,
            "success": False,
            "error": str(e)
        }

def run_all_tests():
    """Run collection operations tests across all 25 combinations."""
    print("=" * 80)
    print("COLLECTION OPERATIONS TEST - ALL 25 COMBINATIONS")
    print("=" * 80)
    print()

    # Test round-trips (5 tests)
    print("Round-Trip Tests (5 total)")
    print("-" * 80)

    round_trip_results = []
    for lang, code in COLLECTION_PATTERNS.items():
        if code is None:
            result = {
                "from": lang,
                "to": lang,
                "success": False,
                "error": "Not implemented"
            }
        else:
            result = test_round_trip(lang, code)

        round_trip_results.append(result)
        status = "✅" if result["success"] else "❌"
        print(f"{status} {lang:12} → {lang:12}: {result.get('error', 'OK')[:40]}")

    print()

    # Cross-language tests (20 tests)
    print("Cross-Language Tests (20 total)")
    print("-" * 80)

    translation_results = []
    languages = list(COLLECTION_PATTERNS.keys())

    for from_lang in languages:
        for to_lang in languages:
            if from_lang == to_lang:
                continue  # Skip round-trips

            from_code = COLLECTION_PATTERNS[from_lang]
            if from_code is None:
                result = {
                    "from": from_lang,
                    "to": to_lang,
                    "success": False,
                    "error": f"{from_lang} not implemented"
                }
            else:
                result = test_translation(from_lang, to_lang, from_code)

            translation_results.append(result)
            status = "✅" if result["success"] else "❌"
            print(f"{status} {from_lang:12} → {to_lang:12}: {result.get('error', 'OK')[:40]}")

    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    round_trip_pass = sum(1 for r in round_trip_results if r["success"])
    round_trip_total = len(round_trip_results)
    round_trip_pct = (round_trip_pass / round_trip_total * 100) if round_trip_total > 0 else 0

    print(f"Round-Trip: {round_trip_pass}/{round_trip_total} ({round_trip_pct:.0f}%)")

    translation_pass = sum(1 for r in translation_results if r["success"])
    translation_total = len(translation_results)
    translation_pct = (translation_pass / translation_total * 100) if translation_total > 0 else 0

    print(f"Translation: {translation_pass}/{translation_total} ({translation_pct:.0f}%)")

    overall_pass = round_trip_pass + translation_pass
    overall_total = round_trip_total + translation_total
    overall_pct = (overall_pass / overall_total * 100) if overall_total > 0 else 0

    print(f"Overall: {overall_pass}/{overall_total} ({overall_pct:.0f}%)")
    print()

    # Improvement calculation
    print("IMPROVEMENT:")
    print(f"  Before: 20% (Python only: 1/5 languages)")
    print(f"  After:  {overall_pct:.0f}% ({round_trip_pass}/5 languages working)")
    improvement = overall_pct - 20
    print(f"  Gain:   +{improvement:.0f} percentage points")
    print()

    return {
        "overall_pct": overall_pct,
        "improvement": improvement
    }

if __name__ == "__main__":
    results = run_all_tests()
