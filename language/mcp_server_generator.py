"""
MCP Server Generator for Promptware agents.

Generates FastAPI-based MCP servers from .pw agent definitions.
"""

from __future__ import annotations

from typing import Any, Dict, List
from language.agent_parser import AgentDefinition, ExposeBlock, ObservabilityConfig, WorkflowDefinition, WorkflowStep


def generate_python_mcp_server(agent: AgentDefinition) -> str:
    """
    Generate a complete Python MCP server from agent definition.

    Returns FastAPI application code that:
    - Runs on the specified port
    - Exposes MCP verbs as HTTP endpoints
    - Handles JSON-RPC requests
    - Returns MCP-formatted responses
    """

    code_parts = []

    # Imports
    code_parts.append(_generate_imports(agent))

    # Temporal workflows and activities (if enabled)
    if agent.temporal and agent.workflows:
        code_parts.append(_generate_temporal_workflows(agent))

    # FastAPI app initialization
    code_parts.append(_generate_app_init(agent))

    # Handler functions for each exposed verb
    for expose in agent.exposes:
        code_parts.append(_generate_verb_handler(expose, agent))

    # Main MCP endpoint
    code_parts.append(_generate_mcp_endpoint(agent))

    # Server startup
    code_parts.append(_generate_server_startup(agent))

    return "\n\n".join(code_parts)


def _generate_imports(agent: AgentDefinition) -> str:
    """Generate import statements."""
    base_imports = """from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Any, Dict, Optional
from datetime import datetime
import time"""

    # Add LangChain imports if agent uses LLM
    if agent.llm:
        langchain_imports = """
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser"""
        base_imports += langchain_imports

    # Add OpenTelemetry imports if observability enabled
    if agent.observability and (agent.observability.traces or agent.observability.metrics):
        otel_imports = """
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource"""
        base_imports += otel_imports

    # Add Temporal imports if workflows enabled
    if agent.temporal and agent.workflows:
        temporal_imports = """
import asyncio
from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker"""
        base_imports += temporal_imports

    return base_imports


def _generate_app_init(agent: AgentDefinition) -> str:
    """Generate FastAPI app initialization."""

    # OpenTelemetry setup if observability enabled
    otel_setup = ""
    if agent.observability and (agent.observability.traces or agent.observability.metrics):
        otel_setup = f'''
# OpenTelemetry setup
resource = Resource.create({{"service.name": "{agent.name}"}})
'''

        if agent.observability.traces:
            otel_setup += '''
# Trace provider
trace_provider = TracerProvider(resource=resource)
trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace_provider.add_span_processor(trace_processor)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)
'''

        if agent.observability.metrics:
            otel_setup += '''
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
'''

    init_code = otel_setup + f'''
# MCP Server for agent: {agent.name}
app = FastAPI(
    title="{agent.name}",
    description="Promptware MCP Agent",
    version="v1"
)'''

    # Auto-instrument FastAPI if observability enabled
    if agent.observability and agent.observability.traces:
        init_code += '''

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)'''

    init_code += f'''

# Agent state (in-memory for demo)
agent_state: Dict[str, Any] = {{
    "agent_name": "{agent.name}",
    "started_at": datetime.now().isoformat(),
    "requests_handled": 0
}}'''

    # Add Temporal client initialization if workflows enabled
    if agent.temporal and agent.workflows:
        init_code += '''

# Temporal client (global)
temporal_client: Optional[Client] = None

async def get_temporal_client() -> Client:
    """Get or create Temporal client."""
    global temporal_client
    if temporal_client is None:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client'''

    # Add LLM initialization if agent uses LLM
    if agent.llm:
        # Parse LLM spec (e.g., "anthropic claude-3-5-sonnet-20241022")
        llm_parts = agent.llm.split()
        provider = llm_parts[0] if llm_parts else "anthropic"
        model_name = " ".join(llm_parts[1:]) if len(llm_parts) > 1 else "claude-3-5-sonnet-20241022"

        llm_init = f'''

# LLM initialization ({agent.llm})
llm = ChatAnthropic(
    model="{model_name}",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    temperature=0,
)'''

        # Add global prompt if specified
        if agent.prompt_template:
            llm_init += f'''

# Global agent prompt
AGENT_SYSTEM_PROMPT = """{agent.prompt_template}"""'''

        init_code += llm_init

    return init_code


