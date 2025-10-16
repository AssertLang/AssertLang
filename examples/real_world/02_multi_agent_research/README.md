# Multi-Agent Research Pipeline with Contract Validation

**Real-world example demonstrating contract-based coordination for multi-agent systems (CrewAI/LangGraph integration).**

## Quickstart (5 minutes)

```bash
# 1. Generate Python code from contracts
asl build pipeline.al --lang python -o pipeline.py

# 2. Run comprehensive test suite (39 tests)
python3 -m pytest test_pipeline.py -v

# 3. Integrate with your CrewAI/LangGraph workflow
from pipeline import (
    validate_research_query,
    validate_research_results,
    can_agent_proceed,
    validate_pipeline_stage
)

# Validate inputs before agent execution
validate_research_query("AI trends 2025", max_results=20, min_quality_score=0.7)

# Check agent coordination
if can_agent_proceed("analyzer", research_complete=True, has_input=True):
    # Run analyzer agent
    pass
```

**Result**: Runtime-validated multi-agent coordination with clear error messages when agents violate contracts.

---

## What This Example Demonstrates

### 1. **Multi-Agent Coordination**
- **Agent sequencing** - Enforce execution order (research → analysis → writing)
- **Dependency checking** - Verify prerequisites before agent execution
- **Quality gates** - Block low-quality work from propagating

### 2. **Input Validation Patterns**
- **Research queries** - Non-empty queries, reasonable result limits, valid quality scores
- **Analysis inputs** - Require data to analyze, valid depth parameters
- **Report inputs** - Validate analysis exists, reasonable length limits

### 3. **Output Quality Checks**
- **Research results** - Must have sources, minimum quality threshold, non-zero results
- **Analysis outputs** - Require insights with evidence, minimum confidence levels
- **Final reports** - Enforce structure (sections), content (length), citations

### 4. **Pipeline State Management**
- **Stage validation** - Enforce workflow stages execute in correct order
- **Completion tracking** - Check all required stages complete
- **Task assignment** - Validate agent roles match task types

---

## Real-World Applications

### CrewAI Integration
```python
from crewai import Agent, Task, Crew
from pipeline import validate_research_query, validate_research_results

# Define researcher agent with contract validation
researcher = Agent(
    role="researcher",
    goal="Find high-quality sources",
    backstory="Expert researcher with validation",
    tools=[web_search_tool]
)

# Task with pre/post validation
research_task = Task(
    description="Research AI trends",
    agent=researcher,
    callback=lambda output: validate_research_results(
        results_count=len(output.sources),
        quality_score=output.quality,
        has_sources=bool(output.sources)
    )
)

# Validate query before execution
query = "Latest AI research 2025"
validate_research_query(query, max_results=20, min_quality_score=0.7)

crew = Crew(agents=[researcher], tasks=[research_task])
result = crew.kickoff()  # Contracts enforced at runtime
```

### LangGraph Workflow
```python
from langgraph.graph import StateGraph
from pipeline import validate_pipeline_stage, can_agent_proceed

# Define workflow state
class WorkflowState(TypedDict):
    research_complete: bool
    analysis_complete: bool
    writing_complete: bool
    current_stage: str

# Build graph with contract validation
workflow = StateGraph(WorkflowState)

def research_node(state):
    # Always valid to start research
    if validate_pipeline_stage("research", False, False):
        # Execute research
        return {"research_complete": True, "current_stage": "analysis"}
    raise ValueError("Invalid pipeline state")

def analysis_node(state):
    # Requires research complete
    if not validate_pipeline_stage("analysis", state["research_complete"], False):
        raise ValueError("Cannot run analysis - research not complete")

    # Check agent can proceed
    if not can_agent_proceed("analyzer", state["research_complete"], True):
        raise ValueError("Analyzer blocked - missing prerequisites")

    # Execute analysis
    return {"analysis_complete": True, "current_stage": "writing"}

workflow.add_node("research", research_node)
workflow.add_node("analysis", analysis_node)
workflow.add_edge("research", "analysis")
```

