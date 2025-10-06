#!/usr/bin/env python3
"""
Quick Quality Assessment - Works with Current System

Tests translation quality using simple patterns that the system can currently handle.
Focuses on measuring what DOES work vs what DOESN'T.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


# Simple patterns that SHOULD work
SIMPLE_PATTERNS = {
    "basic_function": {
        "Python": '''
def add_numbers(a, b):
    return a + b

def multiply(x, y):
    result = x * y
    return result
''',
        "JavaScript": '''
function addNumbers(a, b) {
    return a + b;
}

function multiply(x, y) {
    const result = x * y;
    return result;
}
''',
        "Go": '''
package main

func AddNumbers(a int, b int) int {
    return a + b
}

func Multiply(x int, y int) int {
    result := x * y
    return result
}
''',
        "Rust": '''
pub fn add_numbers(a: i32, b: i32) -> i32 {
    return a + b;
}

pub fn multiply(x: i32, y: i32) -> i32 {
    let result = x * y;
    result
}
''',
        "C#": '''
public class Math
{
    public static int AddNumbers(int a, int b)
    {
        return a + b;
    }

    public static int Multiply(int x, int y)
    {
        int result = x * y;
        return result;
    }
}
''',
    },

    "simple_class": {
        "Python": '''
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return self.name
''',
        "JavaScript": '''
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    getInfo() {
        return this.name;
    }
}
''',
        "Go": '''
package main

type Person struct {
    Name string
    Age  int
}

func NewPerson(name string, age int) *Person {
    return &Person{
        Name: name,
        Age:  age,
    }
}

func (p *Person) GetInfo() string {
    return p.Name
}
''',
        "Rust": '''
pub struct Person {
    pub name: String,
    pub age: i32,
}

impl Person {
    pub fn new(name: String, age: i32) -> Self {
        Person { name, age }
    }

    pub fn get_info(&self) -> String {
        self.name.clone()
    }
}
''',
        "C#": '''
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public string GetInfo()
    {
        return Name;
    }
}
''',
    },
}


def test_single_translation(source_lang, target_lang, pattern_name, source_code, verbose=False):
    """Test a single translation and measure quality."""
    parsers = {
        "Python": PythonParserV2(),
        "JavaScript": NodeJSParserV2(),
        "Go": GoParserV2(),
        "Rust": RustParserV2(),
        "C#": DotNetParserV2(),
    }

    generators = {
        "Python": generate_python,
        "JavaScript": lambda ir: generate_nodejs(ir, typescript=False),
        "Go": generate_go,
        "Rust": generate_rust,
        "C#": generate_csharp,
    }

    try:
        # Parse
        parser = parsers[source_lang]
        ir = parser.parse_source(source_code, "test")

        if not ir or (len(ir.functions) == 0 and len(ir.classes) == 0):
            return {"success": False, "error": "Parse failed - no IR generated"}

        # Generate
        generator = generators[target_lang]
        generated = generator(ir)

        if not generated or len(generated.strip()) == 0:
            return {"success": False, "error": "Generation failed - empty output"}

        # Quality checks
        issues = []
        score = 100

        # Check for placeholders
        if "<unknown>" in generated.lower():
            issues.append("Contains <unknown> placeholders")
            score -= 30

        # Check function count preservation
        source_func_count = len(ir.functions)
        if source_func_count > 0:
            # Count functions in generated code
            target_func_count = 0
            if target_lang == "Python":
                target_func_count = generated.count("def ")
            elif target_lang in ["JavaScript", "TypeScript"]:
                target_func_count = generated.count("function ") + generated.count(" => ")
            elif target_lang == "Go":
                target_func_count = generated.count("func ")
            elif target_lang == "Rust":
                target_func_count = generated.count("fn ") + generated.count("pub fn ")
            elif target_lang == "C#":
                target_func_count = generated.count(" static ") + generated.count(" public ")

            if target_func_count < source_func_count:
                lost = source_func_count - target_func_count
                issues.append(f"Lost {lost} function(s)")
                score -= 20 * lost

        # Check class count preservation
        source_class_count = len(ir.classes)
        if source_class_count > 0:
            target_class_count = generated.count("class ")
            if target_lang == "Go":
                target_class_count = generated.count("type ") + generated.count("struct ")

            if target_class_count < source_class_count:
                lost = source_class_count - target_class_count
                issues.append(f"Lost {lost} class(es)")
                score -= 20 * lost

        # Check syntax validity
        if target_lang == "Python":
            if generated.count("(") != generated.count(")"):
                issues.append("Unbalanced parentheses")
                score -= 20
        elif target_lang in ["JavaScript", "Go", "Rust", "C#"]:
            if generated.count("{") != generated.count("}"):
                issues.append("Unbalanced braces")
                score -= 20

        # Determine quality level
        if score >= 90:
            level = "Excellent"
        elif score >= 70:
            level = "Good"
        elif score >= 50:
            level = "Fair"
        else:
            level = "Poor"

        result = {
            "success": True,
            "score": max(0, score),
            "level": level,
            "issues": issues,
            "source_funcs": source_func_count,
            "source_classes": source_class_count,
            "generated_lines": len(generated.split('\n')),
        }

        if verbose:
            print(f"\n{'='*60}")
            print(f"{source_lang} → {target_lang} ({pattern_name})")
            print(f"{'='*60}")
            print(f"Score: {score}% ({level})")
            print(f"Functions: {source_func_count}")
            print(f"Classes: {source_class_count}")
            if issues:
                print(f"Issues: {', '.join(issues)}")
            print(f"\nGenerated code sample (first 200 chars):")
            print(generated[:200])

        return result

    except Exception as e:
        return {"success": False, "error": str(e)[:100]}


def run_quality_matrix():
    """Run quality assessment on all combinations."""
    print("\n" + "="*80)
    print("QUICK QUALITY ASSESSMENT - SIMPLE PATTERNS")
    print("="*80)
    print("\nTesting 25 language combinations × 2 patterns = 50 tests\n")

    languages = ["Python", "JavaScript", "Go", "Rust", "C#"]
    patterns = list(SIMPLE_PATTERNS.keys())

    # Results matrix
    results = {}
    for source in languages:
        results[source] = {}
        for target in languages:
            results[source][target] = {}

    # Run tests
    total = 0
    excellent = 0
    good = 0
    fair = 0
    poor = 0
    errors = 0

    for source in languages:
        print(f"\n{source} → ALL:")
        for target in languages:
            print(f"  → {target:12s}", end=" ", flush=True)

            pattern_results = []
            for pattern_name in patterns:
                source_code = SIMPLE_PATTERNS[pattern_name].get(source)
                if not source_code:
                    continue

                result = test_single_translation(source, target, pattern_name, source_code)

                if result["success"]:
                    total += 1
                    level = result["level"]

                    if level == "Excellent":
                        excellent += 1
                    elif level == "Good":
                        good += 1
                    elif level == "Fair":
                        fair += 1
                    else:
                        poor += 1

                    pattern_results.append(result["score"])
                else:
                    errors += 1
                    pattern_results.append(0)

            # Average score for this combination
            avg_score = sum(pattern_results) / len(pattern_results) if pattern_results else 0

            if avg_score >= 90:
                print(f"✅ {avg_score:5.1f}% (Excellent)")
            elif avg_score >= 70:
                print(f"🟡 {avg_score:5.1f}% (Good)")
            elif avg_score >= 50:
                print(f"🟠 {avg_score:5.1f}% (Fair)")
            elif avg_score > 0:
                print(f"🔴 {avg_score:5.1f}% (Poor)")
            else:
                print(f"❌ ERROR")

            results[source][target]["avg_score"] = avg_score

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nTotal translations: {total}")
    print(f"Errors: {errors}")
    print(f"\nQuality Distribution:")
    print(f"  Excellent (90-100%): {excellent:3d} ({100*excellent//total if total > 0 else 0}%)")
    print(f"  Good      (70-89%):  {good:3d} ({100*good//total if total > 0 else 0}%)")
    print(f"  Fair      (50-69%):  {fair:3d} ({100*fair//total if total > 0 else 0}%)")
    print(f"  Poor      (<50%):    {poor:3d} ({100*poor//total if total > 0 else 0}%)")

    production_ready = excellent + good
    print(f"\nProduction-Ready: {production_ready}/{total} ({100*production_ready//total if total > 0 else 0}%)")

    # Matrix visualization
    print("\n" + "="*80)
    print("QUALITY MATRIX (Average Score %)")
    print("="*80)
    print("\n        ", end="")
    for target in languages:
        print(f"{target[:4]:>8}", end="")
    print("\n" + "-"*60)

    for source in languages:
        print(f"{source[:8]:>8}", end="")
        for target in languages:
            avg = results[source][target].get("avg_score", 0)
            if avg >= 90:
                print(f" {avg:6.1f}✅", end="")
            elif avg >= 70:
                print(f" {avg:6.1f}🟡", end="")
            elif avg >= 50:
                print(f" {avg:6.1f}🟠", end="")
            elif avg > 0:
                print(f" {avg:6.1f}🔴", end="")
            else:
                print(f"    ❌  ", end="")
        print()

    # Production readiness assessment
    print("\n" + "="*80)
    print("PRODUCTION READINESS ASSESSMENT")
    print("="*80)

    overall_percentage = production_ready / total * 100 if total > 0 else 0

    if overall_percentage >= 80:
        status = "✅ PRODUCTION READY"
        recommendation = "System is ready for real-world use"
    elif overall_percentage >= 60:
        status = "🟡 MOSTLY READY"
        recommendation = "Address key issues before production"
    elif overall_percentage >= 40:
        status = "🟠 NEEDS WORK"
        recommendation = "Significant improvements required"
    else:
        status = "🔴 NOT READY"
        recommendation = "Major fixes needed before production use"

    print(f"\nStatus: {status}")
    print(f"Overall Quality: {overall_percentage:.1f}%")
    print(f"Recommendation: {recommendation}")

    # Identify worst performers
    print("\n" + "="*80)
    print("WEAKEST COMBINATIONS (Need Attention)")
    print("="*80)

    all_combos = []
    for source in languages:
        for target in languages:
            avg = results[source][target].get("avg_score", 0)
            all_combos.append((source, target, avg))

    worst = sorted(all_combos, key=lambda x: x[2])[:10]

    print("\nBottom 10 combinations:")
    for i, (source, target, score) in enumerate(worst, 1):
        print(f"{i:2d}. {source:12s} → {target:12s}: {score:5.1f}%")

    # Best performers
    print("\n" + "="*80)
    print("STRONGEST COMBINATIONS")
    print("="*80)

    best = sorted(all_combos, key=lambda x: -x[2])[:10]

    print("\nTop 10 combinations:")
    for i, (source, target, score) in enumerate(best, 1):
        print(f"{i:2d}. {source:12s} → {target:12s}: {score:5.1f}%")


if __name__ == "__main__":
    run_quality_matrix()
