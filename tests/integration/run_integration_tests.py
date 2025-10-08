#!/usr/bin/env python3
"""
Standalone integration test runner (no pytest required)

Runs all integration tests and generates a comprehensive report.
"""

import sys
import os
import time
import json
import traceback
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import all parsers V2
from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

# Import all generators V2
from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


class TestResult:
    """Test result container"""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.duration_ms = 0
        self.metrics = {}

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} {self.name} ({self.duration_ms:.2f}ms)"


class IntegrationTestRunner:
    """Integration test runner"""

    def __init__(self):
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.results_dir = Path(__file__).parent / "results"
        self.results_dir.mkdir(exist_ok=True)

        self.parsers = {
            "python": PythonParserV2(),
            "nodejs": NodeJSParserV2(),
            "go": GoParserV2(),
            "rust": RustParserV2(),
            "dotnet": DotNetParserV2(),
        }

        self.generators = {
            "python": generate_python,
            "nodejs": generate_nodejs,
            "go": generate_go,
            "rust": generate_rust,
            "dotnet": generate_csharp,
        }

        self.source_files = {
            "python": "simple_service.py",
            "nodejs": "simple_service.js",
            "go": "simple_service.go",
            "rust": "simple_service.rs",
            "dotnet": "simple_service.cs",
        }

        self.results = []

    def run_test(self, test_name: str, test_func):
        """Run a single test and record results"""
        result = TestResult(test_name)
        start_time = time.time()

        try:
            metrics = test_func()
            result.passed = True
            result.metrics = metrics or {}
        except Exception as e:
            result.passed = False
            result.error = str(e)
            print(f"   ERROR: {e}")
            traceback.print_exc()

        result.duration_ms = (time.time() - start_time) * 1000
        self.results.append(result)
        print(result)

        return result

    def compare_ir_semantics(self, original_ir, roundtrip_ir) -> Dict[str, Any]:
        """Compare two IR modules"""
        differences = []

        if len(original_ir.functions) != len(roundtrip_ir.functions):
            differences.append(
                f"Function count: {len(original_ir.functions)} vs {len(roundtrip_ir.functions)}"
            )

        if len(original_ir.types) != len(roundtrip_ir.types):
            differences.append(
                f"Type count: {len(original_ir.types)} vs {len(roundtrip_ir.types)}"
            )

        if len(original_ir.classes) != len(roundtrip_ir.classes):
            differences.append(
                f"Class count: {len(original_ir.classes)} vs {len(roundtrip_ir.classes)}"
            )

        return {
            "match": len(differences) == 0,
            "differences": differences,
            "function_preservation": len(roundtrip_ir.functions) / max(len(original_ir.functions), 1),
            "type_preservation": len(roundtrip_ir.types) / max(len(original_ir.types), 1),
            "class_preservation": len(roundtrip_ir.classes) / max(len(original_ir.classes), 1),
        }

    # ===== ROUND-TRIP TESTS =====

    def test_python_roundtrip(self):
        """Python → IR → Python"""
        source_path = self.fixtures_dir / self.source_files["python"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        ir_module = self.parsers["python"].parse_source(source_code)
        assert ir_module is not None, "Failed to parse Python"
        assert len(ir_module.functions) > 0, "No functions extracted"

        # Generate back to Python
        generated_code = generate_python(ir_module)
        assert generated_code is not None, "Failed to generate Python"
        assert "def " in generated_code, "Missing functions"

        # Parse generated code
        roundtrip_ir = self.parsers["python"].parse_source(generated_code)
        assert roundtrip_ir is not None, "Failed to parse generated Python"

        # Compare
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        return {
            "source_functions": len(ir_module.functions),
            "target_functions": len(roundtrip_ir.functions),
            "preservation": comparison["function_preservation"],
        }

    def test_nodejs_roundtrip(self):
        """Node.js → IR → Node.js"""
        source_path = self.fixtures_dir / self.source_files["nodejs"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = self.parsers["nodejs"].parse_source(source_code)
        assert ir_module is not None

        generated_code = generate_nodejs(ir_module)
        assert generated_code is not None

        roundtrip_ir = self.parsers["nodejs"].parse_source(generated_code)
        assert roundtrip_ir is not None

        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        return {
            "source_functions": len(ir_module.functions),
            "target_functions": len(roundtrip_ir.functions),
            "preservation": comparison["function_preservation"],
        }

    def test_go_roundtrip(self):
        """Go → IR → Go"""
        source_path = self.fixtures_dir / self.source_files["go"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = self.parsers["go"].parse_source(source_code)
        assert ir_module is not None

        generated_code = generate_go(ir_module)
        assert generated_code is not None

        roundtrip_ir = self.parsers["go"].parse_source(generated_code)
        assert roundtrip_ir is not None

        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        return {
            "source_functions": len(ir_module.functions),
            "target_functions": len(roundtrip_ir.functions),
            "preservation": comparison["function_preservation"],
        }

    def test_rust_roundtrip(self):
        """Rust → IR → Rust"""
        source_path = self.fixtures_dir / self.source_files["rust"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = self.parsers["rust"].parse_source(source_code)
        assert ir_module is not None

        generated_code = generate_rust(ir_module)
        assert generated_code is not None

        roundtrip_ir = self.parsers["rust"].parse_source(generated_code)
        assert roundtrip_ir is not None

        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        return {
            "source_functions": len(ir_module.functions),
            "target_functions": len(roundtrip_ir.functions),
            "preservation": comparison["function_preservation"],
        }

    def test_dotnet_roundtrip(self):
        """.NET → IR → .NET"""
        source_path = self.fixtures_dir / self.source_files["dotnet"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = self.parsers["dotnet"].parse_source(source_code)
        assert ir_module is not None

        generated_code = generate_csharp(ir_module)
        assert generated_code is not None

        roundtrip_ir = self.parsers["dotnet"].parse_source(generated_code)
        assert roundtrip_ir is not None

        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        return {
            "source_functions": len(ir_module.functions),
            "target_functions": len(roundtrip_ir.functions),
            "preservation": comparison["function_preservation"],
        }

    # ===== CROSS-LANGUAGE TRANSLATION TESTS =====

    def test_translation(self, source_lang: str, target_lang: str):
        """Test translation from source to target language"""
        # Read source
        source_path = self.fixtures_dir / self.source_files[source_lang]
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse source
        source_ir = self.parsers[source_lang].parse_source(source_code)
        assert source_ir is not None, f"Failed to parse {source_lang}"

        # Generate target
        target_code = self.generators[target_lang](source_ir)
        assert target_code is not None, f"Failed to generate {target_lang}"

        # Parse target back to IR
        target_ir = self.parsers[target_lang].parse_source(target_code)
        assert target_ir is not None, f"Failed to parse generated {target_lang}"

        # Calculate preservation
        func_preservation = len(target_ir.functions) / max(len(source_ir.functions), 1)

        return {
            "source_functions": len(source_ir.functions),
            "target_functions": len(target_ir.functions),
            "preservation": func_preservation,
        }

    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 80)
        print("INTEGRATION TEST SUITE - Universal Code Translation System")
        print("=" * 80)

        # Round-trip tests
        print("\n🔄 ROUND-TRIP TESTS (5 tests)")
        print("-" * 80)

        self.run_test("Python → IR → Python", self.test_python_roundtrip)
        self.run_test("Node.js → IR → Node.js", self.test_nodejs_roundtrip)
        self.run_test("Go → IR → Go", self.test_go_roundtrip)
        self.run_test("Rust → IR → Rust", self.test_rust_roundtrip)
        self.run_test(".NET → IR → .NET", self.test_dotnet_roundtrip)

        # Cross-language translation tests (20 combinations)
        print("\n🔀 CROSS-LANGUAGE TRANSLATION TESTS (20 combinations)")
        print("-" * 80)

        languages = ["python", "nodejs", "go", "rust", "dotnet"]
        lang_names = {
            "python": "Python",
            "nodejs": "Node.js",
            "go": "Go",
            "rust": "Rust",
            "dotnet": ".NET",
        }

        for source_lang in languages:
            for target_lang in languages:
                if source_lang != target_lang:
                    test_name = f"{lang_names[source_lang]} → {lang_names[target_lang]}"
                    self.run_test(
                        test_name,
                        lambda s=source_lang, t=target_lang: self.test_translation(s, t)
                    )

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\nTotal: {total} tests")
        print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)")

        total_time = sum(r.duration_ms for r in self.results)
        avg_time = total_time / total if total > 0 else 0

        print(f"\n⏱️  Total Time: {total_time:.2f}ms")
        print(f"⏱️  Average Time: {avg_time:.2f}ms per test")

        # Preservation rates
        round_trip_results = [r for r in self.results if "→ IR →" in r.name and r.passed]
        if round_trip_results:
            avg_preservation = sum(
                r.metrics.get("preservation", 0) for r in round_trip_results
            ) / len(round_trip_results)
            print(f"\n📊 Average Round-Trip Preservation: {avg_preservation:.1%}")

        # Failed tests
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for r in self.results:
                if not r.passed:
                    print(f"   • {r.name}: {r.error}")

        # Save JSON report
        report = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": passed / total if total > 0 else 0,
                "total_time_ms": total_time,
                "avg_time_ms": avg_time,
            },
            "tests": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration_ms": r.duration_ms,
                    "error": r.error,
                    "metrics": r.metrics,
                }
                for r in self.results
            ],
        }

        report_path = self.results_dir / "integration_test_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Detailed report saved to: {report_path}")

        # Return exit code
        return 0 if failed == 0 else 1


def main():
    """Main entry point"""
    runner = IntegrationTestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