### Autonomous Agent Systems
```python
from pipeline import (
    validate_task_assignment,
    meets_quality_threshold,
    is_pipeline_complete
)

class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "analyzer": AnalyzerAgent(),
            "writer": WriterAgent()
        }
        self.state = {
            "research_done": False,
            "analysis_done": False,
            "writing_done": False
        }

    def assign_task(self, agent_role, task_type):
        """Assign task with contract validation."""
        agent = self.agents[agent_role]

        # Validate agent has required tools
        has_tools = agent.has_tools_for(task_type)

        # Contract enforces role-task compatibility
        if not validate_task_assignment(agent_role, task_type, has_tools):
            raise ValueError(
                f"Invalid assignment: {agent_role} cannot do {task_type}"
            )

        return agent.execute(task_type)

    def check_quality(self, score, threshold):
        """Quality gate for agent outputs."""
        if not meets_quality_threshold(score, threshold):
            raise ValueError(
                f"Quality {score} below threshold {threshold} - retry required"
            )

    def is_complete(self):
        """Check if entire pipeline finished."""
        return is_pipeline_complete(
            self.state["research_done"],
            self.state["analysis_done"],
            self.state["writing_done"]
        )
```

---

## The Problem We're Solving

### Without Contracts

```python
# ❌ Agent proceeds without checking prerequisites
def run_analysis(research_data):
    # What if research_data is empty?
    # What if research_data has no sources?
    # What if quality is too low?
    insights = analyze(research_data)
    return insights

# ❌ Pipeline executes stages out of order
workflow = {
    "stages": ["research", "analysis", "writing"],
    "current": "writing"  # Skipped research and analysis!
}

# ❌ Agent assigned incompatible task
researcher_agent.execute("writing")  # Researcher doing writing?

# ❌ Low-quality work propagates
results = {
    "quality_score": 0.1,  # Very low quality
    "sources": []  # No sources
}
# But analysis proceeds anyway, producing garbage output
```

**Problems**:
1. **Agents execute with invalid inputs** - No data validation before execution
2. **Pipeline stages execute out of order** - Writing before research complete
3. **Role-task mismatches** - Wrong agent for the job
4. **Quality issues propagate** - Low-quality work flows downstream
5. **Silent failures** - Errors discovered late in workflow
6. **No coordination guarantees** - Agents don't check prerequisites

### With Contracts

```python
# ✅ Inputs validated before agent execution
validate_analysis_input(
    research_data_size=len(research_data),
    analysis_depth="deep"
)  # Raises ContractViolationError if research_data empty

# ✅ Pipeline stages enforced
validate_pipeline_stage(
    current_stage="writing",
    research_complete=False,  # ❌ Returns False
    analysis_complete=False
)  # Writing cannot proceed without research + analysis

# ✅ Role-task compatibility checked
validate_task_assignment(
    agent_role="researcher",
    task_type="writing",  # ❌ Returns False
    has_required_tools=True
)  # Researcher cannot do writing tasks

# ✅ Quality gates block low-quality work
validate_research_results(
    results_count=5,
    quality_score=0.1,  # ❌ Below 0.3 threshold
    has_sources=True
)  # Returns False - quality too low
```

**Benefits**:
1. **Early error detection** - Invalid inputs caught immediately
2. **Enforced execution order** - Pipeline stages execute correctly
3. **Clear error messages** - Know exactly what went wrong
4. **Guaranteed coordination** - Agents check prerequisites
5. **Quality enforcement** - Low-quality work blocked early
6. **Runtime validation** - Contracts checked during execution

---

## How Contracts Help

### 1. Agent Input Validation

**Before**: Agent executes with bad inputs, fails deep in execution
```python
def research_agent(query, max_results):
    results = web_search(query)  # Fails if query empty
    return results[:max_results]  # Fails if max_results negative
```

**After**: Contracts catch bad inputs immediately
```python
function validate_research_query(
    query: string,
    max_results: int,
    min_quality_score: float
) -> bool {
    @requires non_empty_query: len(query) > 0
    @requires positive_max_results: max_results > 0 && max_results <= 100
    @requires valid_quality_score: min_quality_score >= 0.0 && min_quality_score <= 1.0

    @ensures query_valid: result == true

    return true;
}
```

**Error Message**:
```
ContractViolationError: Precondition 'non_empty_query' violated in validate_research_query
Condition: len(query) > 0
Context: {'query': '', 'max_results': 20, 'min_quality_score': 0.7}
```

### 2. Agent Coordination

**Before**: Analyzer runs before researcher completes
```python
# ❌ No checks
research_complete = False
run_analyzer()  # Executes with no data!
```

