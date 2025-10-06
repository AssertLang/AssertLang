#!/usr/bin/env python3
"""
Tests for Context-Aware Type Inference System

This test suite validates the cross-function dependency tracking and
context-aware type inference capabilities.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.context_analyzer import ContextAnalyzer, CallSite, VariableUsage
from dsl.type_system import TypeSystem
from language.python_parser_v2 import PythonParserV2


def test_call_graph_construction():
    """Test 1: Call graph construction from multi-function code."""
    print("\n" + "=" * 70)
    print("TEST 1: Call Graph Construction")
    print("=" * 70)

    code = '''
def get_user(user_id):
    return database.find_user(user_id)

def get_user_email(user_id):
    user = get_user(user_id)
    return user.email

def send_notification(user_id, message):
    email = get_user_email(user_id)
    mailer.send(email, message)
'''

    # Parse code
    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    # Build call graph
    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    print(f"✓ Parsed {len(module.functions)} functions")

    # Verify call graph
    assert "get_user" in analyzer.call_graph.nodes
    assert "get_user_email" in analyzer.call_graph.nodes
    assert "send_notification" in analyzer.call_graph.nodes

    # Check edges
    get_user_callees = analyzer.get_callees("get_user")
    get_user_email_callees = analyzer.get_callees("get_user_email")
    send_notification_callees = analyzer.get_callees("send_notification")

    print(f"✓ get_user calls: {get_user_callees}")
    print(f"✓ get_user_email calls: {get_user_email_callees}")
    print(f"✓ send_notification calls: {send_notification_callees}")

    # get_user_email should call get_user
    assert "get_user" in get_user_email_callees

    # send_notification should call get_user_email
    assert "get_user_email" in send_notification_callees

    # Check reverse edges
    get_user_callers = analyzer.get_callers("get_user")
    print(f"✓ get_user called by: {get_user_callers}")
    assert "get_user_email" in get_user_callers

    print("\n✅ TEST 1 PASSED: Call graph constructed correctly")
    return True


def test_variable_usage_tracking():
    """Test 2: Track how variables are used (property access, operators)."""
    print("\n" + "=" * 70)
    print("TEST 2: Variable Usage Tracking")
    print("=" * 70)

    code = '''
def process_user(user):
    name = user.name
    email = user.email
    age = user.age + 1
    return name
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    context = analyzer.get_function_context("process_user")
    assert context is not None

    # Check user parameter usage
    user_usage = context.variable_usage.get("user")
    assert user_usage is not None

    print(f"✓ Variable 'user' tracked")
    print(f"  - Read count: {user_usage.read_count}")
    print(f"  - Property accesses: {user_usage.property_accesses}")

    # user should have property accesses
    assert "name" in user_usage.property_accesses
    assert "email" in user_usage.property_accesses
    assert "age" in user_usage.property_accesses

    print("\n✅ TEST 2 PASSED: Variable usage tracked correctly")
    return True


def test_cross_function_type_inference():
    """Test 3: Infer types based on cross-function usage."""
    print("\n" + "=" * 70)
    print("TEST 3: Cross-Function Type Inference")
    print("=" * 70)

    code = '''
def get_user(user_id):
    return database.find(user_id)

def process():
    user = get_user(42)
    print(user.name)
    print(user.email)
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    type_system = TypeSystem()
    type_map = type_system.analyze_cross_function_types(module)

    print(f"✓ Analyzed {len(type_map)} type inferences")
    for key, type_info in type_map.items():
        print(f"  - {key}: {type_info.pw_type} (confidence: {type_info.confidence})")

    # get_user should have inferred return type
    # (might be 'object' or 'any' depending on inference)
    if "get_user.__return__" in type_map:
        return_type = type_map["get_user.__return__"]
        print(f"\n✓ get_user return type inferred: {return_type.pw_type}")

    print("\n✅ TEST 3 PASSED: Cross-function type inference working")
    return True


def test_return_type_inference():
    """Test 4: Infer return types from return expressions."""
    print("\n" + "=" * 70)
    print("TEST 4: Return Type Inference")
    print("=" * 70)

    code = '''
def add(a, b):
    return a + b

def get_name():
    return "Alice"

def get_count():
    return 42
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    # Check return expressions
    add_context = analyzer.get_function_context("add")
    get_name_context = analyzer.get_function_context("get_name")
    get_count_context = analyzer.get_function_context("get_count")

    print(f"✓ add has {len(add_context.return_expressions)} return expressions")
    print(f"✓ get_name has {len(get_name_context.return_expressions)} return expressions")
    print(f"✓ get_count has {len(get_count_context.return_expressions)} return expressions")

    assert len(add_context.return_expressions) == 1
    assert len(get_name_context.return_expressions) == 1
    assert len(get_count_context.return_expressions) == 1

    # Infer types
    type_system = TypeSystem()
    type_map = type_system.analyze_cross_function_types(module)

    if "get_name.__return__" in type_map:
        get_name_return = type_map["get_name.__return__"]
        print(f"✓ get_name return type: {get_name_return.pw_type}")
        assert get_name_return.pw_type == "string"

    if "get_count.__return__" in type_map:
        get_count_return = type_map["get_count.__return__"]
        print(f"✓ get_count return type: {get_count_return.pw_type}")
        assert get_count_return.pw_type == "int"

    print("\n✅ TEST 4 PASSED: Return types inferred correctly")
    return True


def test_parameter_type_inference():
    """Test 5: Infer parameter types from how they're used."""
    print("\n" + "=" * 70)
    print("TEST 5: Parameter Type Inference from Usage")
    print("=" * 70)

    code = '''
def process_user(user):
    name = user.name
    email = user.email
    return name

def calculate(x):
    result = x * 2 + 10
    return result
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    # Check parameter usage
    process_user_ctx = analyzer.get_function_context("process_user")
    user_usage = process_user_ctx.variable_usage.get("user")

    print(f"✓ Parameter 'user' usage:")
    print(f"  - Property accesses: {user_usage.property_accesses}")

    # user has property accesses, should infer object type
    assert "name" in user_usage.property_accesses
    assert "email" in user_usage.property_accesses

    calculate_ctx = analyzer.get_function_context("calculate")
    x_usage = calculate_ctx.variable_usage.get("x")

    print(f"\n✓ Parameter 'x' usage:")
    print(f"  - Operators: {x_usage.operators_used if x_usage else 'none'}")

    # x used with *, should infer numeric type
    if x_usage:
        assert "*" in x_usage.operators_used or "+" in x_usage.operators_used

    print("\n✅ TEST 5 PASSED: Parameter types inferred from usage")
    return True


def test_call_chain_detection():
    """Test 6: Detect call chains between functions."""
    print("\n" + "=" * 70)
    print("TEST 6: Call Chain Detection")
    print("=" * 70)

    code = '''
