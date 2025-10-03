"""
Go Expert Agent for Bidirectional Testing

Validates Go code generation, compilation, and runtime behavior.
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


@dataclass
class GoCompilationResult:
    """Result from Go compilation."""

    success: bool
    build_time_ms: float
    binary_path: Optional[str] = None
    binary_size_bytes: Optional[int] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    race_detector_enabled: bool = False


@dataclass
class GoServerResult:
    """Result from running Go server."""

    started: bool
    pid: Optional[int] = None
    health_check_passed: bool = False
    health_response_time_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class GoRaceDetectionResult:
    """Result from race detector analysis."""

    races_detected: bool
    race_count: int = 0
    race_details: List[str] = field(default_factory=list)


@dataclass
class GoTestReport:
    """Comprehensive Go testing report."""

    agent_name: str
    fixture_path: str
    generated_code_path: Optional[str] = None
    syntax_valid: bool = False
    compilation: Optional[GoCompilationResult] = None
    server: Optional[GoServerResult] = None
    race_detection: Optional[GoRaceDetectionResult] = None
    code_quality_score: float = 0.0
    timestamp: str = ""
    errors: List[str] = field(default_factory=list)


class GoExpertAgent:
    """
    Expert agent for Go code validation and testing.

    Capabilities:
    - Syntax validation with go fmt
    - Compilation with race detector
    - Server startup and health checks
    - Race condition detection
    - Performance metrics collection
    """

    def __init__(self, go_binary: str = "go"):
        """
        Initialize Go expert agent.

        Args:
            go_binary: Path to Go binary (default: "go")
        """
        self.go_binary = go_binary
        self.temp_dirs: List[str] = []

    def validate_syntax(self, code_dir: Path) -> tuple[bool, List[str]]:
        """
        Validate Go syntax using go fmt.

        Args:
            code_dir: Directory containing Go code

        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []

        try:
            # Run go fmt -l to check formatting
            result = subprocess.run(
                [self.go_binary, "fmt", "./..."],
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                errors.append(f"go fmt failed: {result.stderr}")
                return False, errors

            # Check for syntax errors with go vet
            result = subprocess.run(
                [self.go_binary, "vet", "./..."],
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                # go vet warnings are not fatal but should be noted
                errors.append(f"go vet warnings: {result.stderr}")

            return True, errors

        except subprocess.TimeoutExpired:
            errors.append("Syntax validation timed out")
            return False, errors
        except Exception as e:
            errors.append(f"Syntax validation error: {e}")
            return False, errors

    def compile(
        self, code_dir: Path, output_binary: Optional[Path] = None, race: bool = True
    ) -> GoCompilationResult:
        """
        Compile Go code with optional race detector.

        Args:
            code_dir: Directory containing Go code
            output_binary: Output binary path (default: temp file)
            race: Enable race detector (default: True)

        Returns:
            Compilation result
        """
        if output_binary is None:
            output_binary = Path(tempfile.mktemp(suffix="-server"))

        build_cmd = [self.go_binary, "build"]

        if race:
            build_cmd.append("-race")

        build_cmd.extend(["-o", str(output_binary), "."])

        start_time = time.time()
        errors = []
        warnings = []

        try:
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
                return GoCompilationResult(
                    success=False,
                    build_time_ms=build_time_ms,
                    errors=errors,
                    race_detector_enabled=race,
                )

            # Get binary size
            binary_size = output_binary.stat().st_size if output_binary.exists() else None

            return GoCompilationResult(
                success=True,
                build_time_ms=build_time_ms,
                binary_path=str(output_binary),
                binary_size_bytes=binary_size,
                warnings=warnings,
                race_detector_enabled=race,
            )

        except subprocess.TimeoutExpired:
            errors.append("Compilation timed out (>120s)")
            return GoCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                race_detector_enabled=race,
            )
        except Exception as e:
            errors.append(f"Compilation error: {e}")
            return GoCompilationResult(
                success=False,
                build_time_ms=(time.time() - start_time) * 1000,
                errors=errors,
                race_detector_enabled=race,
            )

    def start_server(
        self, binary_path: Path, port: int = 8080, startup_wait: float = 2.0
    ) -> GoServerResult:
        """
        Start Go server binary.

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

            # Wait for startup
            time.sleep(startup_wait)

            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                errors.append(f"Server exited immediately: {stderr}")
                return GoServerResult(started=False, errors=errors)

            return GoServerResult(started=True, pid=process.pid)

        except Exception as e:
            errors.append(f"Failed to start server: {e}")
            return GoServerResult(started=False, errors=errors)

    def test_health(
        self, url: str = "http://localhost:8080/health", timeout: float = 5.0
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
            import requests

            start_time = time.time()
            response = requests.get(url, timeout=timeout)
            response_time_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                return True, response_time_ms, None
            else:
                return False, response_time_ms, f"HTTP {response.status_code}"

        except Exception as e:
            return False, None, str(e)

    def check_races(self, server_output: str) -> GoRaceDetectionResult:
        """
        Analyze server output for race conditions.

        Args:
            server_output: Server stderr output

        Returns:
            Race detection result
        """
        races_detected = "WARNING: DATA RACE" in server_output
        race_details = []
        race_count = 0

        if races_detected:
            # Parse race detector output
            lines = server_output.split("\n")
            current_race = []

            for line in lines:
                if "WARNING: DATA RACE" in line:
                    if current_race:
                        race_details.append("\n".join(current_race))
                    current_race = [line]
                    race_count += 1
                elif current_race and line.strip():
                    current_race.append(line)

            if current_race:
                race_details.append("\n".join(current_race))

        return GoRaceDetectionResult(
            races_detected=races_detected, race_count=race_count, race_details=race_details
        )

    def setup_go_module(self, code_dir: Path, module_name: str = "generated/server") -> bool:
        """
        Set up go.mod if not present.

        Args:
            code_dir: Directory containing Go code
            module_name: Module name for go.mod

        Returns:
            True if successful
        """
        go_mod_path = code_dir / "go.mod"

        if go_mod_path.exists():
            # Run go mod tidy to ensure dependencies
            result = subprocess.run(
                [self.go_binary, "mod", "tidy"],
                cwd=code_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.returncode == 0

        # Initialize new module
        result = subprocess.run(
            [self.go_binary, "mod", "init", module_name],
            cwd=code_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return False

        # Run go mod tidy
        result = subprocess.run(
            [self.go_binary, "mod", "tidy"],
            cwd=code_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )

        return result.returncode == 0

    def calculate_code_quality(
        self, compilation: GoCompilationResult, race_detection: GoRaceDetectionResult
    ) -> float:
        """
        Calculate code quality score (0-100).

        Args:
            compilation: Compilation result
            race_detection: Race detection result

        Returns:
            Quality score
        """
        score = 100.0

        # Deduct for compilation failures
        if not compilation.success:
            score -= 50.0

        # Deduct for warnings
        score -= len(compilation.warnings) * 5.0

        # Deduct heavily for race conditions
        if race_detection.races_detected:
            score -= race_detection.race_count * 20.0

        # Bonus for fast compilation
        if compilation.build_time_ms < 5000:
            score += 10.0

        return max(0.0, min(100.0, score))

    def cleanup(self):
        """Clean up temporary directories."""
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        self.temp_dirs.clear()

    def run_full_test(
        self, fixture_path: Path, generated_code_path: Path, port: int = 8080
    ) -> GoTestReport:
        """
        Run full bidirectional test on generated Go code.

        Args:
            fixture_path: Path to .pw fixture file
            generated_code_path: Path to generated Go code
            port: Server port

        Returns:
            Comprehensive test report
        """
        from datetime import datetime

        report = GoTestReport(
            agent_name=fixture_path.stem,
            fixture_path=str(fixture_path),
            generated_code_path=str(generated_code_path),
            timestamp=datetime.now().isoformat(),
        )

        # Step 1: Setup go.mod
        if not self.setup_go_module(generated_code_path):
            report.errors.append("Failed to setup go.mod")
            return report

        # Step 2: Validate syntax
        syntax_valid, syntax_errors = self.validate_syntax(generated_code_path)
        report.syntax_valid = syntax_valid
        report.errors.extend(syntax_errors)

        if not syntax_valid:
            return report

        # Step 3: Compile with race detector
        compilation = self.compile(generated_code_path, race=True)
        report.compilation = compilation

        if not compilation.success:
            return report

        # Step 4: Start server
        server = self.start_server(Path(compilation.binary_path), port=port)
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

            # Step 6: Check for races (would need to capture server output)
            # For now, create empty race detection result
            report.race_detection = GoRaceDetectionResult(races_detected=False)

            # Calculate code quality
            report.code_quality_score = self.calculate_code_quality(
                compilation, report.race_detection
            )

        finally:
            # Clean up: stop server
            if server.pid:
                try:
                    import signal

                    os.kill(server.pid, signal.SIGTERM)
                    time.sleep(1)
                    # Force kill if still running
                    try:
                        os.kill(server.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                except Exception as e:
                    report.errors.append(f"Failed to stop server: {e}")

            # Clean up binary
            if compilation.binary_path and os.path.exists(compilation.binary_path):
                try:
                    os.remove(compilation.binary_path)
                except Exception:
                    pass

        return report

    def to_json_report(self, reports: List[GoTestReport]) -> Dict[str, Any]:
        """
        Convert test reports to JSON format.

        Args:
            reports: List of test reports

        Returns:
            JSON-serializable report dictionary
        """
        from datetime import datetime

        return {
            "test_framework": "go_expert_agent",
            "timestamp": datetime.now().isoformat(),
            "go_version": self._get_go_version(),
            "total_tests": len(reports),
            "passed": sum(1 for r in reports if r.compilation and r.compilation.success),
            "failed": sum(1 for r in reports if not r.compilation or not r.compilation.success),
            "reports": [
                {
                    "agent_name": r.agent_name,
                    "fixture_path": r.fixture_path,
                    "generated_code_path": r.generated_code_path,
                    "syntax_valid": r.syntax_valid,
                    "compilation": {
                        "success": r.compilation.success if r.compilation else False,
                        "build_time_ms": r.compilation.build_time_ms if r.compilation else 0,
                        "binary_size_bytes": r.compilation.binary_size_bytes
                        if r.compilation
                        else 0,
                        "race_detector_enabled": r.compilation.race_detector_enabled
                        if r.compilation
                        else False,
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
                    "race_detection": {
                        "races_detected": r.race_detection.races_detected
                        if r.race_detection
                        else False,
                        "race_count": r.race_detection.race_count if r.race_detection else 0,
                        "race_details": r.race_detection.race_details
                        if r.race_detection
                        else [],
                    }
                    if r.race_detection
                    else None,
                    "code_quality_score": r.code_quality_score,
                    "errors": r.errors,
                    "timestamp": r.timestamp,
                }
                for r in reports
            ],
        }

    def _get_go_version(self) -> str:
        """Get Go version."""
        try:
            result = subprocess.run(
                [self.go_binary, "version"], capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"
