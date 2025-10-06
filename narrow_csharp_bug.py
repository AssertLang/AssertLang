#!/usr/bin/env python3
"""Narrow down the exact C# construct causing timeout."""

import sys
import os
import time
import signal
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.dotnet_parser_v2 import DotNetParserV2

def test(name, code):
    """Test parsing with 3s timeout."""
    def timeout_handler(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(3)

    parser = DotNetParserV2()
    start = time.time()
    try:
        ir = parser.parse_source(code, "test.cs")
        signal.alarm(0)
        elapsed = time.time() - start
        print(f"✅ {name}: {elapsed:.3f}s")
        return True
    except TimeoutError:
        signal.alarm(0)
        print(f"❌ {name}: TIMEOUT <<<--- BUG")
        return False

print("Narrowing down bug...")

# Test: Simple while loop
test1 = """
public class Test {
    public void Method() {
        while (true) {
            int x = 1;
        }
    }
}
"""
test("Simple while loop", test1)

# Test: Try-catch
test2 = """
public class Test {
    public void Method() {
        try {
            int x = 1;
        } catch (Exception e) {
            int y = 2;
        }
    }
}
"""
test("Simple try-catch", test2)

# Test: While + try-catch
test3 = """
public class Test {
    public void Method() {
        try {
            while (true) {
                int x = 1;
            }
        } catch (Exception e) {
            int y = 2;
        }
    }
}
"""
test("While inside try-catch", test3)

# Test: Exact problematic code from line 50-65
test4 = """
using System;

namespace Test {
    public static class Functions {
        public static void Animate(object frames = 99999)
        {
            int t = 0;
            try
            {
                while (true)
                {
                    clear();
                    print(galaxy(120, 40, t));
                    print(null);
                    t = (t + 0.1d);
                    time.Sleep(0.08d);
                }
            }
            catch (KeyboardInterrupt)
            {
                clear();
                print("Done");
            }
        }
    }
}
"""
test("Actual problematic Animate function", test4)

# Test: Simpler version with multiline string
test5 = """
public class Test {
    public void Method() {
        string s = "line1
line2";
    }
}
"""
test("Multiline string", test5)

# The actual problematic line might be the string on line 66
test6 = """
public class Test {
    public void Method() {
        print("🌀 Galaxy collapsed. Goodbye.
");
    }
}
"""
test("Exact problematic string from line 66", test6)

print("\nDone")
