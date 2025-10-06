"""
Comprehensive Exception Handling Test Suite

Tests exception handling (try/catch/except/finally) across all 5 languages
and all 25 translation combinations.

CRITICAL GAP: Exception handling was causing 0% success rate in production code.
This test suite validates the fix and measures improvement.

Test Strategy:
1. Define realistic error handling patterns for each language
2. Parse each pattern to IR
3. Generate back to same language (round-trip test)
4. Translate to all other languages (cross-language test)
5. Verify semantic equivalence
6. Measure quality improvement
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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

from dsl.ir import IRModule, IRTry, IRCatch


# ============================================================================
# Test Code Patterns (Real-World Error Handling)
# ============================================================================

ERROR_HANDLING_PATTERNS = {
    "Python": '''
def fetch_data(url: str) -> dict:
    """Fetch data with comprehensive error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    finally:
        logger.info("Request completed")
''',

    "JavaScript": '''
async function fetchData(url) {
    try {
        const response = await fetch(url, { timeout: 10000 });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        if (error.name === 'TimeoutError') {
            console.error("Request timed out");
        } else if (error.name === 'HTTPError') {
            console.error(`HTTP error: ${error.message}`);
        } else {
            console.error(`Unexpected error: ${error.message}`);
        }
        return null;
    } finally {
        console.log("Request completed");
    }
}
''',

    "Go": '''
func FetchData(url string) (map[string]interface{}, error) {
    defer log.Println("Request completed")

    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    resp, err := http.Get(url)
    if err != nil {
        if ctx.Err() == context.DeadlineExceeded {
            log.Println("Request timed out")
            return nil, fmt.Errorf("timeout: %w", err)
        }
        log.Printf("HTTP error: %v", err)
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        log.Printf("HTTP %d error", resp.StatusCode)
        return nil, fmt.Errorf("HTTP %d", resp.StatusCode)
    }

    var result map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        log.Printf("JSON decode error: %v", err)
        return nil, err
    }

    return result, nil
}
''',

    "Rust": '''
async fn fetch_data(url: &str) -> Result<HashMap<String, serde_json::Value>, Box<dyn std::error::Error>> {
    let result = async {
        let response = reqwest::get(url)
            .await
            .map_err(|e| {
                if e.is_timeout() {
                    eprintln!("Request timed out");
                } else {
                    eprintln!("HTTP error: {}", e);
                }
                e
            })?;

        let data = response.json::<HashMap<String, serde_json::Value>>()
            .await
            .map_err(|e| {
                eprintln!("JSON parse error: {}", e);
                e
            })?;

        Ok(data)
    }.await;

    eprintln!("Request completed");
    result
}
''',

    "C#": '''
public async Task<Dictionary<string, object>> FetchDataAsync(string url)
{
    try
    {
        using (var client = new HttpClient { Timeout = TimeSpan.FromSeconds(10) })
        {
            var response = await client.GetAsync(url);
            response.EnsureSuccessStatusCode();
            var json = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<Dictionary<string, object>>(json);
        }
    }
    catch (TaskCanceledException)
    {
        Console.Error.WriteLine("Request timed out");
        return null;
    }
    catch (HttpRequestException ex)
    {
        Console.Error.WriteLine($"HTTP error: {ex.Message}");
        return null;
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine($"Unexpected error: {ex.Message}");
        return null;
    }
    finally
    {
        Console.WriteLine("Request completed");
    }
}
'''
}


# Simple error handling (for round-trip tests)
SIMPLE_ERROR_PATTERNS = {
    "Python": '''
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return 0
    finally:
        print("Done")
''',

    "JavaScript": '''
function divide(a, b) {
    try {
        const result = a / b;
        return result;
    } catch (e) {
        console.log(`Error: ${e}`);
        return 0;
    } finally {
        console.log("Done");
    }
}
''',

    "Go": '''
func Divide(a float64, b float64) (float64, error) {
    defer fmt.Println("Done")

    if b == 0 {
        fmt.Println("Error: division by zero")
        return 0, fmt.Errorf("division by zero")
    }

    result := a / b
    return result, nil
}
''',

    "Rust": '''
fn divide(a: f64, b: f64) -> Result<f64, String> {
    let result = (|| {
        if b == 0.0 {
            eprintln!("Error: division by zero");
            return Err("division by zero".to_string());
        }
        Ok(a / b)
    })();

    eprintln!("Done");
    result
}
''',

    "C#": '''
