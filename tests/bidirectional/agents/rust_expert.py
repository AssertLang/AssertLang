"""
Rust Expert Agent for Bidirectional Testing System.

Validates Rust code generation, compilation, server lifecycle management,
and MCP protocol compliance for Rust-generated servers.
"""

import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


@dataclass
class RustSyntaxResult:
    """Result from Rust syntax validation."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    formatted: bool = False


@dataclass
class RustCompilationResult:
    """Result from Rust compilation."""

    success: bool
    build_time_ms: float
    binary_path: Optional[str] = None
    binary_size_bytes: Optional[int] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    release_mode: bool = True


@dataclass
class RustServerResult:
    """Result from running Rust server."""

    started: bool
    pid: Optional[int] = None
    health_check_passed: bool = False
    health_response_time_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class RustTestReport:
    """Comprehensive Rust testing report."""

    agent_name: str
    fixture_path: str
    generated_code_path: Optional[str] = None
    syntax_validation: Optional[RustSyntaxResult] = None
    compilation: Optional[RustCompilationResult] = None
    server: Optional[RustServerResult] = None
    verb_tests: List[Dict[str, Any]] = field(default_factory=list)
    code_quality_score: float = 0.0
    overall_passed: bool = False
    timestamp: str = ""
    errors: List[str] = field(default_factory=list)


class RustExpertAgent:
    """
    Expert agent for Rust code validation and testing.

    Capabilities:
    - Syntax validation with cargo check
    - Compilation with cargo build --release
    - Server startup and health checks
    - MCP protocol testing
    - Code quality scoring
    """

    def __init__(self, cargo_binary: str = "cargo"):
        """
        Initialize Rust expert agent.

        Args:
            cargo_binary: Path to cargo binary (default: "cargo")
        """
        self.cargo_binary = cargo_binary
        self.temp_dirs: List[str] = []
        self.server_processes: Dict[int, subprocess.Popen] = {}
        self._verify_environment()

    def _verify_environment(self) -> None:
        """Verify Rust and cargo are installed and available."""
        try:
            result = subprocess.run(
                [self.cargo_binary, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.cargo_version = result.stdout.strip()

            result = subprocess.run(
                ["rustc", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.rustc_version = result.stdout.strip()

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"Rust/cargo not available: {e}")

    def validate_syntax(self, code_dir: Path) -> RustSyntaxResult:
        """
        Validate Rust syntax using cargo check.

        Args:
            code_dir: Directory containing Rust project

        Returns:
            Syntax validation result
        """
        errors = []
        warnings = []

        try:
            # First, check if we need to run cargo fmt
            fmt_result = subprocess.run(
                [self.cargo_binary, "fmt", "--check"],
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            formatted = fmt_result.returncode == 0
            if not formatted:
                warnings.append("Code is not properly formatted (cargo fmt)")

            # Run cargo check to validate syntax without building
            check_result = subprocess.run(
                [self.cargo_binary, "check"],
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if check_result.returncode != 0:
                errors.append(f"cargo check failed: {check_result.stderr}")
                return RustSyntaxResult(
                    valid=False, errors=errors, warnings=warnings, formatted=formatted
                )

            # Extract warnings from stderr
            if check_result.stderr:
                warning_lines = [
                    line for line in check_result.stderr.split("\n") if "warning:" in line
                ]
                warnings.extend(warning_lines)

            return RustSyntaxResult(
                valid=True, errors=errors, warnings=warnings, formatted=formatted
            )

        except subprocess.TimeoutExpired:
            errors.append("Syntax validation timed out")
            return RustSyntaxResult(valid=False, errors=errors, warnings=warnings)
        except Exception as e:
            errors.append(f"Syntax validation error: {e}")
            return RustSyntaxResult(valid=False, errors=errors, warnings=warnings)

    def compile(
        self, code_dir: Path, release: bool = True
    ) -> RustCompilationResult:
        """
        Compile Rust code with cargo build.

        Args:
            code_dir: Directory containing Rust project
            release: Use release mode (default: True)

        Returns:
            Compilation result
        """
        build_cmd = [self.cargo_binary, "build"]

        if release:
            build_cmd.append("--release")

        start_time = time.time()
        errors = []
        warnings = []

        try:
            result = subprocess.run(
                build_cmd,
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes for compilation
            )

            build_time_ms = (time.time() - start_time) * 1000

            if result.returncode != 0:
                errors.append(f"Compilation failed: {result.stderr}")
                return RustCompilationResult(
                    success=False,
                    build_time_ms=build_time_ms,
                    errors=errors,
                    release_mode=release,
                )

            # Extract warnings from stderr
            if result.stderr:
                warning_lines = [
                    line for line in result.stderr.split("\n") if "warning:" in line
                ]
                warnings.extend(warning_lines)

            # Find the binary
            target_dir = code_dir / "target" / ("release" if release else "debug")

            # Look for the binary - could be named after the crate
            cargo_toml = code_dir / "Cargo.toml"
            if cargo_toml.exists():
                # Try to extract package name from Cargo.toml
                with open(cargo_toml, 'r') as f:
                    for line in f:
                        if line.strip().startswith("name"):
                            # name = "server"
                            package_name = line.split("=")[1].strip().strip('"').strip("'")
                            binary_path = target_dir / package_name
                            if binary_path.exists():
                                binary_size = binary_path.stat().st_size
                                return RustCompilationResult(
                                    success=True,
                                    build_time_ms=build_time_ms,
                                    binary_path=str(binary_path),
                                    binary_size_bytes=binary_size,
                                    warnings=warnings,
                                    release_mode=release,
                                )

            # Fallback: look for any executable in target directory
            for binary_path in target_dir.iterdir():
                if binary_path.is_file() and os.access(binary_path, os.X_OK):
                    binary_size = binary_path.stat().st_size
                    return RustCompilationResult(
                        success=True,
                        build_time_ms=build_time_ms,
                        binary_path=str(binary_path),
                        binary_size_bytes=binary_size,
                        warnings=warnings,
                        release_mode=release,
                    )

            errors.append("Could not find compiled binary")
            return RustCompilationResult(
                success=False,
                build_time_ms=build_time_ms,
                errors=errors,
                release_mode=release,
            )

        except subprocess.TimeoutExpired:
            errors.append("Compilation timed out (>300s)")
            return RustCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                release_mode=release,
            )
        except Exception as e:
            errors.append(f"Compilation error: {e}")
            return RustCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                release_mode=release,
            )

    def start_server(
        self, binary_path: Path, port: int = 8080, startup_wait: float = 2.0
    ) -> RustServerResult:
        """
        Start Rust server binary.

        Args:
            binary_path: Path to compiled binary
            port: Server port
            startup_wait: Time to wait for startup (seconds)

        Returns:
            Server result
        """
        errors = []

        try:
            # Start server in background
            process = subprocess.Popen(
                [str(binary_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Store process
            self.server_processes[port] = process

            # Wait for startup
            time.sleep(startup_wait)

            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                errors.append(f"Server exited immediately: {stderr}")
                return RustServerResult(started=False, errors=errors)

            return RustServerResult(started=True, pid=process.pid)

        except Exception as e:
            errors.append(f"Failed to start server: {e}")
            return RustServerResult(started=False, errors=errors)

    def stop_server(self, port: int) -> Dict[str, Any]:
        """
        Stop running server process.

        Args:
            port: Port number of server to stop

        Returns:
            Dictionary with stop results
        """
        if port not in self.server_processes:
            return {
                "success": False,
                "message": f"No server running on port {port}",
            }

        process = self.server_processes[port]
        try:
            process.terminate()
            process.wait(timeout=5)
            del self.server_processes[port]
            return {
                "success": True,
                "message": f"Server on port {port} stopped",
            }
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            del self.server_processes[port]
            return {
                "success": True,
                "message": f"Server on port {port} killed (force)",
            }

    def test_health(
        self, port: int, timeout: float = 5.0
    ) -> tuple[bool, Optional[float], Optional[str]]:
        """
        Test server health endpoint.

        Args:
            port: Server port
            timeout: Request timeout

        Returns:
            Tuple of (success, response_time_ms, error)
        """
        url = f"http://localhost:{port}/health"
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            response_time_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                return True, response_time_ms, None
            else:
                return False, response_time_ms, f"HTTP {response.status_code}"

        except Exception as e:
            return False, None, str(e)

    def test_verb_execution(
        self, port: int, verb: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test MCP verb execution via HTTP.

        Args:
            port: Server port
            verb: Verb name (e.g., "echo.message@v1")
            params: Parameters to send

        Returns:
            Dictionary with execution results
        """
        result = {
            "passed": False,
            "verb": verb,
            "params": params,
            "response": None,
            "errors": [],
            "response_time": None,
        }

        try:
            # Construct MCP JSON-RPC request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": verb, "arguments": params},
            }

            start = time.time()
            response = requests.post(
                f"http://localhost:{port}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"},
                timeout=10,
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

    def calculate_code_quality(
        self, syntax: RustSyntaxResult, compilation: RustCompilationResult
    ) -> float:
        """
        Calculate code quality score (0-100).

        Args:
            syntax: Syntax validation result
            compilation: Compilation result

        Returns:
            Quality score
        """
        score = 100.0

        # Deduct for syntax errors
        if not syntax.valid:
            score -= 50.0

        # Deduct for compilation failures
        if not compilation.success:
            score -= 50.0

        # Deduct for warnings
        score -= len(syntax.warnings) * 2.0
        score -= len(compilation.warnings) * 2.0

        # Bonus for proper formatting
        if syntax.formatted:
            score += 5.0

        # Bonus for fast compilation
        if compilation.success and compilation.build_time_ms < 10000:
            score += 5.0

        return max(0.0, min(100.0, score))

    def run_full_validation(
        self, code_dir: Path, port: int, test_verbs: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run complete validation suite.

        Args:
            code_dir: Directory containing Rust project
            port: Server port
            test_verbs: List of dicts with 'verb' and 'params' keys

        Returns:
            Complete test results
        """
        results = {
            "code_path": str(code_dir),
            "port": port,
            "syntax_validation": None,
            "compilation": None,
            "server_startup": None,
            "health_check": None,
            "verb_tests": [],
            "overall_passed": False,
            "total_duration": None,
        }

        start_time = time.time()

        # Step 1: Validate syntax
        syntax_result = self.validate_syntax(code_dir)
        results["syntax_validation"] = {
            "valid": syntax_result.valid,
            "errors": syntax_result.errors,
            "warnings": syntax_result.warnings,
            "formatted": syntax_result.formatted,
        }

        if not syntax_result.valid:
            results["overall_passed"] = False
            results["total_duration"] = time.time() - start_time
            return results

        # Step 2: Compile
        compilation_result = self.compile(code_dir, release=True)
        results["compilation"] = {
            "success": compilation_result.success,
            "build_time_ms": compilation_result.build_time_ms,
            "binary_path": compilation_result.binary_path,
            "binary_size_bytes": compilation_result.binary_size_bytes,
            "errors": compilation_result.errors,
            "warnings": compilation_result.warnings,
            "release_mode": compilation_result.release_mode,
        }

        if not compilation_result.success:
            results["overall_passed"] = False
            results["total_duration"] = time.time() - start_time
            return results

        # Step 3: Start server
        server_result = self.start_server(Path(compilation_result.binary_path), port)
        results["server_startup"] = {
            "started": server_result.started,
            "pid": server_result.pid,
            "errors": server_result.errors,
        }

        if not server_result.started:
            results["overall_passed"] = False
            results["total_duration"] = time.time() - start_time
            return results

        try:
            # Step 4: Health check
            health_ok, health_time, health_error = self.test_health(port)
            results["health_check"] = {
                "passed": health_ok,
                "response_time_ms": health_time,
                "error": health_error,
            }

            # Step 5: Test verbs
            if test_verbs:
                for test in test_verbs:
                    verb_result = self.test_verb_execution(
                        port, test["verb"], test.get("params", {})
                    )
                    results["verb_tests"].append(verb_result)

            # Determine overall pass/fail
            results["overall_passed"] = (
                syntax_result.valid
                and compilation_result.success
                and server_result.started
                and health_ok
                and all(test["passed"] for test in results["verb_tests"])
            )

        finally:
            # Always stop the server
            stop_result = self.stop_server(port)
            results["server_shutdown"] = stop_result
            results["total_duration"] = time.time() - start_time

        return results

    def cleanup(self):
        """Stop all servers and clean up temporary directories."""
        # Stop all running servers
        for port in list(self.server_processes.keys()):
            self.stop_server(port)

        # Clean up temp directories
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        self.temp_dirs.clear()

    def create_test_workspace(self) -> Path:
        """
        Create temporary workspace for testing.

        Returns:
            Path to temporary directory
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="rust_test_"))
        self.temp_dirs.append(str(temp_dir))
        return temp_dir
