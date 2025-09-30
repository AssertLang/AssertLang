from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import time
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource


# OpenTelemetry setup
resource = Resource.create({"service.name": "monitored-service"})

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

# MCP Server for agent: monitored-service
app = FastAPI(
    title="monitored-service",
    description="Promptware MCP Agent",
    version="v1"
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "monitored-service",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

def handle_task_execute_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for task.execute@v1

    Parameters:
        - task_id (string)
        - priority (int)

    Returns:
        - result (string)
        - status (string)
    """
    if "task_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: task_id"}}
    if "priority" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: priority"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("task.execute@v1") as span:
        span.set_attribute("verb", "task.execute@v1")
        span.set_attribute("agent", "monitored-service")
        # TODO: Implement actual handler logic
        # For now, return mock data
        return {
            "result": "result_value",
            "status": "status_value"
        }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "task.execute@v1", "agent": "monitored-service"})
    request_duration.record(duration, {"verb": "task.execute@v1"})

def handle_task_status_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for task.status@v1

    Parameters:
        - task_id (string)

    Returns:
        - status (string)
        - progress (int)
    """
    if "task_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: task_id"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("task.status@v1") as span:
        span.set_attribute("verb", "task.status@v1")
        span.set_attribute("agent", "monitored-service")
        # TODO: Implement actual handler logic
        # For now, return mock data
        return {
            "status": "status_value",
            "progress": 0
        }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "task.status@v1", "agent": "monitored-service"})
    request_duration.record(duration, {"verb": "task.status@v1"})

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
        if method == "task.execute@v1":
            result = handle_task_execute_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "task.status@v1":
            result = handle_task_status_v1(params)
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
        "agent": "monitored-service",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "monitored-service",
        "verbs": ['"task.execute@v1"', '"task.status@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: monitored-service")
    print(f"Port: 23456")
    print(f"Exposed verbs: ['task.execute@v1', 'task.status@v1']")
    print(f"Health check: http://127.0.0.1:23456/health")
    print(f"MCP endpoint: http://127.0.0.1:23456/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23456,
        log_level="info"
    )