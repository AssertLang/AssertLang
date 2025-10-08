#!/usr/bin/env python3
"""Debug C# parser timeout."""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.dotnet_parser_v2 import DotNetParserV2

# Simple C# code to start
simple_cs = """
using System;

public class Test {
    public void Hello() {
        Console.WriteLine("Hello");
    }
}
"""

print("=== Testing C# Parser ===\n")

# Test 1: Simple code
print("Test 1: Simple C# code")
parser = DotNetParserV2()
start = time.time()
try:
    ir = parser.parse_source(simple_cs, "test.cs")
    elapsed = time.time() - start
    print(f"✅ SUCCESS ({elapsed:.2f}s)")
    print(f"   Parsed: {len(ir.classes)} class(es)")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ FAILED ({elapsed:.2f}s): {e}")

# Test 2: Generated code (the one that times out)
print("\nTest 2: Generated C# code (from blind test)")
start = time.time()

# Add timeout using signal (Unix only)
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Parser timed out after 10 seconds")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

try:
    with open("test_code_from_python.cs") as f:
        cs_code = f.read()

    parser2 = DotNetParserV2()
    ir = parser2.parse_source(cs_code, "test_code_from_python.cs")
    signal.alarm(0)  # Cancel timeout
    elapsed = time.time() - start
    print(f"✅ SUCCESS ({elapsed:.2f}s)")
    print(f"   Parsed: {len(ir.classes)} class(es), {len(ir.functions)} function(s)")
except TimeoutError as e:
    signal.alarm(0)
    elapsed = time.time() - start
    print(f"❌ TIMEOUT ({elapsed:.2f}s): {e}")
    print("\n🔍 The parser is hanging. Need to add debug logging to find where.")
except Exception as e:
    signal.alarm(0)
    elapsed = time.time() - start
    print(f"❌ ERROR ({elapsed:.2f}s): {e}")
    import traceback
    traceback.print_exc()
