# CrewAI Contract Integration Design

**Goal:** Enable CrewAI agents to use PW contracts for type-safe, validated coordination.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ PW Contract Definition (.al file)                          │
│                                                             │
│ function analyzeMarket(sector: string) -> MarketReport {   │
│     @requires sector_valid: str.length(sector) > 0         │
│     @ensures report_complete: result.summary != ""         │
│     ...                                                     │
│ }                                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Code Generation (Python + Pydantic)                        │
│                                                             │
│ 1. Generate Python function with contract validation       │
│ 2. Generate Pydantic model for MarketReport                │
│ 3. Generate CrewAI Tool wrapper                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CrewAI Integration Layer                                   │
│                                                             │
│ - ContractTool: Wraps PW functions as CrewAI tools        │
│ - ContractAgent: Agent that validates contracts            │
│ - ContractTask: Task with contract validation              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Runtime Execution                                          │
│                                                             │
│ Agent calls Tool → Validate preconditions → Execute →      │
│ Validate postconditions → Return validated result          │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Pydantic Model Generator

**Input:** PW type definitions
**Output:** Pydantic BaseModel classes

```python
# From PW:
type MarketReport {
    sector: string;
    summary: string;
    confidence: float;
}

# Generate:
from pydantic import BaseModel

class MarketReport(BaseModel):
    sector: str
    summary: str
    confidence: float
```

**Location:** `language/pydantic_generator.py`

### 2. Contract Tool Wrapper

**Purpose:** Wrap PW contract functions as CrewAI tools with validation

```python
from crewai.tools import BaseTool
from promptware.runtime.contracts import check_precondition, check_postcondition

class ContractTool(BaseTool):
    """CrewAI tool that validates PW contracts."""

    name: str = "contract_tool"
    description: str = "Validated function with contracts"

    def __init__(self, contract_func, preconditions, postconditions):
        self.func = contract_func
        self.preconditions = preconditions
        self.postconditions = postconditions

    def _run(self, **kwargs):
        # Validate preconditions
        for clause in self.preconditions:
            check_precondition(
                clause.evaluate(kwargs),
                clause.name,
                clause.expression,
                self.name,
                context=kwargs
            )

        # Execute function
        result = self.func(**kwargs)

        # Validate postconditions
        for clause in self.postconditions:
            check_postcondition(
                clause.evaluate(result, kwargs),
                clause.name,
                clause.expression,
                self.name,
                context={'result': result, **kwargs}
            )

        return result
```

**Location:** `promptware/integrations/crewai/tools.py`

### 3. Contract Agent

**Purpose:** CrewAI agent that uses contract-validated tools

```python
from crewai import Agent
from promptware.integrations.crewai import ContractTool

class ContractAgent(Agent):
    """CrewAI agent with contract validation."""

    def __init__(self, role, goal, backstory, contracts):
        tools = [
            ContractTool.from_pw_function(contract)
            for contract in contracts
        ]
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools
        )
```

**Location:** `promptware/integrations/crewai/agents.py`

### 4. Contract Discovery

**Purpose:** Allow agents to discover and validate each other's contracts

```python
class ContractRegistry:
    """Registry of agent contracts for discovery."""

    def __init__(self):
        self.contracts = {}

    def register(self, agent_name: str, contract_path: str):
        """Register agent's contract."""
        module = parse_pw_file(contract_path)
        self.contracts[agent_name] = module

    def get_contract(self, agent_name: str):
        """Get agent's contract for validation."""
        return self.contracts.get(agent_name)

    def validate_call(self, agent_name: str, function_name: str, **kwargs):
        """Validate a call to another agent's function."""
        contract = self.get_contract(agent_name)
        if not contract:
            raise ValueError(f"No contract for agent {agent_name}")

        func = contract.get_function(function_name)
        # Validate preconditions before delegating
        for clause in func.requires:
            check_precondition(...)
```

**Location:** `promptware/integrations/crewai/registry.py`

## Integration Workflow

### Step 1: Define PW Contract

