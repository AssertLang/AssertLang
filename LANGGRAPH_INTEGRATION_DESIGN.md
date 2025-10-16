# LangGraph Contract Integration Design

**Goal:** Enable LangGraph state machines to use PW contracts for validated state management and node execution.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ PW Contract Definition (.al file)                          │
│                                                             │
│ class AgentState {                                         │
│     messages: list<string>;                                │
│     current_step: string;                                  │
│     confidence: float;                                     │
│ }                                                          │
│                                                             │
│ function analyzeData(state: AgentState) -> AgentState {   │
│     @requires confidence_valid: state.confidence >= 0.0    │
│     @ensures step_updated: result.current_step != ""       │
│     ...                                                     │
│ }                                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Code Generation (Python + TypedDict)                       │
│                                                             │
│ 1. Generate TypedDict state schema                         │
│ 2. Generate node functions with contract validation        │
│ 3. Generate edge conditions from preconditions             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ LangGraph Integration Layer                                │
│                                                             │
│ - ContractNode: Wraps PW functions as LangGraph nodes     │
│ - ContractStateGraph: StateGraph with contract validation │
│ - StateValidator: Validates state at transitions           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Runtime Execution                                          │
│                                                             │
│ Node called → Validate state preconditions → Execute →     │
│ Validate state postconditions → Update state               │
└─────────────────────────────────────────────────────────────┘
```

## Key Differences from CrewAI

| Aspect | CrewAI | LangGraph |
|--------|--------|-----------|
| **Architecture** | Tool-based agents | State machine with nodes |
| **State** | Task-based context | Explicit StateGraph schema |
| **Coordination** | Sequential/hierarchical tasks | Graph edges and transitions |
| **Validation** | Function-level (tool calls) | State-level (transitions) |
| **Integration** | ContractTool wrapping | ContractNode + StateValidator |

## Components

### 1. TypedDict State Generator

**Input:** PW class/type definitions
**Output:** Python TypedDict for LangGraph state schema

```python
# From PW:
class AgentState {
    messages: list<string>;
    current_step: string;
    confidence: float;
}

# Generate:
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[str]
    current_step: str
    confidence: float
```

**Location:** `language/typeddict_generator.py` (or extend pydantic_generator.py)

### 2. Contract Node Wrapper

**Purpose:** Wrap PW contract functions as LangGraph nodes with validation

```python
from typing import TypedDict
from langgraph.graph import StateGraph
from promptware.runtime.contracts import check_precondition, check_postcondition

class ContractNode:
    """LangGraph node with contract validation."""

    def __init__(self, func, preconditions, postconditions, state_schema):
        self.func = func
        self.preconditions = preconditions
        self.postconditions = postconditions
        self.state_schema = state_schema

    def __call__(self, state, config=None, runtime=None):
        """
        Execute node with contract validation.

        Args:
            state: Current graph state (TypedDict)
            config: LangGraph config
            runtime: LangGraph runtime

        Returns:
            State updates (partial dict)
        """
        # Validate preconditions on current state
        for clause in self.preconditions:
            check_precondition(
                clause.evaluate(state),
                clause.name,
                clause.expression,
                self.func.__name__,
                context=state
            )

        # Execute node function
        result = self.func(state, config, runtime)

        # Validate postconditions on updated state
        updated_state = {**state, **result}
        for clause in self.postconditions:
            check_postcondition(
                clause.evaluate(updated_state),
                clause.name,
                clause.expression,
                self.func.__name__,
                context=updated_state
            )

        return result
```

**Location:** `promptware/integrations/langgraph/nodes.py`

### 3. Contract StateGraph

**Purpose:** StateGraph with built-in contract validation

```python
from langgraph.graph import StateGraph
from promptware.integrations.langgraph import StateValidator

class ContractStateGraph(StateGraph):
    """StateGraph with contract validation at state transitions."""

    def __init__(self, state_schema, invariants=None):
        super().__init__(state_schema)
        self.validator = StateValidator(state_schema, invariants)

    def add_node(self, name, func, preconditions=None, postconditions=None):
        """Add node with contract validation."""
        if preconditions or postconditions:
            wrapped = ContractNode(func, preconditions, postconditions, self.state_schema)
            super().add_node(name, wrapped)
        else:
            super().add_node(name, func)

    def add_edge(self, source, target, condition=None):
        """Add edge with optional contract-based condition."""
        if condition:
            # Wrap condition with contract validation
            super().add_conditional_edges(source, condition, {True: target})
        else:
            super().add_edge(source, target)
```

**Location:** `promptware/integrations/langgraph/graph.py`

### 4. State Validator

**Purpose:** Validate state invariants at transitions

```python
class StateValidator:
    """Validates state invariants during graph execution."""

    def __init__(self, state_schema, invariants=None):
        self.state_schema = state_schema
        self.invariants = invariants or []

    def validate(self, state):
        """
        Validate state against invariants.

        Args:
            state: Current state dict

        Raises:
            ContractViolationError: If invariant violated
        """
        for invariant in self.invariants:
            if not invariant.evaluate(state):
                raise ContractViolationError(
                    type="invariant",
                    clause=invariant.name,
                    expression=invariant.expression,
                    context=state
                )
