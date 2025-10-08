#!/bin/bash
# Master test runner for Production Readiness Plan

echo "======================================================================"
echo "PRODUCTION READINESS TEST SUITE - MASTER RUNNER"
echo "======================================================================"

total_tests=0
total_passed=0

# Week 1: Critical Fixes
echo ""
echo "────────────────────────────────────────────────────────────────────"
echo "Week 1: Critical Fixes"
echo "────────────────────────────────────────────────────────────────────"

echo "Running: Type Validation (20 tests)..."
python3 tests/test_type_validation.py && week1_type=20 || week1_type=0
total_tests=$((total_tests + 20))
total_passed=$((total_passed + week1_type))

echo ""
echo "Running: Whitespace Handling (8 tests)..."
python3 tests/test_parser_whitespace.py && week1_white=8 || week1_white=0
total_tests=$((total_tests + 8))
total_passed=$((total_passed + week1_white))

echo ""
echo "Running: Multi-line Syntax (10 tests)..."
python3 tests/test_multiline_syntax.py && week1_multi=10 || week1_multi=0
total_tests=$((total_tests + 10))
total_passed=$((total_passed + week1_multi))

# Week 2: Control Flow
echo ""
echo "────────────────────────────────────────────────────────────────────"
echo "Week 2: Control Flow"
echo "────────────────────────────────────────────────────────────────────"

echo "Running: For Loops (7 tests)..."
python3 tests/test_for_loops.py && week2_for=7 || week2_for=0
total_tests=$((total_tests + 7))
total_passed=$((total_passed + week2_for))

echo ""
echo "Running: While Loops (6 tests)..."
python3 tests/test_while_loops.py && week2_while=6 || week2_while=0
total_tests=$((total_tests + 6))
total_passed=$((total_passed + week2_while))

# Week 3: Data Structures
echo ""
echo "────────────────────────────────────────────────────────────────────"
echo "Week 3: Data Structures"
echo "────────────────────────────────────────────────────────────────────"

echo "Running: Arrays (9 tests)..."
python3 tests/test_arrays.py && week3_arr=9 || week3_arr=0
total_tests=$((total_tests + 9))
total_passed=$((total_passed + week3_arr))

echo ""
echo "Running: Maps (9 tests)..."
python3 tests/test_maps.py && week3_map=9 || week3_map=0
total_tests=$((total_tests + 9))
total_passed=$((total_passed + week3_map))

# Week 4: Classes and Real Programs
echo ""
echo "────────────────────────────────────────────────────────────────────"
echo "Week 4: Classes and Real Programs"
echo "────────────────────────────────────────────────────────────────────"

echo "Running: Classes (8 tests)..."
python3 tests/test_classes.py && week4_class=8 || week4_class=0
total_tests=$((total_tests + 8))
total_passed=$((total_passed + week4_class))

echo ""
echo "Running: Real-World Programs (3 tests)..."
python3 tests/test_all_real_world.py && week4_real=3 || week4_real=0
total_tests=$((total_tests + 3))
total_passed=$((total_passed + week4_real))

# Summary
echo ""
echo "======================================================================"
echo "OVERALL SUMMARY"
echo "======================================================================"

week1_total=$((week1_type + week1_white + week1_multi))
week2_total=$((week2_for + week2_while))
week3_total=$((week3_arr + week3_map))
week4_total=$((week4_class + week4_real))

if [ $week1_type -eq 20 ]; then echo "✅ Week 1: Type Validation: 20/20 (100%)"; else echo "❌ Week 1: Type Validation: $week1_type/20"; fi
if [ $week1_white -eq 8 ]; then echo "✅ Week 1: Whitespace Handling: 8/8 (100%)"; else echo "❌ Week 1: Whitespace Handling: $week1_white/8"; fi
if [ $week1_multi -eq 10 ]; then echo "✅ Week 1: Multi-line Syntax: 10/10 (100%)"; else echo "❌ Week 1: Multi-line Syntax: $week1_multi/10"; fi
if [ $week2_for -eq 7 ]; then echo "✅ Week 2: For Loops: 7/7 (100%)"; else echo "❌ Week 2: For Loops: $week2_for/7"; fi
if [ $week2_while -eq 6 ]; then echo "✅ Week 2: While Loops: 6/6 (100%)"; else echo "❌ Week 2: While Loops: $week2_while/6"; fi
if [ $week3_arr -eq 9 ]; then echo "✅ Week 3: Arrays: 9/9 (100%)"; else echo "❌ Week 3: Arrays: $week3_arr/9"; fi
if [ $week3_map -eq 9 ]; then echo "✅ Week 3: Maps: 9/9 (100%)"; else echo "❌ Week 3: Maps: $week3_map/9"; fi
if [ $week4_class -eq 8 ]; then echo "✅ Week 4: Classes: 8/8 (100%)"; else echo "❌ Week 4: Classes: $week4_class/8"; fi
if [ $week4_real -eq 3 ]; then echo "✅ Week 4: Real Programs: 3/3 (100%)"; else echo "❌ Week 4: Real Programs: $week4_real/3"; fi

echo ""
echo "────────────────────────────────────────────────────────────────────"
percentage=$((100 * total_passed / total_tests))
echo "TOTAL: $total_passed/$total_tests tests passing ($percentage%)"
echo "────────────────────────────────────────────────────────────────────"

echo ""
echo "======================================================================"
echo "WEEK-BY-WEEK PROGRESS"
echo "======================================================================"
if [ $week1_total -eq 38 ]; then echo "✅ Week 1 (Critical Fixes): 38/38 (100%)"; else echo "🟡 Week 1 (Critical Fixes): $week1_total/38"; fi
if [ $week2_total -eq 13 ]; then echo "✅ Week 2 (Control Flow): 13/13 (100%)"; else echo "🟡 Week 2 (Control Flow): $week2_total/13"; fi
if [ $week3_total -eq 18 ]; then echo "✅ Week 3 (Data Structures): 18/18 (100%)"; else echo "🟡 Week 3 (Data Structures): $week3_total/18"; fi
if [ $week4_total -eq 11 ]; then echo "✅ Week 4 (Classes & Programs): 11/11 (100%)"; else echo "🟡 Week 4 (Classes & Programs): $week4_total/11"; fi

echo ""
echo "======================================================================"
if [ $total_passed -eq $total_tests ]; then
    echo "🎉 ALL TESTS PASSING - PRODUCTION READY!"
else
    failed=$((total_tests - total_passed))
    echo "⚠️  $failed tests still failing"
fi
echo "======================================================================"
echo ""

# Exit with success only if all pass
if [ $total_passed -eq $total_tests ]; then
    exit 0
else
    exit 1
fi
