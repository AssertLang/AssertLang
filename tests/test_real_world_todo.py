"""
Test real-world program: Todo List Manager

This tests a complete todo list application that uses:
- Multiple classes with relationships
- Arrays of objects
- CRUD operations
- Filtering and search functionality
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.pw_parser import parse_pw


def test_todo_manager_parses():
    """Test that todo manager program parses without errors."""
    print(f"\n{'='*60}")
    print("Testing Todo List Manager Program")
    print(f"{'='*60}")

    # Read the todo manager program
    todo_file = Path(__file__).parent.parent / "examples" / "todo_list_manager.pw"

    try:
        with open(todo_file) as f:
            pw_code = f.read()

        print(f"  ✅ Read todo manager program: {len(pw_code)} chars")

        # Parse the program
        ir = parse_pw(pw_code)

        print(f"  ✅ Parsed successfully")
        print(f"  ✅ Classes: {len(ir.classes)}")
        print(f"  ✅ Functions: {len(ir.functions)}")

        # Verify expected structure
        assert len(ir.classes) == 2, f"Expected 2 classes, got {len(ir.classes)}"

        class_names = [c.name for c in ir.classes]
        assert "TodoItem" in class_names, "Expected TodoItem class"
        assert "TodoListManager" in class_names, "Expected TodoListManager class"

        # Find TodoItem class
        todo_item = next(c for c in ir.classes if c.name == "TodoItem")
        assert len(todo_item.properties) == 5, f"Expected 5 properties in TodoItem"
        assert todo_item.constructor is not None, "Expected TodoItem constructor"
        assert len(todo_item.methods) >= 5, f"Expected at least 5 methods in TodoItem"

        # Find TodoListManager class
        manager = next(c for c in ir.classes if c.name == "TodoListManager")
        assert len(manager.properties) == 2, f"Expected 2 properties in TodoListManager"
        assert manager.constructor is not None, "Expected TodoListManager constructor"
        assert len(manager.methods) >= 8, f"Expected at least 8 methods in TodoListManager"

        # Verify helper functions
        function_names = [f.name for f in ir.functions]
        assert "create_sample_todos" in function_names
        assert "main" in function_names

        print(f"\n✅ SUCCESS: Todo List Manager program is valid!")
        print(f"\nProgram structure:")
        print(f"  - TodoItem class with {len(todo_item.methods)} methods")
        print(f"  - TodoListManager class with {len(manager.methods)} methods")
        print(f"  - {len(ir.functions)} helper functions")
        print(f"  - Uses: multiple classes, arrays, CRUD operations, filtering")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_todo_manager_parses()
    sys.exit(0 if success else 1)
