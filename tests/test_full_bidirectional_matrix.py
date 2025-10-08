#!/usr/bin/env python3
"""
Full Bidirectional Translation Matrix Test

Tests ALL 25 combinations: 5 source languages × 5 target languages
Goal: ANY real code → PW DSL → ANY target language

This is the core test for the vision: PW as universal intermediate language
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


class BidirectionalMatrixTester:
    """Tests all 25 language combinations."""

    def __init__(self):
        self.parsers = {
            "Python": PythonParserV2(),
            "JavaScript": NodeJSParserV2(),
            "Go": GoParserV2(),
            "Rust": RustParserV2(),
            "C#": DotNetParserV2(),
        }

        self.generators = {
            "Python": generate_python,
            "JavaScript": lambda ir: generate_nodejs(ir, typescript=False),
            "TypeScript": lambda ir: generate_nodejs(ir, typescript=True),
            "Go": generate_go,
            "Rust": generate_rust,
            "C#": generate_csharp,
        }

        self.test_code = {
            "Python": '''
def calculate_discount(price, percent):
    """Calculate discount price."""
    discount = price * (percent / 100)
    final_price = price - discount
    return final_price

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def apply_discount(self, percent):
        return calculate_discount(self.price, percent)
''',
            "JavaScript": '''
function calculateDiscount(price, percent) {
    // Calculate discount price
    const discount = price * (percent / 100);
    const finalPrice = price - discount;
    return finalPrice;
}

class Product {
    constructor(name, price) {
        this.name = name;
        this.price = price;
    }

    applyDiscount(percent) {
        return calculateDiscount(this.price, percent);
    }
}
''',
            "Go": '''
package main

type Product struct {
    Name string
    Price float64
}

func CalculateDiscount(price float64, percent float64) float64 {
    discount := price * (percent / 100)
    finalPrice := price - discount
    return finalPrice
}

func (p *Product) ApplyDiscount(percent float64) float64 {
    return CalculateDiscount(p.Price, percent)
}
''',
            "Rust": '''
pub struct Product {
    pub name: String,
    pub price: f64,
}

pub fn calculate_discount(price: f64, percent: f64) -> f64 {
    let discount = price * (percent / 100.0);
    let final_price = price - discount;
    final_price
}

impl Product {
    pub fn new(name: String, price: f64) -> Self {
        Product { name, price }
    }

    pub fn apply_discount(&self, percent: f64) -> f64 {
        calculate_discount(self.price, percent)
    }
}
''',
            "C#": '''
using System;

public class Product
{
    public string Name { get; set; }
    public double Price { get; set; }

    public Product(string name, double price)
    {
        Name = name;
        Price = price;
    }

    public double ApplyDiscount(double percent)
    {
        return CalculateDiscount(Price, percent);
    }

    public static double CalculateDiscount(double price, double percent)
    {
        double discount = price * (percent / 100);
        double finalPrice = price - discount;
        return finalPrice;
    }
}
''',
        }

        self.results = []
        self.success_matrix = {}

    def test_combination(self, source_lang, target_lang):
        """Test one source → PW → target combination."""
        print(f"\n{'='*70}")
        print(f"Testing: {source_lang} → PW → {target_lang}")
        print(f"{'='*70}")

        try:
            # Step 1: Parse source code → PW (IR)
            source_code = self.test_code.get(source_lang)
            if not source_code:
                print(f"❌ No test code for {source_lang}")
                return False

            parser = self.parsers.get(source_lang)
            if not parser:
                print(f"❌ No parser for {source_lang}")
                return False

            print(f"Step 1: Parsing {source_lang} code...")
            ir = parser.parse_source(source_code, "test")

            # Validate IR
            func_count = len(ir.functions)
            class_count = len(ir.classes)
            print(f"  ✓ Parsed: {func_count} function(s), {class_count} class(es)")

            if func_count == 0 and class_count == 0:
                print(f"  ❌ No functions or classes extracted")
                return False

            # Step 2: Generate target code from PW (IR)
            generator = self.generators.get(target_lang)
            if not generator:
                print(f"❌ No generator for {target_lang}")
                return False

            print(f"Step 2: Generating {target_lang} code from IR...")
            generated = generator(ir)

            # Validate generated code
            if not generated or len(generated.strip()) == 0:
                print(f"  ❌ Generated empty code")
                return False

            print(f"  ✓ Generated {len(generated)} characters")

            # Check for common failure patterns
            failures = []

            if "<unknown>" in generated.lower():
                failures.append("Contains <unknown> placeholders")

            if "undefined" in generated and target_lang in ["JavaScript", "TypeScript"]:
                failures.append("Contains undefined references")

            # Check for syntax validity markers
            if target_lang == "Python":
                if "def " not in generated and "class " not in generated:
                    failures.append("No Python functions/classes found")
            elif target_lang in ["JavaScript", "TypeScript"]:
                if "function " not in generated and "class " not in generated:
                    failures.append("No JS functions/classes found")
            elif target_lang == "Go":
                if "func " not in generated:
                    failures.append("No Go functions found")
            elif target_lang == "Rust":
                if "fn " not in generated and "impl " not in generated:
                    failures.append("No Rust functions found")
            elif target_lang == "C#":
                if "class " not in generated:
                    failures.append("No C# classes found")

            # Report results
            if failures:
                print(f"  ⚠️  Issues detected:")
                for failure in failures:
                    print(f"    - {failure}")
                print(f"\n  Generated code sample (first 300 chars):")
                print(f"  {generated[:300]}")
                return False

            print(f"  ✅ Generated code looks valid")
            print(f"\n  Sample output (first 200 chars):")
            print(f"  {generated[:200]}")

            return True

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_full_matrix(self):
        """Test all 25 combinations."""
        print("\n" + "="*70)
        print("FULL BIDIRECTIONAL TRANSLATION MATRIX TEST")
        print("="*70)
        print("\nTesting ALL 25 combinations: 5 source × 5 target languages")
        print("Goal: ANY code → PW → ANY language\n")

        source_languages = ["Python", "JavaScript", "Go", "Rust", "C#"]
        target_languages = ["Python", "JavaScript", "Go", "Rust", "C#"]

        total = 0
        passed = 0

        for source in source_languages:
            self.success_matrix[source] = {}
            for target in target_languages:
                total += 1
                success = self.test_combination(source, target)
                self.success_matrix[source][target] = success

                if success:
                    passed += 1
                    self.results.append((source, target, "✅ PASS"))
                else:
                    self.results.append((source, target, "❌ FAIL"))

        # Print matrix
        self.print_matrix()

        # Print summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)

        print(f"\nTotal combinations tested: {total}")
        print(f"Successful translations: {passed}")
        print(f"Failed translations: {total - passed}")
        print(f"Success rate: {100*passed//total}%")

        # Group results by source language
        print("\n" + "="*70)
        print("RESULTS BY SOURCE LANGUAGE")
        print("="*70)

        for source in source_languages:
            targets_passed = sum(1 for t in target_languages if self.success_matrix[source][t])
            print(f"\n{source} → ALL languages:")
            print(f"  {targets_passed}/{len(target_languages)} successful translations ({100*targets_passed//len(target_languages)}%)")
            for target in target_languages:
                status = "✅" if self.success_matrix[source][target] else "❌"
                print(f"    {status} → {target}")

        # Identify gaps
        print("\n" + "="*70)
        print("GAPS TO FIX")
        print("="*70)

        failures = [(s, t) for s, t, r in self.results if "FAIL" in r]

        if failures:
            print(f"\nFound {len(failures)} failing combinations:")
            for source, target in failures:
                print(f"  ❌ {source} → {target}")
        else:
            print("\n🎉 NO GAPS! All 25 combinations working!")

        return passed == total

    def print_matrix(self):
        """Print visual matrix of results."""
        print("\n" + "="*70)
        print("TRANSLATION MATRIX")
        print("="*70)

        source_languages = ["Python", "JavaScript", "Go", "Rust", "C#"]
        target_languages = ["Python", "JS", "Go", "Rust", "C#"]

        # Header
        print("\n        ", end="")
        for target in target_languages:
            print(f"{target:>10}", end="")
        print("\n" + "-"*70)

        # Rows
        for source in source_languages:
            print(f"{source:>8} ", end="")
            for target in ["Python", "JavaScript", "Go", "Rust", "C#"]:
                status = "✅" if self.success_matrix[source][target] else "❌"
                print(f"{status:>10}", end="")
            print()


def main():
    tester = BidirectionalMatrixTester()
    success = tester.run_full_matrix()

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
