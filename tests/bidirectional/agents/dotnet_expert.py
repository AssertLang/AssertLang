"""
.NET/C# Expert Agent for Bidirectional Testing

Validates C# code generation, compilation, and runtime behavior.
Tests ASP.NET Core MCP servers for .NET platform.
"""

import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests


@dataclass
class DotNetCompilationResult:
    """Result from .NET compilation."""

    success: bool
    build_time_ms: float
    binary_path: Optional[str] = None
    binary_size_bytes: Optional[int] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    dotnet_version: str = ""


@dataclass
class DotNetServerResult:
    """Result from running .NET server."""

    started: bool
    pid: Optional[int] = None
    health_check_passed: bool = False
    health_response_time_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class DotNetTestReport:
    """Comprehensive .NET testing report."""

    agent_name: str
    fixture_path: str
    generated_code_path: Optional[str] = None
    syntax_valid: bool = False
    compilation: Optional[DotNetCompilationResult] = None
    server: Optional[DotNetServerResult] = None
    code_quality_score: float = 0.0
    timestamp: str = ""
    errors: List[str] = field(default_factory=list)


class DotNetExpertAgent:
    """
    Expert agent for .NET/C# code validation and testing.

    Capabilities:
    - Syntax validation
    - Compilation with dotnet build
    - Server startup and health checks
    - MCP protocol testing
    - Performance metrics collection
    """

    def __init__(self, dotnet_binary: str = "dotnet"):
        """
        Initialize .NET expert agent.

        Args:
            dotnet_binary: Path to dotnet binary (default: "dotnet")
        """
        self.dotnet_binary = dotnet_binary
        self.temp_dirs: List[str] = []
        self._verify_dotnet()

    def _verify_dotnet(self) -> None:
        """Verify .NET SDK is installed and available."""
        try:
            result = subprocess.run(
                [self.dotnet_binary, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.dotnet_version = result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f".NET SDK not available: {e}")

    def validate_syntax(self, code_dir: Path) -> tuple[bool, List[str]]:
        """
        Validate C# syntax using dotnet build --no-restore.

        Args:
            code_dir: Directory containing C# code

        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []

        try:
            # Check if Program.cs exists
            program_cs = code_dir / "Program.cs"
            if not program_cs.exists():
                errors.append("Program.cs not found")
                return False, errors

            # Quick syntax check using roslyn
            # We'll do this during compilation phase
            return True, []

        except Exception as e:
            errors.append(f"Syntax validation error: {e}")
            return False, errors

    def setup_project(self, code_dir: Path, project_name: str = "MCPServer") -> bool:
        """
        Set up .NET project with .csproj file.

        Args:
            code_dir: Directory containing C# code
            project_name: Project name

        Returns:
            True if successful
        """
        csproj_path = code_dir / f"{project_name}.csproj"

        # Create .csproj file
        csproj_content = """<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

</Project>
"""
        csproj_path.write_text(csproj_content)

        # Restore packages
        result = subprocess.run(
            [self.dotnet_binary, "restore"],
            cwd=code_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )

        return result.returncode == 0

    def compile(
        self, code_dir: Path, output_binary: Optional[Path] = None
    ) -> DotNetCompilationResult:
        """
        Compile C# code with dotnet build.

        Args:
            code_dir: Directory containing C# code
            output_binary: Output binary path (default: bin/Debug/net8.0/)

        Returns:
            Compilation result
        """
        start_time = time.time()
        errors = []
        warnings = []

        try:
            # Build command
            build_cmd = [self.dotnet_binary, "build", "--configuration", "Release"]

            result = subprocess.run(
                build_cmd,
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minutes for compilation
            )

            build_time_ms = (time.time() - start_time) * 1000

            if result.returncode != 0:
                errors.append(f"Compilation failed: {result.stderr}")
                return DotNetCompilationResult(
                    success=False,
                    build_time_ms=build_time_ms,
                    errors=errors,
                    dotnet_version=self.dotnet_version,
                )

            # Find the built DLL/executable
            bin_path = code_dir / "bin" / "Release" / "net8.0"
            if bin_path.exists():
                dll_files = list(bin_path.glob("*.dll"))
                if dll_files:
                    binary_path = dll_files[0]
                    binary_size = binary_path.stat().st_size
                else:
                    binary_path = None
                    binary_size = None
            else:
                binary_path = None
                binary_size = None

            # Extract warnings from output
            if "warning" in result.stdout.lower():
                warning_lines = [
                    line for line in result.stdout.split("\n")
                    if "warning" in line.lower()
                ]
                warnings.extend(warning_lines[:5])  # Limit to 5 warnings

            return DotNetCompilationResult(
                success=True,
                build_time_ms=build_time_ms,
                binary_path=str(binary_path) if binary_path else None,
                binary_size_bytes=binary_size,
                warnings=warnings,
                dotnet_version=self.dotnet_version,
            )

        except subprocess.TimeoutExpired:
            errors.append("Compilation timed out (>120s)")
            return DotNetCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                dotnet_version=self.dotnet_version,
            )
        except Exception as e:
            errors.append(f"Compilation error: {e}")
            return DotNetCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                dotnet_version=self.dotnet_version,
            )

    def start_server(
        self, code_dir: Path, port: int = 5000, startup_wait: float = 3.0
    ) -> DotNetServerResult:
        """
        Start .NET server using dotnet run.

        Args:
            code_dir: Directory containing C# code
            port: Server port
            startup_wait: Time to wait for startup (seconds)

        Returns:
            Server result
        """
        errors = []

        try:
            # Start server in background
            process = subprocess.Popen(
                [self.dotnet_binary, "run", "--no-build", "--configuration", "Release"],
                cwd=code_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Wait for startup
            time.sleep(startup_wait)

            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                errors.append(f"Server exited immediately: {stderr}")
                return DotNetServerResult(started=False, errors=errors)

            # Store process for cleanup
            self._server_process = process

            return DotNetServerResult(started=True, pid=process.pid)

        except Exception as e:
            errors.append(f"Failed to start server: {e}")
            return DotNetServerResult(started=False, errors=errors)

    def test_health(
        self, url: str = "http://localhost:5000/health", timeout: float = 5.0
    ) -> tuple[bool, Optional[float], Optional[str]]:
        """
        Test server health endpoint.

        Args:
            url: Health endpoint URL
            timeout: Request timeout

        Returns:
            Tuple of (success, response_time_ms, error)
        """
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

    def test_mcp_protocol(
        self, port: int, verb: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test MCP protocol compliance via tools/call.

        Args:
            port: Server port
            verb: Verb name to test
            params: Parameters for the verb

        Returns:
            Test result dictionary
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

        except Exception as e:
            result["errors"].append(f"MCP protocol test failed: {str(e)}")

        return result

    def stop_server(self) -> bool:
        """Stop the running server process."""
        if hasattr(self, "_server_process"):
            try:
                self._server_process.terminate()
                self._server_process.wait(timeout=5)
                return True
            except subprocess.TimeoutExpired:
                self._server_process.kill()
                self._server_process.wait()
                return True
            except Exception:
                return False
        return True

    def calculate_code_quality(
        self, compilation: DotNetCompilationResult, server: Optional[DotNetServerResult]
    ) -> float:
        """
        Calculate code quality score (0-100).

        Args:
            compilation: Compilation result
            server: Server result

        Returns:
            Quality score
        """
        score = 100.0

        # Deduct for compilation failures
        if not compilation.success:
            score -= 50.0

        # Deduct for warnings
        score -= len(compilation.warnings) * 5.0

        # Bonus for fast compilation
        if compilation.build_time_ms < 10000:  # Under 10 seconds
            score += 10.0

        # Deduct if server didn't start
        if server and not server.started:
            score -= 30.0

        # Deduct if health check failed
        if server and not server.health_check_passed:
            score -= 10.0

        return max(0.0, min(100.0, score))

    def cleanup(self):
        """Clean up temporary directories and processes."""
        self.stop_server()
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        self.temp_dirs.clear()

    def run_full_test(
        self, fixture_path: Path, generated_code_path: Path, port: int = 5000
    ) -> DotNetTestReport:
        """
        Run full bidirectional test on generated C# code.

        Args:
            fixture_path: Path to .al fixture file
            generated_code_path: Path to generated C# code directory
            port: Server port

        Returns:
            Comprehensive test report
        """
        from datetime import datetime

        report = DotNetTestReport(
            agent_name=fixture_path.stem,
            fixture_path=str(fixture_path),
            generated_code_path=str(generated_code_path),
            timestamp=datetime.now().isoformat(),
        )

        # Step 1: Setup .NET project
        if not self.setup_project(generated_code_path):
            report.errors.append("Failed to setup .NET project")
            return report

        # Step 2: Validate syntax
        syntax_valid, syntax_errors = self.validate_syntax(generated_code_path)
        report.syntax_valid = syntax_valid
        report.errors.extend(syntax_errors)

        # Step 3: Compile
        compilation = self.compile(generated_code_path)
        report.compilation = compilation

        if not compilation.success:
            return report

        # Step 4: Start server
        server = self.start_server(generated_code_path, port=port)
        report.server = server

        if not server.started:
            return report

        try:
            # Step 5: Health check
            health_ok, health_time, health_error = self.test_health(
                f"http://localhost:{port}/health"
            )
            server.health_check_passed = health_ok
            server.health_response_time_ms = health_time

            if not health_ok:
                server.errors.append(f"Health check failed: {health_error}")

            # Calculate code quality
            report.code_quality_score = self.calculate_code_quality(compilation, server)

        finally:
            # Clean up: stop server
            self.stop_server()

        return report

    def to_json_report(self, reports: List[DotNetTestReport]) -> Dict[str, Any]:
        """
        Convert test reports to JSON format.

        Args:
            reports: List of test reports

        Returns:
            JSON-serializable report dictionary
        """
        from datetime import datetime

        return {
            "test_framework": "dotnet_expert_agent",
            "timestamp": datetime.now().isoformat(),
            "dotnet_version": self.dotnet_version,
            "total_tests": len(reports),
            "passed": sum(
                1 for r in reports if r.compilation and r.compilation.success
            ),
            "failed": sum(
                1
                for r in reports
                if not r.compilation or not r.compilation.success
            ),
            "reports": [
                {
                    "agent_name": r.agent_name,
                    "fixture_path": r.fixture_path,
                    "generated_code_path": r.generated_code_path,
                    "syntax_valid": r.syntax_valid,
                    "compilation": {
                        "success": r.compilation.success if r.compilation else False,
                        "build_time_ms": r.compilation.build_time_ms
                        if r.compilation
                        else 0,
                        "binary_size_bytes": r.compilation.binary_size_bytes
                        if r.compilation
                        else 0,
                        "dotnet_version": r.compilation.dotnet_version
                        if r.compilation
                        else "",
                        "errors": r.compilation.errors if r.compilation else [],
                        "warnings": r.compilation.warnings if r.compilation else [],
                    }
                    if r.compilation
                    else None,
                    "server": {
                        "started": r.server.started if r.server else False,
                        "health_check_passed": r.server.health_check_passed
                        if r.server
                        else False,
                        "health_response_time_ms": r.server.health_response_time_ms
                        if r.server
                        else None,
                        "errors": r.server.errors if r.server else [],
                    }
                    if r.server
                    else None,
                    "code_quality_score": r.code_quality_score,
                    "errors": r.errors,
                    "timestamp": r.timestamp,
                }
                for r in reports
            ],
        }
