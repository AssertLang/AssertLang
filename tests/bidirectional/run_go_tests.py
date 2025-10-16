#!/usr/bin/env python3
"""
Bidirectional Go Testing Runner

Generates Go servers from .al fixtures and runs comprehensive tests.
"""

import json
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.go_expert import GoExpertAgent, GoTestReport
from language.agent_parser import parse_agent_pw
from language.mcp_server_generator_go import generate_go_mcp_server


def main():
    """Run Go bidirectional tests."""
    print("=" * 80)
    print("Go Expert Agent - Bidirectional Testing System")
    print("=" * 80)
    print()

    # Initialize Go expert agent
    go_expert = GoExpertAgent()

    # Find all Go fixtures
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures = list(fixtures_dir.glob("go_*.al"))

    if not fixtures:
        print("ERROR: No Go fixtures found in", fixtures_dir)
        return 1

    print(f"Found {len(fixtures)} Go fixtures:")
    for fixture in fixtures:
        print(f"  - {fixture.name}")
    print()

    # Run tests for each fixture
    reports = []

    for i, fixture in enumerate(fixtures, 1):
        print(f"[{i}/{len(fixtures)}] Testing {fixture.name}")
        print("-" * 80)

        try:
            # Parse .al file
            print(f"  1. Parsing {fixture.name}...")
            pw_code = fixture.read_text()
            agent = parse_agent_pw(pw_code)
            print(f"     Agent: {agent.name}, Port: {agent.port}")

            # Generate Go code
            print(f"  2. Generating Go code...")
            with tempfile.TemporaryDirectory() as temp_dir:
                output_dir = Path(temp_dir) / "generated"
                output_dir.mkdir(parents=True)

                # Generate Go code (returns string)
                go_code = generate_go_mcp_server(agent)

                # Write to main.go file
                main_go_path = output_dir / "main.go"
                main_go_path.write_text(go_code)
                print(f"     Generated to: {main_go_path}")

                # Check if code was generated
                if not main_go_path.exists() or len(go_code) == 0:
                    print(f"     ERROR: No Go code generated!")
                    reports.append(
                        GoTestReport(
                            agent_name=agent.name,
                            fixture_path=str(fixture),
                            errors=["No Go code generated"],
                        )
                    )
                    print()
                    continue

                print(f"     Generated {len(go_code)} bytes of Go code")

                # Run full test suite
                print(f"  3. Running full test suite...")
                report = go_expert.run_full_test(fixture, output_dir, port=agent.port)
                reports.append(report)

                # Print test results
                print(f"\n  Test Results:")
                print(f"    Syntax Valid:    {report.syntax_valid}")

                if report.compilation:
                    print(
                        f"    Compilation:     {'PASS' if report.compilation.success else 'FAIL'}"
                    )
                    print(f"    Build Time:      {report.compilation.build_time_ms:.0f}ms")
                    if report.compilation.binary_size_bytes:
                        size_mb = report.compilation.binary_size_bytes / (1024 * 1024)
                        print(f"    Binary Size:     {size_mb:.2f} MB")
                    if report.compilation.errors:
                        print(f"    Errors:          {len(report.compilation.errors)}")
                        for error in report.compilation.errors[:3]:
                            print(f"      - {error}")

                if report.server:
                    print(f"    Server Started:  {'YES' if report.server.started else 'NO'}")
                    print(
                        f"    Health Check:    {'PASS' if report.server.health_check_passed else 'FAIL'}"
                    )
                    if report.server.health_response_time_ms:
                        print(f"    Health Time:     {report.server.health_response_time_ms:.0f}ms")

                if report.race_detection:
                    races = "DETECTED" if report.race_detection.races_detected else "NONE"
                    print(f"    Race Conditions: {races}")
                    if report.race_detection.race_count > 0:
                        print(f"    Race Count:      {report.race_detection.race_count}")

                print(f"    Quality Score:   {report.code_quality_score:.1f}/100")

                if report.errors:
                    print(f"\n  Errors:")
                    for error in report.errors:
                        print(f"    - {error}")

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback

            traceback.print_exc()
            reports.append(
                GoTestReport(
                    agent_name=fixture.stem, fixture_path=str(fixture), errors=[str(e)]
                )
            )

        print()

    # Generate final report
    print("=" * 80)
    print("Final Report")
    print("=" * 80)

    json_report = go_expert.to_json_report(reports)

    # Print summary
    print(f"\nGo Version: {json_report['go_version']}")
    print(f"Total Tests: {json_report['total_tests']}")
    print(f"Passed: {json_report['passed']}")
    print(f"Failed: {json_report['failed']}")
    print()

    # Quality scores
    scores = [r.code_quality_score for r in reports if r.code_quality_score > 0]
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"Average Quality Score: {avg_score:.1f}/100")
        print()

    # Save report
    report_path = Path(__file__).parent / "reports" / "go_test_report.json"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(json_report, f, indent=2)

    print(f"Full report saved to: {report_path}")
    print()

    # Cleanup
    go_expert.cleanup()

    # Return exit code
    return 0 if json_report["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
