import time
from datetime import datetime
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from opentelemetry import metrics, trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# OpenTelemetry setup
resource = Resource.create({"service.name": "test-runner"})

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

# MCP Server for agent: test-runner
app = FastAPI(
    title="test-runner",
    description="AssertLang MCP Agent",
    version="v1"
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "test-runner",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

def handle_test_run_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for test.run@v1

    Parameters:
        - project_path (string)
        - test_suite (string)
        - environment (string)

    Returns:
        - test_id (string)
        - status (string)
        - total_tests (int)
        - passed (int)
        - failed (int)
    """
    if "project_path" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: project_path"}}
    if "test_suite" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: test_suite"}}
    if "environment" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: environment"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("test.run@v1") as span:
        span.set_attribute("verb", "test.run@v1")
        span.set_attribute("agent", "test-runner")
        # TODO: Implement actual handler logic
        # For now, return mock data
        return {
            "test_id": "test_id_value",
            "status": "status_value",
            "total_tests": 0,
            "passed": 0,
            "failed": 0
        }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "test.run@v1", "agent": "test-runner"})
    request_duration.record(duration, {"verb": "test.run@v1"})

def handle_test_status_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for test.status@v1

    Parameters:
        - test_id (string)

    Returns:
        - status (string)
        - progress (int)
        - results (array)
    """
    if "test_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: test_id"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("test.status@v1") as span:
        span.set_attribute("verb", "test.status@v1")
        span.set_attribute("agent", "test-runner")
        # TODO: Implement actual handler logic
        # For now, return mock data
        return {
            "status": "status_value",
            "progress": 0,
            "results": []
        }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "test.status@v1", "agent": "test-runner"})
    request_duration.record(duration, {"verb": "test.status@v1"})

def handle_test_report_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for test.report@v1

    Parameters:
        - test_id (string)

    Returns:
        - report (string)
        - coverage (float)
        - duration (float)
    """
    if "test_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: test_id"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("test.report@v1") as span:
        span.set_attribute("verb", "test.report@v1")
        span.set_attribute("agent", "test-runner")
        # TODO: Implement actual handler logic
        # For now, return mock data
        return {
            "report": "report_value",
            "coverage": None,
            "duration": None
        }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "test.report@v1", "agent": "test-runner"})
    request_duration.record(duration, {"verb": "test.report@v1"})

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
        if method == "test.run@v1":
            result = handle_test_run_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "test.status@v1":
            result = handle_test_status_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "test.report@v1":
            result = handle_test_report_v1(params)
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
        "agent": "test-runner",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "test-runner",
        "verbs": ['"test.run@v1"', '"test.status@v1"', '"test.report@v1"']
    }

if __name__ == "__main__":
    print("Starting MCP server for agent: test-runner")
    print("Port: 23451")
    print("Exposed verbs: ['test.run@v1', 'test.status@v1', 'test.report@v1']")
    print("Health check: http://127.0.0.1:23451/health")
    print("MCP endpoint: http://127.0.0.1:23451/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23451,
        log_level="info"
    )