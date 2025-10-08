#!/usr/bin/env python3
"""Isolate which part of the C# code causes timeout."""

import sys
import os
import time
import signal
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.dotnet_parser_v2 import DotNetParserV2

def test_parse(name, code, timeout_sec=5):
    """Test parsing with timeout."""
    print(f"\n{name}:")
    print(f"  Code length: {len(code)} chars")

    def timeout_handler(signum, frame):
        raise TimeoutError(f"Timeout after {timeout_sec}s")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_sec)

    parser = DotNetParserV2()
    start = time.time()
    try:
        ir = parser.parse_source(code, "test.cs")
        signal.alarm(0)
        elapsed = time.time() - start
        print(f"  ✅ SUCCESS ({elapsed:.3f}s) - {len(ir.classes)} class(es), {len(ir.functions)} function(s)")
        return True
    except TimeoutError:
        signal.alarm(0)
        elapsed = time.time() - start
        print(f"  ❌ TIMEOUT ({elapsed:.1f}s) <<<--- BUG HERE")
        return False
    except Exception as e:
        signal.alarm(0)
        elapsed = time.time() - start
        print(f"  ❌ ERROR ({elapsed:.3f}s): {str(e)[:100]}")
        return False

print("=" * 70)
print("ISOLATING C# PARSER TIMEOUT BUG")
print("=" * 70)

# Test 1: Empty variable names (from blind test issue)
test1 = """
public class Test {
    public void Method() {
        object  = <unknown>;
    }
}
"""
test_parse("Test 1: Empty variable name", test1)

# Test 2: Malformed expression
test2 = """
public class Test {
    public void Method() {
        object cx = <unknown>;
        object cy = <unknown>;
    }
}
"""
test_parse("Test 2: Unknown expression", test2)

# Test 3: Complex nesting
test3 = """
public class Test {
    public void Method() {
        foreach (var x in range(10)) {
            foreach (var y in range(10)) {
                object val = x;
            }
        }
    }
}
"""
test_parse("Test 3: Nested foreach", test3)

# Test 4: Multiple classes
test4 = """
public class Test1 {
    public void Method1() {
        int x = 1;
    }
}

public class Test2 {
    public void Method2() {
        int y = 2;
    }
}
"""
test_parse("Test 4: Multiple classes", test4)

# Test 5: The actual problematic code (first 20 lines)
with open("test_code_from_python.cs") as f:
    full_code = f.read()

# Try just first function
test5 = """
using System;

namespace testcodeoriginal
{
    public static class Functions
    {
        public static void Clear()
        {
            os.System(((os.Name == "nt") ? "cls" : "clear"));
        }
    }
}
"""
test_parse("Test 5: Just Clear() function", test5)

# Try with Galaxy function
test6 = full_code[:500]
result6 = test_parse("Test 6: First 500 chars of full code", test6)

if result6:
    # Progressively try more
    for length in [750, 1000, 1500, 2000]:
        if not test_parse(f"Test: First {length} chars", full_code[:length]):
            print(f"\n🔍 BUG ISOLATED: Timeout occurs between {length-250} and {length} characters")
            print("\nProblematic section:")
            print(full_code[length-250:length])
            break

print("\n" + "=" * 70)