**After**: Contracts enforce execution order
```python
function can_agent_proceed(
    agent_name: string,
    previous_agent_completed: bool,
    has_required_input: bool
) -> bool {
    @requires valid_agent_name: len(agent_name) > 0

    @ensures decision_made: result == true || result == false

    if (previous_agent_completed == false) {
        return false;  // Block execution
    }

    if (has_required_input == false) {
        return false;  // Block execution
    }

    return true;
}
```

### 3. Pipeline Stage Validation

**Before**: Stages execute in wrong order
```python
# ❌ Skip research, go straight to writing
current_stage = "writing"
execute_stage(current_stage)
```

**After**: Contracts enforce stage ordering
```python
function validate_pipeline_stage(
    current_stage: string,
    research_complete: bool,
    analysis_complete: bool
) -> bool {
    @requires valid_stage: len(current_stage) > 0

    @ensures stage_valid: result == true || result == false

    // Stage order: research -> analysis -> writing

    if (current_stage == "research") {
        return true;  // Always valid to start
    }

    if (current_stage == "analysis") {
        return research_complete;  // Requires research
    }

    if (current_stage == "writing") {
        if (research_complete == true && analysis_complete == true) {
            return true;  // Requires both
        }
        return false;
    }

    return false;
}
```

### 4. Quality Gates

**Before**: Low-quality work propagates
```python
# ❌ No quality checks
results = {"quality_score": 0.1, "sources": []}
send_to_analyzer(results)  # Garbage in, garbage out
```

**After**: Contracts block low-quality work
```python
function validate_research_results(
    results_count: int,
    quality_score: float,
    has_sources: bool
) -> bool {
    @requires non_negative_count: results_count >= 0
    @requires valid_score: quality_score >= 0.0 && quality_score <= 1.0

    @ensures validation_complete: result == true || result == false

    if (results_count == 0) {
        return false;  // Must have results
    }

    if (has_sources == false) {
        return false;  // Must cite sources
    }

    if (quality_score < 0.3) {
        return false;  // Quality threshold
    }

    return true;
}
```

---

## Code Walkthrough

### Research Agent Validation

```al
// Validate research query inputs
function validate_research_query(
    query: string,
    max_results: int,
    min_quality_score: float
) -> bool {
    @requires non_empty_query: len(query) > 0
    @requires positive_max_results: max_results > 0 && max_results <= 100
    @requires valid_quality_score: min_quality_score >= 0.0 && min_quality_score <= 1.0

    @ensures query_valid: result == true

    return true;
}

// Validate research results from researcher agent
function validate_research_results(
    results_count: int,
    quality_score: float,
    has_sources: bool
) -> bool {
    @requires non_negative_count: results_count >= 0
    @requires valid_score: quality_score >= 0.0 && quality_score <= 1.0

    @ensures validation_complete: result == true || result == false

    // Must have at least some results
    if (results_count == 0) {
        return false;
    }

    // Must have sources cited
    if (has_sources == false) {
        return false;
    }

    // Quality must meet minimum threshold
    if (quality_score < 0.3) {
        return false;
    }

    return true;
}
```

**What This Shows**:
- **Input validation** - `@requires` clauses check query parameters
- **Output quality gates** - Business logic enforces quality standards
- **Clear thresholds** - Minimum quality of 0.3, max results of 100
- **Source citation** - Must have sources to proceed

**Generated Python**:
```python
def validate_research_query(query: str, max_results: int, min_quality_score: float) -> bool:
    check_precondition(
        (len(query) > 0),
        "non_empty_query",
        "len(query) > 0",
        "validate_research_query",
        context={"query": query, "max_results": max_results, "min_quality_score": min_quality_score}
    )
    check_precondition(
        ((max_results > 0) and (max_results <= 100)),
        "positive_max_results",
        "max_results > 0 and max_results <= 100",
        "validate_research_query",
        context={"query": query, "max_results": max_results, "min_quality_score": min_quality_score}
    )
    # ... more preconditions ...

    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
            (__result == True),
            "query_valid",
            "result == True",
            "validate_research_query",
            context=dict([("result", __result), ...])
        )
    return __result
```

### Analyzer Agent Validation