def _generate_verb_handler(expose: ExposeBlock, agent: AgentDefinition) -> str:
    """Generate handler function for an exposed MCP verb."""

    # Parse verb name (e.g., "task.execute@v1" -> "task_execute_v1")
    handler_name = expose.verb.replace(".", "_").replace("@", "_")

    # Build parameter validation
    param_names = [p["name"] for p in expose.params]
    param_checks = []
    for param in expose.params:
        param_checks.append(f'''    if "{param["name"]}" not in params:
        return {{"error": {{"code": "E_ARGS", "message": "Missing required parameter: {param["name"]}"}}}}''')

    param_validation = "\n".join(param_checks) if param_checks else "    # No required parameters"

    # Add tracing and metrics if observability enabled
    observability_setup = ""
    observability_record = ""
    has_tracing = agent.observability and agent.observability.traces

    if agent.observability:
        if agent.observability.metrics:
            observability_setup = '''    start_time = time.time()
'''
            observability_record = f'''
    # Record metrics
    duration = time.time() - start_time
    request_counter.add(1, {{"verb": "{expose.verb}", "agent": "{agent.name}"}})
    request_duration.record(duration, {{"verb": "{expose.verb}"}})'''

    # Generate handler body based on type
    if agent.temporal and expose.verb == "workflow.execute@v1":
        # Special handler for workflow execution
        handler_body = _generate_workflow_execution_handler(agent)
    elif agent.llm and expose.prompt_template:
        # AI-powered handler using LangChain
        handler_body = _generate_ai_handler_body(expose, agent, param_names)
    elif agent.llm:
        # LLM available but no specific prompt - generic implementation
        handler_body = _generate_generic_ai_handler_body(expose, agent, param_names)
    else:
        # Non-AI handler - mock implementation
        handler_body = _generate_mock_handler_body(expose)

    # Wrap handler body with tracing span if enabled
    if has_tracing:
        # Indent handler body for span context
        lines = handler_body.split("\n")
        indented_lines = []
        for line in lines:
            if line.strip():
                indented_lines.append("    " + line)
            else:
                indented_lines.append(line)
        indented_body = "\n".join(indented_lines)

        handler_body = f'''    with tracer.start_as_current_span("{expose.verb}") as span:
        span.set_attribute("verb", "{expose.verb}")
        span.set_attribute("agent", "{agent.name}")
{indented_body}'''

    return f'''def handle_{handler_name}(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for {expose.verb}

    Parameters:
{_format_params_doc(expose.params)}

    Returns:
{_format_returns_doc(expose.returns)}
    """
{param_validation}

    agent_state["requests_handled"] += 1
{observability_setup}{handler_body}{observability_record}'''


def _generate_workflow_execution_handler(agent: AgentDefinition) -> str:
    """Generate handler for workflow.execute@v1 verb."""
    if not agent.workflows:
        return _generate_mock_handler_body(ExposeBlock(verb="workflow.execute@v1"))

    workflow_def = agent.workflows[0]
    workflow_class_name = workflow_def.name.replace("@", "_").replace(".", "_").title() + "Workflow"

    return f'''    # Execute Temporal workflow
    try:
        workflow_id = params.get("workflow_id")
        workflow_params = params.get("params", {{}})

        # Get Temporal client
        client = asyncio.run(get_temporal_client())

        # Start workflow execution
        handle = asyncio.run(
            client.start_workflow(
                {workflow_class_name}.run,
                **workflow_params,
                id=workflow_id,
                task_queue="{agent.name}-task-queue",
            )
        )

        return {{
            "execution_id": handle.id,
            "status": "running"
        }}
    except Exception as e:
        return {{
            "error": {{
                "code": "E_RUNTIME",
                "message": f"Workflow execution failed: {{str(e)}}"
            }}
        }}'''


def _generate_mock_handler_body(expose: ExposeBlock) -> str:
    """Generate mock implementation for non-AI handlers."""
    return_fields = {}
    for ret in expose.returns:
        if ret["type"] == "string":
            return_fields[ret["name"]] = f'"{ret["name"]}_value"'
        elif ret["type"] == "int":
            return_fields[ret["name"]] = "0"
        elif ret["type"] == "bool":
            return_fields[ret["name"]] = "True"
        elif ret["type"] == "object":
            return_fields[ret["name"]] = "{}"
        elif ret["type"] == "array":
            return_fields[ret["name"]] = "[]"
        else:
            return_fields[ret["name"]] = "None"

    return_dict = ",\n        ".join([f'"{k}": {v}' for k, v in return_fields.items()])

    return f'''    # TODO: Implement actual handler logic
    # For now, return mock data
    return {{
        {return_dict}
    }}'''


