#!/usr/bin/env python3
"""Pinpoint the exact cause."""

import sys, os, time, signal
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from language.dotnet_parser_v2 import DotNetParserV2

def test(name, code):
    def timeout_handler(signum, frame):
        raise TimeoutError()
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    parser = DotNetParserV2()
    try:
        parser.parse_source(code, "test.cs")
        signal.alarm(0)
        print(f"✅ {name}")
        return True
    except TimeoutError:
        signal.alarm(0)
        print(f"❌ {name}: TIMEOUT")
        return False

# Simplify step by step
base = """
using System;
namespace Test {
    public static class Functions {
"""

end = """
    }
}
"""

# Test 1: Just signature
test("Default parameter", base + """
        public static void Animate(object frames = 99999) {
        }
""" + end)

# Test 2: Add while
test("With while loop", base + """
        public static void Animate(object frames = 99999) {
            while (true) { }
        }
""" + end)

# Test 3: Add try
test("With try-catch", base + """
        public static void Animate(object frames = 99999) {
            try {
                while (true) { }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 4: Add variable
test("With variable", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) { }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 5: Add function calls
test("With function calls", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) {
                    clear();
                }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 6: Add more calls
test("With multiple calls", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) {
                    clear();
                    print(galaxy(120, 40, t));
                }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 7: Add ALL calls
test("With all 4 calls", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) {
                    clear();
                    print(galaxy(120, 40, t));
                    print(null);
                    t = (t + 0.1d);
                }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 8: Add time.Sleep
test("With time.Sleep", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) {
                    clear();
                    print(galaxy(120, 40, t));
                    print(null);
                    t = (t + 0.1d);
                    time.Sleep(0.08d);
                }
            } catch (KeyboardInterrupt) { }
        }
""" + end)

# Test 9: Add catch body
test("With catch body", base + """
        public static void Animate(object frames = 99999) {
            int t = 0;
            try {
                while (true) {
                    clear();
                    print(galaxy(120, 40, t));
                    print(null);
                    t = (t + 0.1d);
                    time.Sleep(0.08d);
                }
            } catch (KeyboardInterrupt) {
                clear();
            }
        }
""" + end)

# Test 10: EXACT function (with problematic print)
test("EXACT Animate function", base + """
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
                print("🌀 Galaxy collapsed. Goodbye.
");
            }
        }
""" + end)
