from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import time
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource


# OpenTelemetry setup
resource = Resource.create({"service.name": "code-reviewer"})

# Trace provider
trace_provider = TracerProvider(resource=resource)
trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace_provider.add_span_processor(trace_processor)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

# Metrics provider
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Metrics instruments
request_counter = meter.create_counter(
    "mcp_requests_total",
    description="Total number of MCP requests"
)
request_duration = meter.create_histogram(
    "mcp_request_duration_seconds",
    description="MCP request duration in seconds"
)
error_counter = meter.create_counter(
    "mcp_errors_total",
    description="Total number of MCP errors"
)

# MCP Server for agent: code-reviewer
app = FastAPI(
    title="code-reviewer",
    description="Promptware MCP Agent",
    version="v1"
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "code-reviewer",
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
AGENT_SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of:
- Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Performance issues (N+1 queries, memory leaks, inefficient algorithms)
- Code quality (readability, maintainability, best practices)
- Testing coverage and quality
Provide actionable, specific feedback with severity levels."""

def handle_review_analyze_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for review.analyze@v1

    Parameters:
        - code (string)
        - language (string)
        - context (string)

    Returns:
        - summary (string)
        - issues (array)
        - severity (string)
    """
    if "code" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: code"}}
    if "language" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: language"}}
    if "context" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: context"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("review.analyze@v1") as span:
        span.set_attribute("verb", "review.analyze@v1")
        span.set_attribute("agent", "code-reviewer")
        # AI-powered handler using LangChain
        try:
            # Build prompt with parameters
            user_prompt = f"""
    Analyze the following {language} code for security issues, bugs, and quality concerns.
    Context: {context}
    Provide a structured review with:
    1. Summary (2-3 sentences)
    2. List of specific issues with line numbers
    3. Overall severity (low/medium/high/critical)
    Return as JSON with keys: summary, issues (array), severity

    Input parameters:
        code: {params["code"]}
        language: {params["language"]}
        context: {params["context"]}
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
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "review.analyze@v1", "agent": "code-reviewer"})
    request_duration.record(duration, {"verb": "review.analyze@v1"})

def handle_review_approve_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for review.approve@v1

    Parameters:
        - review_id (string)
        - approved (bool)
        - comments (string)

    Returns:
        - status (string)
        - next_step (string)
    """
    if "review_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: review_id"}}
    if "approved" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: approved"}}
    if "comments" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: comments"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("review.approve@v1") as span:
        span.set_attribute("verb", "review.approve@v1")
        span.set_attribute("agent", "code-reviewer")
        # Generic AI handler
        try:
            user_prompt = f"Process the following request for review.approve@v1:\n"
            user_prompt += f"Parameters: {params.get('review_id')}, {params.get('approved')}, {params.get('comments')}"

            messages = [HumanMessage(content=user_prompt)]
            response = llm.invoke(messages)

            return {
                "status": response.content
            }
        except Exception as e:
            return {
                "error": {
                    "code": "E_RUNTIME",
                    "message": f"LLM call failed: {str(e)}"
                }
            }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "review.approve@v1", "agent": "code-reviewer"})
    request_duration.record(duration, {"verb": "review.approve@v1"})

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
        elif method == "review.approve@v1":
            result = handle_review_approve_v1(params)
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
        "verbs": ['"review.analyze@v1"', '"review.approve@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: code-reviewer")
    print(f"Port: 23450")
    print(f"Exposed verbs: ['review.analyze@v1', 'review.approve@v1']")
    print(f"Health check: http://127.0.0.1:23450/health")
    print(f"MCP endpoint: http://127.0.0.1:23450/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23450,
        log_level="info"
    )