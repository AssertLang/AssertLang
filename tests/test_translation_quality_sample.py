#!/usr/bin/env python3
"""
Translation Quality Assessment - Sampled Tests

Tests a sample of critical language combinations to assess quality quickly.
Focuses on representative patterns and high-priority combinations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the full test infrastructure
from test_translation_quality import (
    REAL_WORLD_PATTERNS,
    QualityAssessor,
    QualityMatrixTester
)


class SampledQualityTester(QualityMatrixTester):
    """Run quality tests on a representative sample."""

    def run_sampled_tests(self):
        """Test critical combinations only."""
        print("\n" + "="*80)
        print("SAMPLED TRANSLATION QUALITY ASSESSMENT")
        print("="*80)
        print("\nTesting 15 critical combinations (sample of 25 total)")
        print("Patterns: async_http, error_handling, collections, class_with_methods")
        print("Measuring: Compilation, Semantics, Idioms, Type Accuracy\n")

        # Critical combinations to test (15 total)
        test_combinations = [
            # Round-trip tests (same source/target)
            ("Python", "Python"),
            ("JavaScript", "JavaScript"),
            ("Go", "Go"),
            ("Rust", "Rust"),
            ("C#", "C#"),

            # Python to others
            ("Python", "JavaScript"),
            ("Python", "Go"),
            ("Python", "Rust"),

            # JavaScript to others
            ("JavaScript", "Python"),
            ("JavaScript", "Go"),

            # Go to others
            ("Go", "Python"),
            ("Go", "Rust"),

            # Rust to others
            ("Rust", "Python"),
            ("Rust", "Go"),

            # C# to others
            ("C#", "Python"),
        ]

        # Critical patterns to test (4 most important)
        critical_patterns = [
            "error_handling",
            "collections_operations",
            "class_with_methods",
            "control_flow",
        ]

        total_tests = 0
        excellent_count = 0
        good_count = 0
        fair_count = 0
        poor_count = 0
        error_count = 0

        for source_lang, target_lang in test_combinations:
            combo_key = f"{source_lang}→{target_lang}"
            print(f"\nTesting {combo_key}...")
            self.results[combo_key] = []

            for pattern_name in critical_patterns:
                print(f"  {pattern_name}...", end=" ", flush=True)

                result = self.test_pattern(pattern_name, source_lang, target_lang)
                self.results[combo_key].append((pattern_name, result))

                if result["success"]:
                    total_tests += 1
                    level = result["quality_level"]
                    score = result["quality_score"]

                    if level == "Excellent":
                        excellent_count += 1
                        print(f"✅ {score:.1f}% (Excellent)")
                    elif level == "Good":
                        good_count += 1
                        print(f"🟡 {score:.1f}% (Good)")
                    elif level == "Fair":
                        fair_count += 1
                        print(f"🟠 {score:.1f}% (Fair)")
                    else:
                        poor_count += 1
                        print(f"🔴 {score:.1f}% (Poor)")
                else:
                    error_count += 1
                    print(f"❌ ERROR: {result.get('error', 'Unknown')[:40]}")

        # Print summary
        print("\n" + "="*80)
        print("SAMPLED QUALITY SUMMARY")
        print("="*80)
        print(f"\nTotal translations tested: {total_tests}")
        print(f"Errors encountered: {error_count}")
        print(f"\nQuality Distribution:")
        print(f"  Excellent (90-100%): {excellent_count:3d} ({100*excellent_count//total_tests if total_tests > 0 else 0}%)")
        print(f"  Good      (70-89%):  {good_count:3d} ({100*good_count//total_tests if total_tests > 0 else 0}%)")
        print(f"  Fair      (50-69%):  {fair_count:3d} ({100*fair_count//total_tests if total_tests > 0 else 0}%)")
        print(f"  Poor      (<50%):    {poor_count:3d} ({100*poor_count//total_tests if total_tests > 0 else 0}%)")

        production_ready = excellent_count + good_count
        print(f"\nProduction-Ready: {production_ready}/{total_tests} ({100*production_ready//total_tests if total_tests > 0 else 0}%)")

        # Detailed gap analysis
        self.print_sampled_gap_analysis()

        # Recommendations
        self.print_recommendations(excellent_count, good_count, fair_count, poor_count, total_tests)

    def print_sampled_gap_analysis(self):
        """Print top issues found."""
        print("\n" + "="*80)
        print("TOP ISSUES FOUND")
        print("="*80)

        # Collect all issues
        all_issues = []

        for combo_key, pattern_results in self.results.items():
            for pattern_name, result in pattern_results:
                if result["success"] and "metrics" in result:
                    for metric_name, metric in result["metrics"].items():
                        if metric.issues:
                            for issue in metric.issues:
                                all_issues.append({
                                    "combo": combo_key,
                                    "pattern": pattern_name,
                                    "category": metric_name,
                                    "issue": issue,
                                })

        if not all_issues:
            print("\n✅ No quality issues found in sampled tests!")
            return

        # Group by issue text
        issue_counts = {}
        for item in all_issues:
            issue_text = item["issue"]
            if issue_text not in issue_counts:
                issue_counts[issue_text] = {
                    "count": 0,
                    "combos": set(),
                    "category": item["category"]
                }
            issue_counts[issue_text]["count"] += 1
            issue_counts[issue_text]["combos"].add(item["combo"])

        # Print top 10 issues
        print("\nTop Issues by Frequency:")
        print("-" * 80)

        for i, (issue_text, data) in enumerate(sorted(issue_counts.items(),
                                                       key=lambda x: -x[1]["count"])[:10], 1):
            print(f"\n{i}. {issue_text}")
            print(f"   Category: {data['category']}")
            print(f"   Occurrences: {data['count']}")
            print(f"   Affected combinations: {len(data['combos'])}")

            if len(data['combos']) <= 3:
                for combo in sorted(data['combos']):
                    print(f"     - {combo}")
            else:
                for combo in sorted(list(data['combos']))[:2]:
                    print(f"     - {combo}")
                print(f"     ... and {len(data['combos'])-2} more")

    def print_recommendations(self, excellent, good, fair, poor, total):
        """Print actionable recommendations."""
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)

        production_ready_pct = (excellent + good) / total * 100 if total > 0 else 0

        if production_ready_pct >= 80:
            print("\n✅ EXCELLENT - System is production-ready!")
            print("\nNext steps:")
            print("  1. Expand test coverage to all 25 combinations")
            print("  2. Test on real-world GitHub repositories")
            print("  3. Performance optimization")
            print("  4. Documentation and examples")

        elif production_ready_pct >= 60:
            print("\n🟡 GOOD - System is mostly functional with some gaps")
            print("\nPriority fixes:")
            print("  1. Address top 3-5 most frequent issues")
            print("  2. Focus on 'Poor' rated combinations first")
            print("  3. Improve type inference accuracy")
            print("  4. Re-test after fixes")

        elif production_ready_pct >= 40:
            print("\n🟠 FAIR - System needs significant improvements")
            print("\nCritical fixes needed:")
            print("  1. Fix compilation issues (syntax errors)")
            print("  2. Improve semantic preservation (lost functions/classes)")
            print("  3. Add missing language features")
            print("  4. Comprehensive re-testing required")

        else:
            print("\n🔴 POOR - System not ready for production")
            print("\nMajor work required:")
            print("  1. Review and fix parsers (semantic extraction)")
            print("  2. Review and fix generators (code emission)")
            print("  3. Add comprehensive error handling")
            print("  4. Full system redesign may be needed")

        # Specific recommendations based on issues
        print("\n" + "="*80)
        print("SPECIFIC IMPROVEMENT PRIORITIES")
        print("="*80)

        print("\n1. Type System Improvements:")
        print("   - Implement better type inference from context")
        print("   - Reduce 'any'/'object'/'interface{}' fallbacks")
        print("   - Add type propagation through function calls")

        print("\n2. Code Generation Quality:")
        print("   - Ensure idiomatic naming conventions per language")
        print("   - Fix indentation/formatting issues")
        print("   - Add language-specific optimizations")

        print("\n3. Semantic Preservation:")
        print("   - Verify all functions/classes are translated")
        print("   - Preserve function call chains")
        print("   - Maintain control flow structure")

        print("\n4. Compilation Validity:")
        print("   - Add syntax validation before generation")
        print("   - Fix brace/parenthesis balancing")
        print("   - Test generated code with actual compilers")


def main():
    """Run sampled quality assessment."""
    tester = SampledQualityTester()
    tester.run_sampled_tests()

    return 0


if __name__ == "__main__":
    exit(main())
