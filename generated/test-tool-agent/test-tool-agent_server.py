from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import time
import sys
import os
from pathlib import Path

# Add project root to path for tool registry imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.registry import get_registry
from language.tool_executor import ToolExecutor


# MCP Server for agent: test-tool-agent
app = FastAPI(
    title="test-tool-agent",
    description="Promptware MCP Agent",
    version="v1"
)


# Error handling middleware
import logging
import traceback
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_errors(func):
    """Decorator for consistent error handling."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return {
                "error": {
                    "code": -32602,
                    "message": f"Invalid parameters: {str(e)}"
                }
            }
        except TimeoutError as e:
            logger.error(f"Timeout: {e}")
            return {
                "error": {
                    "code": -32004,
                    "message": f"Operation timed out: {str(e)}"
                }
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            return {
                "error": {
                    "code": -32603,
                    "message": "Internal server error",
                    "data": str(e) if os.environ.get("DEBUG") else None
                }
            }
    return wrapper



# Health check endpoints
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any

class HealthCheck:
    """Health check manager for MCP server."""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.ready = False
        self.dependencies = {}

    async def check_readiness(self) -> Dict[str, Any]:
        """Check if server is ready to accept requests."""
        checks = {
            "server": "ok",
            "dependencies": {}
        }

        # Check tool registry
        try:
            # Verify tools are loadable
            checks["dependencies"]["tools"] = "ok"
        except Exception as e:
            checks["dependencies"]["tools"] = f"error: {e}"
            checks["server"] = "not_ready"

        return {
            "status": checks["server"],
            "checks": checks["dependencies"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def check_liveness(self) -> Dict[str, Any]:
        """Check if server is alive (basic ping)."""
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()

        return {
            "status": "alive",
            "uptime_seconds": uptime,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

health_checker = HealthCheck()



def validate_params(params: dict, required: list[str], types: dict[str, type] = None) -> tuple[bool, str]:
    """Validate request parameters."""
    for param in required:
        if param not in params:
            return False, f"Missing required parameter: {param}"

    if types:
        for param, expected_type in types.items():
            if param in params and not isinstance(params[param], expected_type):
                return False, f"Parameter '{param}' must be of type {expected_type.__name__}"

    return True, ""



# Security middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Trusted host middleware
if os.environ.get("ALLOWED_HOSTS"):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=os.environ.get("ALLOWED_HOSTS").split(",")
    )

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "test-tool-agent",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

# Tool executor (if agent has tools)
tool_executor = None
if ['http']:
    tool_executor = ToolExecutor(['http'])

def handle_fetch_url_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for fetch.url@v1

    Parameters:
        - url (string)
        - method (string)

    Returns:
        - status (int)
        - body (string)
        - summary (string)
    """
    if "url" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: url"}}
    if "method" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: method"}}

    agent_state["requests_handled"] += 1
    # TODO: Implement actual handler logic
    # For now, return mock data
    return {
        "status": 0,
        "body": "body_value",
        "summary": "summary_value"
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
                            "name": "test-tool-agent",
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
                        "tools": [{'name': 'fetch.url@v1', 'description': 'Execute fetch.url@v1', 'inputSchema': {'type': 'object', 'properties': {'url': {'type': 'string', 'description': 'Parameter: url'}, 'method': {'type': 'string', 'description': 'Parameter: method'}}, 'required': ['url', 'method']}}]
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

            if verb_name == "fetch.url@v1":
                verb_result = handle_fetch_url_v1(verb_params)
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
                    "agent_name": "test-tool-agent",
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
async def health():
    """Basic health check (liveness probe)."""
    return await health_checker.check_liveness()



@app.get("/ready")
async def ready():
    """Readiness probe - checks dependencies."""
    return await health_checker.check_readiness()


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "test-tool-agent",
        "verbs": ['"fetch.url@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: test-tool-agent")
    print(f"Port: 23460")
    print(f"Exposed verbs: ['fetch.url@v1']")
    print(f"Health check: http://127.0.0.1:23460/health")
    print(f"MCP endpoint: http://127.0.0.1:23460/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23460,
        log_level="info"
    )