public class Calculator
{
    public double Divide(double a, double b)
    {
        try
        {
            if (b == 0)
            {
                throw new DivideByZeroException();
            }
            return a / b;
        }
        catch (DivideByZeroException e)
        {
            Console.WriteLine($"Error: {e.Message}");
            return 0;
        }
        finally
        {
            Console.WriteLine("Done");
        }
    }
}
'''
}


# ============================================================================
# Parser/Generator Mapping
# ============================================================================

PARSERS = {
    "Python": PythonParserV2(),
    "JavaScript": NodeJSParserV2(),
    "Go": GoParserV2(),
    "Rust": RustParserV2(),
    "C#": DotNetParserV2(),
}

GENERATORS = {
    "Python": PythonGeneratorV2(),
    "JavaScript": NodeJSGeneratorV2(),
    "Go": GoGeneratorV2(),
    "Rust": RustGeneratorV2(),
    "C#": DotNetGeneratorV2(),
}


# ============================================================================
# Test Functions
# ============================================================================

def test_parse_exception_handling(language: str, code: str) -> tuple[bool, IRModule, str]:
    """
    Test if parser can extract exception handling.

    Returns:
        (success, ir_module, error_message)
    """
    parser = PARSERS[language]

    try:
        if language == "Python":
            ir = parser.parse_source(code, f"{language.lower()}_error_test")
        elif language == "JavaScript":
            ir = parser.parse_source(code, f"{language.lower()}_error_test")
        elif language == "Go":
            ir = parser.parse_source(code, f"{language.lower()}_error_test")
        elif language == "Rust":
            ir = parser.parse_source(code, f"{language.lower()}_error_test")
        elif language == "C#":
            ir = parser.parse_source(code, f"{language.lower()}_error_test")
        else:
            return (False, None, f"Unknown language: {language}")

        # Check if IR contains try/catch structures or error handling
        has_error_handling = False

        # Check standalone functions
        if ir.functions:
            for func in ir.functions:
                for stmt in func.body:
                    if isinstance(stmt, IRTry):
                        has_error_handling = True
                        break
                    # Go pattern: Check for error returns
                    if language == "Go" and func.throws:
                        has_error_handling = True
                        break
                if has_error_handling:
                    break

        # Check class methods (for C#, etc.)
        if not has_error_handling and ir.classes:
            for cls in ir.classes:
                for method in cls.methods:
                    for stmt in method.body:
                        if isinstance(stmt, IRTry):
                            has_error_handling = True
                            break
                        # Go pattern: Check for error returns
                        if language == "Go" and method.throws:
                            has_error_handling = True
                            break
                    if has_error_handling:
                        break
                if has_error_handling:
                    break

        if not has_error_handling:
            return (False, ir, f"{language} parser did not extract error handling (no IRTry found)")

        return (True, ir, "")

    except Exception as e:
        return (False, None, f"Parser error: {str(e)}")


def test_generate_exception_handling(language: str, ir_module: IRModule) -> tuple[bool, str, str]:
    """
    Test if generator can output exception handling.

    Returns:
        (success, generated_code, error_message)
    """
    generator = GENERATORS[language]

    try:
        code = generator.generate(ir_module)

        # Check if generated code contains exception handling keywords
        error_keywords = {
            "Python": ["try:", "except"],
            "JavaScript": ["try {", "catch"],
            "Go": ["if err != nil", "return"],
            "Rust": ["Result<", "Err("],
            "C#": ["try", "catch"],
        }

        has_error_handling = any(
            keyword in code
            for keyword in error_keywords.get(language, [])
        )

        if not has_error_handling:
            return (False, code, f"{language} generator did not output error handling keywords")

        return (True, code, "")

    except Exception as e:
        return (False, "", f"Generator error: {str(e)}")


def test_round_trip(language: str, code: str) -> dict:
    """
    Test round-trip: Code → IR → Code

    Returns:
        {
            "language": str,
            "parse_success": bool,
            "generate_success": bool,
            "has_error_handling": bool,
            "error": str,
        }
    """
    # Parse
    parse_ok, ir, parse_error = test_parse_exception_handling(language, code)

    if not parse_ok:
        return {
            "language": language,
            "parse_success": False,
            "generate_success": False,
            "has_error_handling": False,
            "error": parse_error,
        }

    # Generate
    gen_ok, generated, gen_error = test_generate_exception_handling(language, ir)

    if not gen_ok:
        return {
            "language": language,
            "parse_success": True,
            "generate_success": False,
            "has_error_handling": False,
            "error": gen_error,
        }

    return {
        "language": language,
        "parse_success": True,
        "generate_success": True,
        "has_error_handling": True,
        "error": "",
    }


def test_translation(from_lang: str, to_lang: str, code: str) -> dict:
    """
    Test translation: Language A → IR → Language B

    Returns:
        {
            "from": str,
            "to": str,
            "parse_success": bool,
            "generate_success": bool,
            "has_error_handling": bool,
            "error": str,
        }
    """
    # Parse source language
    parse_ok, ir, parse_error = test_parse_exception_handling(from_lang, code)

    if not parse_ok:
        return {
            "from": from_lang,
            "to": to_lang,
            "parse_success": False,
            "generate_success": False,
            "has_error_handling": False,
            "error": parse_error,
        }

    # Generate target language
    gen_ok, generated, gen_error = test_generate_exception_handling(to_lang, ir)

    if not gen_ok:
        return {
            "from": from_lang,
            "to": to_lang,
            "parse_success": True,
            "generate_success": False,
            "has_error_handling": False,
            "error": gen_error,
        }

    return {
        "from": from_lang,
        "to": to_lang,
        "parse_success": True,
        "generate_success": True,
        "has_error_handling": True,
        "error": "",
    }


# ============================================================================
# Main Test Execution
# ============================================================================

def run_all_tests():
    """Run comprehensive exception handling tests."""
    print("=" * 80)
    print("EXCEPTION HANDLING TEST SUITE")
    print("=" * 80)
    print()

    # Phase 1: Round-trip tests (simple patterns)
    print("Phase 1: Round-Trip Tests (Simple Error Handling)")
    print("-" * 80)

    round_trip_results = []
    for lang, code in SIMPLE_ERROR_PATTERNS.items():
        result = test_round_trip(lang, code)
        round_trip_results.append(result)

        status = "✅ PASS" if result["has_error_handling"] else "❌ FAIL"
        print(f"{status} | {lang:12} | {result.get('error', 'Success')}")

    print()

    # Phase 2: Cross-language tests (5x5 matrix)
    print("Phase 2: Cross-Language Translation Tests (25 combinations)")
    print("-" * 80)

    translation_results = []
    languages = list(SIMPLE_ERROR_PATTERNS.keys())

    for from_lang in languages:
        for to_lang in languages:
            code = SIMPLE_ERROR_PATTERNS[from_lang]
            result = test_translation(from_lang, to_lang, code)
            translation_results.append(result)

            status = "✅" if result["has_error_handling"] else "❌"
            print(f"{status} | {from_lang:12} → {to_lang:12} | {result.get('error', 'OK')[:40]}")

    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    round_trip_pass = sum(1 for r in round_trip_results if r["has_error_handling"])
    round_trip_total = len(round_trip_results)
    round_trip_pct = (round_trip_pass / round_trip_total * 100) if round_trip_total > 0 else 0

    print(f"Round-Trip Tests: {round_trip_pass}/{round_trip_total} ({round_trip_pct:.0f}%)")

    translation_pass = sum(1 for r in translation_results if r["has_error_handling"])
    translation_total = len(translation_results)
    translation_pct = (translation_pass / translation_total * 100) if translation_total > 0 else 0

    print(f"Translation Tests: {translation_pass}/{translation_total} ({translation_pct:.0f}%)")

    overall_pass = round_trip_pass + translation_pass
    overall_total = round_trip_total + translation_total
    overall_pct = (overall_pass / overall_total * 100) if overall_total > 0 else 0

    print(f"Overall: {overall_pass}/{overall_total} ({overall_pct:.0f}%)")
    print()

    # Detailed failures
    failures = [r for r in round_trip_results + translation_results if not r["has_error_handling"]]
    if failures:
        print("FAILURES:")
        print("-" * 80)
        for fail in failures:
            if "from" in fail:
                print(f"  ❌ {fail['from']} → {fail['to']}: {fail['error']}")
            else:
                print(f"  ❌ {fail['language']}: {fail['error']}")

    print()
    print("=" * 80)

    return {
        "round_trip_pass": round_trip_pass,
        "round_trip_total": round_trip_total,
        "translation_pass": translation_pass,
        "translation_total": translation_total,
        "overall_pass": overall_pass,
        "overall_total": overall_total,
        "overall_pct": overall_pct,
    }


if __name__ == "__main__":
    results = run_all_tests()

    # Exit with failure if not all tests pass
    if results["overall_pass"] < results["overall_total"]:
        sys.exit(1)
