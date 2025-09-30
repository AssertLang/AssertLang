from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import time
import sys
from pathlib import Path

# Add project root to path for tool registry imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.registry import get_registry
from language.tool_executor import ToolExecutor


# MCP Server for agent: order-service
app = FastAPI(
    title="order-service",
    description="Promptware MCP Agent",
    version="v1"
)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "order-service",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

# Tool executor (if agent has tools)
tool_executor = None
if ['storage', 'http']:
    tool_executor = ToolExecutor(['storage', 'http'])

def handle_order_create_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for order.create@v1

    Parameters:
        - user_id (string)
        - items (array)
        - total_amount (string)

    Returns:
        - order_id (string)
        - user_id (string)
        - user_name (string)
        - items (array)
        - total_amount (string)
        - status (string)
        - created_at (string)
    """
    if "user_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: user_id"}}
    if "items" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: items"}}
    if "total_amount" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: total_amount"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "order_id": "order_id_value",
        "user_id": "user_id_value",
        "user_name": "user_name_value",
        "items": [],
        "total_amount": "total_amount_value",
        "status": "status_value",
        "created_at": "created_at_value"
    }

def handle_order_get_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for order.get@v1

    Parameters:
        - order_id (string)

    Returns:
        - order_id (string)
        - user_id (string)
        - items (array)
        - total_amount (string)
        - status (string)
        - created_at (string)
    """
    if "order_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: order_id"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "order_id": "order_id_value",
        "user_id": "user_id_value",
        "items": [],
        "total_amount": "total_amount_value",
        "status": "status_value",
        "created_at": "created_at_value"
    }

def handle_order_list_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for order.list@v1

    Parameters:
        - user_id (string)
        - limit (int)
        - offset (int)

    Returns:
        - orders (array)
        - total (int)
    """
    if "user_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: user_id"}}
    if "limit" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: limit"}}
    if "offset" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: offset"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "orders": [],
        "total": 0
    }

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Main MCP endpoint - implements full MCP JSON-RPC protocol.

    Supports methods:
    - initialize: Return server capabilities
    - tools/list: List all available tools
    - tools/call: Execute a tool/verb
    """
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id", 1)

        if not method:
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: missing method"
                    }
                }
            )

        # Handle MCP protocol methods
        if method == "initialize":
            # Return server capabilities
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "0.1.0",
                        "capabilities": {
                            "tools": {},
                            "prompts": {}
                        },
                        "serverInfo": {
                            "name": "order-service",
                            "version": "v1"
                        }
                    }
                }
            )

        elif method == "tools/list":
            # Return tool schemas
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [{'name': 'order.create@v1', 'description': 'Execute order.create@v1', 'inputSchema': {'type': 'object', 'properties': {'user_id': {'type': 'string', 'description': 'Parameter: user_id'}, 'items': {'type': 'array', 'description': 'Parameter: items'}, 'total_amount': {'type': 'string', 'description': 'Parameter: total_amount'}}, 'required': ['user_id', 'items', 'total_amount']}}, {'name': 'order.get@v1', 'description': 'Execute order.get@v1', 'inputSchema': {'type': 'object', 'properties': {'order_id': {'type': 'string', 'description': 'Parameter: order_id'}}, 'required': ['order_id']}}, {'name': 'order.list@v1', 'description': 'Execute order.list@v1', 'inputSchema': {'type': 'object', 'properties': {'user_id': {'type': 'string', 'description': 'Parameter: user_id'}, 'limit': {'type': 'integer', 'description': 'Parameter: limit'}, 'offset': {'type': 'integer', 'description': 'Parameter: offset'}}, 'required': ['user_id', 'limit', 'offset']}}]
                    }
                }
            )

        elif method == "tools/call":
            # Execute tool with full MCP envelope
            tool_name = params.get("name")
            verb_params = params.get("arguments", {})

            if not tool_name:
                return JSONResponse(
                    status_code=400,
                    content={
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": "Invalid params: missing tool name"
                        }
                    }
                )

            agent_state["requests_handled"] += 1

            # Execute tools first (if agent has tools)
            tool_results = {}
            tools_executed = []
            if tool_executor and tool_executor.has_tools():
                tool_results = tool_executor.execute_tools(verb_params)
                tools_executed = list(tool_results.keys())

            # Route to appropriate verb handler
            verb_name = tool_name
            verb_result = None

            if verb_name == "order.create@v1":
                verb_result = handle_order_create_v1(verb_params)
            elif verb_name == "order.get@v1":
                verb_result = handle_order_get_v1(verb_params)
            elif verb_name == "order.list@v1":
                verb_result = handle_order_list_v1(verb_params)
            else:
                return JSONResponse(
                    status_code=404,
                    content={
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {tool_name}"
                        }
                    }
                )

            # Check for errors
            if verb_result and "error" in verb_result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32000,
                            "message": verb_result["error"].get("message", "Unknown error")
                        }
                    }
                )

            # Determine mode (IDE-integrated vs standalone AI)
            import os
            has_api_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
            mode = "standalone_ai" if (has_api_key and False) else "ide_integrated"

            # Build MCP-compliant response
            response_data = {
                "input_params": verb_params,
                "tool_results": tool_results,
                "metadata": {
                    "mode": mode,
                    "agent_name": "order-service",
                    "timestamp": datetime.now().isoformat(),
                    "tools_executed": tools_executed
                }
            }

            # Merge verb result into response
            if verb_result:
                response_data.update(verb_result)

            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": response_data
                }
            )

        else:
            return JSONResponse(
                status_code=404,
                content={
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": body.get("id", 1) if "body" in locals() else 1,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "order-service",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "order-service",
        "verbs": ['"order.create@v1"', '"order.get@v1"', '"order.list@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: order-service")
    print(f"Port: 23451")
    print(f"Exposed verbs: ['order.create@v1', 'order.get@v1', 'order.list@v1']")
    print(f"Health check: http://127.0.0.1:23451/health")
    print(f"MCP endpoint: http://127.0.0.1:23451/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23451,
        log_level="info"
    )