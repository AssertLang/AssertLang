#!/usr/bin/env python3
"""
Python Expert Agent for Bidirectional Testing System.

Validates and tests Python-generated MCP servers.
"""

import ast
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests
import socket


class PythonExpertAgent:
    """Expert agent for Python server validation and testing."""

    def __init__(self, server_path: Path, port: int):
        """
        Initialize Python expert agent.

        Args:
            server_path: Path to generated Python server file
            port: Port the server should run on
        """
        self.server_path = server_path
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.base_url = f"http://localhost:{port}"

    def validate_syntax(self) -> Dict[str, Any]:
        """
        Parse Python code with ast module to validate syntax.

        Returns:
            Dict with validation results
        """
        result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "imports_found": [],
            "classes_found": [],
            "functions_found": []
        }

        try:
            with open(self.server_path, 'r') as f:
                code = f.read()

            # Parse with AST
            tree = ast.parse(code, filename=str(self.server_path))
            result["valid"] = True

            # Extract structural information
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports_found"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result["imports_found"].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    result["classes_found"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    result["functions_found"].append(node.name)

            # Check for required components
            required_imports = ["fastapi", "uvicorn"]
            missing_imports = [imp for imp in required_imports
                             if not any(imp in found for found in result["imports_found"])]

            if missing_imports:
                result["warnings"].append(
                    f"Missing recommended imports: {', '.join(missing_imports)}"
                )

        except SyntaxError as e:
            result["errors"].append(f"Syntax error at line {e.lineno}: {e.msg}")
        except Exception as e:
            result["errors"].append(f"Parsing error: {str(e)}")

        return result

    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("localhost", port))
            sock.close()
            return True
        except OSError:
            return False

    def start_server(self, timeout: int = 30) -> Dict[str, Any]:
        """
        Launch Python server subprocess.

        Args:
            timeout: Maximum seconds to wait for server startup

        Returns:
            Dict with startup results
        """
        result = {
            "started": False,
            "pid": None,
            "errors": [],
            "startup_time": None
        }

        # Check if port is already in use
        if not self._is_port_available(self.port):
            result["errors"].append(f"Port {self.port} is already in use")
            return result

        try:
            start_time = time.time()

            # Start the server process
            self.process = subprocess.Popen(
                [sys.executable, str(self.server_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            result["pid"] = self.process.pid

            # Wait for server to become ready
            max_wait = time.time() + timeout
            while time.time() < max_wait:
                if self.process.poll() is not None:
                    # Process died
                    stdout, stderr = self.process.communicate()
                    result["errors"].append(f"Server process died: {stderr}")
                    return result

                try:
                    response = requests.get(
                        f"{self.base_url}/health",
                        timeout=1
                    )
                    if response.status_code == 200:
                        result["started"] = True
                        result["startup_time"] = time.time() - start_time
                        return result
                except requests.exceptions.RequestException:
                    time.sleep(0.5)

            result["errors"].append(f"Server did not start within {timeout} seconds")

        except Exception as e:
            result["errors"].append(f"Failed to start server: {str(e)}")

        return result

    def test_health(self) -> Dict[str, Any]:
        """
        Verify health endpoint responds correctly.

        Returns:
            Dict with health check results
        """
        result = {
            "passed": False,
            "status_code": None,
            "response": None,
            "errors": [],
            "response_time": None
        }

        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=5)
            result["response_time"] = time.time() - start
            result["status_code"] = response.status_code

            if response.status_code == 200:
                data = response.json()
                result["response"] = data

                # Validate health response format
                if "status" in data:
                    result["passed"] = True
                else:
                    result["errors"].append("Health response missing 'status' field")
            else:
                result["errors"].append(
                    f"Health check returned status {response.status_code}"
                )

        except requests.exceptions.Timeout:
            result["errors"].append("Health check timed out")
        except requests.exceptions.ConnectionError:
            result["errors"].append("Could not connect to server")
        except Exception as e:
            result["errors"].append(f"Health check failed: {str(e)}")

        return result

    def test_verb_execution(self, verb: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call verbs via MCP protocol.

        Args:
            verb: Verb name (e.g., "echo.message@v1")
            params: Parameters for the verb

        Returns:
            Dict with execution results
        """
        result = {
            "passed": False,
            "verb": verb,
            "params": params,
            "response": None,
            "errors": [],
            "response_time": None
        }

        try:
            # Construct MCP JSON-RPC request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": verb,
                    "arguments": params
                }
            }

            start = time.time()
            response = requests.post(
                f"{self.base_url}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            result["response_time"] = time.time() - start

            if response.status_code == 200:
                data = response.json()
                result["response"] = data

                # Check for MCP error response
                if "error" in data:
                    result["errors"].append(
                        f"MCP error: {data['error'].get('message', 'Unknown error')}"
                    )
                elif "result" in data:
                    result["passed"] = True
                else:
                    result["errors"].append("Invalid MCP response format")
            else:
                result["errors"].append(
                    f"HTTP error: {response.status_code} - {response.text}"
                )

        except requests.exceptions.Timeout:
            result["errors"].append("Verb execution timed out")
        except requests.exceptions.ConnectionError:
            result["errors"].append("Could not connect to server")
        except Exception as e:
            result["errors"].append(f"Verb execution failed: {str(e)}")

        return result

    def test_tool_execution(self, tool_name: str) -> Dict[str, Any]:
        """
        Validate tools work correctly.

        Args:
            tool_name: Name of the tool to test

        Returns:
            Dict with tool validation results
        """
        result = {
            "passed": False,
            "tool": tool_name,
            "errors": [],
            "tests_run": []
        }

        # Tool-specific test cases
        test_cases = {
            "http": {
                "verb": "fetch.data@v1",
                "params": {"url": "https://httpbin.org/status/200"}
            },
            "storage": {
                "verb": "store.item@v1",
                "params": {"key": "test_key", "value": "test_value"}
            },
            "logger": {
                "verb": "task.create@v1",
                "params": {
                    "title": "Test Task",
                    "description": "Test description",
                    "priority": 1
                }
            }
        }

        if tool_name not in test_cases:
            result["errors"].append(f"No test case defined for tool: {tool_name}")
            return result

        test_case = test_cases[tool_name]
        verb_result = self.test_verb_execution(
            test_case["verb"],
            test_case["params"]
        )

        result["tests_run"].append({
            "verb": test_case["verb"],
            "passed": verb_result["passed"],
            "errors": verb_result["errors"]
        })

        result["passed"] = verb_result["passed"]
        if not verb_result["passed"]:
            result["errors"].extend(verb_result["errors"])

        return result

    def stop_server(self) -> Dict[str, Any]:
        """
        Stop the server process.

        Returns:
            Dict with shutdown results
        """
        result = {
            "stopped": False,
            "errors": []
        }

        if self.process is None:
            result["errors"].append("No server process to stop")
            return result

        try:
            self.process.terminate()

            # Wait up to 5 seconds for graceful shutdown
            try:
                self.process.wait(timeout=5)
                result["stopped"] = True
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't stop
                self.process.kill()
                self.process.wait()
                result["stopped"] = True
                result["errors"].append("Had to force kill server process")

        except Exception as e:
            result["errors"].append(f"Error stopping server: {str(e)}")

        return result

    def run_full_validation(self, test_verbs: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run complete validation suite.

        Args:
            test_verbs: List of dicts with 'verb' and 'params' keys

        Returns:
            Complete test results
        """
        results = {
            "server_path": str(self.server_path),
            "port": self.port,
            "syntax_validation": None,
            "server_startup": None,
            "health_check": None,
            "verb_tests": [],
            "overall_passed": False,
            "total_duration": None
        }

        start_time = time.time()

        # Step 1: Validate syntax
        results["syntax_validation"] = self.validate_syntax()
        if not results["syntax_validation"]["valid"]:
            results["overall_passed"] = False
            results["total_duration"] = time.time() - start_time
            return results

        # Step 2: Start server
        results["server_startup"] = self.start_server()
        if not results["server_startup"]["started"]:
            results["overall_passed"] = False
            results["total_duration"] = time.time() - start_time
            return results

        try:
            # Step 3: Health check
            results["health_check"] = self.test_health()

            # Step 4: Test verbs
            if test_verbs:
                for test in test_verbs:
                    verb_result = self.test_verb_execution(
                        test["verb"],
                        test.get("params", {})
                    )
                    results["verb_tests"].append(verb_result)

            # Determine overall pass/fail
            results["overall_passed"] = (
                results["syntax_validation"]["valid"] and
                results["server_startup"]["started"] and
                results["health_check"]["passed"] and
                all(test["passed"] for test in results["verb_tests"])
            )

        finally:
            # Always stop the server
            stop_result = self.stop_server()
            results["server_shutdown"] = stop_result
            results["total_duration"] = time.time() - start_time

        return results


def main():
    """Example usage of PythonExpertAgent."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python python_expert.py <server_path> [port]")
        sys.exit(1)

    server_path = Path(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 23470

    agent = PythonExpertAgent(server_path, port)

    # Example test verbs
    test_verbs = [
        {"verb": "health.check@v1", "params": {}},
        {"verb": "echo.message@v1", "params": {"message": "Hello, World!"}}
    ]

    results = agent.run_full_validation(test_verbs)

    print(json.dumps(results, indent=2))
    sys.exit(0 if results["overall_passed"] else 1)


if __name__ == "__main__":
    main()
