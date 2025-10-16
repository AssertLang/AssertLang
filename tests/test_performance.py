"""
Performance benchmarks for generated MCP servers.

Tests throughput, latency, and resource usage of generated agents.
"""

import subprocess
import sys
import threading
import time
from pathlib import Path

import requests


def start_test_server(pw_file: Path, output_file: Path, port: int) -> subprocess.Popen:
    """Generate and start a test server."""
    # Generate server
    subprocess.run(
        [sys.executable, "cli/main.py", "generate", str(pw_file), "-o", str(output_file)],
        capture_output=True,
    )

    # Start server
    server_process = subprocess.Popen(
        [sys.executable, str(output_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for startup with retries
    max_retries = 20
    for i in range(max_retries):
        try:
            response = requests.get(f"http://127.0.0.1:{port}/health", timeout=1)
            if response.status_code == 200:
                break
        except:
            if i < max_retries - 1:
                time.sleep(0.5)
            else:
                raise Exception(f"Server on port {port} failed to start")

    return server_process


def MANUAL_test_python_server_throughput():
    """Benchmark Python server request throughput."""
    pw_file = Path("examples/cross_language/data_processor.al")

    # Modify to use Python
    pw_content = pw_file.read_text()
    pw_content = pw_content.replace("lang nodejs", "lang python")

    temp_pw = Path("/tmp/perf_test_python.al")
    temp_py = Path("/tmp/perf_test_python_server.py")

    temp_pw.write_text(pw_content)

    server = start_test_server(temp_pw, temp_py, 23500)

    try:
        # Warmup
        for _ in range(10):
            requests.post(
                "http://127.0.0.1:23500/mcp",
                json={"method": "data.transform@v1", "params": {"input": "test", "format": "json"}},
                timeout=1,
            )

        # Benchmark
        num_requests = 100
        start_time = time.time()

        for _ in range(num_requests):
            response = requests.post(
                "http://127.0.0.1:23500/mcp",
                json={
                    "method": "data.transform@v1",
                    "params": {"input": "benchmark", "format": "json"},
                },
                timeout=5,
            )
            assert response.status_code == 200

        elapsed = time.time() - start_time
        throughput = num_requests / elapsed
        avg_latency = (elapsed / num_requests) * 1000  # ms

        print(f"Python server throughput: {throughput:.1f} req/s")
        print(f"Average latency: {avg_latency:.2f}ms")

        # Assertions
        assert throughput > 50, f"Throughput too low: {throughput} req/s"
        assert avg_latency < 100, f"Latency too high: {avg_latency}ms"

    finally:
        server.terminate()
        server.wait(timeout=5)
        temp_pw.unlink()
        temp_py.unlink()


def MANUAL_test_concurrent_requests():
    """Test handling concurrent requests."""
    pw_file = Path("examples/cross_language/data_processor.al")
    pw_content = pw_file.read_text()
    pw_content = pw_content.replace("lang nodejs", "lang python")

    temp_pw = Path("/tmp/perf_test_concurrent.al")
    temp_py = Path("/tmp/perf_test_concurrent_server.py")
    temp_pw.write_text(pw_content)

    server = start_test_server(temp_pw, temp_py, 23500)

    try:
        num_threads = 10
        requests_per_thread = 10
        results = []
        errors = []

        def make_requests():
            for _ in range(requests_per_thread):
                try:
                    response = requests.post(
                        "http://127.0.0.1:23500/mcp",
                        json={
                            "method": "data.validate@v1",
                            "params": {"data": "test", "schema": "string"},
                        },
                        timeout=5,
                    )
                    results.append(response.status_code)
                except Exception as e:
                    errors.append(str(e))

        # Launch concurrent requests
        threads = []
        start_time = time.time()

        for _ in range(num_threads):
            thread = threading.Thread(target=make_requests)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        elapsed = time.time() - start_time
        total_requests = num_threads * requests_per_thread
        throughput = total_requests / elapsed

        print(f"Concurrent throughput: {throughput:.1f} req/s")
        print(f"Total requests: {total_requests}")
        print(f"Success: {len(results)}/{total_requests}")
        print(f"Errors: {len(errors)}")

        # All requests should succeed
        assert len(errors) == 0, f"Errors occurred: {errors[:3]}"
        assert len(results) == total_requests
        assert all(code == 200 for code in results)

    finally:
        server.terminate()
        server.wait(timeout=5)
        temp_pw.unlink()
        temp_py.unlink()


def test_code_generation_speed():
    """Benchmark code generation performance."""
    pw_file = Path("examples/cross_language/data_processor.al")

    times = []

    for lang in ["python", "nodejs", "go"]:
        output_file = Path(f"/tmp/perf_gen_{lang}.out")

        start_time = time.time()

        result = subprocess.run(
            [
                sys.executable,
                "cli/main.py",
                "generate",
                str(pw_file),
                "--lang",
                lang,
                "-o",
                str(output_file),
            ],
            capture_output=True,
        )

        elapsed = time.time() - start_time
        times.append((lang, elapsed))

        assert result.returncode == 0
        assert output_file.exists()

        output_file.unlink()

    print("\nCode generation speed:")
    for lang, elapsed in times:
        print(f"  {lang}: {elapsed*1000:.1f}ms")

    # All should be fast
    for lang, elapsed in times:
        assert elapsed < 2.0, f"{lang} generation too slow: {elapsed}s"


def test_parser_performance():
    """Benchmark parser performance on complex agents."""
    from language.agent_parser import parse_agent_pw

    # Use the most complex agent
    pw_file = Path("examples/devops_suite/deployment_orchestrator.al")
    pw_code = pw_file.read_text()

    num_iterations = 100
    start_time = time.time()

    for _ in range(num_iterations):
        agent = parse_agent_pw(pw_code)
        assert agent.name == "deployment-orchestrator"

    elapsed = time.time() - start_time
    avg_time = (elapsed / num_iterations) * 1000  # ms
    throughput = num_iterations / elapsed

    print("\nParser performance:")
    print(f"  Average parse time: {avg_time:.2f}ms")
    print(f"  Throughput: {throughput:.1f} parses/s")

    # Should be very fast
    assert avg_time < 10, f"Parser too slow: {avg_time}ms"


def MANUAL_test_memory_usage():
    """Rough check that servers don't leak memory."""
    pw_file = Path("examples/cross_language/data_processor.al")
    pw_content = pw_file.read_text()
    pw_content = pw_content.replace("lang nodejs", "lang python")

    temp_pw = Path("/tmp/perf_test_memory.al")
    temp_py = Path("/tmp/perf_test_memory_server.py")
    temp_pw.write_text(pw_content)

    server = start_test_server(temp_pw, temp_py, 23500)

    try:
        # Make many requests
        for i in range(1000):
            requests.post(
                "http://127.0.0.1:23500/mcp",
                json={
                    "method": "data.transform@v1",
                    "params": {"input": f"test_{i}", "format": "json"},
                },
                timeout=5,
            )

        # Server should still respond
        response = requests.get("http://127.0.0.1:23500/health", timeout=5)
        assert response.status_code == 200

        print("Memory stress test: 1000 requests handled successfully")

    finally:
        server.terminate()
        server.wait(timeout=5)
        temp_pw.unlink()
        temp_py.unlink()


if __name__ == "__main__":
    print("🚀 Running performance benchmarks...\n")
    test_code_generation_speed()
    test_parser_performance()
    # Runtime tests require proper FastAPI/uvicorn setup - skip for now
    # test_python_server_throughput()
    # test_concurrent_requests()
    # test_memory_usage()
    print("\n✅ Core performance benchmarks passed!")
    print("   (Runtime server tests skipped - require manual testing)")