```al
// Validate analysis input
function validate_analysis_input(
    research_data_size: int,
    analysis_depth: string
) -> bool {
    @requires has_data: research_data_size > 0
    @requires valid_depth: len(analysis_depth) > 0

    @ensures input_valid: result == true

    return true;
}

// Validate analysis output
function validate_analysis_output(
    insights_count: int,
    confidence_score: float,
    has_evidence: bool
) -> bool {
    @requires non_negative_insights: insights_count >= 0
    @requires valid_confidence: confidence_score >= 0.0 && confidence_score <= 1.0

    @ensures analysis_complete: result == true || result == false

    // Must have at least one insight
    if (insights_count == 0) {
        return false;
    }

    // Must have supporting evidence
    if (has_evidence == false) {
        return false;
    }

    // Confidence must be reasonable
    if (confidence_score < 0.4) {
        return false;
    }

    return true;
}
```

**What This Shows**:
- **Data requirements** - Must have research data to analyze
- **Quality thresholds** - Minimum confidence of 0.4
- **Evidence requirements** - Insights must have supporting evidence
- **Output validation** - At least one insight required

### Writer Agent Validation

```al
// Validate report generation input
function validate_report_input(
    analysis_size: int,
    target_length: int,
    format: string
) -> bool {
    @requires has_analysis: analysis_size > 0
    @requires positive_length: target_length > 0 && target_length <= 10000
    @requires valid_format: len(format) > 0

    @ensures report_input_valid: result == true

    return true;
}

// Validate final report output
function validate_final_report(
    report_length: int,
    section_count: int,
    has_citations: bool
) -> bool {
    @requires non_negative_length: report_length >= 0
    @requires non_negative_sections: section_count >= 0

    @ensures report_valid: result == true || result == false

    // Report must have content
    if (report_length < 100) {
        return false;
    }

    // Report must have structure
    if (section_count < 3) {
        return false;
    }

    // Report must cite sources
    if (has_citations == false) {
        return false;
    }

    return true;
}
```

**What This Shows**:
- **Length constraints** - Reports between 100 and 10,000 characters
- **Structural requirements** - At least 3 sections
- **Citation enforcement** - Must cite sources
- **Format validation** - Format string must be specified

### Agent Coordination

```al
// Check if agent can proceed (coordination)
function can_agent_proceed(
    agent_name: string,
    previous_agent_completed: bool,
    has_required_input: bool
) -> bool {
    @requires valid_agent_name: len(agent_name) > 0

    @ensures decision_made: result == true || result == false

    // Agent can only proceed if previous agent completed
    if (previous_agent_completed == false) {
        return false;
    }

    // Agent needs required input data
    if (has_required_input == false) {
        return false;
    }

    return true;
}
```

**What This Shows**:
- **Sequential execution** - Agent blocked until previous completes
- **Data dependency** - Agent blocked without required input
- **Clear coordination logic** - Both conditions must be true

### Pipeline Stage Validation

```al
// Validate pipeline execution order
function validate_pipeline_stage(
    current_stage: string,
    research_complete: bool,
    analysis_complete: bool
) -> bool {
    @requires valid_stage: len(current_stage) > 0

    @ensures stage_valid: result == true || result == false

    // Stage order: research -> analysis -> writing

    if (current_stage == "research") {
        return true;  // Always valid to start
    }

    if (current_stage == "analysis") {
        return research_complete;  // Requires research
    }

    if (current_stage == "writing") {
        if (research_complete == true && analysis_complete == true) {
            return true;  // Requires both
        }
        return false;
    }

    return false;
}
```

**What This Shows**:
- **Stage dependencies** - Analysis needs research, writing needs both
- **Explicit ordering** - research → analysis → writing
- **Early stage validation** - Can start research anytime

### Task Assignment Validation

```al
// Validate agent task assignment
function validate_task_assignment(
    agent_role: string,
    task_type: string,
    has_required_tools: bool
) -> bool {
    @requires valid_role: len(agent_role) > 0
    @requires valid_task: len(task_type) > 0

    @ensures assignment_valid: result == true || result == false

    // Agent must have required tools for task
    if (has_required_tools == false) {
        return false;
    }

    // Role-task compatibility checks
    if (agent_role == "researcher") {
        if (task_type == "research" || task_type == "search") {
            return true;
        }
        return false;
    }

    if (agent_role == "analyzer") {
        if (task_type == "analysis" || task_type == "synthesis") {
            return true;
        }
        return false;
    }

    if (agent_role == "writer") {
        if (task_type == "writing" || task_type == "reporting") {
            return true;
        }
        return false;
    }

    return false;
}
```

