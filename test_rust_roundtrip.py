#!/usr/bin/env python3
"""
Test full round-trip: PW → Rust → PW
"""

import os
import tempfile
from pathlib import Path
from reverse_parsers.rust_parser import RustReverseParser

def normalize_pw(pw_text: str) -> str:
    """Normalize PW DSL for comparison (remove comments, extra whitespace)."""
    lines = []
    for line in pw_text.split('\n'):
        # Remove comments
        if line.strip().startswith('#'):
            continue
        # Keep non-empty lines
        if line.strip():
            lines.append(line.rstrip())
    return '\n'.join(lines)

def compare_pw_files(original: str, extracted: str) -> dict:
    """Compare two PW files and return analysis."""
    orig_normalized = normalize_pw(original)
    extr_normalized = normalize_pw(extracted)

    # Split into sections
    orig_lines = [l for l in orig_normalized.split('\n') if l.strip()]
    extr_lines = [l for l in extr_normalized.split('\n') if l.strip()]

    # Count matches
    matching_lines = 0
    for line in orig_lines:
        if line in extr_lines:
            matching_lines += 1

    accuracy = (matching_lines / len(orig_lines) * 100) if orig_lines else 0

    return {
        'total_lines': len(orig_lines),
        'matching_lines': matching_lines,
        'accuracy': accuracy,
        'original_normalized': orig_normalized,
        'extracted_normalized': extr_normalized,
        'identical': orig_normalized == extr_normalized
    }

def test_roundtrip(pw_file: str, rust_file: str):
    """Test PW → Rust → PW round-trip."""
    print(f"\n{'='*80}")
    print(f"Round-trip test: {Path(pw_file).name}")
    print(f"{'='*80}")

    # Read original PW
    with open(pw_file, 'r') as f:
        original_pw = f.read()

    print(f"\n1. Original PW file: {pw_file}")

    # Parse Rust code
    print(f"\n2. Parsing Rust code: {rust_file}")
    parser = RustReverseParser()
    agent = parser.parse_file(rust_file)

    print(f"   - Extracted agent: {agent.name}")
    print(f"   - Port: {agent.port}")
    print(f"   - Framework: {agent.framework}")
    print(f"   - Verbs: {len(agent.verbs)}")
    print(f"   - Tools: {len(agent.tools)}")
    print(f"   - Confidence: {agent.confidence_score:.0%}")

    # Convert back to PW
    print(f"\n3. Converting back to PW DSL...")
    extracted_pw = parser.to_pw_dsl(agent, include_metadata=False)

    # Compare
    print(f"\n4. Comparing original vs extracted...")
    comparison = compare_pw_files(original_pw, extracted_pw)

    print(f"\n   Results:")
    print(f"   - Total lines in original: {comparison['total_lines']}")
    print(f"   - Matching lines: {comparison['matching_lines']}")
    print(f"   - Accuracy: {comparison['accuracy']:.1f}%")
    print(f"   - Identical: {comparison['identical']}")

    if not comparison['identical']:
        print(f"\n   Differences:")
        print(f"\n   Original (normalized):")
        print("   " + "\n   ".join(comparison['original_normalized'].split('\n')))
        print(f"\n   Extracted (normalized):")
        print("   " + "\n   ".join(comparison['extracted_normalized'].split('\n')))

    return comparison


if __name__ == '__main__':
    base_dir = '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware'

    tests = [
        {
            'name': 'Minimal Rust Agent',
            'pw': f'{base_dir}/tests/bidirectional/fixtures/rust_minimal.pw',
            'rust': f'{base_dir}/tests/bidirectional/generated/rust/minimal_rust_agent/src/main.rs',
        },
        {
            'name': 'Tool Rust Agent',
            'pw': f'{base_dir}/tests/bidirectional/fixtures/rust_with_tools.pw',
            'rust': f'{base_dir}/tests/bidirectional/generated/rust/tool_rust_agent/src/main.rs',
        },
    ]

    results = []
    for test in tests:
        result = test_roundtrip(test['pw'], test['rust'])
        results.append({
            'name': test['name'],
            'accuracy': result['accuracy'],
            'identical': result['identical']
        })

    # Summary
    print(f"\n\n{'='*80}")
    print("ROUND-TRIP TEST SUMMARY")
    print(f"{'='*80}")

    for result in results:
        status = "✓ PERFECT" if result['identical'] else f"○ {result['accuracy']:.1f}%"
        print(f"{result['name']:30s} {status}")

    avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
    perfect_count = sum(1 for r in results if r['identical'])

    print(f"\n{'='*80}")
    print(f"Average Accuracy: {avg_accuracy:.1f}%")
    print(f"Perfect Round-trips: {perfect_count}/{len(results)}")
    print(f"{'='*80}\n")
