"""
Comprehensive Bidirectional Translation Matrix Test

Tests ALL possible language pair combinations to ensure bidirectional translation
preserves semantics. Tests both directions for each pair.

Matrix: 5 languages × 5 languages × 2 directions = 50 total tests
(but skip self-translations: 5×4×2 = 40 actual tests)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2
from language.go_parser_v2 import GoParserV2

from language.python_generator_v2 import PythonGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code samples with collection operations
SAMPLES = {
    "python": """
def filter_positives(numbers):
    result = [n * 2 for n in numbers if n > 0]
    return result
""",
    "javascript": """
function filterPositives(numbers) {
    const result = numbers.filter(n => n > 0).map(n => n * 2);
    return result;
}
""",
    "rust": """
pub fn filter_positives(numbers: Vec<i32>) -> Vec<i32> {
    let result = numbers.iter().filter(|n| *n > 0).map(|n| n * 2).collect();
    return result;
}
""",
    "csharp": """
public class Processor {
    public List<int> FilterPositives(List<int> numbers) {
        var result = numbers.Where(n => n > 0).Select(n => n * 2).ToList();
        return result;
    }
}
""",
    "go": """
package main

func FilterPositives(numbers []int) []int {
    result := []int{}
    for _, n := range numbers {
        if n > 0 {
            result = append(result, n * 2)
        }
    }
    return result
}
"""
}

PARSERS = {
    "python": PythonParserV2(),
    "javascript": NodeJSParserV2(),
    "rust": RustParserV2(),
    "csharp": DotNetParserV2(),
    "go": GoParserV2()
}

GENERATORS = {
    "python": PythonGeneratorV2(),
    "javascript": NodeJSGeneratorV2(),
    "rust": RustGeneratorV2(),
    "csharp": DotNetGeneratorV2(),
    "go": GoGeneratorV2()
}

EXTENSIONS = {
    "python": ".py",
    "javascript": ".js",
    "rust": ".rs",
    "csharp": ".cs",
    "go": ".go"
}


def verify_collection_pattern(code, lang):
    """Verify the code contains collection operation patterns."""
    patterns = {
        "python": ["for", "in", "["],  # Comprehension
        "javascript": [".filter(", ".map("],  # Array methods
        "rust": [".iter(", ".collect("],  # Iterator chain
        "csharp": [".Where(", ".Select("],  # LINQ
        "go": ["for", "range", "append"]  # For-append
    }
    
    required = patterns.get(lang, [])
    for pattern in required:
        if pattern not in code:
            return False
    return True


def test_translation(source_lang, target_lang, verbose=False):
    """Test translation from source_lang to target_lang."""
    
    # Get source code
    source_code = SAMPLES[source_lang]
    
    # Parse source → IR
    parser = PARSERS[source_lang]
    ext = EXTENSIONS[source_lang]
    
    try:
        ir = parser.parse_source(source_code, f"test{ext}")
    except Exception as e:
        return False, f"Parse failed: {str(e)[:100]}"
    
    # Generate IR → target
    generator = GENERATORS[target_lang]
    
    try:
        target_code = generator.generate(ir)
    except Exception as e:
        return False, f"Generate failed: {str(e)[:100]}"
    
    # Verify target contains collection pattern
    if not verify_collection_pattern(target_code, target_lang):
        return False, f"Missing collection pattern in {target_lang}"
    
    if verbose:
        print(f"\n{source_lang} → {target_lang}:")
        print(target_code[:200] + "...")
    
    return True, "OK"


def test_round_trip(lang1, lang2, verbose=False):
    """Test round-trip: lang1 → lang2 → lang1"""
    
    # Original code
    original = SAMPLES[lang1]
    
    # Parse lang1 → IR
    parser1 = PARSERS[lang1]
    ext1 = EXTENSIONS[lang1]
    
    try:
        ir1 = parser1.parse_source(original, f"test{ext1}")
    except Exception as e:
        return False, f"Parse1 failed: {str(e)[:100]}"
    
    # Generate IR → lang2
    gen2 = GENERATORS[lang2]
    try:
        code2 = gen2.generate(ir1)
    except Exception as e:
        return False, f"Gen2 failed: {str(e)[:100]}"
    
    # Parse lang2 → IR
    parser2 = PARSERS[lang2]
    ext2 = EXTENSIONS[lang2]
    
    try:
        ir2 = parser2.parse_source(code2, f"test{ext2}")
    except Exception as e:
        return False, f"Parse2 failed: {str(e)[:100]}"
    
    # Generate IR → lang1 (back to original)
    gen1 = GENERATORS[lang1]
    try:
        code_back = gen1.generate(ir2)
    except Exception as e:
        return False, f"Gen1 failed: {str(e)[:100]}"
    
    # Verify round-trip preserved collection pattern
    if not verify_collection_pattern(code_back, lang1):
        return False, f"Lost collection pattern in round-trip"
    
    if verbose:
        print(f"\n{lang1} → {lang2} → {lang1}: Round-trip preserved")
    
    return True, "OK"


def run_bidirectional_matrix():
    """Run complete bidirectional translation matrix."""
    
    print("\n" + "="*70)
    print("BIDIRECTIONAL TRANSLATION MATRIX TEST")
    print("="*70)
    
    languages = ["python", "javascript", "rust", "csharp", "go"]
    
    results = {
        "one_way": {},
        "round_trip": {}
    }
    
    total_tests = 0
    passed_tests = 0
    
    # Test one-way translations
    print("\n1. ONE-WAY TRANSLATIONS (20 pairs)")
    print("-" * 70)
    
    for source in languages:
        for target in languages:
            if source == target:
                continue
            
            total_tests += 1
            success, msg = test_translation(source, target)
            
            key = f"{source}→{target}"
            results["one_way"][key] = success
            
            status = "✅" if success else "❌"
            print(f"{status} {source:12} → {target:12}  {msg if not success else ''}")
            
            if success:
                passed_tests += 1
    
    # Test round-trips
    print("\n2. ROUND-TRIP TRANSLATIONS (20 pairs)")
    print("-" * 70)
    
    for lang1 in languages:
        for lang2 in languages:
            if lang1 == lang2:
                continue
            
            total_tests += 1
            success, msg = test_round_trip(lang1, lang2)
            
            key = f"{lang1}↔{lang2}"
            results["round_trip"][key] = success
            
            status = "✅" if success else "❌"
            print(f"{status} {lang1:12} ↔ {lang2:12}  {msg if not success else ''}")
            
            if success:
                passed_tests += 1
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    one_way_passed = sum(1 for v in results["one_way"].values() if v)
    one_way_total = len(results["one_way"])
    
    round_trip_passed = sum(1 for v in results["round_trip"].values() if v)
    round_trip_total = len(results["round_trip"])
    
    print(f"\nOne-way translations:  {one_way_passed}/{one_way_total} passing " +
          f"({one_way_passed*100//one_way_total}%)")
    print(f"Round-trip translations: {round_trip_passed}/{round_trip_total} passing " +
          f"({round_trip_passed*100//round_trip_total}%)")
    print(f"\nOverall: {passed_tests}/{total_tests} passing ({passed_tests*100//total_tests}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 PERFECT SCORE - ALL BIDIRECTIONAL TRANSLATIONS WORKING!")
        return True
    else:
        failed = total_tests - passed_tests
        print(f"\n⚠️  {failed} translations need improvement")
        return False


if __name__ == "__main__":
    success = run_bidirectional_matrix()
    sys.exit(0 if success else 1)