def _generate_ai_handler_body(expose: ExposeBlock, agent: AgentDefinition, param_names: List[str]) -> str:
    """Generate AI-powered handler using LangChain with specific prompt."""
    # Build prompt with parameters
    param_refs = ", ".join([f"{{params['{p}']}}" for p in param_names])

    # Format parameters for prompt
    param_placeholders = "\n    ".join([f'{p}: {{params["{p}"]}}' for p in param_names])

    return f'''    # AI-powered handler using LangChain
    try:
        # Build prompt with parameters
        user_prompt = f"""
{expose.prompt_template}

Input parameters:
    {param_placeholders}
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
        return {{
            "{expose.returns[0]["name"] if expose.returns else "result"}": result_text
        }}

    except Exception as e:
        return {{
            "error": {{
                "code": "E_RUNTIME",
                "message": f"LLM call failed: {{str(e)}}"
            }}
        }}'''


def _generate_generic_ai_handler_body(expose: ExposeBlock, agent: AgentDefinition, param_names: List[str]) -> str:
    """Generate generic AI handler when LLM is available but no specific prompt."""
    param_str = ", ".join([f"{{params.get('{p}')}}" for p in param_names])

    return f'''    # Generic AI handler
    try:
        user_prompt = f"Process the following request for {expose.verb}:\\n"
        user_prompt += f"Parameters: {param_str}"

        messages = [HumanMessage(content=user_prompt)]
        response = llm.invoke(messages)

        return {{
            "{expose.returns[0]["name"] if expose.returns else "result"}": response.content
        }}
    except Exception as e:
        return {{
            "error": {{
                "code": "E_RUNTIME",
                "message": f"LLM call failed: {{str(e)}}"
            }}
        }}'''


def _format_params_doc(params: List[Dict[str, str]]) -> str:
    """Format parameters for docstring."""
    if not params:
        return "        None"
    return "\n".join([f'        - {p["name"]} ({p["type"]})' for p in params])


def _format_returns_doc(returns: List[Dict[str, str]]) -> str:
    """Format returns for docstring."""
    if not returns:
        return "        None"
    return "\n".join([f'        - {r["name"]} ({r["type"]})' for r in returns])


def _generate_mcp_endpoint(agent: AgentDefinition) -> str:
    """Generate main MCP JSON-RPC endpoint."""

    # Build verb routing
    verb_routes = []
    for i, expose in enumerate(agent.exposes):
        handler_name = expose.verb.replace(".", "_").replace("@", "_")
        prefix = "if" if i == 0 else "elif"
        verb_routes.append(f'''        {prefix} method == "{expose.verb}":
            result = handle_{handler_name}(params)
            if "error" in result:
                return JSONResponse(
                    status_code=400,
                    content={{
                        "ok": False,
                        "version": "v1",
                        "error": result["error"]
                    }}
                )''')

    verb_routing = "\n".join(verb_routes)

    return f'''@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Main MCP endpoint - handles JSON-RPC requests.

    Request format:
    {{
        "method": "verb.name@v1",
        "params": {{...}}
    }}

    Response format:
    {{
        "ok": true,
        "version": "v1",
        "data": {{...}}
    }}
    """
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {{}})

        if not method:
            return JSONResponse(
                status_code=400,
                content={{
                    "ok": False,
                    "version": "v1",
                    "error": {{
                        "code": "E_ARGS",
                        "message": "Missing 'method' in request"
                    }}
                }}
            )

        # Route to appropriate handler
{verb_routing}
        else:
            return JSONResponse(
                status_code=404,
                content={{
                    "ok": False,
                    "version": "v1",
                    "error": {{
                        "code": "E_METHOD",
                        "message": f"Unknown method: {{method}}"
                    }}
                }}
            )

        # Success response
        return JSONResponse(
            content={{
                "ok": True,
                "version": "v1",
                "data": result
            }}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={{
                "ok": False,
                "version": "v1",
                "error": {{
                    "code": "E_RUNTIME",
                    "message": str(e)
                }}
            }}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {{
        "status": "healthy",
        "agent": "{agent.name}",
        "uptime": agent_state.get("requests_handled", 0)
    }}


@app.get("/verbs")
async def list_verbs():
    """List all exposed MCP verbs."""
    return {{
        "agent": "{agent.name}",
        "verbs": {[f'"{e.verb}"' for e in agent.exposes]}
    }}'''


def _generate_temporal_workflows(agent: AgentDefinition) -> str:
    """Generate Temporal workflow and activity classes."""
    code_parts = []

    for workflow_def in agent.workflows:
        # Generate activity functions for each step
        for step in workflow_def.steps:
            code_parts.append(_generate_activity_function(step, workflow_def))

        # Generate workflow class
        code_parts.append(_generate_workflow_class(workflow_def, agent))

    return "\n\n".join(code_parts)


