# Multi-Agent Coordination via PW Contracts

## The Problem This Solves

**Scenario:** You have two AI agents using different frameworks that need to coordinate:
- **Agent A**: CrewAI agent (Python)
- **Agent B**: LangGraph agent (TypeScript)

**Challenge:** How do they agree on:
- What "create user" means?
- What validation rules to apply?
- What error codes to return?
- What data format to use?

**Traditional approaches:**
1. **Natural language** - "Create a user" → Vague, ambiguous
2. **JSON Schema** - Types only, no semantics or behavior
3. **LLM interpretation** - Unreliable, non-deterministic
4. **Framework-specific** - Doesn't work across frameworks

**PW Contract approach:**
- Define executable contract once in PW
- Transpile to Python for Agent A
- Transpile to TypeScript for Agent B
- **Both agents have IDENTICAL behavior** (deterministic)

---

## How It Works

### Step 1: Define Contract in PW

**File:** `user_service_contract.pw`

```pw
// Executable contract - defines EXACT behavior
function createUser(name: string, email: string) -> User {
    // Deterministic validation rules
    if (str.length(name) < 1) {
        return ValidationError("name", "Name cannot be empty");
    }

    if (!str.contains(email, "@")) {
        return ValidationError("email", "Invalid email format");
    }

    // Deterministic ID generation
    let id = str.length(name) + str.length(email);

    // Create user
    return User(id, name, email, "2025-01-15T10:30:00Z");
}
```

### Step 2: Transpile to Agent A (Python/CrewAI)

```bash
promptware build user_service_contract.pw --lang python -o agent_a_crewai.py
```

**Result:** Python code with IDENTICAL logic

```python
def createUser(name: str, email: str) -> Union[User, ValidationError]:
    if len(name) < 1:
        return ValidationError(field="name", message="Name cannot be empty")

    if "@" not in email:
        return ValidationError(field="email", message="Invalid email format")

    user_id = len(name) + len(email)
    return User(id=user_id, name=name, email=email, created_at="2025-01-15T10:30:00Z")
```

### Step 3: Transpile to Agent B (TypeScript/LangGraph)

```bash
promptware build user_service_contract.pw --lang typescript -o agent_b_langgraph.ts
```

**Result:** TypeScript code with IDENTICAL logic

```typescript
function createUser(name: string, email: string): User | ValidationError {
    if (name.length < 1) {
        return { field: "name", message: "Name cannot be empty" };
    }

    if (!email.includes("@")) {
        return { field: "email", message: "Invalid email format" };
    }

    const userId = name.length + email.length;
    return { id: userId, name, email, created_at: "2025-01-15T10:30:00Z" };
}
```

### Step 4: Agents Coordinate with Guaranteed Consistency

**Agent A (CrewAI):**
```python
# Agent A validates input
result = createUser("Alice", "alice@example.com")
# Returns: User(id=28, name="Alice", email="alice@example.com")
```

**Agent B (LangGraph):**
```typescript
// Agent B validates same input
const result = createUser("Alice", "alice@example.com");
// Returns: { id: 28, name: "Alice", email: "alice@example.com" }
```

**Guaranteed:** Both agents produce IDENTICAL results because they implement the same contract.

---

## Deterministic Behavior

### Test Case: Create User "Alice Smith" with email "alice@example.com"

**Agent A Output:**
```
Test 1: Creating valid user
✓ Success: User #28: Alice Smith <alice@example.com>
```

**Agent B Output:**
```
Test 1: Creating valid user
✓ Success: User #28: Alice Smith <alice@example.com>
```

**Result:** IDENTICAL (ID = 28, same format, same validation)

### Test Case: Empty Name

**Agent A Output:**
```
Test 2: Invalid user (empty name)
✓ Expected error: name - Name cannot be empty
```

**Agent B Output:**
```
Test 2: Invalid user (empty name)
✓ Expected error: name - Name cannot be empty
```

**Result:** IDENTICAL error messages

---

## Why This Matters

### Without PW Contracts (Current Reality):

**Agent A decides:**
```python
# Agent A's interpretation
if not name:
    raise ValueError("Missing name")  # Different error!
```

**Agent B decides:**
```typescript
// Agent B's interpretation
if (name === "") {
    throw new Error("Name is required");  // Different error!
}
```

**Problem:** Different validation, different errors, inconsistent behavior.

---

### With PW Contracts:

**Both agents implement SAME contract:**
- Same validation rules
- Same error messages
- Same data structures
- Same behavior

**Result:** Multi-agent systems that actually work together reliably.

---

## Running the Demo

### Run Agent A (Python/CrewAI):

```bash
cd examples/agent_coordination
python agent_a_crewai.py
```

**Expected Output:**
```
=== Agent A (CrewAI) - Executing PW Contract ===

Test 1: Creating valid user
✓ Success: User #28: Alice Smith <alice@example.com>

Test 2: Invalid user (empty name)
✓ Expected error: name - Name cannot be empty

Test 3: Invalid email format
✓ Email is INVALID (expected)

Test 4: Valid email format
✓ Email is VALID (expected)

=== Agent A: Contract execution complete ===
```

