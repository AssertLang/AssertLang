import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Add project root to path for tool registry imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.tool_executor import ToolExecutor

# MCP Server for agent: user-service
app = FastAPI(
    title="user-service",
    description="AssertLang MCP Agent",
    version="v1"
)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "user-service",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

# Tool executor (if agent has tools)
tool_executor = None
if ['storage']:
    tool_executor = ToolExecutor(['storage'])

def handle_user_create_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for user.create@v1

    Parameters:
        - email (string)
        - name (string)

    Returns:
        - user_id (string)
        - email (string)
        - name (string)
        - status (string)
        - created_at (string)
    """
    if "email" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: email"}}
    if "name" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: name"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "user_id": "user_id_value",
        "email": "email_value",
        "name": "name_value",
        "status": "status_value",
        "created_at": "created_at_value"
    }

def handle_user_get_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for user.get@v1

    Parameters:
        - user_id (string)

    Returns:
        - user_id (string)
        - email (string)
        - name (string)
        - status (string)
        - created_at (string)
    """
    if "user_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: user_id"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "user_id": "user_id_value",
        "email": "email_value",
        "name": "name_value",
        "status": "status_value",
        "created_at": "created_at_value"
    }

def handle_user_list_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for user.list@v1

    Parameters:
        - limit (int)
        - offset (int)

    Returns:
        - users (array)
        - total (int)
    """
    if "limit" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: limit"}}
    if "offset" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: offset"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "users": [],
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
                            "name": "user-service",
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
                        "tools": [{'name': 'user.create@v1', 'description': 'Execute user.create@v1', 'inputSchema': {'type': 'object', 'properties': {'email': {'type': 'string', 'description': 'Parameter: email'}, 'name': {'type': 'string', 'description': 'Parameter: name'}}, 'required': ['email', 'name']}}, {'name': 'user.get@v1', 'description': 'Execute user.get@v1', 'inputSchema': {'type': 'object', 'properties': {'user_id': {'type': 'string', 'description': 'Parameter: user_id'}}, 'required': ['user_id']}}, {'name': 'user.list@v1', 'description': 'Execute user.list@v1', 'inputSchema': {'type': 'object', 'properties': {'limit': {'type': 'integer', 'description': 'Parameter: limit'}, 'offset': {'type': 'integer', 'description': 'Parameter: offset'}}, 'required': ['limit', 'offset']}}]
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

            if verb_name == "user.create@v1":
                verb_result = handle_user_create_v1(verb_params)
            elif verb_name == "user.get@v1":
                verb_result = handle_user_get_v1(verb_params)
            elif verb_name == "user.list@v1":
                verb_result = handle_user_list_v1(verb_params)
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
                    "agent_name": "user-service",
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
        "agent": "user-service",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "user-service",
        "verbs": ['"user.create@v1"', '"user.get@v1"', '"user.list@v1"']
    }

if __name__ == "__main__":
    print("Starting MCP server for agent: user-service")
    print("Port: 23450")
    print("Exposed verbs: ['user.create@v1', 'user.get@v1', 'user.list@v1']")
    print("Health check: http://127.0.0.1:23450/health")
    print("MCP endpoint: http://127.0.0.1:23450/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23450,
        log_level="info"
    )