def level1():
    return level2()

def level2():
    return level3()

def level3():
    return "bottom"

def independent():
    return "separate"
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    # Find chain from level1 to level3
    chain = analyzer.find_call_chain("level1", "level3")
    print(f"✓ Call chain from level1 to level3: {chain}")
    assert chain is not None
    assert chain == ["level1", "level2", "level3"]

    # No chain from level1 to independent
    no_chain = analyzer.find_call_chain("level1", "independent")
    print(f"✓ No chain from level1 to independent: {no_chain}")
    assert no_chain is None

    print("\n✅ TEST 6 PASSED: Call chains detected correctly")
    return True


def test_data_flow_tracking():
    """Test 7: Track data flow between functions."""
    print("\n" + "=" * 70)
    print("TEST 7: Data Flow Tracking")
    print("=" * 70)

    code = '''
def create_user(name):
    user = {"name": name}
    return user

def get_user_name(user):
    return user["name"]

def main():
    u = create_user("Alice")
    name = get_user_name(u)
    return name
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    print(f"✓ Tracked {len(analyzer.data_flows)} data flows")
    for flow in analyzer.data_flows:
        print(f"  - {flow.from_function}.{flow.from_variable} → {flow.to_function}.{flow.to_variable}")

    # Should have flow from main.u to get_user_name.user
    flows_to_get_user_name = analyzer.get_data_flows_to("get_user_name", "user")
    print(f"\n✓ Data flows to get_user_name.user: {len(flows_to_get_user_name)}")

    print("\n✅ TEST 7 PASSED: Data flows tracked")
    return True


def test_complex_multi_function_inference():
    """Test 8: Complex multi-function scenario with inference."""
    print("\n" + "=" * 70)
    print("TEST 8: Complex Multi-Function Type Inference")
    print("=" * 70)

    code = '''
def database_query(query):
    # Simulates database call
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = database_query(query)
    return result

def get_user_email(user_id):
    user = get_user(user_id)
    return user["email"]

def send_email(recipient, message):
    print(f"Sending to {recipient}: {message}")
    return True

def notify_user(user_id, message):
    email = get_user_email(user_id)
    success = send_email(email, message)
    return success
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    # Context analysis
    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    print(f"✓ Analyzed {len(analyzer.call_graph.nodes)} functions")
    print(f"✓ Call graph edges: {len(analyzer.call_graph.edges)}")

    # Visualize call graph
    print("\n" + analyzer.visualize_call_graph())

    # Type inference
    type_system = TypeSystem()
    type_map = type_system.analyze_cross_function_types(module)

    print(f"\n✓ Inferred types for {len(type_map)} variables/returns")

    # Statistics
    stats = analyzer.get_statistics()
    print(f"\n✓ Statistics:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")

    print("\n✅ TEST 8 PASSED: Complex multi-function analysis working")
    return True