```

**Location:** `promptware/integrations/langgraph/validation.py`

## Integration Workflow

### Step 1: Define PW Contract with State

```pw
// contracts/data_processor_agent.al

class ProcessorState {
    input_data: list<string>;
    processed_data: list<string>;
    current_stage: string;
    error_count: int;
}

function loadData(state: ProcessorState) -> ProcessorState {
    @requires stage_is_init: state.current_stage == "init"
    @ensures stage_updated: result.current_stage == "loaded"
    @ensures data_exists: str.length(result.input_data) > 0

    // Load data logic
    let new_state = ProcessorState {
        input_data: ["data1", "data2", "data3"],
        processed_data: state.processed_data,
        current_stage: "loaded",
        error_count: state.error_count
    };
    return new_state;
}

function processData(state: ProcessorState) -> ProcessorState {
    @requires stage_is_loaded: state.current_stage == "loaded"
    @requires has_input: str.length(state.input_data) > 0
    @ensures stage_updated: result.current_stage == "processed"
    @ensures output_exists: str.length(result.processed_data) > 0

    // Process data logic
    let new_state = ProcessorState {
        input_data: state.input_data,
        processed_data: ["processed1", "processed2"],
        current_stage: "processed",
        error_count: state.error_count
    };
    return new_state;
}
```

### Step 2: Generate Python with TypedDict

```bash
asl build contracts/data_processor_agent.al --lang python --typeddict -o generated/processor.py
```

Generates:
```python
from typing import TypedDict
from promptware.runtime.contracts import check_precondition, check_postcondition

class ProcessorState(TypedDict):
    input_data: list[str]
    processed_data: list[str]
    current_stage: str
    error_count: int

def loadData(state: ProcessorState, config=None, runtime=None) -> dict:
    # Precondition validation
    check_precondition(
        state["current_stage"] == "init",
        "stage_is_init",
        "state.current_stage == \"init\"",
        "loadData",
        context=state
    )

    # Function body
    new_state = {
        "input_data": ["data1", "data2", "data3"],
        "processed_data": state["processed_data"],
        "current_stage": "loaded",
        "error_count": state["error_count"]
    }

    # Postcondition validation
    updated = {**state, **new_state}
    check_postcondition(
        updated["current_stage"] == "loaded",
        "stage_updated",
        "result.current_stage == \"loaded\"",
        "loadData",
        context=updated
    )
    check_postcondition(
        len(updated["input_data"]) > 0,
        "data_exists",
        "str.length(result.input_data) > 0",
        "loadData",
        context=updated
    )

    return new_state
```

### Step 3: Create LangGraph with Contracts

```python
from langgraph.graph import StateGraph, END
from generated.processor import ProcessorState, loadData, processData

# Create state graph
workflow = StateGraph(ProcessorState)

# Add nodes (contracts already embedded in functions)
workflow.add_node("load", loadData)
workflow.add_node("process", processData)

# Add edges
workflow.add_edge("load", "process")
workflow.add_edge("process", END)

# Set entry point
workflow.set_entry_point("load")

# Compile
app = workflow.compile()

# Run with initial state
initial_state = {
    "input_data": [],
    "processed_data": [],
    "current_stage": "init",
    "error_count": 0
}

result = app.invoke(initial_state)
# Contract validation happens automatically at each node
```

## Benefits

1. **State Validation** - Contracts enforce state invariants at every transition
2. **Type Safety** - TypedDict provides type checking for state schema
3. **Edge Conditions** - Preconditions can determine graph routing
4. **Debugging** - Contract violations pinpoint exact state transition errors
5. **Documentation** - Contracts document state machine behavior
6. **Composability** - Mix contract-validated and regular nodes

## Implementation Plan

1. **Phase 3.4 Tasks:**
   - [ ] Extend pydantic_generator or create typeddict_generator
   - [ ] Implement ContractNode wrapper
   - [ ] Build StateValidator for invariants
   - [ ] Create ContractStateGraph (optional, can use vanilla StateGraph)
   - [ ] Add CLI support: `--typeddict` flag
   - [ ] Integration tests with LangGraph

## Files to Create

```
promptware/integrations/
├── langgraph/
│   ├── __init__.py
│   ├── nodes.py           # ContractNode
│   ├── graph.py           # ContractStateGraph (optional)
│   ├── validation.py      # StateValidator
│   └── edges.py           # Contract-based edge conditions (optional)
```

```
language/
├── typeddict_generator.py  # Or extend pydantic_generator.py
```

```
tests/integration/
├── test_langgraph_integration.py
```

## Key Design Decision

**Use Vanilla LangGraph + Contract-Embedded Functions**

Instead of building a custom ContractStateGraph, we can:
1. Generate node functions with embedded contract validation
2. Use standard LangGraph StateGraph
3. Contracts validate automatically when nodes execute

This is **simpler** and **more compatible** with existing LangGraph code.

## Next Step

Start with TypedDict generation - extend pydantic_generator.py to support TypedDict output mode.
