#!/usr/bin/env python3
"""Benchmark Promptware compilation performance"""

import time
import os
import sys
import subprocess
from pathlib import Path

# Add promptware to path
sys.path.insert(0, str(Path(__file__).parent))

def run_benchmark(pw_file, lang, iterations=3):
    """Benchmark compilation of a .pw file to target language"""
    times = []
    file_size = os.path.getsize(pw_file)
    lines = len(open(pw_file).readlines())

    print(f"\n{'='*60}")
    print(f"Benchmarking: {Path(pw_file).name}")
    print(f"Size: {file_size} bytes, {lines} lines")
    print(f"Target: {lang}")
    print(f"{'='*60}")

    for i in range(iterations):
        start = time.time()

        # Run promptware build
        result = subprocess.run(
            [sys.executable, "-m", "promptware.cli", "build", pw_file, "--lang", lang, "-o", f"/tmp/bench_output.{lang}"],
            capture_output=True,
            text=True
        )

        end = time.time()
        elapsed = end - start
        times.append(elapsed)

        if result.returncode != 0:
            print(f"  ❌ Run {i+1}: FAILED")
            print(result.stderr[:200])
            return None
        else:
            print(f"  ✅ Run {i+1}: {elapsed:.3f}s")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\n  Average: {avg_time:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")
    print(f"  LOC/sec: {lines/avg_time:.0f}")

    return {
        'file': Path(pw_file).name,
        'lines': lines,
        'bytes': file_size,
        'lang': lang,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'loc_per_sec': lines/avg_time
    }

def main():
    examples_dir = Path(__file__).parent / "examples"

    # Test files of different sizes
    test_files = [
        ("hello-world.pw", "python"),          # 4 lines
        ("calculator.pw", "python"),           # 178 lines
        ("todo_list_manager.pw", "python"),    # 245 lines
        ("simple_web_api.pw", "python"),       # 321 lines
    ]

    results = []

    print("\n" + "="*60)
    print("PROMPTWARE v2.1.0b1 PERFORMANCE BENCHMARKS")
    print("="*60)

    for pw_file, lang in test_files:
        file_path = examples_dir / pw_file
        if file_path.exists():
            result = run_benchmark(str(file_path), lang)
            if result:
                results.append(result)
        else:
            print(f"⚠️  File not found: {file_path}")

    # Summary table
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'File':<25} {'Lines':>6} {'Time':>8} {'LOC/sec':>10}")
    print("-"*60)

    for r in results:
        print(f"{r['file']:<25} {r['lines']:>6} {r['avg_time']:>7.3f}s {r['loc_per_sec']:>9.0f}")

    if results:
        total_lines = sum(r['lines'] for r in results)
        total_time = sum(r['avg_time'] for r in results)
        print("-"*60)
        print(f"{'TOTAL':<25} {total_lines:>6} {total_time:>7.3f}s {total_lines/total_time:>9.0f}")

    return results

if __name__ == "__main__":
    results = main()
