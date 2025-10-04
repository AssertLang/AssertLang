#!/usr/bin/env python3
"""
Test .NET Reverse Parser

Generate C# code from .pw fixtures and reverse parse back to PW DSL.
"""

import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from language.agent_parser import parse_agent_pw
from language.mcp_server_generator_dotnet import generate_dotnet_mcp_server
from reverse_parsers.dotnet_parser import DotNetReverseParser


def test_reverse_parser(fixture_path: Path):
    """Test round-trip: PW → C# → PW"""
    print(f"\nTesting: {fixture_path.name}")
    print("-" * 80)

    # Step 1: Parse original .pw file
    print("1. Parsing original .pw file...")
    original_pw = fixture_path.read_text()
    original_agent = parse_agent_pw(original_pw)
    print(f"   Agent: {original_agent.name}")
    print(f"   Port: {original_agent.port}")
    print(f"   Verbs: {len(original_agent.exposes)}")
    print(f"   Tools: {original_agent.tools}")

    # Step 2: Generate C# code
    print("\n2. Generating C# code...")
    csharp_code = generate_dotnet_mcp_server(original_agent)
    print(f"   Generated {len(csharp_code)} bytes of C# code")

    # Step 3: Save C# code to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cs', delete=False) as f:
        temp_cs_path = Path(f.name)
        f.write(csharp_code)

    print(f"   Saved to: {temp_cs_path}")

    # Step 4: Reverse parse C# → PW
    print("\n3. Reverse parsing C# → PW...")
    parser = DotNetReverseParser()
    extracted = parser.parse_file(str(temp_cs_path))

    print(f"   Extracted agent: {extracted.name}")
    print(f"   Framework: {extracted.framework}")
    print(f"   Port: {extracted.port}")
    print(f"   Verbs: {len(extracted.verbs)}")
    print(f"   Tools: {extracted.tools}")
    print(f"   Confidence: {extracted.confidence_score:.0%}")

    # Step 5: Convert to PW DSL
    print("\n4. Converting to PW DSL...")
    regenerated_pw = parser.to_pw_dsl(extracted, include_metadata=True)

    print("\n" + "=" * 80)
    print("ORIGINAL PW:")
    print("=" * 80)
    print(original_pw)

    print("\n" + "=" * 80)
    print("EXTRACTED PW:")
    print("=" * 80)
    print(regenerated_pw)

    print("\n" + "=" * 80)
    print("C# CODE SAMPLE (first 2000 chars):")
    print("=" * 80)
    print(csharp_code[:2000])
    print("...")

    # Step 6: Compare
    print("\n" + "=" * 80)
    print("COMPARISON:")
    print("=" * 80)

    # Compare verbs
    original_verbs = {v.verb for v in original_agent.exposes}
    extracted_verbs = {v['name'] for v in extracted.verbs}

    print(f"Original verbs: {original_verbs}")
    print(f"Extracted verbs: {extracted_verbs}")

    if original_verbs == extracted_verbs:
        print("✓ All verbs extracted correctly!")
    else:
        missing = original_verbs - extracted_verbs
        extra = extracted_verbs - original_verbs
        if missing:
            print(f"✗ Missing verbs: {missing}")
        if extra:
            print(f"✗ Extra verbs: {extra}")

    # Compare tools
    original_tools = set(original_agent.tools)
    extracted_tools = set(extracted.tools)

    print(f"\nOriginal tools: {original_tools}")
    print(f"Extracted tools: {extracted_tools}")

    if original_tools == extracted_tools:
        print("✓ All tools extracted correctly!")
    else:
        missing = original_tools - extracted_tools
        extra = extracted_tools - original_tools
        if missing:
            print(f"✗ Missing tools: {missing}")
        if extra:
            print(f"✗ Extra tools: {extra}")

    # Compare params and returns
    print("\nVerb details:")
    for verb in extracted.verbs:
        print(f"\n  {verb['name']}:")
        if verb['params']:
            params_str = [f"{p['name']} ({p['type']})" for p in verb['params']]
            print(f"    params: {params_str}")
        else:
            print(f"    params: (none extracted)")
        if verb['returns']:
            returns_str = [f"{r['name']} ({r['type']})" for r in verb['returns']]
            print(f"    returns: {returns_str}")
        else:
            print(f"    returns: (none extracted)")

    # Success metrics
    print("\n" + "=" * 80)
    print("SUCCESS METRICS:")
    print("=" * 80)
    print(f"Confidence Score: {extracted.confidence_score:.0%}")
    print(f"Verbs Match: {original_verbs == extracted_verbs}")
    print(f"Tools Match: {original_tools == extracted_tools}")

    verbs_coverage = len(extracted_verbs & original_verbs) / len(original_verbs) if original_verbs else 1.0
    print(f"Verbs Coverage: {verbs_coverage:.0%}")

    # Count params/returns extracted
    total_params = sum(len(v['params']) for v in extracted.verbs)
    total_returns = sum(len(v['returns']) for v in extracted.verbs)
    print(f"Params Extracted: {total_params}")
    print(f"Returns Extracted: {total_returns}")

    # Cleanup
    temp_cs_path.unlink()

    return extracted.confidence_score >= 0.9 and verbs_coverage >= 0.9


def main():
    """Run all tests."""
    print("=" * 80)
    print(".NET REVERSE PARSER TESTS")
    print("=" * 80)

    # Find all .NET fixtures
    fixtures_dir = project_root / "tests" / "bidirectional" / "fixtures"
    fixtures = list(fixtures_dir.glob("dotnet_*.pw"))

    if not fixtures:
        print(f"ERROR: No .NET fixtures found in {fixtures_dir}")
        return 1

    print(f"\nFound {len(fixtures)} .NET fixtures:")
    for fixture in fixtures:
        print(f"  - {fixture.name}")

    # Run tests
    results = []
    for fixture in fixtures:
        try:
            success = test_reverse_parser(fixture)
            results.append((fixture.name, success))
        except Exception as e:
            print(f"\nERROR testing {fixture.name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((fixture.name, False))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} passed ({passed/total*100:.0f}%)")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
