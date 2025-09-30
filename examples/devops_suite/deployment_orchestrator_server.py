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
import asyncio
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker

@activity.defn(name="fetch_code_changes", start_to_close_timeout=timedelta(minutes=5))
async def fetch_code_changes(**kwargs) -> Dict[str, Any]:
    """
    Activity: fetch_code_changes
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: fetch_code_changes")
    return {"status": "completed"}

@activity.defn(name="run_code_review", start_to_close_timeout=timedelta(minutes=10))
async def run_code_review(**kwargs) -> Dict[str, Any]:
    """
    Activity: run_code_review
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: run_code_review")
    return {"status": "completed"}

@activity.defn(name="run_tests", start_to_close_timeout=timedelta(minutes=15))
async def run_tests(**kwargs) -> Dict[str, Any]:
    """
    Activity: run_tests
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: run_tests")
    return {"status": "completed"}

@activity.defn(name="build_artifacts", start_to_close_timeout=timedelta(minutes=20))
async def build_artifacts(**kwargs) -> Dict[str, Any]:
    """
    Activity: build_artifacts
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: build_artifacts")
    return {"status": "completed"}

@activity.defn(name="deploy_to_staging", start_to_close_timeout=timedelta(minutes=10))
async def deploy_to_staging(**kwargs) -> Dict[str, Any]:
    """
    Activity: deploy_to_staging
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: deploy_to_staging")
    return {"status": "completed"}

@activity.defn(name="run_smoke_tests", start_to_close_timeout=timedelta(minutes=5))
async def run_smoke_tests(**kwargs) -> Dict[str, Any]:
    """
    Activity: run_smoke_tests
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: run_smoke_tests")
    return {"status": "completed"}

@activity.defn(name="deploy_to_production", start_to_close_timeout=timedelta(minutes=15))
async def deploy_to_production(**kwargs) -> Dict[str, Any]:
    """
    Activity: deploy_to_production
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: deploy_to_production")
    return {"status": "completed"}

@activity.defn(name="verify_deployment", start_to_close_timeout=timedelta(minutes=5))
async def verify_deployment(**kwargs) -> Dict[str, Any]:
    """
    Activity: verify_deployment
    Workflow: ci_cd_pipeline@v1
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: verify_deployment")
    return {"status": "completed"}

@workflow.defn(name="ci_cd_pipeline@v1")
class Ci_Cd_Pipeline_V1Workflow:
    """
    Temporal workflow: ci_cd_pipeline@v1

    Parameters: service, version, branch, commit_sha
    Returns: deployment_id, status, deployed_at
    """

    def __init__(self):
        self.workflow_state = {}

    @workflow.run
    async def run(self, service: str, version: str, branch: str, commit_sha: str) -> Dict[str, Any]:
        """Execute workflow steps."""
        # Step 1: fetch_code_changes
        result_0 = await workflow.execute_activity(
            fetch_code_changes,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=2)
        )

        # Step 2: run_code_review
        result_1 = await workflow.execute_activity(
            run_code_review,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=1)
        )
        if result_1.get("status") != "completed":
            # Compensation: notify_review_failure
            await workflow.execute_activity(
                notify_review_failure,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step run_code_review failed")

        # Step 3: run_tests
        result_2 = await workflow.execute_activity(
            run_tests,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=2)
        )
        if result_2.get("status") != "completed":
            # Compensation: notify_test_failure
            await workflow.execute_activity(
                notify_test_failure,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step run_tests failed")

        # Step 4: build_artifacts
        result_3 = await workflow.execute_activity(
            build_artifacts,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=1)
        )

        # Step 5: deploy_to_staging
        result_4 = await workflow.execute_activity(
            deploy_to_staging,
            schedule_to_close_timeout=timedelta(minutes=10)
        )
        if result_4.get("status") != "completed":
            # Compensation: rollback_staging
            await workflow.execute_activity(
                rollback_staging,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step deploy_to_staging failed")

        # Step 6: run_smoke_tests
        result_5 = await workflow.execute_activity(
            run_smoke_tests,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=1)
        )

        # Step 7: deploy_to_production
        result_6 = await workflow.execute_activity(
            deploy_to_production,
            schedule_to_close_timeout=timedelta(minutes=10)
        )
        if result_6.get("status") != "completed":
            # Compensation: rollback_production
            await workflow.execute_activity(
                rollback_production,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step deploy_to_production failed")

        # Wait for approval before continuing
        await workflow.wait_condition(lambda: workflow_state.get("approved_6", False))

        # Step 8: verify_deployment
        result_7 = await workflow.execute_activity(
            verify_deployment,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=2)
        )

        # Return workflow result
        return {
            "deployment_id": "value", "status": "value", "deployed_at": "value"
        }


# OpenTelemetry setup
resource = Resource.create({"service.name": "deployment-orchestrator"})

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

