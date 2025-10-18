#!/usr/bin/env python3
"""
Real-world translation demo: Test on actual code samples
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2

from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_1_simple_function():
    """Demo 1: Simple function translation"""
    print_section("DEMO 1: Simple Function (Python → All Languages)")

    python_code = '''
def calculate_total(items, tax_rate):
    """Calculate total price with tax."""
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax
'''

    print("📝 Original Python Code:")
    print(python_code)

    # Parse Python → IR
    parser = PythonParserV2()
    ir_module = parser.parse_source(python_code, "demo")

    print(f"✅ Parsed to IR: {len(ir_module.functions)} function(s)\n")

    # Generate all languages
    languages = [
        ("JavaScript", generate_nodejs(ir_module, typescript=False)),
        ("TypeScript", generate_nodejs(ir_module, typescript=True)),
        ("Go", generate_go(ir_module)),
        ("Rust", generate_rust(ir_module)),
        ("C#", generate_csharp(ir_module)),
    ]

    for lang_name, code in languages:
        print(f"🔄 Translated to {lang_name}:")
        print("-" * 70)
        print(code)
        print()


def demo_2_class_with_methods():
    """Demo 2: Class with methods"""
    print_section("DEMO 2: Class with Methods (Python → Go, Rust)")

    python_code = '''
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.active = True

    def deactivate(self):
        self.active = False

    def send_email(self, message):
        if self.active:
            return f"Sending to {self.email}: {message}"
        return "User is inactive"
'''

    print("📝 Original Python Code:")
    print(python_code)

    parser = PythonParserV2()
    ir_module = parser.parse_source(python_code, "demo")

    print(f"✅ Parsed to IR: {len(ir_module.classes)} class(es)\n")

    # Translate to Go
    go_code = generate_go(ir_module)
    print("🔄 Translated to Go:")
    print("-" * 70)
    print(go_code)
    print()

    # Translate to Rust
    rust_code = generate_rust(ir_module)
    print("🔄 Translated to Rust:")
    print("-" * 70)
    print(rust_code)
    print()


def demo_3_javascript_to_python():
    """Demo 3: JavaScript → Python"""
    print_section("DEMO 3: JavaScript → Python (Real API Handler)")

    js_code = '''
async function getUserById(userId) {
    const user = await database.findUser(userId);

    if (!user) {
        throw new Error("User not found");
    }

    return {
        id: user.id,
        name: user.name,
        email: user.email
    };
}

async function createUser(userData) {
    const newUser = await database.insertUser(userData);
    await sendWelcomeEmail(newUser.email);
    return newUser;
}
'''

    print("📝 Original JavaScript Code:")
    print(js_code)

    # Parse JS → IR
    parser = NodeJSParserV2()
    ir_module = parser.parse_source(js_code, "demo")

    print(f"✅ Parsed to IR: {len(ir_module.functions)} function(s)\n")

    # Translate to Python
    python_code = generate_python(ir_module)
    print("🔄 Translated to Python:")
    print("-" * 70)
    print(python_code)
    print()

    # Translate to Go
    go_code = generate_go(ir_module)
    print("🔄 Translated to Go:")
    print("-" * 70)
    print(go_code)
    print()


def demo_4_go_to_rust():
    """Demo 4: Go → Rust"""
    print_section("DEMO 4: Go → Rust (Idiomatic Translation)")

    go_code = '''
package main

type Point struct {
    X int
    Y int
}

func NewPoint(x, y int) Point {
    return Point{X: x, Y: y}
}

func (p Point) Distance(other Point) float64 {
    dx := p.X - other.X
    dy := p.Y - other.Y
    return math.Sqrt(float64(dx*dx + dy*dy))
}
'''

    print("📝 Original Go Code:")
    print(go_code)

    # Parse Go → IR
    parser = GoParserV2()
    ir_module = parser.parse_source(go_code, "main")

    print(f"✅ Parsed to IR: {len(ir_module.types)} type(s), {len(ir_module.functions)} function(s)\n")

    # Translate to Rust
    rust_code = generate_rust(ir_module)
    print("🔄 Translated to Rust:")
    print("-" * 70)
    print(rust_code)
    print()


def demo_5_round_trip():
    """Demo 5: Round-trip preservation"""
    print_section("DEMO 5: Round-Trip Test (Python → IR → Python)")

    original_python = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def factorial(n):
    if n <= 1:
        return 1
    result = 1
    i = 2
    while i <= n:
        result = result * i
        i = i + 1
    return result
'''

    print("📝 Original Python Code:")
    print(original_python)

    # Parse
    parser = PythonParserV2()
    ir_module = parser.parse_source(original_python, "demo")

    # Generate back to Python
    regenerated_python = generate_python(ir_module)

    print("🔄 Regenerated Python Code:")
    print("-" * 70)
    print(regenerated_python)
    print()

    # Compare structure
    ir_module_2 = parser.parse_source(regenerated_python, "demo")

    print("📊 Comparison:")
    print(f"  Original functions: {len(ir_module.functions)}")
    print(f"  Regenerated functions: {len(ir_module_2.functions)}")
    print(f"  Function names match: {[f.name for f in ir_module.functions] == [f.name for f in ir_module_2.functions]}")
    print()


def demo_6_all_combinations():
    """Demo 6: Translation matrix"""
    print_section("DEMO 6: Translation Matrix (1 Function → 5 Languages)")

    python_code = '''
def greet(name):
    return f"Hello, {name}!"
'''

    print("📝 Source (Python):")
    print(python_code)

    parser = PythonParserV2()
    ir_module = parser.parse_source(python_code, "demo")

    # Generate all 5 languages
    translations = {
        "Python": generate_python(ir_module),
        "JavaScript": generate_nodejs(ir_module, typescript=False),
        "TypeScript": generate_nodejs(ir_module, typescript=True),
        "Go": generate_go(ir_module),
        "Rust": generate_rust(ir_module),
        "C#": generate_csharp(ir_module),
    }

    for lang, code in translations.items():
        print(f"\n🔄 {lang}:")
        print("-" * 70)
        # Show just the function, not imports
        lines = code.split('\n')
        func_lines = [l for l in lines if l and not l.startswith('import') and not l.startswith('using') and not l.startswith('package') and not l.startswith('from')]
        print('\n'.join(func_lines))


def main():
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║         ASSERTLANG V2 - REAL-WORLD TRANSLATION DEMO              ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    demos = [
        ("Simple Function Translation", demo_1_simple_function),
        ("Class Translation", demo_2_class_with_methods),
        ("JavaScript → Python", demo_3_javascript_to_python),
        ("Go → Rust", demo_4_go_to_rust),
        ("Round-Trip Preservation", demo_5_round_trip),
        ("Translation Matrix", demo_6_all_combinations),
    ]

    print("\nAvailable demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos) + 1}. Run all demos")

    try:
        choice = input("\nSelect demo (1-7): ").strip()

        if choice == str(len(demos) + 1):
            # Run all
            for name, demo_func in demos:
                demo_func()
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                demos[idx][1]()
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("\n\nDemo cancelled.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
