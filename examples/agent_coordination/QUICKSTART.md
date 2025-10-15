# Quick Start: Multi-Agent Coordination Demo

**Time to run:** < 1 minute
**Prerequisites:** Python 3.10+, Node.js 16+

---

## What This Demo Shows

Two agents from different frameworks execute IDENTICAL logic:

- **Agent A**: Python + CrewAI framework
- **Agent B**: JavaScript + LangGraph framework
- **Contract**: `user_service_contract.pw` (single source of truth)

**Result:** 100% identical behavior (5/5 tests match)

---

## Running the Demo

### Option 1: Automated Demo (Recommended)

```bash
cd examples/agent_coordination
./run_demo.sh
```

This runs both agents and shows their outputs side-by-side.

### Option 2: Manual Execution

**Run Agent A (Python/CrewAI):**
```bash
python agent_a_crewai.py
```

**Run Agent B (JavaScript/LangGraph):**
```bash
node agent_b_langgraph.js
```

**Compare outputs** - they're identical!

---

## Expected Output

Both agents will output:

```
Test 1: Creating valid user
✓ Success: User #28: Alice Smith <alice@example.com>

Test 2: Invalid user (empty name)
✓ Expected error: name - Name cannot be empty

Test 3: Invalid email format
✓ Email is INVALID (expected)

Test 4: Valid email format
✓ Email is VALID (expected)
```

**Framework integration test:**
```json
{
  "success": true,
  "user": {
    "id": 24,
    "name": "Bob Jones",
    "email": "bob@example.com",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Same ID (24), same timestamp, same everything.**

---

## What's Happening

### 1. The Contract

`user_service_contract.pw` defines the EXACT behavior:

```pw
function createUser(name: string, email: string) -> User {
    if (str.length(name) < 1) {
        return ValidationError("name", "Name cannot be empty");
    }

    if (!str.contains(email, "@")) {
        return ValidationError("email", "Invalid email format");
    }

    let id = str.length(name) + str.length(email);
    return User(id, name, email, timestamp());
}
```

### 2. Agent A Implementation

`agent_a_crewai.py` transpiles the contract to Python:

```python
def createUser(name: str, email: str) -> Union[User, ValidationError]:
    if len(name) < 1:
        return ValidationError(field="name", message="Name cannot be empty")

    if "@" not in email:
        return ValidationError(field="email", message="Invalid email format")

    user_id = len(name) + len(email)
    # ... rest of implementation
```

### 3. Agent B Implementation

`agent_b_langgraph.js` transpiles the same contract to JavaScript:

```javascript
function createUser(name, email) {
    if (name.length < 1) {
        return {field: "name", message: "Name cannot be empty"};
    }

    if (!email.includes("@")) {
        return {field: "email", message: "Invalid email format"};
    }

    const userId = name.length + email.length;
    // ... rest of implementation
}
```

### 4. The Guarantee

**Same contract → Same semantics → Same behavior**

No matter the language, no matter the framework, the logic is IDENTICAL.

---

## Key Insights

### ✅ Deterministic Validation
Both agents validate email the same way (`contains "@"`)

### ✅ Deterministic ID Generation
Both agents calculate ID the same way (`name.length + email.length`)

### ✅ Deterministic Error Messages
Both agents return identical error messages

### ✅ Framework Independence
CrewAI and LangGraph agents coordinate seamlessly

### ✅ No LLM Ambiguity
No interpretation required - just execute the contract

---

## Files in This Demo

| File | Purpose |
|------|---------|
| `user_service_contract.pw` | PW contract (source of truth) |
| `agent_a_crewai.py` | Python/CrewAI implementation |
| `agent_b_langgraph.js` | JavaScript/LangGraph implementation |
| `run_demo.sh` | Automated demo script |
| `PROOF_OF_DETERMINISM.md` | Detailed test results |
| `README.md` | Full explanation |
| `QUICKSTART.md` | This file |

---

## Next Steps

1. **Modify the contract**: Change validation rules in `user_service_contract.pw`
2. **Regenerate agents**: Transpile to Python and JavaScript again
3. **Run demo**: See that both agents still match 100%

**Example modification:**

Change minimum name length from 1 to 3:
```pw
if (str.length(name) < 3) {  // Changed from < 1
    return ValidationError("name", "Name must be at least 3 characters");
}
```

Transpile and run - both agents will now enforce 3-character minimum.

---

## Troubleshooting

**Python not found:**
```bash
# Install Python 3.10+
# macOS: brew install python3
# Ubuntu: sudo apt install python3
```

**Node.js not found:**
```bash
# Install Node.js 16+
# macOS: brew install node
# Ubuntu: sudo apt install nodejs npm
```

**Demo script won't run:**
```bash
chmod +x run_demo.sh
./run_demo.sh
```

---

## Questions?

- **Full explanation**: Read `README.md` in this directory
- **Test results**: Read `PROOF_OF_DETERMINISM.md`
- **How it works**: Read main project `README.md`
- **Issues**: [github.com/Promptware-dev/promptware/issues](https://github.com/Promptware-dev/promptware/issues)

---

**Time to run:** < 1 minute
**Lines of code:** ~400 total
**Frameworks demonstrated:** 2 (CrewAI, LangGraph)
**Test match rate:** 100% (5/5)

**This is deterministic multi-agent coordination.**