def _generate_activity_function(step: WorkflowStep, workflow_def: WorkflowDefinition) -> str:
    """Generate a Temporal activity function."""
    activity_name = step.activity

    # Parse timeout (e.g., "10m" -> timedelta(minutes=10))
    timeout_code = ""
    if step.timeout:
        timeout_code = f", start_to_close_timeout=timedelta({_parse_timeout(step.timeout)})"

    return f'''@activity.defn(name="{activity_name}"{timeout_code})
async def {activity_name}(**kwargs) -> Dict[str, Any]:
    """
    Activity: {activity_name}
    Workflow: {workflow_def.name}
    """
    # TODO: Implement actual activity logic
    print(f"Executing activity: {activity_name}")
    return {{"status": "completed"}}'''


def _generate_workflow_class(workflow_def: WorkflowDefinition, agent: AgentDefinition) -> str:
    """Generate a Temporal workflow class."""
    workflow_name = workflow_def.name.replace("@", "_").replace(".", "_")

    # Build workflow steps execution
    steps_code = []
    for i, step in enumerate(workflow_def.steps):
        activity_name = step.activity

        # Build retry policy
        retry_policy = ""
        if step.retry > 0:
            retry_policy = f", retry_policy=workflow.RetryPolicy(maximum_attempts={step.retry})"

        # Build activity execution
        step_code = f'''        # Step {i+1}: {activity_name}
        result_{i} = await workflow.execute_activity(
            {activity_name},
            schedule_to_close_timeout=timedelta(minutes=10){retry_policy}
        )'''

        # Add compensation logic if on_failure is specified
        if step.on_failure:
            step_code += f'''
        if result_{i}.get("status") != "completed":
            # Compensation: {step.on_failure}
            await workflow.execute_activity(
                {step.on_failure},
                schedule_to_close_timeout=timedelta(minutes=5)
            )
            raise workflow.ApplicationError("Step {activity_name} failed")'''

        # Add approval wait if required
        if step.requires_approval:
            step_code += f'''

        # Wait for approval before continuing
        await workflow.wait_condition(lambda: workflow_state.get("approved_{i}", False))'''

        steps_code.append(step_code)

    steps_execution = "\n\n".join(steps_code)

    # Build params and returns
    param_types = ", ".join([f"{p['name']}: {_map_pw_type_to_python(p['type'])}" for p in workflow_def.params])
    return_type = "Dict[str, Any]"

    return f'''@workflow.defn(name="{workflow_def.name}")
class {workflow_name.title()}Workflow:
    """
    Temporal workflow: {workflow_def.name}

    Parameters: {", ".join([p["name"] for p in workflow_def.params])}
    Returns: {", ".join([r["name"] for r in workflow_def.returns])}
    """

    def __init__(self):
        self.workflow_state = {{}}

    @workflow.run
    async def run(self, {param_types}) -> {return_type}:
        """Execute workflow steps."""
{steps_execution}

        # Return workflow result
        return {{
            {", ".join([f'"{r["name"]}": "value"' for r in workflow_def.returns])}
        }}'''


def _parse_timeout(timeout_str: str) -> str:
    """Parse timeout string (e.g., '10m', '5s') to timedelta args."""
    if timeout_str.endswith('m'):
        return f"minutes={timeout_str[:-1]}"
    elif timeout_str.endswith('s'):
        return f"seconds={timeout_str[:-1]}"
    elif timeout_str.endswith('h'):
        return f"hours={timeout_str[:-1]}"
    else:
        return f"seconds={timeout_str}"


def _map_pw_type_to_python(pw_type: str) -> str:
    """Map .pw types to Python type hints."""
    type_map = {
        "string": "str",
        "int": "int",
        "bool": "bool",
        "object": "Dict[str, Any]",
        "array": "List[Any]"
    }
    return type_map.get(pw_type, "Any")


def _generate_server_startup(agent: AgentDefinition) -> str:
    """Generate server startup code."""
    return f'''if __name__ == "__main__":
    print(f"Starting MCP server for agent: {agent.name}")
    print(f"Port: {agent.port}")
    print(f"Exposed verbs: {[e.verb for e in agent.exposes]}")
    print(f"Health check: http://127.0.0.1:{agent.port}/health")
    print(f"MCP endpoint: http://127.0.0.1:{agent.port}/mcp")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port={agent.port},
        log_level="info"
    )'''


def generate_mcp_server_from_pw(pw_code: str) -> str:
    """
    Convenience function: parse .pw code and generate MCP server.

    Args:
        pw_code: .pw file content

    Returns:
        Python code for MCP server
    """
    from language.agent_parser import parse_agent_pw

    agent = parse_agent_pw(pw_code)
    return generate_python_mcp_server(agent)