# MCP Server for agent: deployment-orchestrator
app = FastAPI(
    title="deployment-orchestrator",
    description="Promptware MCP Agent",
    version="v1"
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "deployment-orchestrator",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}

# Temporal client (global)
temporal_client: Optional[Client] = None

async def get_temporal_client() -> Client:
    """Get or create Temporal client."""
    global temporal_client
    if temporal_client is None:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client

# LLM initialization (anthropic claude-3-5-sonnet-20241022)
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0,
)

# Global agent prompt
AGENT_SYSTEM_PROMPT = """You are a DevOps orchestrator that coordinates code reviews, testing, and deployments.
Make intelligent decisions about deployment readiness based on review and test results."""

def handle_workflow_execute_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for workflow.execute@v1

    Parameters:
        - workflow_id (string)
        - params (object)

    Returns:
        - execution_id (string)
        - status (string)
    """
    if "workflow_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: workflow_id"}}
    if "params" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: params"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("workflow.execute@v1") as span:
        span.set_attribute("verb", "workflow.execute@v1")
        span.set_attribute("agent", "deployment-orchestrator")
        # Execute Temporal workflow
        try:
            workflow_id = params.get("workflow_id")
            workflow_params = params.get("params", {})

            # Get Temporal client
            client = asyncio.run(get_temporal_client())

            # Start workflow execution
            handle = asyncio.run(
                client.start_workflow(
                    Ci_Cd_Pipeline_V1Workflow.run,
                    **workflow_params,
                    id=workflow_id,
                    task_queue="deployment-orchestrator-task-queue",
                )
            )

            return {
                "execution_id": handle.id,
                "status": "running"
            }
        except Exception as e:
            return {
                "error": {
                    "code": "E_RUNTIME",
                    "message": f"Workflow execution failed: {str(e)}"
                }
            }
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {"verb": "workflow.execute@v1", "agent": "deployment-orchestrator"})
    request_duration.record(duration, {"verb": "workflow.execute@v1"})

def handle_deployment_status_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for deployment.status@v1

    Parameters:
        - deployment_id (string)

    Returns:
        - status (string)
        - current_step (string)
        - progress (int)
    """
    if "deployment_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: deployment_id"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("deployment.status@v1") as span:
        span.set_attribute("verb", "deployment.status@v1")
        span.set_attribute("agent", "deployment-orchestrator")
        # Generic AI handler
        try:
            user_prompt = f"Process the following request for deployment.status@v1:\n"
            user_prompt += f"Parameters: {params.get('deployment_id')}"

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
    request_counter.add(1, {"verb": "deployment.status@v1", "agent": "deployment-orchestrator"})
    request_duration.record(duration, {"verb": "deployment.status@v1"})

def handle_deployment_approve_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for deployment.approve@v1

    Parameters:
        - deployment_id (string)
        - approved (bool)
        - approver (string)

    Returns:
        - status (string)
    """
    if "deployment_id" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: deployment_id"}}
    if "approved" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: approved"}}
    if "approver" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: approver"}}

    agent_state["requests_handled"] += 1
    start_time = time.time()
    with tracer.start_as_current_span("deployment.approve@v1") as span:
        span.set_attribute("verb", "deployment.approve@v1")
        span.set_attribute("agent", "deployment-orchestrator")
        # AI-powered handler using LangChain
        try:
            # Build prompt with parameters
            user_prompt = f"""
    Evaluate if this deployment should be approved based on:
    - Code review results
    - Test coverage and results
    - Staging environment health
    - Risk assessment
    Provide recommendation: approve/reject with reasoning.

    Input parameters:
        deployment_id: {params["deployment_id"]}
        approved: {params["approved"]}
        approver: {params["approver"]}
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
                "status": result_text
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
    request_counter.add(1, {"verb": "deployment.approve@v1", "agent": "deployment-orchestrator"})
    request_duration.record(duration, {"verb": "deployment.approve@v1"})

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
        if method == "workflow.execute@v1":
            result = handle_workflow_execute_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "deployment.status@v1":
            result = handle_deployment_status_v1(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }
                )
        elif method == "deployment.approve@v1":
            result = handle_deployment_approve_v1(params)
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
        "agent": "deployment-orchestrator",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "deployment-orchestrator",
        "verbs": ['"workflow.execute@v1"', '"deployment.status@v1"', '"deployment.approve@v1"']
    }

if __name__ == "__main__":
    print(f"Starting MCP server for agent: deployment-orchestrator")
    print(f"Port: 23452")
    print(f"Exposed verbs: ['workflow.execute@v1', 'deployment.status@v1', 'deployment.approve@v1']")
    print(f"Health check: http://127.0.0.1:23452/health")
    print(f"MCP endpoint: http://127.0.0.1:23452/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23452,
        log_level="info"
    )