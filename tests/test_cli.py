"""
Tests for CLI commands.
"""

import subprocess
import sys
from pathlib import Path


def test_cli_version():
    """Test version command."""
    result = subprocess.run(
        [sys.executable, "cli/main.py", "version"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Promptware v0.3.0" in result.stdout
    assert "Python" in result.stdout
    assert "Node.js" in result.stdout
    assert "Go" in result.stdout


def test_cli_test_command():
    """Test the test command."""
    result = subprocess.run(
        [sys.executable, "cli/main.py", "test", "examples/cross_language/data_processor.pw"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Parse: OK" in result.stdout
    assert "data-processor" in result.stdout
    assert "Generation: OK" in result.stdout
    assert "All tests passed!" in result.stdout


def test_cli_generate_command():
    """Test the generate command."""
    # Use a temporary output file
    output_file = Path("test_output_server.js")

    try:
        result = subprocess.run(
            [
                sys.executable, "cli/main.py", "generate",
                "examples/cross_language/data_processor.pw",
                "-o", str(output_file)
            ],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "Success!" in result.stdout
        assert output_file.exists()
        assert output_file.stat().st_size > 0

        # Check generated content
        content = output_file.read_text()
        assert "const express = require('express')" in content
        assert "data-processor" in content

    finally:
        # Cleanup
        if output_file.exists():
            output_file.unlink()


def test_cli_generate_python():
    """Test generating Python server."""
    output_file = Path("test_python_server.py")

    try:
        result = subprocess.run(
            [
                sys.executable, "cli/main.py", "generate",
                "examples/cross_language/data_processor.pw",
                "--lang", "python",
                "-o", str(output_file)
            ],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert output_file.exists()

        content = output_file.read_text()
        assert "from fastapi import FastAPI" in content
        assert "data-processor" in content

    finally:
        if output_file.exists():
            output_file.unlink()


def test_cli_generate_go():
    """Test generating Go server."""
    output_file = Path("test_go_server.go")

    try:
        result = subprocess.run(
            [
                sys.executable, "cli/main.py", "generate",
                "examples/cross_language/cache_service.pw",
                "-o", str(output_file)
            ],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert output_file.exists()

        content = output_file.read_text()
        assert "package main" in content
        assert "import (" in content

    finally:
        if output_file.exists():
            output_file.unlink()


def test_cli_invalid_file():
    """Test error handling for non-existent file."""
    result = subprocess.run(
        [sys.executable, "cli/main.py", "test", "nonexistent.pw"],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "Error" in result.stdout or "Error" in result.stderr


def test_cli_help():
    """Test help output."""
    result = subprocess.run(
        [sys.executable, "cli/main.py", "--help"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "generate" in result.stdout
    assert "run" in result.stdout
    assert "test" in result.stdout
    assert "version" in result.stdout