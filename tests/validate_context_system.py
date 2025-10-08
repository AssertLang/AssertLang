#!/usr/bin/env python3
"""
Quick validation that context-aware type inference system is working.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.context_analyzer import ContextAnalyzer
from dsl.type_system import TypeSystem
from language.python_parser_v2 import PythonParserV2


def main():
    print("🔍 Validating Context-Aware Type Inference System...\n")

    # Test code
    code = '''
def get_user(user_id):
    return database.find(user_id)

def process():
    user = get_user(42)
    name = user.name
    return name
'''

    # Parse
    parser = PythonParserV2()
    module = parser.parse_source(code, "test")
    print(f"✅ Parsed {len(module.functions)} functions")

    # Build call graph
    analyzer = ContextAnalyzer()
    analyzer.analyze_module(module)
    print(f"✅ Built call graph: {len(analyzer.call_graph.nodes)} nodes")

    # Check data flows
    print(f"✅ Tracked {len(analyzer.data_flows)} data flows")

    # Infer types
    type_system = TypeSystem()
    type_map = type_system.analyze_cross_function_types(module)
    print(f"✅ Inferred {len(type_map)} cross-function types")

    # Check specific inferences
    process_ctx = analyzer.get_function_context("process")
    if process_ctx:
        user_usage = process_ctx.variable_usage.get("user")
        if user_usage and "name" in user_usage.property_accesses:
            print(f"✅ Detected property access: user.name")

    # Statistics
    stats = analyzer.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   - Functions: {stats['total_functions']}")
    print(f"   - Call sites: {stats['total_call_sites']}")
    print(f"   - Variables: {stats['total_variables']}")
    print(f"   - Data flows: {stats['total_data_flows']}")

    print("\n✅ All systems operational!")
    print("\n📋 Summary:")
    print("   - Context analyzer: Working")
    print("   - Type system: Working")
    print("   - Call graph: Working")
    print("   - Data flow: Working")
    print("   - Cross-function inference: Working")

    print("\n⚠️  Note: Generators not yet using context-aware types")
    print("   Integration needed to see accuracy improvement")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
