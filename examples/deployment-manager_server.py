import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from temporalio import activity, workflow
from temporalio.client import Client


@activity.defn(name="build_image", start_to_close_timeout=timedelta(minutes=10))
async def build_image(**kwargs) -> Dict[str, Any]:
    """
    Activity: build_image
    Workflow: deploy_service@v1
    """
    # TODO: Implement actual activity logic
    print("Executing activity: build_image")
    return {"status": "completed"}

@activity.defn(name="run_tests", start_to_close_timeout=timedelta(minutes=5))
async def run_tests(**kwargs) -> Dict[str, Any]:
    """
    Activity: run_tests
    Workflow: deploy_service@v1
    """
    # TODO: Implement actual activity logic
    print("Executing activity: run_tests")
    return {"status": "completed"}

@activity.defn(name="deploy_to_staging", start_to_close_timeout=timedelta(minutes=3))
async def deploy_to_staging(**kwargs) -> Dict[str, Any]:
    """
    Activity: deploy_to_staging
    Workflow: deploy_service@v1
    """
    # TODO: Implement actual activity logic
    print("Executing activity: deploy_to_staging")
    return {"status": "completed"}

@activity.defn(name="health_check", start_to_close_timeout=timedelta(minutes=2))
async def health_check(**kwargs) -> Dict[str, Any]:
    """
    Activity: health_check
    Workflow: deploy_service@v1
    """
    # TODO: Implement actual activity logic
    print("Executing activity: health_check")
    return {"status": "completed"}

@activity.defn(name="deploy_to_production", start_to_close_timeout=timedelta(minutes=5))
async def deploy_to_production(**kwargs) -> Dict[str, Any]:
    """
    Activity: deploy_to_production
    Workflow: deploy_service@v1
    """
    # TODO: Implement actual activity logic
    print("Executing activity: deploy_to_production")
    return {"status": "completed"}

@workflow.defn(name="deploy_service@v1")
class Deploy_Service_V1Workflow:
    """
    Temporal workflow: deploy_service@v1

    Parameters: service, version
    Returns: deployment_id, status
    """

    def __init__(self):
        self.workflow_state = {}

    @workflow.run
    async def run(self, service: str, version: str) -> Dict[str, Any]:
        """Execute workflow steps."""
        # Step 1: build_image
        await workflow.execute_activity(
            build_image,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=3)
        )

        # Step 2: run_tests
        await workflow.execute_activity(
            run_tests,
            schedule_to_close_timeout=timedelta(minutes=10), retry_policy=workflow.RetryPolicy(maximum_attempts=2)
        )

        # Step 3: deploy_to_staging
        result_2 = await workflow.execute_activity(
            deploy_to_staging,
            schedule_to_close_timeout=timedelta(minutes=10)
        )
        if result_2.get("status") != "completed":
            # Compensation: rollback_staging
            await workflow.execute_activity(
                rollback_staging,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step deploy_to_staging failed")

        # Step 4: health_check
        await workflow.execute_activity(
            health_check,
            schedule_to_close_timeout=timedelta(minutes=10)
        )

        # Step 5: deploy_to_production
        result_4 = await workflow.execute_activity(
            deploy_to_production,
            schedule_to_close_timeout=timedelta(minutes=10)
        )
        if result_4.get("status") != "completed":
            # Compensation: rollback_production
            await workflow.execute_activity(
                rollback_production,
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step deploy_to_production failed")

        # Wait for approval before continuing
        await workflow.wait_condition(lambda: workflow_state.get("approved_4", False))

        # Return workflow result
        return {
            "deployment_id": "value", "status": "value"
        }


# MCP Server for agent: deployment-manager
app = FastAPI(
    title="deployment-manager",
    description="AssertLang MCP Agent",
    version="v1"
)

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {
    "agent_name": "deployment-manager",
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
    # Execute Temporal workflow
    try:
        workflow_id = params.get("workflow_id")
        workflow_params = params.get("params", {})

        # Get Temporal client
        client = asyncio.run(get_temporal_client())

        # Start workflow execution
        handle = asyncio.run(
            client.start_workflow(
                Deploy_Service_V1Workflow.run,
                **workflow_params,
                id=workflow_id,
                task_queue="deployment-manager-task-queue",
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
        "agent": "deployment-manager",
        "uptime": agent_state.get("requests_handled", 0)
    }


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {
        "agent": "deployment-manager",
        "verbs": ['"workflow.execute@v1"']
    }

if __name__ == "__main__":
    print("Starting MCP server for agent: deployment-manager")
    print("Port: 23456")
    print("Exposed verbs: ['workflow.execute@v1']")
    print("Health check: http://127.0.0.1:23456/health")
    print("MCP endpoint: http://127.0.0.1:23456/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=23456,
        log_level="info"
    )