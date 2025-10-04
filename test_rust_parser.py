#!/usr/bin/env python3
"""
Test the Rust reverse parser on generated Rust code.
"""

from reverse_parsers.rust_parser import RustReverseParser

def test_parser(rust_file: str, expected_pw_file: str):
    """Test parsing a Rust file and compare with expected PW."""
    parser = RustReverseParser()

    print(f"\n{'='*80}")
    print(f"Testing: {rust_file}")
    print(f"{'='*80}")

    # Parse the Rust file
    agent = parser.parse_file(rust_file)

    # Convert to PW DSL
    pw_output = parser.to_pw_dsl(agent, include_metadata=True)

    print("\nExtracted Agent:")
    print(f"  Name: {agent.name}")
    print(f"  Port: {agent.port}")
    print(f"  Framework: {agent.framework}")
    print(f"  Tools: {agent.tools}")
    print(f"  Verbs: {[v['name'] for v in agent.verbs]}")
    print(f"  Confidence: {agent.confidence_score:.0%}")
    if agent.extraction_notes:
        print(f"  Notes: {agent.extraction_notes}")

    print("\nGenerated PW DSL:")
    print("-" * 80)
    print(pw_output)
    print("-" * 80)

    # Read expected PW file
    with open(expected_pw_file, 'r') as f:
        expected_pw = f.read().strip()

    print("\nExpected PW DSL:")
    print("-" * 80)
    print(expected_pw)
    print("-" * 80)

    # Compare verbs
    print("\nDetailed Verb Comparison:")
    for i, verb in enumerate(agent.verbs, 1):
        print(f"\n  Verb {i}: {verb['name']}")
        params_str = [f"{p['name']} ({p['type']})" for p in verb['params']]
        returns_str = [f"{r['name']} ({r['type']})" for r in verb['returns']]
        print(f"    Params: {params_str}")
        print(f"    Returns: {returns_str}")

    return agent, pw_output, expected_pw


if __name__ == '__main__':
    # Test minimal Rust agent
    print("\n" + "="*80)
    print("TEST 1: Minimal Rust Agent")
    print("="*80)
    agent1, pw1, expected1 = test_parser(
        '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/bidirectional/generated/rust/minimal_rust_agent/src/main.rs',
        '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/bidirectional/fixtures/rust_minimal.pw'
    )

    # Test tool Rust agent
    print("\n\n" + "="*80)
    print("TEST 2: Tool Rust Agent")
    print("="*80)
    agent2, pw2, expected2 = test_parser(
        '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/bidirectional/generated/rust/tool_rust_agent/src/main.rs',
        '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tests/bidirectional/fixtures/rust_with_tools.pw'
    )

    # Summary
    print("\n\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nTest 1 (Minimal):")
    print(f"  Verbs extracted: {len(agent1.verbs)}")
    print(f"  Confidence: {agent1.confidence_score:.0%}")

    print(f"\nTest 2 (With Tools):")
    print(f"  Verbs extracted: {len(agent2.verbs)}")
    print(f"  Tools extracted: {agent2.tools}")
    print(f"  Confidence: {agent2.confidence_score:.0%}")

    print("\n" + "="*80)
    print("Tests complete!")
    print("="*80)
