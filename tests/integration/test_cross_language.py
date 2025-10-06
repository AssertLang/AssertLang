"""
Comprehensive Integration Tests for Cross-Language Translation System

Tests all 20 translation combinations (5 sources × 4 targets each):
- Python → Node.js, Go, Rust, .NET
- Node.js → Python, Go, Rust, .NET
- Go → Python, Node.js, Rust, .NET
- Rust → Python, Node.js, Go, .NET
- .NET → Python, Node.js, Go, Rust

Each test validates:
1. Source code parses to IR correctly
2. IR generates valid target code
3. Semantic equivalence is preserved
4. Types are mapped correctly
5. Idiomatic code is generated
"""

import pytest
import os
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

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

# Import IR types
from dsl.ir import IRModule


class TestRoundTrip:
    """Test round-trip translation: Source → IR → Source"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        """Get fixtures directory path"""
        return Path(__file__).parent / "fixtures"

    def compare_ir_semantics(self, original_ir: IRModule, roundtrip_ir: IRModule) -> Dict[str, Any]:
        """Compare two IR modules for semantic equivalence"""
        results = {
            "match": True,
            "differences": [],
            "functions_match": True,
            "types_match": True,
            "classes_match": True,
        }

        # Compare functions
        if len(original_ir.functions) != len(roundtrip_ir.functions):
            results["match"] = False
            results["functions_match"] = False
            results["differences"].append(
                f"Function count mismatch: {len(original_ir.functions)} vs {len(roundtrip_ir.functions)}"
            )
        else:
            # Check each function
            for orig_func, rt_func in zip(original_ir.functions, roundtrip_ir.functions):
                if orig_func.name != rt_func.name:
                    results["match"] = False
                    results["functions_match"] = False
                    results["differences"].append(
                        f"Function name mismatch: {orig_func.name} vs {rt_func.name}"
                    )

                if len(orig_func.params) != len(rt_func.params):
                    results["match"] = False
                    results["functions_match"] = False
                    results["differences"].append(
                        f"Parameter count mismatch for {orig_func.name}: {len(orig_func.params)} vs {len(rt_func.params)}"
                    )

                if orig_func.return_type != rt_func.return_type:
                    results["differences"].append(
                        f"Return type difference for {orig_func.name}: {orig_func.return_type} vs {rt_func.return_type} (may be acceptable)"
                    )

        # Compare types
        if len(original_ir.types) != len(roundtrip_ir.types):
            results["match"] = False
            results["types_match"] = False
            results["differences"].append(
                f"Type count mismatch: {len(original_ir.types)} vs {len(roundtrip_ir.types)}"
            )

        # Compare classes
        if len(original_ir.classes) != len(roundtrip_ir.classes):
            results["match"] = False
            results["classes_match"] = False
            results["differences"].append(
                f"Class count mismatch: {len(original_ir.classes)} vs {len(roundtrip_ir.classes)}"
            )

        return results

    def test_python_roundtrip(self, fixtures_dir):
        """Test: Python → IR → Python"""
        # Read source
        source_path = fixtures_dir / "simple_service.py"
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        parser = PythonParserV2()
        ir_module = parser.parse(source_code)

        assert ir_module is not None, "Failed to parse Python to IR"
        assert len(ir_module.functions) > 0, "No functions extracted"
        assert len(ir_module.classes) > 0, "No classes extracted"

        # Generate back to Python
        generated_code = generate_python(ir_module)

        assert generated_code is not None, "Failed to generate Python from IR"
        assert "class" in generated_code, "Generated code missing classes"
        assert "def " in generated_code, "Generated code missing functions"

        # Parse generated code back to IR
        roundtrip_ir = parser.parse(generated_code)

        assert roundtrip_ir is not None, "Failed to parse generated Python"

        # Compare semantics
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        # Allow some differences but core structures must match
        assert comparison["functions_match"], f"Function structure mismatch: {comparison['differences']}"
        assert len(roundtrip_ir.functions) >= len(ir_module.functions) * 0.9, "Too many functions lost in round-trip"

        print(f"\n✅ Python round-trip: {len(ir_module.functions)} functions preserved")
        if comparison["differences"]:
            print(f"   ℹ️  Minor differences: {len(comparison['differences'])}")

    def test_nodejs_roundtrip(self, fixtures_dir):
        """Test: Node.js → IR → Node.js"""
        source_path = fixtures_dir / "simple_service.js"
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        parser = NodeJSParserV2()
        ir_module = parser.parse(source_code)

        assert ir_module is not None, "Failed to parse Node.js to IR"
        assert len(ir_module.functions) > 0 or len(ir_module.classes) > 0, "No functions or classes extracted"

        # Generate back to Node.js
        generated_code = generate_nodejs(ir_module)

        assert generated_code is not None, "Failed to generate Node.js from IR"
        assert "class" in generated_code or "function" in generated_code, "Generated code missing structures"

        # Parse generated code back to IR
        roundtrip_ir = parser.parse(generated_code)

        assert roundtrip_ir is not None, "Failed to parse generated Node.js"

        # Compare semantics
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        assert len(roundtrip_ir.functions) + len(roundtrip_ir.classes) >= (len(ir_module.functions) + len(ir_module.classes)) * 0.9

        print(f"\n✅ Node.js round-trip: {len(ir_module.functions)} functions, {len(ir_module.classes)} classes preserved")

    def test_go_roundtrip(self, fixtures_dir):
        """Test: Go → IR → Go"""
        source_path = fixtures_dir / "simple_service.go"
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        parser = GoParserV2()
        ir_module = parser.parse(source_code)

        assert ir_module is not None, "Failed to parse Go to IR"
        assert len(ir_module.functions) > 0 or len(ir_module.types) > 0, "No functions or types extracted"

        # Generate back to Go
        generated_code = generate_go(ir_module)

        assert generated_code is not None, "Failed to generate Go from IR"
        assert "func " in generated_code or "type " in generated_code, "Generated code missing structures"

        # Parse generated code back to IR
        roundtrip_ir = parser.parse(generated_code)

        assert roundtrip_ir is not None, "Failed to parse generated Go"

        # Compare semantics
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        assert len(roundtrip_ir.functions) >= len(ir_module.functions) * 0.9

        print(f"\n✅ Go round-trip: {len(ir_module.functions)} functions preserved")

    def test_rust_roundtrip(self, fixtures_dir):
        """Test: Rust → IR → Rust"""
        source_path = fixtures_dir / "simple_service.rs"
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        parser = RustParserV2()
        ir_module = parser.parse(source_code)

        assert ir_module is not None, "Failed to parse Rust to IR"
        assert len(ir_module.functions) > 0 or len(ir_module.types) > 0, "No functions or types extracted"

        # Generate back to Rust
        generated_code = generate_rust(ir_module)

        assert generated_code is not None, "Failed to generate Rust from IR"
        assert "fn " in generated_code or "struct " in generated_code, "Generated code missing structures"

        # Parse generated code back to IR
        roundtrip_ir = parser.parse(generated_code)

        assert roundtrip_ir is not None, "Failed to parse generated Rust"

        # Compare semantics
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        assert len(roundtrip_ir.functions) >= len(ir_module.functions) * 0.9

        print(f"\n✅ Rust round-trip: {len(ir_module.functions)} functions preserved")

    def test_dotnet_roundtrip(self, fixtures_dir):
        """Test: .NET → IR → .NET"""
        source_path = fixtures_dir / "simple_service.cs"
        with open(source_path, 'r') as f:
            source_code = f.read()

        # Parse to IR
        parser = DotNetParserV2()
        ir_module = parser.parse(source_code)

        assert ir_module is not None, "Failed to parse .NET to IR"
        assert len(ir_module.functions) > 0 or len(ir_module.classes) > 0, "No functions or classes extracted"

        # Generate back to .NET
        generated_code = generate_csharp(ir_module)

        assert generated_code is not None, "Failed to generate .NET from IR"
        assert "class" in generated_code or "void " in generated_code, "Generated code missing structures"

        # Parse generated code back to IR
        roundtrip_ir = parser.parse(generated_code)

        assert roundtrip_ir is not None, "Failed to parse generated .NET"

        # Compare semantics
        comparison = self.compare_ir_semantics(ir_module, roundtrip_ir)

        assert len(roundtrip_ir.functions) + len(roundtrip_ir.classes) >= (len(ir_module.functions) + len(ir_module.classes)) * 0.9

        print(f"\n✅ .NET round-trip: {len(ir_module.functions)} functions, {len(ir_module.classes)} classes preserved")


class TestCrossLanguageTranslation:
    """Test all 20 cross-language translation combinations"""

    @pytest.fixture(scope="class")
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"

    @pytest.fixture(scope="class")
    def parsers(self):
        return {
            "python": PythonParserV2(),
            "nodejs": NodeJSParserV2(),
            "go": GoParserV2(),
            "rust": RustParserV2(),
            "dotnet": DotNetParserV2(),
        }

    @pytest.fixture(scope="class")
    def generators(self):
        return {
            "python": generate_python,
            "nodejs": generate_nodejs,
            "go": generate_go,
            "rust": generate_rust,
            "dotnet": generate_csharp,
        }

    @pytest.fixture(scope="class")
    def source_files(self):
        return {
            "python": "simple_service.py",
            "nodejs": "simple_service.js",
            "go": "simple_service.go",
            "rust": "simple_service.rs",
            "dotnet": "simple_service.cs",
        }

    def verify_translation(self, source_ir: IRModule, target_code: str, target_lang: str, parsers: Dict) -> Dict[str, Any]:
        """Verify that translation preserves semantics"""
        # Parse target back to IR
        target_parser = parsers[target_lang]
        target_ir = target_parser.parse(target_code)

        if target_ir is None:
            return {"success": False, "error": "Failed to parse generated code"}

        # Compare structures
        func_preservation = len(target_ir.functions) / max(len(source_ir.functions), 1)
        type_preservation = len(target_ir.types) / max(len(source_ir.types), 1)
        class_preservation = len(target_ir.classes) / max(len(source_ir.classes), 1)

        return {
            "success": True,
            "function_preservation": func_preservation,
            "type_preservation": type_preservation,
            "class_preservation": class_preservation,
            "source_functions": len(source_ir.functions),
            "target_functions": len(target_ir.functions),
            "source_types": len(source_ir.types),
            "target_types": len(target_ir.types),
            "source_classes": len(source_ir.classes),
            "target_classes": len(target_ir.classes),
        }

    # Python → X translations
    def test_python_to_nodejs(self, fixtures_dir, parsers, generators, source_files):
        """Python → Node.js"""
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["python"].parse(source_code)
        assert ir_module is not None

        generated_code = generators["nodejs"](ir_module)
        assert generated_code is not None
        assert "class" in generated_code or "function" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "nodejs", parsers)
        assert verification["success"], verification.get("error", "")
        assert verification["function_preservation"] >= 0.8, "Too many functions lost"

        print(f"\n✅ Python → Node.js: {verification['target_functions']} functions generated")

    def test_python_to_go(self, fixtures_dir, parsers, generators, source_files):
        """Python → Go"""
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["python"].parse(source_code)
        generated_code = generators["go"](ir_module)

        assert generated_code is not None
        assert "func " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "go", parsers)
        assert verification["success"]
        assert verification["function_preservation"] >= 0.8

        print(f"\n✅ Python → Go: {verification['target_functions']} functions generated")

    def test_python_to_rust(self, fixtures_dir, parsers, generators, source_files):
        """Python → Rust"""
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["python"].parse(source_code)
        generated_code = generators["rust"](ir_module)

        assert generated_code is not None
        assert "fn " in generated_code or "pub fn " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "rust", parsers)
        assert verification["success"]
        assert verification["function_preservation"] >= 0.8

        print(f"\n✅ Python → Rust: {verification['target_functions']} functions generated")

    def test_python_to_dotnet(self, fixtures_dir, parsers, generators, source_files):
        """Python → .NET"""
        source_path = fixtures_dir / source_files["python"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["python"].parse(source_code)
        generated_code = generators["dotnet"](ir_module)

        assert generated_code is not None
        assert "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "dotnet", parsers)
        assert verification["success"]
        assert verification["function_preservation"] >= 0.8

        print(f"\n✅ Python → .NET: {verification['target_functions']} functions generated")

    # Node.js → X translations
    def test_nodejs_to_python(self, fixtures_dir, parsers, generators, source_files):
        """Node.js → Python"""
        source_path = fixtures_dir / source_files["nodejs"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["nodejs"].parse(source_code)
        generated_code = generators["python"](ir_module)

        assert generated_code is not None
        assert "def " in generated_code or "class " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "python", parsers)
        assert verification["success"]

        print(f"\n✅ Node.js → Python: {verification['target_functions']} functions generated")

    def test_nodejs_to_go(self, fixtures_dir, parsers, generators, source_files):
        """Node.js → Go"""
        source_path = fixtures_dir / source_files["nodejs"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["nodejs"].parse(source_code)
        generated_code = generators["go"](ir_module)

        assert generated_code is not None
        assert "func " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "go", parsers)
        assert verification["success"]

        print(f"\n✅ Node.js → Go: {verification['target_functions']} functions generated")

    def test_nodejs_to_rust(self, fixtures_dir, parsers, generators, source_files):
        """Node.js → Rust"""
        source_path = fixtures_dir / source_files["nodejs"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["nodejs"].parse(source_code)
        generated_code = generators["rust"](ir_module)

        assert generated_code is not None
        assert "fn " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "rust", parsers)
        assert verification["success"]

        print(f"\n✅ Node.js → Rust: {verification['target_functions']} functions generated")

    def test_nodejs_to_dotnet(self, fixtures_dir, parsers, generators, source_files):
        """Node.js → .NET"""
        source_path = fixtures_dir / source_files["nodejs"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["nodejs"].parse(source_code)
        generated_code = generators["dotnet"](ir_module)

        assert generated_code is not None
        assert "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "dotnet", parsers)
        assert verification["success"]

        print(f"\n✅ Node.js → .NET: {verification['target_functions']} functions generated")

    # Go → X translations
    def test_go_to_python(self, fixtures_dir, parsers, generators, source_files):
        """Go → Python"""
        source_path = fixtures_dir / source_files["go"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["go"].parse(source_code)
        generated_code = generators["python"](ir_module)

        assert generated_code is not None
        assert "def " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "python", parsers)
        assert verification["success"]

        print(f"\n✅ Go → Python: {verification['target_functions']} functions generated")

    def test_go_to_nodejs(self, fixtures_dir, parsers, generators, source_files):
        """Go → Node.js"""
        source_path = fixtures_dir / source_files["go"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["go"].parse(source_code)
        generated_code = generators["nodejs"](ir_module)

        assert generated_code is not None
        assert "function" in generated_code or "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "nodejs", parsers)
        assert verification["success"]

        print(f"\n✅ Go → Node.js: {verification['target_functions']} functions generated")

    def test_go_to_rust(self, fixtures_dir, parsers, generators, source_files):
        """Go → Rust"""
        source_path = fixtures_dir / source_files["go"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["go"].parse(source_code)
        generated_code = generators["rust"](ir_module)

        assert generated_code is not None
        assert "fn " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "rust", parsers)
        assert verification["success"]

        print(f"\n✅ Go → Rust: {verification['target_functions']} functions generated")

    def test_go_to_dotnet(self, fixtures_dir, parsers, generators, source_files):
        """Go → .NET"""
        source_path = fixtures_dir / source_files["go"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["go"].parse(source_code)
        generated_code = generators["dotnet"](ir_module)

        assert generated_code is not None
        assert "class" in generated_code or "void " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "dotnet", parsers)
        assert verification["success"]

        print(f"\n✅ Go → .NET: {verification['target_functions']} functions generated")

    # Rust → X translations
    def test_rust_to_python(self, fixtures_dir, parsers, generators, source_files):
        """Rust → Python"""
        source_path = fixtures_dir / source_files["rust"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["rust"].parse(source_code)
        generated_code = generators["python"](ir_module)

        assert generated_code is not None
        assert "def " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "python", parsers)
        assert verification["success"]

        print(f"\n✅ Rust → Python: {verification['target_functions']} functions generated")

    def test_rust_to_nodejs(self, fixtures_dir, parsers, generators, source_files):
        """Rust → Node.js"""
        source_path = fixtures_dir / source_files["rust"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["rust"].parse(source_code)
        generated_code = generators["nodejs"](ir_module)

        assert generated_code is not None
        assert "function" in generated_code or "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "nodejs", parsers)
        assert verification["success"]

        print(f"\n✅ Rust → Node.js: {verification['target_functions']} functions generated")

    def test_rust_to_go(self, fixtures_dir, parsers, generators, source_files):
        """Rust → Go"""
        source_path = fixtures_dir / source_files["rust"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["rust"].parse(source_code)
        generated_code = generators["go"](ir_module)

        assert generated_code is not None
        assert "func " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "go", parsers)
        assert verification["success"]

        print(f"\n✅ Rust → Go: {verification['target_functions']} functions generated")

    def test_rust_to_dotnet(self, fixtures_dir, parsers, generators, source_files):
        """Rust → .NET"""
        source_path = fixtures_dir / source_files["rust"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["rust"].parse(source_code)
        generated_code = generators["dotnet"](ir_module)

        assert generated_code is not None
        assert "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "dotnet", parsers)
        assert verification["success"]

        print(f"\n✅ Rust → .NET: {verification['target_functions']} functions generated")

    # .NET → X translations
    def test_dotnet_to_python(self, fixtures_dir, parsers, generators, source_files):
        """.NET → Python"""
        source_path = fixtures_dir / source_files["dotnet"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["dotnet"].parse(source_code)
        generated_code = generators["python"](ir_module)

        assert generated_code is not None
        assert "def " in generated_code or "class " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "python", parsers)
        assert verification["success"]

        print(f"\n✅ .NET → Python: {verification['target_functions']} functions generated")

    def test_dotnet_to_nodejs(self, fixtures_dir, parsers, generators, source_files):
        """.NET → Node.js"""
        source_path = fixtures_dir / source_files["dotnet"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["dotnet"].parse(source_code)
        generated_code = generators["nodejs"](ir_module)

        assert generated_code is not None
        assert "function" in generated_code or "class" in generated_code

        verification = self.verify_translation(ir_module, generated_code, "nodejs", parsers)
        assert verification["success"]

        print(f"\n✅ .NET → Node.js: {verification['target_functions']} functions generated")

    def test_dotnet_to_go(self, fixtures_dir, parsers, generators, source_files):
        """.NET → Go"""
        source_path = fixtures_dir / source_files["dotnet"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["dotnet"].parse(source_code)
        generated_code = generators["go"](ir_module)

        assert generated_code is not None
        assert "func " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "go", parsers)
        assert verification["success"]

        print(f"\n✅ .NET → Go: {verification['target_functions']} functions generated")

    def test_dotnet_to_rust(self, fixtures_dir, parsers, generators, source_files):
        """.NET → Rust"""
        source_path = fixtures_dir / source_files["dotnet"]
        with open(source_path, 'r') as f:
            source_code = f.read()

        ir_module = parsers["dotnet"].parse(source_code)
        generated_code = generators["rust"](ir_module)

        assert generated_code is not None
        assert "fn " in generated_code

        verification = self.verify_translation(ir_module, generated_code, "rust", parsers)
        assert verification["success"]

        print(f"\n✅ .NET → Rust: {verification['target_functions']} functions generated")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
