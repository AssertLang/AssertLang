"""
Performance Benchmarks for Universal Code Translation System

Measures:
1. Translation speed (parsing + generation)
2. Memory usage
3. Accuracy metrics
4. Type inference accuracy
5. Code size comparison
"""

import pytest
import time
import json
from pathlib import Path
from typing import Dict, List, Any
import tracemalloc

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


class TestTranslationSpeed:
    """Measure translation speed for each language combination"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"

    @pytest.fixture(scope="class")
    def source_files(self):
        return {
            "python": "simple_service.py",
            "nodejs": "simple_service.js",
            "go": "simple_service.go",
            "rust": "simple_service.rs",
            "dotnet": "simple_service.cs",
        }

    def measure_parse_time(self, parser, code: str) -> Dict[str, Any]:
        """Measure parsing time"""
        start_time = time.time()
        tracemalloc.start()

        ir_module = parser.parse(code)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()

        return {
            "time_ms": (end_time - start_time) * 1000,
            "memory_kb": peak / 1024,
            "success": ir_module is not None,
            "functions": len(ir_module.functions) if ir_module else 0,
            "types": len(ir_module.types) if ir_module else 0,
            "classes": len(ir_module.classes) if ir_module else 0,
        }

    def measure_generate_time(self, generator, ir_module) -> Dict[str, Any]:
        """Measure generation time"""
        start_time = time.time()
        tracemalloc.start()

        generated_code = generator(ir_module)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()

        return {
            "time_ms": (end_time - start_time) * 1000,
            "memory_kb": peak / 1024,
            "success": generated_code is not None,
            "code_size": len(generated_code) if generated_code else 0,
        }

    def test_python_parsing_speed(self, fixtures_dir, source_files):
        """Benchmark Python parsing"""
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = PythonParserV2()
        results = self.measure_parse_time(parser, code)

        assert results["success"]
        assert results["time_ms"] < 1000, f"Parsing too slow: {results['time_ms']:.2f}ms"

        print(f"\n📊 Python parsing: {results['time_ms']:.2f}ms, {results['memory_kb']:.2f}KB")
        print(f"   Extracted: {results['functions']} functions, {results['classes']} classes")

    def test_nodejs_parsing_speed(self, fixtures_dir, source_files):
        """Benchmark Node.js parsing"""
        source_path = fixtures_dir / source_files["nodejs"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = NodeJSParserV2()
        results = self.measure_parse_time(parser, code)

        assert results["success"]
        assert results["time_ms"] < 1000

        print(f"\n📊 Node.js parsing: {results['time_ms']:.2f}ms, {results['memory_kb']:.2f}KB")

    def test_go_parsing_speed(self, fixtures_dir, source_files):
        """Benchmark Go parsing"""
        source_path = fixtures_dir / source_files["go"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = GoParserV2()
        results = self.measure_parse_time(parser, code)

        assert results["success"]
        assert results["time_ms"] < 1000

        print(f"\n📊 Go parsing: {results['time_ms']:.2f}ms, {results['memory_kb']:.2f}KB")

    def test_rust_parsing_speed(self, fixtures_dir, source_files):
        """Benchmark Rust parsing"""
        source_path = fixtures_dir / source_files["rust"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = RustParserV2()
        results = self.measure_parse_time(parser, code)

        assert results["success"]
        assert results["time_ms"] < 1000

        print(f"\n📊 Rust parsing: {results['time_ms']:.2f}ms, {results['memory_kb']:.2f}KB")

    def test_dotnet_parsing_speed(self, fixtures_dir, source_files):
        """Benchmark .NET parsing"""
        source_path = fixtures_dir / source_files["dotnet"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = DotNetParserV2()
        results = self.measure_parse_time(parser, code)

        assert results["success"]
        assert results["time_ms"] < 1000

        print(f"\n📊 .NET parsing: {results['time_ms']:.2f}ms, {results['memory_kb']:.2f}KB")

    def test_generation_speed_all_languages(self, fixtures_dir, source_files):
        """Benchmark code generation for all languages"""
        # Use Python as source
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            code = f.read()

        parser = PythonParserV2()
        ir_module = parser.parse(code)

        generators = {
            "Python": generate_python,
            "Node.js": generate_nodejs,
            "Go": generate_go,
            "Rust": generate_rust,
            "C#": generate_csharp,
        }

        print("\n📊 Code generation benchmarks:")
        for lang, generator in generators.items():
            results = self.measure_generate_time(generator, ir_module)
            assert results["success"], f"{lang} generation failed"
            assert results["time_ms"] < 500, f"{lang} generation too slow: {results['time_ms']:.2f}ms"

            print(f"   {lang}: {results['time_ms']:.2f}ms, {results['code_size']} bytes")


class TestAccuracyMetrics:
    """Measure translation accuracy"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"

    def calculate_preservation_rate(self, source_ir, target_ir) -> Dict[str, float]:
        """Calculate what percentage of constructs are preserved"""
        return {
            "function_preservation": len(target_ir.functions) / max(len(source_ir.functions), 1),
            "type_preservation": len(target_ir.types) / max(len(source_ir.types), 1),
            "class_preservation": len(target_ir.classes) / max(len(source_ir.classes), 1),
        }

    def test_python_to_go_accuracy(self, fixtures_dir):
        """Measure Python → Go translation accuracy"""
        source_path = fixtures_dir / "simple_service.py"
        with open(source_path, 'r') as f:
            python_code = f.read()

        # Parse source
        python_parser = PythonParserV2()
        source_ir = python_parser.parse(python_code)

        # Generate target
        go_code = generate_go(source_ir)

        # Parse target
        go_parser = GoParserV2()
        target_ir = go_parser.parse(go_code)

        # Calculate accuracy
        metrics = self.calculate_preservation_rate(source_ir, target_ir)

        print(f"\n📊 Python → Go Accuracy:")
        print(f"   Functions: {metrics['function_preservation']:.1%}")
        print(f"   Types: {metrics['type_preservation']:.1%}")
        print(f"   Classes: {metrics['class_preservation']:.1%}")

        assert metrics["function_preservation"] >= 0.8, "Too many functions lost"

    def test_go_to_rust_accuracy(self, fixtures_dir):
        """Measure Go → Rust translation accuracy"""
        source_path = fixtures_dir / "simple_service.go"
        with open(source_path, 'r') as f:
            go_code = f.read()

        go_parser = GoParserV2()
        source_ir = go_parser.parse(go_code)

        rust_code = generate_rust(source_ir)

        rust_parser = RustParserV2()
        target_ir = rust_parser.parse(rust_code)

        metrics = self.calculate_preservation_rate(source_ir, target_ir)

        print(f"\n📊 Go → Rust Accuracy:")
        print(f"   Functions: {metrics['function_preservation']:.1%}")
        print(f"   Types: {metrics['type_preservation']:.1%}")

        assert metrics["function_preservation"] >= 0.8

    def test_nodejs_to_python_accuracy(self, fixtures_dir):
        """Measure Node.js → Python translation accuracy"""
        source_path = fixtures_dir / "simple_service.js"
        with open(source_path, 'r') as f:
            nodejs_code = f.read()

        nodejs_parser = NodeJSParserV2()
        source_ir = nodejs_parser.parse(nodejs_code)

        python_code = generate_python(source_ir)

        python_parser = PythonParserV2()
        target_ir = python_parser.parse(python_code)

        metrics = self.calculate_preservation_rate(source_ir, target_ir)

        print(f"\n📊 Node.js → Python Accuracy:")
        print(f"   Functions: {metrics['function_preservation']:.1%}")
        print(f"   Classes: {metrics['class_preservation']:.1%}")

        # Node.js often has more functions due to class methods being separate
        assert metrics["function_preservation"] >= 0.7


