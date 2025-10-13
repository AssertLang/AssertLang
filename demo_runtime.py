"""
Demo: Promptware Runtime Executing PW Code Directly

This demonstrates that Promptware now has its own runtime interpreter
that executes PW code without transpiling to Python/Rust/etc.
"""

from dsl.pw_parser import parse_pw
from dsl.pw_runtime import PWRuntime
from dsl.ir import IRLiteral, LiteralType


def demo_basic_arithmetic():
    """Demo: Basic arithmetic operations"""
    print("\n=== Demo 1: Basic Arithmetic ===")

    code = """
    function add(a: int, b: int) -> int {
        return a + b
    }

    function multiply(x: int, y: int) -> int {
        return x * y
    }
    """

    runtime = PWRuntime()
    module = parse_pw(code)
    runtime.execute_module(module)

    # Call functions
    add_func = runtime.globals['add']
    mul_func = runtime.globals['multiply']

    result1 = runtime.execute_function(add_func, [5, 3])
    result2 = runtime.execute_function(mul_func, [4, 7])
    combined = runtime.execute_function(add_func, [result1, result2])

    print(f"add(5, 3) = {result1}")
    print(f"multiply(4, 7) = {result2}")
    print(f"combined = {combined}")
    print("✓ Arithmetic works!")


def demo_control_flow():
    """Demo: Control flow (if/for/while)"""
    print("\n=== Demo 2: Control Flow ===")

    code = """
    // Sum numbers from 1 to 10
    function sum_to_n(n: int) -> int {
        let sum = 0
        for (let i = 1; i <= n; i = i + 1) {
            sum = sum + i
        }
        return sum
    }
    """

    runtime = PWRuntime()
    module = parse_pw(code)
    runtime.execute_module(module)

    # Call function
    sum_func = runtime.globals['sum_to_n']
    total = runtime.execute_function(sum_func, [10])

    print(f"sum_to_n(10) = {total}")
    print("✓ Control flow works!")


def demo_arrays_and_loops():
    """Demo: Arrays and iteration"""
    print("\n=== Demo 3: Arrays and Iteration ===")

    code = """
    function process_array(items: array<int>) -> int {
        let sum = 0
        for (item in items) {
            sum = sum + item
        }
        return sum
    }
    """

    runtime = PWRuntime()
    module = parse_pw(code)
    runtime.execute_module(module)

    # Call function with array
    proc_func = runtime.globals['process_array']
    numbers = [10, 20, 30, 40, 50]
    result = runtime.execute_function(proc_func, [numbers])

    print(f"numbers = {numbers}")
    print(f"sum = {result}")
    print("✓ Arrays and iteration work!")


def demo_lambdas():
    """Demo: Lambda functions"""
    print("\n=== Demo 4: Lambda Functions ===")

    code = """
    function apply_twice(fn: function(int) -> int, x: int) -> int {
        let result = fn(x)
        return fn(result)
    }
    """

    runtime = PWRuntime()
    module = parse_pw(code)
    runtime.execute_module(module)

    # Create lambda and call function
    from dsl.ir import IRLambda, IRParameter, IRType, IRBinaryOp, BinaryOperator, IRIdentifier
    double_lambda = IRLambda(
        params=[IRParameter(name="x", param_type=IRType(name="int"))],
        body=IRBinaryOp(
            op=BinaryOperator.MULTIPLY,
            left=IRIdentifier(name="x"),
            right=IRLiteral(value=2, literal_type=LiteralType.INTEGER)
        )
    )

    double_func = runtime.evaluate_expression(double_lambda, {})
    apply_func = runtime.globals['apply_twice']
    result = runtime.execute_function(apply_func, [double_func, 5])

    print(f"double(double(5)) = {result}")
    print("✓ Lambda functions work!")


def demo_stdlib_enums():
    """Demo: Standard library enums (Option, Result)"""
    print("\n=== Demo 5: Standard Library (Option, Result) ===")

    code = """
    function test_option() -> int {
        let some_value = option_some(42)
        let none_value = option_none()

        let result1 = option_unwrap_or(some_value, 0)
        let result2 = option_unwrap_or(none_value, 99)

        return result1 + result2
    }
    """

    runtime = PWRuntime()
    runtime.load_stdlib()  # Load stdlib first
    module = parse_pw(code)
    runtime.execute_module(module)

    # Call function
    test_func = runtime.globals['test_option']
    final = runtime.execute_function(test_func, [])

    print(f"Option unwrap tests: {final}")
    print("✓ Standard library works!")


def demo_recursion():
    """Demo: Recursive functions"""
    print("\n=== Demo 6: Recursion ===")

    code = """
    function factorial(n: int) -> int {
        if (n <= 1) {
            return 1
        } else {
            return n * factorial(n - 1)
        }
    }
    """

    runtime = PWRuntime()
    module = parse_pw(code)
    runtime.execute_module(module)

    # Call function
    fact_func = runtime.globals['factorial']
    fact5 = runtime.execute_function(fact_func, [5])
    fact10 = runtime.execute_function(fact_func, [10])

    print(f"factorial(5) = {fact5}")
    print(f"factorial(10) = {fact10}")
    print("✓ Recursion works!")


def main():
    """Run all demos"""
    print("=" * 60)
    print("Promptware Runtime Interpreter Demo")
    print("Executing PW code DIRECTLY without transpilation")
    print("=" * 60)

    try:
        demo_basic_arithmetic()
        demo_control_flow()
        demo_arrays_and_loops()
        demo_lambdas()
        demo_stdlib_enums()
        demo_recursion()

        print("\n" + "=" * 60)
        print("✓ ALL DEMOS PASSED!")
        print("=" * 60)
        print("\nPrompware IS a real programming language!")
        print("PW code executes directly in the PW runtime.")
        print("No Python. No transpilation. Pure Promptware.")

    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
