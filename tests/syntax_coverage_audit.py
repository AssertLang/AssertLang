#!/usr/bin/env python3
"""
Comprehensive Syntax Coverage Audit

This script tests language-specific syntax patterns across all 5 languages
to identify gaps in parser and generator support.

Goal: Achieve comprehensive coverage of common language idioms to improve
translation accuracy from current 83% to 88-93%.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2


@dataclass
class SyntaxPattern:
    """Represents a language-specific syntax pattern to test"""
    name: str
    code: str
    language: str
    category: str  # comprehension, context_manager, destructuring, etc.
    expected_features: List[str]  # What IR features we expect to see


@dataclass
class AuditResult:
    """Result of testing a syntax pattern"""
    pattern: SyntaxPattern
    success: bool
    found_features: List[str]
    missing_features: List[str]
    error: str = ""


# ============================================================================
# PYTHON SYNTAX PATTERNS
# ============================================================================

PYTHON_PATTERNS = [
    SyntaxPattern(
        name="f-strings",
        code='''
def format_greeting(name, age):
    return f"Hello {name}, you are {age} years old"
''',
        language="python",
        category="string_formatting",
        expected_features=["function", "return", "f-string"]
    ),

    SyntaxPattern(
        name="list_comprehension",
        code='''
def get_squares(numbers):
    return [x * x for x in numbers]
''',
        language="python",
        category="comprehension",
        expected_features=["function", "list_comprehension", "return"]
    ),

    SyntaxPattern(
        name="dict_comprehension",
        code='''
def create_lookup(items):
    return {item.id: item.name for item in items}
''',
        language="python",
        category="comprehension",
        expected_features=["function", "dict_comprehension", "return"]
    ),

    SyntaxPattern(
        name="set_comprehension",
        code='''
def get_unique_ids(users):
    return {user.id for user in users}
''',
        language="python",
        category="comprehension",
        expected_features=["function", "set_comprehension", "return"]
    ),

    SyntaxPattern(
        name="context_manager",
        code='''
def read_config():
    with open("config.json") as f:
        data = f.read()
    return data
''',
        language="python",
        category="context_manager",
        expected_features=["function", "with_statement", "return"]
    ),

    SyntaxPattern(
        name="decorators",
        code='''
@staticmethod
def calculate(x, y):
    return x + y

@property
def full_name(self):
    return f"{self.first} {self.last}"
''',
        language="python",
        category="decorator",
        expected_features=["decorator", "function", "property"]
    ),

    SyntaxPattern(
        name="slice_notation",
        code='''
def get_subset(items):
    first_three = items[:3]
    last_two = items[-2:]
    middle = items[1:-1]
    return middle
''',
        language="python",
        category="slice",
        expected_features=["function", "slice", "return"]
    ),

    SyntaxPattern(
        name="tuple_unpacking",
        code='''
def swap(a, b):
    a, b = b, a
    return a, b
''',
        language="python",
        category="unpacking",
        expected_features=["function", "tuple_unpacking", "return"]
    ),

    SyntaxPattern(
        name="generator_expression",
        code='''
def sum_squares(numbers):
    return sum(x * x for x in numbers)
''',
        language="python",
        category="generator",
        expected_features=["function", "generator_expression", "return"]
    ),

    SyntaxPattern(
        name="walrus_operator",
        code='''
def process_data(items):
    if (n := len(items)) > 10:
        return n
    return 0
''',
        language="python",
        category="assignment_expression",
        expected_features=["function", "walrus_operator", "if", "return"]
    ),
]


# ============================================================================
# JAVASCRIPT/TYPESCRIPT SYNTAX PATTERNS
# ============================================================================

JAVASCRIPT_PATTERNS = [
    SyntaxPattern(
        name="template_literals",
        code='''
function formatGreeting(name, age) {
    return `Hello ${name}, you are ${age} years old`;
}
''',
        language="javascript",
        category="string_formatting",
        expected_features=["function", "return", "template_literal"]
    ),

    SyntaxPattern(
        name="destructuring_object",
        code='''
function processUser({ name, email, age }) {
    return { name, email };
}
''',
        language="javascript",
        category="destructuring",
        expected_features=["function", "object_destructuring", "return"]
    ),

    SyntaxPattern(
        name="destructuring_array",
        code='''
function getFirstTwo(items) {
    const [first, second] = items;
    return [first, second];
}
''',
        language="javascript",
        category="destructuring",
        expected_features=["function", "array_destructuring", "return"]
    ),

    SyntaxPattern(
        name="spread_operator",
        code='''
function mergeArrays(arr1, arr2) {
    return [...arr1, ...arr2];
}

function mergeObjects(obj1, obj2) {
    return { ...obj1, ...obj2 };
}
''',
        language="javascript",
        category="spread",
        expected_features=["function", "spread_operator", "return"]
    ),

    SyntaxPattern(
        name="arrow_functions",
        code='''
const double = x => x * 2;
const add = (a, b) => a + b;
const process = items => items.map(x => x * 2);
''',
        language="javascript",
        category="arrow_function",
        expected_features=["arrow_function", "const"]
    ),

    SyntaxPattern(
        name="optional_chaining",
        code='''
function getUserEmail(user) {
    return user?.profile?.email;
}
''',
        language="javascript",
        category="optional_chaining",
        expected_features=["function", "optional_chaining", "return"]
    ),

    SyntaxPattern(
        name="nullish_coalescing",
        code='''
function getPort(config) {
    return config.port ?? 8080;
}
''',
        language="javascript",
        category="nullish_coalescing",
        expected_features=["function", "nullish_coalescing", "return"]
    ),

    SyntaxPattern(
        name="async_await",
        code='''
async function fetchUser(userId) {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return data;
}
''',
        language="javascript",
        category="async",
        expected_features=["async_function", "await", "return"]
    ),

    SyntaxPattern(
        name="default_parameters",
        code='''
function greet(name = "Guest", greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
''',
        language="javascript",
        category="default_params",
        expected_features=["function", "default_parameter", "return"]
    ),
]


# ============================================================================
# GO SYNTAX PATTERNS
# ============================================================================

GO_PATTERNS = [
    SyntaxPattern(
        name="defer",
        code='''
package main

func readFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()

    data, err := io.ReadAll(file)
    return err
}
''',
        language="go",
        category="defer",
        expected_features=["function", "defer", "error_handling"]
    ),

    SyntaxPattern(
        name="channels",
        code='''
package main

func sendMessages(ch chan string) {
    ch <- "Hello"
    ch <- "World"
    close(ch)
}

func receiveMessages(ch chan string) {
    for msg := range ch {
        println(msg)
    }
}
''',
        language="go",
        category="channels",
        expected_features=["function", "channel", "send", "receive", "range"]
    ),

    SyntaxPattern(
        name="select_statement",
        code='''
package main

func selectChannel(ch1, ch2 chan int) int {
    select {
    case val := <-ch1:
        return val
    case val := <-ch2:
        return val
    default:
        return 0
    }
}
''',
        language="go",
        category="select",
        expected_features=["function", "select", "channel", "receive"]
    ),

    SyntaxPattern(
        name="goroutines",
        code='''
package main

func processAsync(data []string) {
    for _, item := range data {
        go func(s string) {
            process(s)
        }(item)
    }
}
''',
        language="go",
        category="concurrency",
        expected_features=["function", "goroutine", "anonymous_function"]
    ),

    SyntaxPattern(
        name="multiple_return",
        code='''
package main

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
''',
        language="go",
        category="multiple_return",
        expected_features=["function", "multiple_return", "error_handling"]
    ),

    SyntaxPattern(
        name="type_switch",
        code='''
package main

func printType(v interface{}) {
    switch v := v.(type) {
    case int:
        println("int:", v)
    case string:
        println("string:", v)
    default:
        println("unknown")
    }
}
''',
        language="go",
        category="type_switch",
        expected_features=["function", "type_switch", "interface"]
    ),
]


# ============================================================================
# RUST SYNTAX PATTERNS
# ============================================================================

RUST_PATTERNS = [
    SyntaxPattern(
        name="pattern_matching",
        code='''
fn process_option(value: Option<i32>) -> i32 {
    match value {
        Some(x) => x * 2,
        None => 0,
    }
}
''',
        language="rust",
        category="pattern_matching",
        expected_features=["function", "match", "option"]
    ),

    SyntaxPattern(
        name="result_handling",
        code='''
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}
''',
        language="rust",
        category="result",
        expected_features=["function", "result", "error_handling"]
    ),

    SyntaxPattern(
        name="question_mark_operator",
        code='''
fn read_file(path: &str) -> Result<String, std::io::Error> {
    let content = std::fs::read_to_string(path)?;
    Ok(content)
}
''',
        language="rust",
        category="question_mark",
        expected_features=["function", "question_mark", "result"]
    ),

    SyntaxPattern(
        name="lifetimes",
        code='''
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
''',
        language="rust",
        category="lifetimes",
        expected_features=["function", "lifetime", "reference"]
    ),

    SyntaxPattern(
        name="traits",
        code='''
trait Drawable {
    fn draw(&self);
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle");
    }
}
''',
        language="rust",
        category="traits",
        expected_features=["trait", "impl", "function"]
    ),

    SyntaxPattern(
        name="macros",
        code='''
fn create_vector() -> Vec<i32> {
    vec![1, 2, 3, 4, 5]
}

fn print_debug(value: &str) {
    println!("Debug: {}", value);
}
''',
        language="rust",
        category="macros",
        expected_features=["function", "vec_macro", "println_macro"]
    ),

    SyntaxPattern(
        name="iterator_chains",
        code='''
fn process_numbers(nums: Vec<i32>) -> Vec<i32> {
    nums.iter()
        .filter(|&x| x > 0)
        .map(|&x| x * 2)
        .collect()
}
''',
        language="rust",
        category="iterators",
        expected_features=["function", "iterator", "filter", "map", "collect"]
    ),

    SyntaxPattern(
        name="if_let",
        code='''
fn unwrap_or_default(value: Option<i32>) -> i32 {
    if let Some(x) = value {
        x
    } else {
        0
    }
}
''',
        language="rust",
        category="if_let",
        expected_features=["function", "if_let", "option"]
    ),
]


# ============================================================================
# C# SYNTAX PATTERNS
# ============================================================================

CSHARP_PATTERNS = [
    SyntaxPattern(
        name="linq_method_syntax",
        code='''
public List<int> GetEvenNumbers(List<int> numbers)
{
    return numbers
        .Where(x => x % 2 == 0)
        .Select(x => x * 2)
        .ToList();
}
''',
        language="csharp",
        category="linq",
        expected_features=["function", "linq", "where", "select", "lambda"]
    ),

    SyntaxPattern(
        name="async_await",
        code='''
public async Task<User> GetUserAsync(int userId)
{
    var response = await httpClient.GetAsync($"/api/users/{userId}");
    var user = await response.Content.ReadAsAsync<User>();
    return user;
}
''',
        language="csharp",
        category="async",
        expected_features=["async_function", "await", "task", "return"]
    ),

    SyntaxPattern(
        name="properties",
        code='''
public class User
{
    public string Name { get; set; }
    public int Age { get; private set; }
    public string FullName => $"{FirstName} {LastName}";
}
''',
        language="csharp",
        category="properties",
        expected_features=["class", "auto_property", "expression_property"]
    ),

    SyntaxPattern(
        name="events",
        code='''
public class Button
{
    public event EventHandler Click;

    public void OnClick()
    {
        Click?.Invoke(this, EventArgs.Empty);
    }
}
''',
        language="csharp",
        category="events",
        expected_features=["class", "event", "function", "null_conditional"]
    ),

    SyntaxPattern(
        name="using_statement",
        code='''
public string ReadFile(string path)
{
    using (var reader = new StreamReader(path))
    {
        return reader.ReadToEnd();
    }
}
''',
        language="csharp",
        category="using",
        expected_features=["function", "using", "return"]
    ),

    SyntaxPattern(
        name="pattern_matching",
        code='''
public string Describe(object obj)
{
    return obj switch
    {
        int i => $"Integer: {i}",
        string s => $"String: {s}",
        _ => "Unknown"
    };
}
''',
        language="csharp",
        category="pattern_matching",
        expected_features=["function", "switch_expression", "pattern_matching"]
    ),

    SyntaxPattern(
        name="nullable_types",
        code='''
public int? FindUser(string name)
{
    var user = database.FindByName(name);
    return user?.Id;
}
''',
        language="csharp",
        category="nullable",
        expected_features=["function", "nullable_type", "null_conditional"]
    ),
]


# ============================================================================
# AUDIT EXECUTION
# ============================================================================

def audit_python_patterns() -> List[AuditResult]:
    """Audit Python syntax pattern support"""
    results = []
    parser = PythonParserV2()

    for pattern in PYTHON_PATTERNS:
        try:
            ir_module = parser.parse_source(pattern.code, "test")

            # Check what features we found
            found_features = []

            # Check for functions
            if ir_module.functions:
                found_features.append("function")

            # Check for comprehensions (would be in IR expressions)
            # For now, we just check if parsing succeeded
            if "comprehension" in pattern.category:
                # Check if we have any list/dict/set literals
                for func in ir_module.functions:
                    for stmt in func.body:
                        if hasattr(stmt, 'value'):
                            found_features.append(f"{pattern.category}_parsed")

            # Check for context managers (with statements)
            if "context_manager" in pattern.category:
                # Check for specific IR nodes (would need IRWith)
                pass

            missing = [f for f in pattern.expected_features if f not in found_features]

            results.append(AuditResult(
                pattern=pattern,
                success=len(missing) == 0,
                found_features=found_features,
                missing_features=missing
            ))

        except Exception as e:
            results.append(AuditResult(
                pattern=pattern,
                success=False,
                found_features=[],
                missing_features=pattern.expected_features,
                error=str(e)
            ))

    return results


def audit_javascript_patterns() -> List[AuditResult]:
    """Audit JavaScript syntax pattern support"""
    results = []
    parser = NodeJSParserV2()

    for pattern in JAVASCRIPT_PATTERNS:
        try:
            ir_module = parser.parse_source(pattern.code, "test")

            found_features = []

            if ir_module.functions:
                found_features.append("function")

            # Check for async functions
            for func in ir_module.functions:
                if func.is_async:
                    found_features.append("async_function")

            missing = [f for f in pattern.expected_features if f not in found_features]

            results.append(AuditResult(
                pattern=pattern,
                success=len(missing) == 0,
                found_features=found_features,
                missing_features=missing
            ))

        except Exception as e:
            results.append(AuditResult(
                pattern=pattern,
                success=False,
                found_features=[],
                missing_features=pattern.expected_features,
                error=str(e)
            ))

    return results


def audit_go_patterns() -> List[AuditResult]:
    """Audit Go syntax pattern support"""
    results = []
    parser = GoParserV2()

    for pattern in GO_PATTERNS:
        try:
            ir_module = parser.parse_source(pattern.code, "main")

            found_features = []

            if ir_module.functions:
                found_features.append("function")

            # Check for specific Go features
            # (would need to inspect IR for defer, channels, etc.)

            missing = [f for f in pattern.expected_features if f not in found_features]

            results.append(AuditResult(
                pattern=pattern,
                success=len(missing) == 0,
                found_features=found_features,
                missing_features=missing
            ))

        except Exception as e:
            results.append(AuditResult(
                pattern=pattern,
                success=False,
                found_features=[],
                missing_features=pattern.expected_features,
                error=str(e)
            ))

    return results


def print_audit_summary(language: str, results: List[AuditResult]):
    """Print summary of audit results"""
    print(f"\n{'='*70}")
    print(f"  {language.upper()} SYNTAX COVERAGE AUDIT")
    print(f"{'='*70}\n")

    total = len(results)
    passed = sum(1 for r in results if r.success)
    failed = total - passed

    print(f"Total patterns tested: {total}")
    print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")
    print()

    # Group by category
    by_category = {}
    for result in results:
        cat = result.pattern.category
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(result)

    for category, cat_results in sorted(by_category.items()):
        cat_passed = sum(1 for r in cat_results if r.success)
        cat_total = len(cat_results)
        status = "✅" if cat_passed == cat_total else "❌"
        print(f"{status} {category}: {cat_passed}/{cat_total}")

        for result in cat_results:
            if not result.success:
                print(f"   ❌ {result.pattern.name}")
                if result.missing_features:
                    print(f"      Missing: {', '.join(result.missing_features)}")
                if result.error:
                    print(f"      Error: {result.error[:100]}")

    print()

    # List all missing features
    all_missing = []
    for result in results:
        if not result.success:
            all_missing.extend(result.missing_features)

    if all_missing:
        unique_missing = list(set(all_missing))
        print(f"🔧 Missing Features to Implement ({len(unique_missing)}):")
        for feature in sorted(unique_missing):
            count = all_missing.count(feature)
            print(f"   - {feature} (needed by {count} pattern{'s' if count > 1 else ''})")


def main():
    """Run comprehensive syntax coverage audit"""
    print("\n" + "="*70)
    print("  ASSERTLANG SYNTAX COVERAGE AUDIT")
    print("  Goal: Identify missing patterns to improve 83% → 88-93% accuracy")
    print("="*70 + "\n")

    # Audit all languages
    python_results = audit_python_patterns()
    print_audit_summary("Python", python_results)

    javascript_results = audit_javascript_patterns()
    print_audit_summary("JavaScript", javascript_results)

    go_results = audit_go_patterns()
    print_audit_summary("Go", go_results)

    # Rust and C# would need parsers to be available
    # rust_results = audit_rust_patterns()
    # print_audit_summary("Rust", rust_results)

    # csharp_results = audit_csharp_patterns()
    # print_audit_summary("C#", csharp_results)

    # Overall summary
    all_results = python_results + javascript_results + go_results
    total = len(all_results)
    passed = sum(1 for r in all_results if r.success)

    print("\n" + "="*70)
    print("  OVERALL SUMMARY")
    print("="*70 + "\n")
    print(f"Total patterns tested: {total}")
    print(f"Overall coverage: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"Target: 90%+ coverage")
    print(f"Gap: {max(0, int(0.9 * total) - passed)} patterns need work")
    print()


if __name__ == "__main__":
    main()