class TestEndToEndPerformance:
    """Measure complete translation pipeline performance"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"

    def test_full_translation_pipeline(self, fixtures_dir):
        """Benchmark full pipeline: Source → IR → Target for all combinations"""
        source_files = {
            "python": "simple_service.py",
            "nodejs": "simple_service.js",
            "go": "simple_service.go",
            "rust": "simple_service.rs",
            "dotnet": "simple_service.cs",
        }

        parsers = {
            "python": PythonParserV2(),
            "nodejs": NodeJSParserV2(),
            "go": GoParserV2(),
            "rust": RustParserV2(),
            "dotnet": DotNetParserV2(),
        }

        generators = {
            "python": generate_python,
            "nodejs": generate_nodejs,
            "go": generate_go,
            "rust": generate_rust,
            "dotnet": generate_csharp,
        }

        results = []

        # Test a subset of combinations for performance
        test_combinations = [
            ("python", "go"),
            ("python", "rust"),
            ("nodejs", "python"),
            ("go", "rust"),
            ("rust", "python"),
        ]

        print("\n📊 Full Pipeline Benchmarks:")
        for source_lang, target_lang in test_combinations:
            # Read source
            source_path = fixtures_dir / source_files[source_lang]
            with open(source_path, 'r') as f:
                source_code = f.read()

            # Measure full pipeline
            start_time = time.time()
            tracemalloc.start()

            # Parse
            ir_module = parsers[source_lang].parse(source_code)

            # Generate
            target_code = generators[target_lang](ir_module)

            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()

            total_time = (end_time - start_time) * 1000
            memory_used = peak / 1024

            result = {
                "source": source_lang,
                "target": target_lang,
                "time_ms": total_time,
                "memory_kb": memory_used,
                "success": target_code is not None,
            }
            results.append(result)

            print(f"   {source_lang.capitalize()} → {target_lang.capitalize()}: "
                  f"{total_time:.2f}ms, {memory_used:.2f}KB")

            # Assert performance requirements
            assert total_time < 2000, f"Pipeline too slow: {total_time:.2f}ms"
            assert memory_used < 50000, f"Too much memory: {memory_used:.2f}KB"

        # Calculate averages
        avg_time = sum(r["time_ms"] for r in results) / len(results)
        avg_memory = sum(r["memory_kb"] for r in results) / len(results)

        print(f"\n📊 Average Performance:")
        print(f"   Time: {avg_time:.2f}ms")
        print(f"   Memory: {avg_memory:.2f}KB")
        print(f"   Success rate: {sum(1 for r in results if r['success'])}/{len(results)}")


class TestCodeQuality:
    """Measure generated code quality metrics"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"

    def test_generated_code_size(self, fixtures_dir):
        """Compare generated code sizes across languages"""
        source_path = fixtures_dir / "simple_service.py"
        with open(source_path, 'r') as f:
            python_code = f.read()

        parser = PythonParserV2()
        ir_module = parser.parse(python_code)

        generators = {
            "Python": generate_python,
            "Node.js": generate_nodejs,
            "Go": generate_go,
            "Rust": generate_rust,
            "C#": generate_csharp,
        }

        print("\n📊 Generated Code Sizes:")
        sizes = {}
        for lang, generator in generators.items():
            code = generator(ir_module)
            size = len(code)
            sizes[lang] = size
            lines = code.count('\n')
            print(f"   {lang}: {size} bytes, {lines} lines")

        # Verify reasonable sizes
        for lang, size in sizes.items():
            assert size > 0, f"{lang} generated empty code"
            assert size < 100000, f"{lang} generated excessively large code"

    def test_syntax_validity(self, fixtures_dir):
        """Verify generated code has valid syntax (basic check)"""
        source_path = fixtures_dir / "simple_service.py"
        with open(source_path, 'r') as f:
            python_code = f.read()

        parser = PythonParserV2()
        ir_module = parser.parse(python_code)

        # Generate Python and verify it's parseable
        generated_python = generate_python(ir_module)
        roundtrip_ir = parser.parse(generated_python)
        assert roundtrip_ir is not None, "Generated Python has syntax errors"

        # Generate Node.js and do basic checks
        generated_nodejs = generate_nodejs(ir_module)
        assert "{" in generated_nodejs and "}" in generated_nodejs, "Missing braces in Node.js"
        assert "function" in generated_nodejs or "class" in generated_nodejs, "Missing functions/classes"

        # Generate Go and do basic checks
        generated_go = generate_go(ir_module)
        assert "func " in generated_go, "Missing functions in Go"
        assert "package" in generated_go, "Missing package declaration"

        print("\n✅ All generated code passes basic syntax checks")


if __name__ == "__main__":
    # Save results to file
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    pytest.main([__file__, "-v", "-s", f"--json-report", f"--json-report-file={results_dir}/benchmarks.json"])
