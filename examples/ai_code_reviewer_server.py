from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# MCP Server for agent: ai-code-reviewer
app = FastAPI(
    title="ai-code-reviewer",
    description="Promptware MCP Agent",
    version="v1"
)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "ai-code-reviewer",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

# LLM initialization (anthropic claude-3-5-sonnet-20241022)
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0,
)

# Global agent prompt
AGENT_SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of software security,
performance optimization, and best practices across multiple programming languages.
Your goal is to analyze code thoroughly and provide actionable feedback."""

def handle_review_analyze_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for review.analyze@v1

    Parameters:
        - repo (string)
        - pr_number (int)

    Returns:
        - summary (string)
        - issues (array)
        - suggestions (array)
    """
    if "repo" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: repo"}}
    if "pr_number" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: pr_number"}}

    agent_state["requests_handled"] += 1

    # AI-powered handler using LangChain
    try:
        # Build prompt with parameters
        user_prompt = f"""
Analyze the pull request from the following repository and PR number.
Look for:
- Security vulnerabilities (SQL injection, XSS, authentication flaws)
- Performance issues (N+1 queries, inefficient algorithms)
- Code quality problems (duplicated code, poor naming, missing tests)
- Best practice violations
For each issue found, provide:
- Severity level (critical, high, medium, low)
- File and line number
- Description of the problem
- Suggested fix
Return your analysis in the following structure:
- summary: Brief overview of the code quality
- issues: Array of problems found
- suggestions: Array of improvement recommendations

Input parameters:
    repo: {params["repo"]}
    pr_number: {params["pr_number"]}
"""

        # Call LLM
        messages = []
        if hasattr(globals().get('AGENT_SYSTEM_PROMPT'), '__len__'):
            messages.append(SystemMessage(content=AGENT_SYSTEM_PROMPT))
        messages.append(HumanMessage(content=user_prompt))

        response = llm.invoke(messages)
        result_text = response.content

        # Parse response and structure return values
        # TODO: Improve response parsing based on return types
        return {
            "summary": result_text
        }

    except Exception as e:
        return {
            "error": {
                "code": "E_RUNTIME",
                "message": f"LLM call failed: {str(e)}"
            }
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

    agent_state["requests_handled"] += 1

    # AI-powered handler using LangChain
    try:
        # Build prompt with parameters
        user_prompt = f"""
You are reviewing a pull request at the given URL.
Create a review ID and return pending status.
This is a quick acknowledgment before full analysis.

Input parameters:
    pr_url: {params["pr_url"]}
"""

        # Call LLM
        messages = []
        if hasattr(globals().get('AGENT_SYSTEM_PROMPT'), '__len__'):
            messages.append(SystemMessage(content=AGENT_SYSTEM_PROMPT))
        messages.append(HumanMessage(content=user_prompt))

        response = llm.invoke(messages)
        result_text = response.content

        # Parse response and structure return values
        # TODO: Improve response parsing based on return types
        return {
            "review_id": result_text
        }

    except Exception as e:
        return {
            "error": {
                "code": "E_RUNTIME",
                "message": f"LLM call failed: {str(e)}"
            }
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
        if method == "review.analyze@v1":
            result = handle_review_analyze_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "review.submit@v1":
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
        "agent": "ai-code-reviewer",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "ai-code-reviewer",
        "verbs": ['"review.analyze@v1"', '"review.submit@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: ai-code-reviewer")
    print(f"Port: 23456")
    print(f"Exposed verbs: ['review.analyze@v1', 'review.submit@v1']")
    print(f"Health check: http://127.0.0.1:23456/health")
    print(f"MCP endpoint: http://127.0.0.1:23456/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23456,
        log_level="info"
    )