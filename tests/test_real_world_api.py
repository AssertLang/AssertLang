"""
Test real-world program: Simple Web API

This tests a complete web API that uses:
- Multiple classes (Request, Response, User, Server)
- HTTP request/response handling
- CRUD operations
- Route handlers
- Status codes
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dsl.al_parser import parse_al


def test_api_server_parses():
    """Test that API server program parses without errors."""
    print(f"\n{'='*60}")
    print("Testing Simple Web API Program")
    print(f"{'='*60}")

    # Read the API server program
    api_file = Path(__file__).parent.parent / "examples" / "simple_web_api.al"

    try:
        with open(api_file) as f:
            pw_code = f.read()

        print(f"  ✅ Read API server program: {len(pw_code)} chars")

        # Parse the program
        ir = parse_al(pw_code)

        print(f"  ✅ Parsed successfully")
        print(f"  ✅ Classes: {len(ir.classes)}")
        print(f"  ✅ Functions: {len(ir.functions)}")

        # Verify expected structure
        assert len(ir.classes) == 4, f"Expected 4 classes, got {len(ir.classes)}"

        class_names = [c.name for c in ir.classes]
        assert "HttpRequest" in class_names, "Expected HttpRequest class"
        assert "HttpResponse" in class_names, "Expected HttpResponse class"
        assert "User" in class_names, "Expected User class"
        assert "ApiServer" in class_names, "Expected ApiServer class"

        # Find classes
        http_request = next(c for c in ir.classes if c.name == "HttpRequest")
        http_response = next(c for c in ir.classes if c.name == "HttpResponse")
        user = next(c for c in ir.classes if c.name == "User")
        api_server = next(c for c in ir.classes if c.name == "ApiServer")

        # Verify HttpRequest
        assert len(http_request.properties) == 5, f"Expected 5 properties in HttpRequest"
        assert http_request.constructor is not None, "Expected HttpRequest constructor"

        # Verify HttpResponse
        assert len(http_response.properties) == 3, f"Expected 3 properties in HttpResponse"
        assert http_response.constructor is not None, "Expected HttpResponse constructor"

        # Verify User
        assert len(user.properties) == 4, f"Expected 4 properties in User"
        assert user.constructor is not None, "Expected User constructor"

        # Verify ApiServer
        assert len(api_server.properties) == 2, f"Expected 2 properties in ApiServer"
        assert api_server.constructor is not None, "Expected ApiServer constructor"
        assert len(api_server.methods) >= 6, f"Expected at least 6 methods in ApiServer"

        # Verify route handlers
        function_names = [f.name for f in ir.functions]
        assert "handle_get_users" in function_names
        assert "handle_get_user" in function_names
        assert "handle_create_user" in function_names
        assert "handle_update_user" in function_names
        assert "handle_delete_user" in function_names
        assert "handle_request" in function_names
        assert "initialize_server" in function_names
        assert "simulate_requests" in function_names
        assert "main" in function_names

        print(f"\n✅ SUCCESS: Simple Web API program is valid!")
        print(f"\nProgram structure:")
        print(f"  - HttpRequest class")
        print(f"  - HttpResponse class")
        print(f"  - User model class")
        print(f"  - ApiServer class with {len(api_server.methods)} methods")
        print(f"  - {len(ir.functions)} route handlers and utilities")
        print(f"  - Uses: HTTP handling, CRUD, routing, status codes")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_api_server_parses()
    sys.exit(0 if success else 1)