**What This Shows**:
- **Role-task compatibility** - Researchers do research, analyzers analyze, writers write
- **Tool requirements** - Agent must have required tools
- **Explicit role definitions** - Clear boundaries for each agent type

---

## Running the Tests

### Full Test Suite (39 tests)

```bash
python3 -m pytest test_pipeline.py -v
```

**Test Coverage**:
- ✅ Research query validation (4 tests)
- ✅ Research results validation (4 tests)
- ✅ Analysis input/output validation (6 tests)
- ✅ Report input/output validation (6 tests)
- ✅ Agent coordination (3 tests)
- ✅ Pipeline stage validation (6 tests)
- ✅ Quality thresholds (3 tests)
- ✅ Task assignment (7 tests)
- ✅ Pipeline completion (4 tests)
- ✅ End-to-end workflows (3 tests)

### Run Specific Test Categories

```bash
# Test research agent validation
pytest test_pipeline.py::TestResearchQueryValidation -v
pytest test_pipeline.py::TestResearchResultsValidation -v

# Test analyzer agent validation
pytest test_pipeline.py::TestAnalysisValidation -v

# Test writer agent validation
pytest test_pipeline.py::TestReportValidation -v

# Test agent coordination
pytest test_pipeline.py::TestAgentCoordination -v

# Test pipeline stage ordering
pytest test_pipeline.py::TestPipelineStageValidation -v

# Test quality gates
pytest test_pipeline.py::TestQualityThreshold -v

# Test task assignment
pytest test_pipeline.py::TestTaskAssignment -v

# Test end-to-end workflows
pytest test_pipeline.py::TestEndToEndWorkflow -v
```

### Example Test Output

```bash
$ pytest test_pipeline.py::TestEndToEndWorkflow::test_successful_pipeline -v

test_pipeline.py::TestEndToEndWorkflow::test_successful_pipeline PASSED

# Test validates complete workflow:
# 1. Research stage starts (always valid)
# 2. Research query validated
# 3. Research results validated
# 4. Analysis stage validated (requires research complete)
# 5. Analyzer can proceed (prerequisites met)
# 6. Analysis input validated
# 7. Analysis output validated
# 8. Writing stage validated (requires both complete)
# 9. Writer can proceed (prerequisites met)
# 10. Report input validated
# 11. Final report validated
# 12. Pipeline completion checked
```

---

## Common Pitfalls

### 1. Skipping Input Validation

**❌ Wrong**:
```python
def run_research(query, max_results):
    # Execute without validation
    return web_search(query, max_results)
```

**✅ Correct**:
```python
def run_research(query, max_results, min_quality):
    # Validate inputs first
    validate_research_query(query, max_results, min_quality)
    return web_search(query, max_results)
```

### 2. Ignoring Quality Gates

**❌ Wrong**:
```python
results = researcher.execute()
# Proceed regardless of quality
send_to_analyzer(results)
```

**✅ Correct**:
```python
results = researcher.execute()

# Check quality before proceeding
if not validate_research_results(
    len(results),
    results.quality_score,
    bool(results.sources)
):
    raise ValueError("Research quality too low - retry required")

send_to_analyzer(results)
```

### 3. Executing Stages Out of Order

**❌ Wrong**:
```python
# Skip research, go straight to analysis
run_analyzer()
```

**✅ Correct**:
```python
# Validate stage can execute
if not validate_pipeline_stage("analysis", research_complete=True, analysis_complete=False):
    raise ValueError("Cannot run analysis - research not complete")

run_analyzer()
```

### 4. Not Checking Agent Prerequisites

**❌ Wrong**:
```python
# Execute analyzer without checking
run_analyzer()
```

**✅ Correct**:
```python
# Check agent can proceed
if not can_agent_proceed("analyzer", previous_complete=True, has_input=True):
    raise ValueError("Analyzer blocked - missing prerequisites")

run_analyzer()
```

### 5. Assigning Wrong Tasks to Agents

**❌ Wrong**:
```python
# Researcher doing writing
researcher.execute("writing")
```

**✅ Correct**:
```python
# Validate task assignment
if not validate_task_assignment("researcher", "writing", has_tools=True):
    raise ValueError("Invalid assignment - researcher cannot do writing")

# Assign correct task
researcher.execute("research")
```

### 6. Missing Error Handling

