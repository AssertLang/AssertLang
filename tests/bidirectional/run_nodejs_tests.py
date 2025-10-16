#!/usr/bin/env python3
"""
Node.js Bidirectional Test Runner.

Runs comprehensive tests on Node.js code generation:
1. Parse .al fixtures
2. Generate Node.js servers
3. Validate syntax
4. Install dependencies
5. Start servers
6. Test MCP protocol compliance
7. Generate JSON report
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directories to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import from relative paths
sys.path.insert(0, str(Path(__file__).parent))
from agents.nodejs_expert import NodeJSExpert
from language.nodejs_server_generator import generate_nodejs_server_from_pw


class NodeJSTestRunner:
    """Orchestrates Node.js bidirectional testing."""

    def __init__(self):
        self.expert = NodeJSExpert()
        self.results: Dict[str, Any] = {
            "test_suite": "nodejs_bidirectional",
            "started_at": datetime.utcnow().isoformat(),
            "node_version": self.expert.node_version,
            "npm_version": self.expert.npm_version,
            "tests": [],
            "summary": {},
        }

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all Node.js tests and return results."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        fixtures = [
            fixtures_dir / "nodejs_minimal.al",
            fixtures_dir / "nodejs_with_tools.al",
        ]

        for fixture in fixtures:
            if fixture.exists():
                print(f"\n{'=' * 60}")
                print(f"Testing: {fixture.name}")
                print(f"{'=' * 60}")
                result = self.test_fixture(fixture)
                self.results["tests"].append(result)
            else:
                print(f"WARNING: Fixture not found: {fixture}")

        # Generate summary
        self.generate_summary()

        # Cleanup
        self.expert.cleanup()

        self.results["completed_at"] = datetime.utcnow().isoformat()
        return self.results

    def test_fixture(self, fixture_path: Path) -> Dict[str, Any]:
        """
        Test a single .al fixture file.

        Args:
            fixture_path: Path to .al fixture

        Returns:
            Dictionary with test results
        """
        test_result = {
            "fixture": fixture_path.name,
            "stages": {},
            "passed": False,
            "errors": [],
        }

        try:
            # Stage 1: Read fixture
            print(f"\n[1/7] Reading fixture...")
            pw_content = fixture_path.read_text()
            test_result["stages"]["read"] = {
                "passed": True,
                "message": f"Read {len(pw_content)} bytes",
            }
            print(f"  ✓ Read {len(pw_content)} bytes")

            # Stage 2: Generate Node.js code
            print(f"\n[2/7] Generating Node.js code...")
            try:
                js_code = generate_nodejs_server_from_pw(pw_content)
                test_result["stages"]["generation"] = {
                    "passed": True,
                    "message": f"Generated {len(js_code)} bytes of JavaScript",
                    "code_size": len(js_code),
                }
                print(f"  ✓ Generated {len(js_code)} bytes")
            except Exception as e:
                test_result["stages"]["generation"] = {
                    "passed": False,
                    "error": str(e),
                }
                test_result["errors"].append(f"Generation failed: {e}")
                print(f"  ✗ Generation failed: {e}")
                return test_result

            # Stage 3: Validate syntax
            print(f"\n[3/7] Validating JavaScript syntax...")
            syntax_result = self.expert.validate_syntax(js_code)
            test_result["stages"]["syntax"] = syntax_result
            if syntax_result["valid"]:
                print(f"  ✓ Syntax valid")
            else:
                print(f"  ✗ Syntax invalid: {syntax_result.get('error', 'Unknown error')}")
                test_result["errors"].append("Syntax validation failed")
                return test_result

            # Stage 4: Check async/await handling
            print(f"\n[4/7] Checking async/await handling...")
            async_result = self.expert.validate_async_handling(js_code)
            test_result["stages"]["async_handling"] = async_result
            if async_result["valid"]:
                print(f"  ✓ Async handling looks good")
            else:
                print(f"  ⚠ Async issues found: {async_result['issues']}")

            # Stage 5: Create workspace and install dependencies
            print(f"\n[5/7] Setting up workspace and installing dependencies...")
            workspace = self.expert.create_test_workspace()
            server_file = workspace / "server.js"
            server_file.write_text(js_code)

            install_result = self.expert.install_deps(workspace)
            test_result["stages"]["install"] = install_result
            if install_result["success"]:
                print(f"  ✓ Dependencies installed")
            else:
                print(f"  ✗ Install failed: {install_result.get('error', 'Unknown error')}")
                test_result["errors"].append("Dependency installation failed")
                return test_result

            # Stage 6: Start server
            print(f"\n[6/7] Starting server...")
            # Extract port from pw_content
            port = self._extract_port(pw_content)
            startup_result = self.expert.start_server(server_file, port)
            test_result["stages"]["startup"] = startup_result
            if startup_result["success"]:
                print(f"  ✓ Server started on port {port}")
            else:
                print(f"  ✗ Startup failed: {startup_result.get('message', 'Unknown error')}")
                test_result["errors"].append("Server startup failed")
                return test_result

            # Stage 7: Test endpoints
            print(f"\n[7/7] Testing endpoints...")
            endpoint_results = {}

            # Test health endpoint
            print(f"  Testing /health...")
            health_result = self.expert.test_health(port)
            endpoint_results["health"] = health_result
            if health_result["success"]:
                print(f"    ✓ Health check passed")
            else:
                print(f"    ✗ Health check failed")

            # Test verbs listing
            print(f"  Testing /verbs...")
            verbs_result = self.expert.test_verbs_listing(port)
            endpoint_results["verbs"] = verbs_result
            if verbs_result["success"]:
                verbs = verbs_result.get("verbs", [])
                print(f"    ✓ Found {len(verbs)} verbs: {verbs}")
            else:
                print(f"    ✗ Verbs listing failed")

            # Test verb execution
            if verbs_result.get("success") and verbs_result.get("verbs"):
                verb = verbs_result["verbs"][0]
                print(f"  Testing verb execution: {verb}...")

                # Prepare test params based on fixture
                test_params = self._get_test_params(fixture_path.name, verb)
                exec_result = self.expert.test_verb_execution(port, verb, test_params)
                endpoint_results["verb_execution"] = exec_result

                if exec_result["success"]:
                    print(f"    ✓ Verb execution successful")
                else:
                    print(f"    ✗ Verb execution failed")

            test_result["stages"]["endpoints"] = endpoint_results

            # Stop server
            self.expert.stop_server(port)

            # Determine overall pass/fail
            test_result["passed"] = (
                len(test_result["errors"]) == 0
                and health_result["success"]
                and verbs_result["success"]
            )

            if test_result["passed"]:
                print(f"\n✓ All tests passed for {fixture_path.name}")
            else:
                print(f"\n✗ Some tests failed for {fixture_path.name}")

        except Exception as e:
            test_result["errors"].append(f"Unexpected error: {str(e)}")
            test_result["passed"] = False
            print(f"\n✗ Unexpected error: {e}")

        return test_result

    def _extract_port(self, pw_content: str) -> int:
        """Extract port number from .al content."""
        for line in pw_content.split("\n"):
            if line.strip().startswith("port "):
                return int(line.split()[1])
        return 20100  # Default

    def _get_test_params(self, fixture_name: str, verb: str) -> Dict[str, Any]:
        """Get appropriate test parameters for a verb."""
        if "minimal" in fixture_name:
            return {"message": "Hello from test"}
        elif "tools" in fixture_name:
            if "process.data" in verb:
                return {"input": "test data", "format": "json"}
            else:
                return {}
        return {}

    def generate_summary(self) -> None:
        """Generate test summary."""
        total = len(self.results["tests"])
        passed = sum(1 for t in self.results["tests"] if t["passed"])
        failed = total - passed

        self.results["summary"] = {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed / total * 100) if total > 0 else 0:.1f}%",
        }

        print(f"\n{'=' * 60}")
        print(f"SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Pass rate: {self.results['summary']['pass_rate']}")


def main():
    """Main entry point."""
    print("Node.js Bidirectional Test Runner")
    print("=" * 60)

    runner = NodeJSTestRunner()
    results = runner.run_all_tests()

    # Save results to JSON
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"nodejs_test_report_{timestamp}.json"

    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nReport saved to: {report_file}")

    # Return exit code based on results
    if results["summary"]["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
