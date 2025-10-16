#!/usr/bin/env python3
"""
Bidirectional Testing System - Rust Test Runner

Orchestrates the complete test flow:
1. Parse .al fixtures
2. Generate Rust servers
3. Validate and test servers
4. Collect results
"""

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from language.agent_parser import parse_agent_pw
from tests.bidirectional.agents.rust_expert import RustExpertAgent


class RustTestRunner:
    """Orchestrates bidirectional testing for Rust servers."""

    def __init__(self, fixtures_dir: Path, output_dir: Path):
        """
        Initialize test runner.

        Args:
            fixtures_dir: Directory containing .al test fixtures
            output_dir: Directory for generated servers
        """
        self.fixtures_dir = fixtures_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[Dict[str, Any]] = []
        self.rust_expert = RustExpertAgent()

    def parse_fixture(self, fixture_path: Path) -> Dict[str, Any]:
        """
        Parse a .al fixture file.

        Args:
            fixture_path: Path to .al file

        Returns:
            Dict with parsing results
        """
        result = {
            "fixture": str(fixture_path.name),
            "parsed": False,
            "agent": None,
            "errors": [],
        }

        try:
            # Read the file content
            with open(fixture_path, "r") as f:
                content = f.read()

            # Parse the agent definition
            agent = parse_agent_pw(content)
            result["parsed"] = True
            result["agent"] = agent
        except Exception as e:
            result["errors"].append(f"Failed to parse fixture: {str(e)}")

        return result

    def generate_server(self, agent, fixture_name: str) -> Dict[str, Any]:
        """
        Generate Rust server from agent definition.

        Args:
            agent: Parsed agent definition
            fixture_name: Name of the fixture file

        Returns:
            Dict with generation results
        """
        result = {
            "fixture": fixture_name,
            "generated": False,
            "server_path": None,
            "errors": [],
        }

        try:
            # Check if Rust generator exists
            try:
                from language.mcp_server_generator_rust import generate_rust_mcp_server

                generator_exists = True
            except ImportError:
                generator_exists = False
                result["errors"].append(
                    "Rust generator not found: generate_rust_mcp_server() does not exist in mcp_server_generator_rust.py"
                )
                return result

            # Create project directory
            project_name = agent.name.replace("-", "_")
            project_dir = self.output_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)

            # Generate server code
            server_code = generate_rust_mcp_server(agent)

            # Write Cargo.toml
            cargo_toml_content = f"""[package]
name = "{project_name}"
version = "0.1.0"
edition = "2021"

[workspace]

[dependencies]
tokio = {{ version = "1", features = ["full"] }}
warp = "0.3"
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"
chrono = "0.4"
"""
            cargo_toml_path = project_dir / "Cargo.toml"
            cargo_toml_path.write_text(cargo_toml_content)

            # Create src directory and write main.rs
            src_dir = project_dir / "src"
            src_dir.mkdir(exist_ok=True)
            main_rs_path = src_dir / "main.rs"
            main_rs_path.write_text(server_code)

            result["generated"] = True
            result["server_path"] = str(project_dir)

        except Exception as e:
            result["errors"].append(f"Failed to generate server: {str(e)}")

        return result

    def test_server(
        self, server_path: Path, agent, fixture_name: str
    ) -> Dict[str, Any]:
        """
        Test generated server using RustExpertAgent.

        Args:
            server_path: Path to generated server project
            agent: Agent definition
            fixture_name: Name of fixture

        Returns:
            Dict with test results
        """
        result = {
            "fixture": fixture_name,
            "agent_name": agent.name,
            "port": agent.port,
            "server_path": str(server_path),
            "tests": {},
            "overall_passed": False,
        }

        try:
            # Build test verbs from agent definition
            test_verbs = []
            for expose in agent.exposes:
                # Create basic test params based on param types
                test_params = {}
                for param in expose.params:
                    param_name = param["name"]
                    param_type = param["type"]

                    if param_type == "string":
                        test_params[param_name] = f"test_{param_name}"
                    elif param_type == "int":
                        test_params[param_name] = 42
                    elif param_type == "bool":
                        test_params[param_name] = True
                    else:
                        test_params[param_name] = None

                test_verbs.append({"verb": expose.verb, "params": test_params})

            # Run full validation
            validation_results = self.rust_expert.run_full_validation(
                server_path, agent.port, test_verbs
            )
            result["tests"] = validation_results
            result["overall_passed"] = validation_results["overall_passed"]

        except Exception as e:
            result["tests"]["error"] = str(e)
            result["overall_passed"] = False

        return result

    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run complete test suite on all Rust fixtures.

        Returns:
            Complete test results
        """
        summary = {
            "start_time": time.time(),
            "fixtures_dir": str(self.fixtures_dir),
            "output_dir": str(self.output_dir),
            "fixtures_tested": 0,
            "fixtures_passed": 0,
            "fixtures_failed": 0,
            "test_results": [],
            "errors": [],
        }

        # Find all Rust .al fixtures
        fixtures = list(self.fixtures_dir.glob("rust_*.al"))
        if not fixtures:
            summary["errors"].append(
                f"No rust_*.al fixtures found in {self.fixtures_dir}"
            )
            return summary

        print(f"Found {len(fixtures)} Rust fixture(s) to test")
        print("-" * 60)

        for fixture_path in fixtures:
            print(f"\nTesting: {fixture_path.name}")
            print("-" * 60)

            test_result = {
                "fixture": fixture_path.name,
                "stages": {},
                "passed": False,
            }

            # Stage 1: Parse fixture
            print("  [1/3] Parsing fixture...")
            parse_result = self.parse_fixture(fixture_path)
            test_result["stages"]["parse"] = parse_result

            if not parse_result["parsed"]:
                print(f"    FAILED: {parse_result['errors']}")
                test_result["passed"] = False
                summary["test_results"].append(test_result)
                summary["fixtures_failed"] += 1
                continue

            print("    OK")
            agent = parse_result["agent"]

            # Stage 2: Generate server
            print("  [2/3] Generating server...")
            gen_result = self.generate_server(agent, fixture_path.name)
            test_result["stages"]["generate"] = gen_result

            if not gen_result["generated"]:
                print(f"    FAILED: {gen_result['errors']}")
                test_result["passed"] = False
                summary["test_results"].append(test_result)
                summary["fixtures_failed"] += 1
                continue

            print(f"    OK - {gen_result['server_path']}")
            server_path = Path(gen_result["server_path"])

            # Stage 3: Test server
            print("  [3/3] Testing server...")
            test_server_result = self.test_server(
                server_path, agent, fixture_path.name
            )
            test_result["stages"]["test"] = test_server_result

            if test_server_result["overall_passed"]:
                print("    PASSED")
                test_result["passed"] = True
                summary["fixtures_passed"] += 1
            else:
                print("    FAILED")
                # Print detailed error info
                if "tests" in test_server_result:
                    tests = test_server_result["tests"]
                    if "syntax_validation" in tests and tests["syntax_validation"]:
                        if not tests["syntax_validation"].get("valid", False):
                            print(f"      Syntax errors: {tests['syntax_validation'].get('errors', [])}")
                    if "compilation" in tests and tests["compilation"]:
                        if not tests["compilation"].get("success", False):
                            print(f"      Compilation errors: {tests['compilation'].get('errors', [])}")
                    if "server_startup" in tests and tests["server_startup"]:
                        if not tests["server_startup"].get("started", False):
                            print(f"      Server startup errors: {tests['server_startup'].get('errors', [])}")
                test_result["passed"] = False
                summary["fixtures_failed"] += 1

            summary["test_results"].append(test_result)
            summary["fixtures_tested"] += 1

        summary["end_time"] = time.time()
        summary["total_duration"] = summary["end_time"] - summary["start_time"]

        return summary


def main():
    """Main entry point."""
    # Setup paths
    test_dir = Path(__file__).parent
    fixtures_dir = test_dir / "fixtures"
    output_dir = test_dir / "generated" / "rust"

    print("=" * 60)
    print("Rust Bidirectional Testing System")
    print("=" * 60)
    print(f"Fixtures: {fixtures_dir}")
    print(f"Output: {output_dir}")
    print()

    # Run tests
    runner = RustTestRunner(fixtures_dir, output_dir)
    results = runner.run_all_tests()

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Fixtures tested: {results['fixtures_tested']}")
    print(f"Passed: {results['fixtures_passed']}")
    print(f"Failed: {results['fixtures_failed']}")
    print(f"Total duration: {results['total_duration']:.2f}s")

    # Save results to JSON
    results_file = test_dir / "reports" / "rust_test_results.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nDetailed results saved to: {results_file}")

    # Print detailed results
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    print(json.dumps(results, indent=2, default=str))

    # Exit with appropriate code
    sys.exit(0 if results["fixtures_failed"] == 0 else 1)


if __name__ == "__main__":
    main()