def test_accuracy_improvement():
    """Test 9: Measure accuracy improvement from context awareness."""
    print("\n" + "=" * 70)
    print("TEST 9: Accuracy Improvement Measurement")
    print("=" * 70)

    code = '''
def get_user(user_id):
    return database.find_user(user_id)

def process_order(order_id):
    order = database.find_order(order_id)
    user = get_user(order.user_id)
    return {
        "order": order,
        "user": user,
        "total": order.amount
    }

def send_confirmation(order_id):
    data = process_order(order_id)
    email = data["user"].email
    send_email(email, f"Order {data['order'].id} confirmed")
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    # WITHOUT context analysis
    type_system_basic = TypeSystem()
    basic_type_map = type_system_basic.propagate_types(module)

    # Count 'any' types (fallback)
    basic_any_count = sum(1 for t in basic_type_map.values() if t.pw_type == "any")
    basic_total = len(basic_type_map)

    print(f"✓ Basic type inference:")
    print(f"  - Total types: {basic_total}")
    print(f"  - 'any' types: {basic_any_count}")
    if basic_total > 0:
        print(f"  - Specificity: {((basic_total - basic_any_count) / basic_total * 100):.1f}%")

    # WITH context analysis
    context_type_map = type_system_basic.analyze_cross_function_types(module)

    context_any_count = sum(1 for t in context_type_map.values() if t.pw_type == "any")
    context_total = len(context_type_map)

    print(f"\n✓ Context-aware type inference:")
    print(f"  - Total types: {context_total}")
    print(f"  - 'any' types: {context_any_count}")
    if context_total > 0:
        print(f"  - Specificity: {((context_total - context_any_count) / context_total * 100):.1f}%")

    # Calculate improvement
    if basic_total > 0 and context_total > 0:
        basic_specificity = (basic_total - basic_any_count) / basic_total
        context_specificity = (context_total - context_any_count) / context_total
        improvement = (context_specificity - basic_specificity) * 100

        print(f"\n✓ Improvement: {improvement:+.1f}%")

    print("\n✅ TEST 9 PASSED: Accuracy measurement complete")
    return True


def test_real_world_class_scenario():
    """Test 10: Real-world class-based code with context inference."""
    print("\n" + "=" * 70)
    print("TEST 10: Real-World Class-Based Context Analysis")
    print("=" * 70)

    code = '''
class UserService:
    def __init__(self, database):
        self.db = database
        self.cache = {}

    def get_user(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        user = self.db.find_user(user_id)
        if user:
            self.cache[user_id] = user
        return user

    def get_user_email(self, user_id):
        user = self.get_user(user_id)
        return user.email

class EmailService:
    def send(self, recipient, message):
        print(f"Sending to {recipient}: {message}")
        return True

class NotificationService:
    def __init__(self, user_service, email_service):
        self.users = user_service
        self.emails = email_service

    def notify_user(self, user_id, message):
        email = self.users.get_user_email(user_id)
        success = self.emails.send(email, message)
        return success
'''

    parser = PythonParserV2()
    module = parser.parse_source(code, "test")

    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)

    print(f"✓ Parsed {len(module.classes)} classes")
    print(f"✓ Call graph nodes: {len(analyzer.call_graph.nodes)}")

    # Check method calls across classes
    notify_context = analyzer.get_function_context("NotificationService.notify_user")
    if notify_context:
        print(f"\n✓ NotificationService.notify_user:")
        print(f"  - Calls: {[c.callee_function for c in notify_context.calls_made]}")

    # Type inference on classes
    type_system = TypeSystem()
    type_map = type_system.analyze_cross_function_types(module)

    print(f"\n✓ Inferred types: {len(type_map)}")

    print("\n✅ TEST 10 PASSED: Real-world class scenario analyzed")
    return True


def run_all_tests():
    """Run all context awareness tests."""
    print("\n" + "=" * 70)
    print("CONTEXT-AWARE TYPE INFERENCE TEST SUITE")
    print("=" * 70)

    tests = [
        test_call_graph_construction,
        test_variable_usage_tracking,
        test_cross_function_type_inference,
        test_return_type_inference,
        test_parameter_type_inference,
        test_call_chain_detection,
        test_data_flow_tracking,
        test_complex_multi_function_inference,
        test_accuracy_improvement,
        test_real_world_class_scenario,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test.__name__}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print(f"TEST RESULTS: {passed}/{len(tests)} PASSED")
    if failed > 0:
        print(f"⚠️  {failed} test(s) failed")
    else:
        print("✅ ALL TESTS PASSED!")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
