"""
Node.js Expert Agent for AssertLang Bidirectional Testing System.

This agent validates Node.js code generation, manages server lifecycle,
and tests MCP protocol compliance for Node.js-generated servers.
"""

import json
import os
import subprocess
import time
import requests
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any


class NodeJSExpert:
    """Expert agent for Node.js code validation and testing."""

    def __init__(self, node_path: str = "node", npm_path: str = "npm"):
        """
        Initialize NodeJS Expert Agent.

        Args:
            node_path: Path to node executable
            npm_path: Path to npm executable
        """
        self.node_path = node_path
        self.npm_path = npm_path
        self.server_processes: Dict[str, subprocess.Popen] = {}
        self.temp_dirs: List[Path] = []

        # Verify node and npm are available
        self._verify_environment()

    def _verify_environment(self) -> None:
        """Verify Node.js and npm are installed and available."""
        try:
            node_result = subprocess.run(
                [self.node_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.node_version = node_result.stdout.strip()

            npm_result = subprocess.run(
                [self.npm_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.npm_version = npm_result.stdout.strip()

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"Node.js/npm not available: {e}")

    def validate_syntax(self, js_code: str) -> Dict[str, Any]:
        """
        Validate JavaScript syntax without executing.

        Args:
            js_code: JavaScript code to validate

        Returns:
            Dictionary with validation results
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".js", delete=False
        ) as f:
            f.write(js_code)
            temp_file = f.name

        try:
            # Use node --check to validate syntax
            result = subprocess.run(
                [self.node_path, "--check", temp_file],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return {
                    "valid": True,
                    "message": "Syntax validation passed",
                }
            else:
                return {
                    "valid": False,
                    "message": "Syntax validation failed",
                    "error": result.stderr,
                }

        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "message": "Syntax validation timeout",
            }
        finally:
            os.unlink(temp_file)

    def install_deps(self, work_dir: Path) -> Dict[str, Any]:
        """
        Install Node.js dependencies using npm.

        Args:
            work_dir: Directory containing package.json

        Returns:
            Dictionary with installation results
        """
        # Create package.json if it doesn't exist
        package_json = work_dir / "package.json"
        if not package_json.exists():
            package_data = {
                "name": "assertlang-test-agent",
                "version": "1.0.0",
                "description": "Generated MCP agent for testing",
                "main": "server.js",
                "dependencies": {"express": "^4.18.2"},
            }
            with open(package_json, "w") as f:
                json.dump(package_data, f, indent=2)

        try:
            # Run npm install
            result = subprocess.run(
                [self.npm_path, "install"],
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Dependencies installed successfully",
                    "stdout": result.stdout,
                }
            else:
                return {
                    "success": False,
                    "message": "npm install failed",
                    "error": result.stderr,
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "npm install timeout (>120s)",
            }

    def start_server(
        self, server_file: Path, port: int, timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Start Node.js server as subprocess.

        Args:
            server_file: Path to server.js file
            port: Port number server should listen on
            timeout: Seconds to wait for server startup

        Returns:
            Dictionary with startup results
        """
        server_id = f"server_{port}"

        try:
            # Start server process
            process = subprocess.Popen(
                [self.node_path, str(server_file)],
                cwd=server_file.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait for server to be ready
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(
                        f"http://127.0.0.1:{port}/health", timeout=1
                    )
                    if response.status_code == 200:
                        self.server_processes[server_id] = process
                        return {
                            "success": True,
                            "message": f"Server started on port {port}",
                            "pid": process.pid,
                            "port": port,
                        }
                except requests.RequestException:
                    time.sleep(0.5)

            # Timeout reached
            process.terminate()
            process.wait(timeout=5)
            return {
                "success": False,
                "message": f"Server startup timeout after {timeout}s",
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to start server: {str(e)}",
            }

    def stop_server(self, port: int) -> Dict[str, Any]:
        """
        Stop running server process.

        Args:
            port: Port number of server to stop

        Returns:
            Dictionary with stop results
        """
        server_id = f"server_{port}"
        if server_id not in self.server_processes:
            return {
                "success": False,
                "message": f"No server running on port {port}",
            }

        process = self.server_processes[server_id]
        try:
            process.terminate()
            process.wait(timeout=5)
            del self.server_processes[server_id]
            return {
                "success": True,
                "message": f"Server on port {port} stopped",
            }
        except subprocess.TimeoutExpired:
            process.kill()
            del self.server_processes[server_id]
            return {
                "success": True,
                "message": f"Server on port {port} killed (force)",
            }

    def test_health(self, port: int) -> Dict[str, Any]:
        """
        Test health endpoint.

        Args:
            port: Port number of server

        Returns:
            Dictionary with health check results
        """
        try:
            response = requests.get(
                f"http://127.0.0.1:{port}/health", timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": "healthy",
                    "data": data,
                }
            else:
                return {
                    "success": False,
                    "status": "unhealthy",
                    "status_code": response.status_code,
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "status": "unreachable",
                "error": str(e),
            }

    def test_verb_execution(
        self, port: int, verb: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test MCP verb execution via HTTP.

        Args:
            port: Port number of server
            verb: Verb name (e.g., "echo@v1")
            params: Parameters to send

        Returns:
            Dictionary with execution results
        """
        try:
            response = requests.post(
                f"http://127.0.0.1:{port}/mcp",
                json={"method": verb, "params": params},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data,
                    "status_code": response.status_code,
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }

    def test_verbs_listing(self, port: int) -> Dict[str, Any]:
        """
        Test /verbs endpoint that lists available verbs.

        Args:
            port: Port number of server

        Returns:
            Dictionary with verbs listing results
        """
        try:
            response = requests.get(
                f"http://127.0.0.1:{port}/verbs", timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "verbs": data.get("verbs", []),
                    "agent": data.get("agent", "unknown"),
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                }

        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }

    def validate_async_handling(self, js_code: str) -> Dict[str, Any]:
        """
        Check if generated code properly handles async/await.

        Args:
            js_code: JavaScript code to analyze

        Returns:
            Dictionary with async validation results
        """
        issues = []

        # Check for async/await usage
        has_async = "async " in js_code
        has_await = "await " in js_code

        if has_await and not has_async:
            issues.append("Found 'await' without 'async' function")

        # Check for Promise handling
        has_then = ".then(" in js_code
        has_catch = ".catch(" in js_code

        if has_then and not has_catch:
            issues.append("Found .then() without .catch() - missing error handling")

        return {
            "valid": len(issues) == 0,
            "has_async": has_async,
            "has_await": has_await,
            "has_promises": has_then or has_catch,
            "issues": issues,
        }

    def cleanup(self) -> None:
        """Stop all servers and clean up temporary directories."""
        # Stop all running servers
        for server_id in list(self.server_processes.keys()):
            port = int(server_id.split("_")[1])
            self.stop_server(port)

        # Clean up temp directories
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        self.temp_dirs.clear()

    def create_test_workspace(self) -> Path:
        """
        Create temporary workspace for testing.

        Returns:
            Path to temporary directory
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="nodejs_test_"))
        self.temp_dirs.append(temp_dir)
        return temp_dir