```pw
// contracts/market_analyst.al

type MarketReport {
    sector: string;
    summary: string;
    trends: list<string>;
    confidence: float;
}

function analyzeMarket(sector: string, depth: int) -> MarketReport {
    @requires sector_not_empty: str.length(sector) > 0
    @requires depth_valid: depth >= 1 && depth <= 5
    @ensures report_has_summary: str.length(result.summary) > 10
    @ensures confidence_valid: result.confidence >= 0.0 && result.confidence <= 1.0

    // Implementation would be AI-generated
    let report = MarketReport {
        sector: sector,
        summary: "AI analysis here",
        trends: ["trend1", "trend2"],
        confidence: 0.85
    };
    return report;
}
```

### Step 2: Generate Python + Pydantic

```bash
asl build contracts/market_analyst.al --lang python --pydantic -o generated/market_analyst.py
```

Generates:
```python
from pydantic import BaseModel
from promptware.runtime.contracts import check_precondition, check_postcondition

class MarketReport(BaseModel):
    sector: str
    summary: str
    trends: list[str]
    confidence: float

def analyzeMarket(sector: str, depth: int) -> MarketReport:
    # Precondition validation
    check_precondition(
        len(sector) > 0,
        "sector_not_empty",
        "str.length(sector) > 0",
        "analyzeMarket",
        context={"sector": sector, "depth": depth}
    )
    check_precondition(
        depth >= 1 and depth <= 5,
        "depth_valid",
        "depth >= 1 && depth <= 5",
        "analyzeMarket",
        context={"sector": sector, "depth": depth}
    )

    # Function body (AI-implemented)
    report = MarketReport(
        sector=sector,
        summary="AI analysis here",
        trends=["trend1", "trend2"],
        confidence=0.85
    )

    # Postcondition validation
    check_postcondition(
        len(report.summary) > 10,
        "report_has_summary",
        "str.length(result.summary) > 10",
        "analyzeMarket",
        context={"result": report, "sector": sector, "depth": depth}
    )
    check_postcondition(
        report.confidence >= 0.0 and report.confidence <= 1.0,
        "confidence_valid",
        "result.confidence >= 0.0 && result.confidence <= 1.0",
        "analyzeMarket",
        context={"result": report, "sector": sector, "depth": depth}
    )

    return report
```

### Step 3: Create CrewAI Agent with Contract

```python
from crewai import Agent, Task, Crew
from promptware.integrations.crewai import ContractTool
from generated.market_analyst import analyzeMarket, MarketReport

# Create contract tool from PW function
analyze_tool = ContractTool.from_function(
    analyzeMarket,
    name="analyze_market",
    description="Analyze market sector with contract validation"
)

# Create agent with contract tool
analyst = Agent(
    role="Senior Market Analyst",
    goal="Provide validated market analysis",
    backstory="Expert analyst with strict quality standards",
    tools=[analyze_tool]
)

# Create task
analysis_task = Task(
    description="Analyze the technology sector with depth 3",
    expected_output="Validated MarketReport with confidence >= 0.7",
    agent=analyst
)

# Run crew
crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()
```

## Benefits

1. **Type Safety** - Pydantic models ensure data structure correctness
2. **Contract Validation** - Preconditions/postconditions enforced at runtime
3. **Agent Coordination** - Contracts define clear interfaces between agents
4. **Error Handling** - Contract violations raise clear errors with context
5. **Discoverability** - Contract registry enables agent-to-agent validation
6. **Modularity** - Contracts defined separately from agent implementation

## Implementation Plan

1. ✅ **Done:** Core contract system (Python generator, runtime validation)
2. **Phase 3.3 Tasks:**
   - [ ] Build Pydantic model generator
   - [ ] Implement ContractTool wrapper
   - [ ] Create ContractAgent class
   - [ ] Build ContractRegistry for discovery
   - [ ] Add CLI support: `--pydantic` flag for Pydantic generation
   - [ ] Integration tests with real CrewAI agents

## Files to Create

```
promptware/integrations/
├── __init__.py
├── crewai/
│   ├── __init__.py
│   ├── tools.py          # ContractTool
│   ├── agents.py         # ContractAgent
│   ├── registry.py       # ContractRegistry
│   └── tasks.py          # ContractTask (optional)
├── langgraph/            # Future: Phase 3.4
│   └── ...
```

```
language/
├── pydantic_generator.py  # New: IR → Pydantic models
```

```
tests/integration/
├── test_crewai_integration.py
```

## Next Step

Start with Pydantic model generator - this is the foundation for CrewAI integration.
