#!/usr/bin/env python3
"""
Go Return Value Fix - Before/After Demonstration

Shows the exact fix applied to resolve the "extra nil" bug.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.go_parser_v2 import GoParserV2
from language.go_generator_v2 import generate_go


def main():
    print("\n" + "="*70)
    print("GO RETURN VALUE FIX - BEFORE/AFTER DEMONSTRATION")
    print("="*70)

    test_code = '''
package main

type User struct {
    Name string
    Age  int
}

func GetUser(id int) (User, error) {
    user := User{Name: "Alice", Age: 30}
    return user, nil
}
'''

    print("\n📝 ORIGINAL GO CODE:")
    print(test_code)

    # Parse
    parser = GoParserV2()
    ir = parser.parse_source(test_code, "main")

    # Generate
    generated = generate_go(ir)

    print("\n" + "="*70)
    print("🔄 GENERATED GO CODE:")
    print("="*70)
    print(generated)

    # Extract return statement
    return_line = [line for line in generated.split('\n') if 'return user' in line]

    print("\n" + "="*70)
    print("🔍 ANALYSIS:")
    print("="*70)

    print("\n📌 ORIGINAL RETURN STATEMENT:")
    print("   return user, nil")

    print("\n📌 GENERATED RETURN STATEMENT:")
    if return_line:
        print(f"   {return_line[0].strip()}")

    print("\n" + "="*70)
    print("✅ VERIFICATION:")
    print("="*70)

    if 'return user, nil, nil' in generated:
        print("❌ BUG PRESENT: Extra nil added")
        print("   Expected: return user, nil")
        print("   Found:    return user, nil, nil")
        return 1
    elif 'return user, nil' in generated:
        print("✅ BUG FIXED: Correct return value count")
        print("   Expected: return user, nil (2 values)")
        print("   Found:    return user, nil (2 values)")
        print("\n📊 Function signature: (User, error)")
        print("📊 Return values:      2 (matches signature)")
        return 0
    else:
        print("⚠️  UNEXPECTED: Return statement format changed")
        return 2

    print("\n" + "="*70)
    print("ROOT CAUSE:")
    print("="*70)
    print("""
The bug was in two places:

1. **Parser** (go_parser_v2.py, _parse_return_statement):
   - Input: "return user, nil"
   - Problem: Treated "user, nil" as single expression
   - Fix: Detect comma-separated values and create IRArray

2. **Generator** (go_generator_v2.py, _generate_return):
   - Input: IRReturn with value containing "user, nil"
   - Problem: Blindly appended ", nil" → "user, nil, nil"
   - Fix: Check if value is IRArray or already contains error handling

SOLUTION:
- Parser now creates IRArray([user, nil]) for multiple returns
- Generator checks for IRArray and generates comma-separated list
- Generator also checks if string already contains ", nil" or ", err"
""")


if __name__ == "__main__":
    exit(main())
