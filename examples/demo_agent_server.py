from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime

# MCP Server for agent: code-reviewer
app = FastAPI(
    title="code-reviewer",
    description="Promptware MCP Agent",
    version="v1"
)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "code-reviewer",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

def handle_review_submit_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for review.submit@v1

    Parameters:
        - pr_url (string)

    Returns:
        - review_id (string)
        - status (string)
    """
    if "pr_url" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: pr_url"}}

    # TODO: Implement actual handler logic
    # For now, return mock data
    agent_state["requests_handled"] += 1

    return {
        "review_id": "review_id_value",
        "status": "status_value"
    }

def handle_review_status_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for review.status@v1

    Parameters:
        - review_id (string)

    Returns:
        - status (string)
        - progress (int)
        - comments (array)
    """
    if "review_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: review_id"}}

    # TODO: Implement actual handler logic
    # For now, return mock data
    agent_state["requests_handled"] += 1

    return {
        "status": "status_value",
        "progress": 0,
        "comments": []
    }

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Main MCP endpoint - handles JSON-RPC requests.

    Request format:
    {
        "method": "verb.name@v1",
        "params": {...}
    }

    Response format:
    {
        "ok": true,
        "version": "v1",
        "data": {...}
    }
    """
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})

        if not method:
            return JSONResponse(
                status_code=400,
                content={
                    "ok": False,
                    "version": "v1",
                    "error": {
                        "code": "E_ARGS",
                        "message": "Missing 'method' in request"
                    }
                }
            )

        # Route to appropriate handler
        if method == "review.submit@v1":
            result = handle_review_submit_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "review.status@v1":
            result = handle_review_status_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "ok": False,
                    "version": "v1",
                    "error": {
                        "code": "E_METHOD",
                        "message": f"Unknown method: {method}"
                    }
                }
            )

        # Success response
        return JSONResponse(
            content={
                "ok": True,
                "version": "v1",
                "data": result
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "version": "v1",
                "error": {
                    "code": "E_RUNTIME",
                    "message": str(e)
                }
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "code-reviewer",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "code-reviewer",
        "verbs": ['"review.submit@v1"', '"review.status@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: code-reviewer")
    print(f"Port: 23456")
    print(f"Exposed verbs: ['review.submit@v1', 'review.status@v1']")
    print(f"Health check: http://127.0.0.1:23456/health")
    print(f"MCP endpoint: http://127.0.0.1:23456/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23456,
        log_level="info"
    )