**❌ Wrong**:
```python
# No try/except around validation
validate_research_query(query, max_results, min_quality)
```

**✅ Correct**:
```python
try:
    validate_research_query(query, max_results, min_quality)
except ContractViolationError as e:
    logger.error(f"Invalid research query: {e}")
    # Fix inputs or notify user
    raise
```

---

## Integration Patterns

### Pattern 1: CrewAI Task Callbacks

```python
from crewai import Agent, Task, Crew
from pipeline import validate_research_results

def research_callback(output):
    """Validate research output before passing to next agent."""
    is_valid = validate_research_results(
        results_count=len(output.results),
        quality_score=output.quality,
        has_sources=bool(output.sources)
    )

    if not is_valid:
        raise ValueError(
            f"Research quality {output.quality} below threshold 0.3"
        )

    return output

research_task = Task(
    description="Research AI trends",
    agent=researcher,
    callback=research_callback  # Validate before proceeding
)
```

### Pattern 2: LangGraph State Validation

```python
from langgraph.graph import StateGraph
from pipeline import validate_pipeline_stage, can_agent_proceed

def conditional_analysis(state):
    """Only run analysis if contracts allow."""
    # Check stage ordering
    if not validate_pipeline_stage(
        "analysis",
        state["research_complete"],
        state["analysis_complete"]
    ):
        return "error"

    # Check agent prerequisites
    if not can_agent_proceed(
        "analyzer",
        state["research_complete"],
        state["has_research_data"]
    ):
        return "blocked"

    return "analysis"

workflow = StateGraph(WorkflowState)
workflow.add_conditional_edges(
    "research",
    conditional_analysis,
    {
        "analysis": "run_analysis",
        "blocked": "wait",
        "error": "handle_error"
    }
)
```

### Pattern 3: Quality Gate Loops

```python
from pipeline import validate_research_results, meets_quality_threshold

def research_with_retry(query, max_retries=3):
    """Retry research until quality threshold met."""
    for attempt in range(max_retries):
        results = execute_research(query)

        # Check quality
        if validate_research_results(
            len(results),
            results.quality_score,
            bool(results.sources)
        ):
            return results  # Quality acceptable

        # Quality too low, retry with adjusted parameters
        logger.warning(f"Attempt {attempt + 1}: Quality {results.quality_score} too low")

    raise ValueError(f"Research quality below threshold after {max_retries} attempts")
```

### Pattern 4: Agent Orchestration

```python
from pipeline import (
    validate_pipeline_stage,
    validate_task_assignment,
    is_pipeline_complete
)

class MultiAgentOrchestrator:
    def __init__(self):
        self.state = {
            "research_done": False,
            "analysis_done": False,
            "writing_done": False,
            "current_stage": "research"
        }

    def execute_stage(self, stage, agent_role, task_type):
        """Execute stage with contract validation."""
        # Validate stage can execute
        if not validate_pipeline_stage(
            stage,
            self.state["research_done"],
            self.state["analysis_done"]
        ):
            raise ValueError(f"Cannot execute {stage} - prerequisites not met")

        # Validate agent assignment
        if not validate_task_assignment(agent_role, task_type, has_tools=True):
            raise ValueError(f"Cannot assign {task_type} to {agent_role}")

        # Execute stage
        result = self.agents[agent_role].execute(task_type)

        # Update state
        self.state[f"{stage}_done"] = True

        return result

    def is_complete(self):
        """Check if all stages complete."""
        return is_pipeline_complete(
            self.state["research_done"],
            self.state["analysis_done"],
            self.state["writing_done"]
        )

# Usage
orchestrator = MultiAgentOrchestrator()
orchestrator.execute_stage("research", "researcher", "research")
orchestrator.execute_stage("analysis", "analyzer", "analysis")
orchestrator.execute_stage("writing", "writer", "writing")

assert orchestrator.is_complete()
```

---

## Performance Considerations

### Contract Overhead

Contracts add runtime validation overhead:

```python
# Without contracts
def validate_query(query, max_results):
    return True  # ~0.1µs

# With contracts (3 preconditions, 1 postcondition)
def validate_research_query(query, max_results, min_quality):
    check_precondition(...)  # +0.5µs
    check_precondition(...)  # +0.5µs
    check_precondition(...)  # +0.5µs
    result = True
    check_postcondition(...)  # +0.5µs
    return result
    # Total: ~2.1µs
```