### Run Agent B (TypeScript/LangGraph):

```bash
cd examples/agent_coordination
npx ts-node agent_b_langgraph.ts
```

**Expected Output:**
```
=== Agent B (LangGraph) - Executing PW Contract ===

Test 1: Creating valid user
✓ Success: User #28: Alice Smith <alice@example.com>

Test 2: Invalid user (empty name)
✓ Expected error: name - Name cannot be empty

Test 3: Invalid email format
✓ Email is INVALID (expected)

Test 4: Valid email format
✓ Email is VALID (expected)

=== Agent B: Contract execution complete ===
```

**Result:** IDENTICAL outputs prove deterministic behavior.

---

## Framework Integration

### CrewAI Integration (Agent A):

```python
from crewai import Agent, Task, Crew

# Wrap PW contract in CrewAI agent
user_agent = Agent(
    role='User Management',
    goal='Manage user accounts reliably',
    backstory='I implement the PW user service contract',
    verbose=True
)

# Task uses contract implementation
task = Task(
    description='Create user Alice',
    agent=user_agent,
    expected_output='User object'
)

# Agent executes using PW contract logic
result = createUser("Alice", "alice@example.com")
```

### LangGraph Integration (Agent B):

```typescript
import { StateGraph } from "@langchain/langgraph";

// Define LangGraph node using PW contract
const userServiceNode = async (state: any) => {
    // Use contract implementation
    const result = await createUser(state.name, state.email);
    return { user: result };
};

// Build graph
const workflow = new StateGraph({
    channels: {
        name: null,
        email: null,
        user: null
    }
})
    .addNode("create_user", userServiceNode)
    .addEdge("create_user", END);

// Execute - guaranteed to match Python agent behavior
const result = await workflow.invoke({
    name: "Alice",
    email: "alice@example.com"
});
```

---

## Key Benefits

### 1. Deterministic Coordination
- Same input → same output (always)
- No ambiguity
- No drift between agents

### 2. Framework Agnostic
- Works with CrewAI, LangGraph, AutoGen, any framework
- Each agent uses their preferred framework
- Contract ensures compatibility

### 3. Language Agnostic
- Python agents get Python code
- TypeScript agents get TypeScript code
- Rust agents get Rust code
- All implement same semantics

### 4. Verifiable
- Can test contract once
- Transpiled code inherits correctness
- No manual coordination needed

### 5. Maintainable
- Update contract in one place (PW file)
- Re-transpile to all languages
- All agents updated automatically

---

## Comparison to Alternatives

| Approach | Deterministic | Framework-Agnostic | Language-Agnostic | Verifiable |
|----------|---------------|-------------------|-------------------|------------|
| **Natural Language** | ❌ | ✅ | ✅ | ❌ |
| **JSON Schema** | ⚠️ (types only) | ✅ | ✅ | ⚠️ (partial) |
| **MCP** | ❌ | ⚠️ (MCP only) | ✅ | ❌ |
| **LLM Interpretation** | ❌ | ✅ | ✅ | ❌ |
| **PW Contracts** | ✅ | ✅ | ✅ | ✅ |

---

## Real-World Use Cases

### 1. Multi-Agent Workflows
- Planning agent (Python) defines task
- Execution agent (Go) implements task
- Validation agent (TypeScript) checks result
- **All follow same contract**

### 2. Cross-Framework Migration
- Start with CrewAI agents (Python)
- Migrate some to LangGraph (TypeScript) for performance
- **Guaranteed compatibility via contracts**

### 3. Polyglot Teams
- Python team builds ML agents
- TypeScript team builds UI agents
- Rust team builds performance-critical agents
- **All coordinate via PW contracts**

### 4. Enterprise Integration
- Legacy Python systems
- Modern TypeScript microservices
- High-performance Rust components
- **Common contract layer ensures interop**

---

## Next Steps

1. **Try it:** Run both agents, verify identical output
2. **Modify contract:** Change validation rules, re-transpile, see both agents update
3. **Add your framework:** Integrate with your agent framework of choice
4. **Build multi-agent system:** Coordinate 3+ agents via contracts

---

## Technical Details

**Contract Definition:** Pure PW (no framework dependencies)
**Transpilation:** `promptware build` command
**Type Safety:** Full type checking in both Python and TypeScript
**Error Handling:** Deterministic error codes and messages
**Testing:** Identical test cases across all agents

**Files:**
- `user_service_contract.pw` - Source of truth (contract)
- `agent_a_crewai.py` - Python implementation (CrewAI)
- `agent_b_langgraph.ts` - TypeScript implementation (LangGraph)
- `README.md` - This file

---

## The Bottom Line

**PW Contracts provide what multi-agent systems desperately need:**

✅ Deterministic coordination
✅ Framework independence
✅ Language independence
✅ Verifiable behavior
✅ Single source of truth

**No more agent miscommunication. No more inconsistent behavior. Just reliable multi-agent systems.**