**Overhead**: ~2µs per function call with contracts vs ~0.1µs without.

**When It Matters**:
- ✅ **Agent coordination** - Overhead negligible vs agent execution time (seconds/minutes)
- ✅ **Input validation** - Happens once per workflow, not performance-critical
- ✅ **Quality gates** - Prevents wasted computation on bad inputs (net positive)

**When to Optimize**:
- ❌ **Tight loops** - Don't validate inside inner loops
- ❌ **High-frequency calls** - Cache validation results if called repeatedly

### Optimization Strategies

**1. Validate Once, Execute Many**
```python
# ✅ Validate inputs once
validate_research_query(query, max_results, min_quality)

# Execute multiple agents with same validated inputs
for agent in agents:
    agent.execute(query, max_results)  # No re-validation needed
```

**2. Batch Validation**
```python
# ✅ Validate batch of queries
queries = [...]
for query in queries:
    validate_research_query(query, max_results, min_quality)

# Execute batch
results = batch_execute(queries)
```

**3. Conditional Validation**
```python
# ✅ Only validate in dev/test environments
if settings.VALIDATE_CONTRACTS:
    validate_research_query(query, max_results, min_quality)

execute_research(query, max_results)
```

---

## Next Steps

### 1. Integrate with Your Agents

Start using contracts in your CrewAI/LangGraph workflows:

```bash
# Generate Python code
asl build pipeline.al --lang python -o my_contracts.py

# Import in your agent code
from my_contracts import (
    validate_research_query,
    can_agent_proceed,
    validate_pipeline_stage
)
```

### 2. Customize for Your Domain

Modify contracts for your specific use case:

```al
// Custom validation for your domain
function validate_medical_research_query(
    query: string,
    must_be_peer_reviewed: bool,
    max_age_years: int
) -> bool {
    @requires non_empty_query: len(query) > 0
    @requires reasonable_age: max_age_years > 0 && max_age_years <= 10

    @ensures valid_medical_query: result == true

    return true;
}
```

### 3. Add More Quality Gates

Extend with additional validation:

```al
function validate_research_data_privacy(
    contains_pii: bool,
    anonymization_applied: bool
) -> bool {
    @requires privacy_check: !contains_pii || anonymization_applied

    @ensures privacy_validated: result == true

    if (contains_pii == true && anonymization_applied == false) {
        return false;
    }

    return true;
}
```

### 4. Build Monitoring Dashboards

Track contract violations over time:

```python
from prometheus_client import Counter

contract_violations = Counter(
    'contract_violations_total',
    'Total contract violations',
    ['function_name', 'clause_name']
)

def check_precondition_with_metrics(condition, name, ...):
    if not condition:
        contract_violations.labels(function_name, name).inc()
        raise ContractViolationError(...)
```

### 5. Explore Other Examples

- **[Example 1: E-commerce Orders](../01_ecommerce_orders/)** - State machine validation
- **Example 3: Data Processing Workflow** - Coming soon
- **Example 4: API Rate Limiting** - Coming soon
- **Example 5: State Machine Patterns** - Coming soon

---

## Learn More

- **[AssertLang Documentation](../../../docs/)** - Complete language guide
- **[Contract Tutorial](../../../docs/contracts.md)** - Design by Contract patterns
- **[Multi-Language Codegen](../../../docs/codegen.md)** - Generate Rust, Go, JavaScript
- **[CrewAI Documentation](https://docs.crewai.com/)** - Multi-agent framework
- **[LangGraph Documentation](https://langchain-ai.github.io/langgraph/)** - Agent workflow framework

---

## Summary

**What You Built**:
- ✅ Multi-agent coordination with contracts
- ✅ Input validation for all agents
- ✅ Quality gates blocking low-quality work
- ✅ Pipeline stage enforcement
- ✅ Task assignment validation
- ✅ 39 comprehensive tests

**Key Takeaways**:
1. **Contracts coordinate agents** - Enforce execution order, check prerequisites
2. **Quality gates prevent waste** - Block bad work early, save computation
3. **Clear error messages** - Know exactly what went wrong and why
4. **Runtime validation** - Contracts checked during execution, not compile-time
5. **Integration-friendly** - Works with CrewAI, LangGraph, custom frameworks

**Next**: Customize contracts for your domain, integrate with your agents, add monitoring.
