# Getting Started with AssertLang

Welcome to AssertLang! This guide will help you get up and running in just a few minutes.

## What is AssertLang?

AssertLang (AL) is a multi-language transpiler for executable contracts in multi-agent systems. Write your agent behavior once in AL, then transpile to Python, JavaScript, TypeScript, Go, Rust, or C#. All agents execute **identical logic**, guaranteed.

**Key benefit:** No more drift between agents. One contract, multiple languages, deterministic behavior.

---

## Installation

### Requirements

- Python 3.9 or higher
- pip (Python package manager)

### Install from PyPI

```bash
pip install assertlang
```

### Verify Installation

```bash
asl --version
# Should output: AssertLang CLI v0.1.6 (or newer)
```

---

## Your First Contract (5 Minutes)

Let's write a simple contract and transpile it to Python.

### Step 1: Create a Contract File

Create a file called `greeting.al`:

```al
// greeting.al - A simple greeting contract

function greet(name: string) -> string {
    // Validate input
    if (str.length(name) < 1) {
        return "Hello, Guest!";
    }

    // Return personalized greeting
    return "Hello, " + name + "!";
}

function greet_formal(firstName: string, lastName: string) -> string {
    // Build formal greeting
    let fullName = firstName + " " + lastName;
    return "Good day, " + fullName + ".";
}
```

### Step 2: Transpile to Python

```bash
asl build greeting.al --lang python -o greeting.py
```

### Step 3: Use the Generated Code

```python
# test_greeting.py
from greeting import greet, greet_formal

# Test the functions
print(greet("Alice"))           # Output: Hello, Alice!
print(greet(""))                # Output: Hello, Guest!
print(greet_formal("Bob", "Smith"))  # Output: Good day, Bob Smith.
```

### Step 4: Run It

```bash
python test_greeting.py
```

**That's it!** You've written your first AssertLang contract and used it in Python.

---

## Multi-Language Example

The same contract can be transpiled to **any supported language**:

### Python (for CrewAI, AutoGen, LangChain)
```bash
asl build greeting.al --lang python -o greeting.py
```

### JavaScript (for LangGraph, Node.js)
```bash
asl build greeting.al --lang javascript -o greeting.js
```

### TypeScript (for type-safe Node.js)
```bash
asl build greeting.al --lang typescript -o greeting.ts
```

### Go (for high-performance agents)
```bash
asl build greeting.al --lang go -o greeting.go
```

### Rust (for performance-critical agents)
```bash
asl build greeting.al --lang rust -o greeting.rs
```

### C# (for Windows/enterprise agents)
```bash
asl build greeting.al --lang csharp -o greeting.cs
```

**All of them will execute identical logic!** ✅

---

## Key Language Features

### Types

AssertLang supports strong typing:

```al
function calculate_dose(weight: float, age: int) -> float {
    let base_dose: float = weight * 1.5;
    return base_dose;
}
```

**Supported types:**
- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings
- `bool` - Boolean (true/false)
- `list` - Lists/arrays
- `map` - Dictionaries/maps
- Custom types (classes)

### Control Flow

```al
// If/else
function check_age(age: int) -> string {
    if (age >= 18) {
        return "Adult";
    } else {
        return "Minor";
    }
}

// For loops
function sum_list(numbers: list) -> int {
    let total = 0;
    for (num in numbers) {
        total = total + num;
    }
    return total;
}

// While loops
function count_down(n: int) -> int {
    while (n > 0) {
        n = n - 1;
    }
    return n;
}
```

### Standard Library Functions

AssertLang provides built-in modules for common operations:

#### String Operations (al_str)

```al
function format_name(name: string) -> string {
    let length = str.length(name);           // Get length
    let upper = str.upper(name);             // Uppercase
    let lower = str.lower(name);             // Lowercase
    let trimmed = str.trim(name);            // Remove whitespace
    let contains = str.contains(name, "@");  // Check substring
    return upper;
}
```

#### Math Operations (al_math)

```al
function calculate(x: float, y: float) -> float {
    let rounded = math.round(x);        // Round to nearest integer
    let max_val = math.max(x, y);       // Maximum of two values
    let min_val = math.min(x, y);       // Minimum of two values
    let power = math.pow(2, 3);         // 2^3 = 8
    let floor = math.floor(x);          // Round down
    let ceil = math.ceil(x);            // Round up
    let abs = math.abs(x);              // Absolute value
    return floor;
}
```

#### List Operations (al_list)

```al
function process_items(items: list) -> list {
    let first = list.first(items);      // Get first element
    let last = list.last(items);        // Get last element
    let length = list.length(items);    // Get list length
    let reversed = list.reverse(items); // Reverse list
    return reversed;
}
```

**Important:** The transpiler automatically imports these modules when you use them! (v0.1.6+)

### Classes

```al
class User {
    id: int;
    name: string;
    email: string;

    function __init__(id: int, name: string, email: string) {
        self.id = id;
        self.name = name;
        self.email = email;
    }

    function format() -> string {
        return "User #" + str(self.id) + ": " + self.name;
    }
}

function create_user(name: string, email: string) -> User {
    let id = str.length(name) + str.length(email);
    return User(id, name, email);
}
```

### Result Types (Error Handling)

```al
function validate_email(email: string) -> Result<string, string> {
    if (!str.contains(email, "@")) {
        return Error("Invalid email: missing @");
    }
    return Ok(email);
}
```

---

## Production Example: Medical Dosing System

Here's a real-world example that was validated in production (680+ lines, 67/67 tests passed):

```al
// dosing.al - Medical dosing calculation contract

class Patient {
    id: int;
    weight: float;
    age: int;

    function __init__(id: int, weight: float, age: int) {
        self.id = id;
        self.weight = weight;
        self.age = age;
    }
}

class DoseRecommendation {
    patient_id: int;
    dose_mg: float;
    frequency: string;
    warnings: list;

    function __init__(patient_id: int, dose_mg: float, frequency: string, warnings: list) {
        self.patient_id = patient_id;
        self.dose_mg = dose_mg;
        self.frequency = frequency;
        self.warnings = warnings;
    }
}

function calculate_dose(patient: Patient, drug_name: string) -> Result<DoseRecommendation, string> {
    // Validate inputs
    if (patient.weight <= 0) {
        return Error("Invalid weight: must be positive");
    }

    if (patient.age < 0) {
        return Error("Invalid age: cannot be negative");
    }

    // Calculate base dose (1.5 mg per kg)
    let base_dose = patient.weight * 1.5;

    // Age-based adjustments
    let adjusted_dose = base_dose;
    let warnings = [];

    if (patient.age < 18) {
        adjusted_dose = base_dose * 0.8;  // Reduce for pediatric
        warnings = ["Pediatric dosing - reduced by 20%"];
    } else if (patient.age > 65) {
        adjusted_dose = base_dose * 0.9;  // Reduce for elderly
        warnings = ["Geriatric dosing - reduced by 10%"];
    }

    // Round and apply safety limits
    let final_dose = math.round(adjusted_dose);
    let minimum = math.max(final_dose, 10);    // Minimum 10mg
    let safe_dose = math.min(minimum, 100);    // Maximum 100mg

    // Create recommendation
    let recommendation = DoseRecommendation(
        patient.id,
        safe_dose,
        "Every 8 hours",
        warnings
    );

    return Ok(recommendation);
}
```

### Transpile to Python

```bash
asl build dosing.al --lang python -o dosing.py
```

### Use in CrewAI Agent

```python
from crewai import Agent, Task, Crew
from dosing import Patient, calculate_dose

# Create medical dosing agent
dosing_agent = Agent(
    role='Medical Dosing Specialist',
    goal='Calculate safe medication doses',
    backstory='I use the AL dosing contract for consistent calculations',
    verbose=True
)

# Create task
patient = Patient(id=1, weight=70.0, age=45)
result = calculate_dose(patient, "Medication-X")

if result.is_ok():
    recommendation = result.value
    print(f"Dose: {recommendation.dose_mg}mg")
    print(f"Frequency: {recommendation.frequency}")
else:
    print(f"Error: {result.error}")
```

**Key benefit:** The exact same contract can be used by a JavaScript/LangGraph agent, and both agents will calculate **identical doses**. No drift, no ambiguity.

---

## What's New in v0.1.6 - Zero Manual Fixes!

Previous versions required manual imports. **v0.1.6 eliminates this completely.**

### Before v0.1.6:
```python
# Generated code - REQUIRED MANUAL FIX:
# from assertlang.runtime import Ok, Error, Result, al_math as math

def calculate(x):
    return math.round(x)  # ❌ NameError: math not defined
```

### After v0.1.6:
```python
# Generated by AssertLang v0.1.6
# Source: example.al
# DO NOT EDIT - Regenerate from source instead

from assertlang.runtime import Ok, Error, Result, al_math as math

def calculate(x):
    return math.round(x)  # ✅ Works perfectly!
```

**The transpiler now:**
1. Scans your contract for module usage (math, str, list)
2. Automatically imports only what you need
3. Generates production-ready code with zero manual intervention
4. Includes version headers for tracking

---

## CLI Reference

### Build Command

```bash
asl build <input_file> --lang <language> -o <output_file>
```

**Options:**
- `<input_file>` - Path to your .al contract file
- `--lang <language>` - Target language (python, javascript, typescript, go, rust, csharp)
- `-o <output_file>` - Output file path
- `--help` - Show help

**Examples:**
```bash
# Python
asl build contract.al --lang python -o output.py

# JavaScript
asl build contract.al --lang javascript -o output.js

# Multiple files
asl build contracts/*.al --lang python -o generated/
```

### Version Command

```bash
asl --version
```

### Help Command

```bash
asl --help
asl build --help
```

---

## Integration with Agent Frameworks

### CrewAI (Python)

```python
from crewai import Agent, Task, Crew
from my_contract import my_function  # Generated from AL

agent = Agent(
    role='Contract Executor',
    goal='Execute AL contract consistently',
    backstory='I use AL contracts for deterministic behavior'
)

task = Task(
    description='Execute contract',
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

### LangGraph (JavaScript)

```javascript
const { my_function } = require('./my_contract');  // Generated from AL

const graph = new StateGraph({
  channels: {
    messages: messagesChannel,
  },
})
  .addNode("execute_contract", async (state) => {
    const result = my_function(state.input);
    return { messages: [result] };
  });
```

### AutoGen (Python)

```python
from autogen import Agent
from my_contract import my_function  # Generated from AL

agent = Agent(
    name="contract_executor",
    system_message="I execute AL contracts",
    llm_config=llm_config
)

result = my_function(input_data)
```

---

## Testing Your Contracts

### Write Unit Tests

```python
# test_contract.py
import pytest
from my_contract import greet, validate_email

def test_greet_with_name():
    assert greet("Alice") == "Hello, Alice!"

def test_greet_empty_name():
    assert greet("") == "Hello, Guest!"

def test_validate_email_valid():
    result = validate_email("user@example.com")
    assert result.is_ok()
    assert result.value == "user@example.com"

def test_validate_email_invalid():
    result = validate_email("invalid-email")
    assert result.is_error()
    assert "missing @" in result.error
```

### Run Tests

```bash
pytest test_contract.py -v
```

---

## Best Practices

### 1. Use Strong Types

```al
// ✅ Good - Explicit types
function calculate(x: float, y: float) -> float {
    return x + y;
}

// ❌ Avoid - Ambiguous types
function calculate(x, y) {
    return x + y;
}
```

### 2. Validate Inputs

```al
function process_user(name: string, age: int) -> Result<User, string> {
    // Validate inputs
    if (str.length(name) < 1) {
        return Error("Name cannot be empty");
    }

    if (age < 0 || age > 150) {
        return Error("Invalid age");
    }

    // Process...
    return Ok(User(name, age));
}
```

### 3. Use Descriptive Names

```al
// ✅ Good - Clear intent
function calculate_patient_dose(weight: float, age: int) -> float {
    let base_dose = weight * 1.5;
    return base_dose;
}

// ❌ Avoid - Unclear
function calc(w: float, a: int) -> float {
    let d = w * 1.5;
    return d;
}
```

### 4. Document Complex Logic

```al
function adjust_dose_for_age(base_dose: float, age: int) -> float {
    // Pediatric patients (< 18) receive 80% of adult dose
    // per clinical guidelines section 4.2.1
    if (age < 18) {
        return base_dose * 0.8;
    }

    // Geriatric patients (> 65) receive 90% of adult dose
    // to account for reduced metabolism
    if (age > 65) {
        return base_dose * 0.9;
    }

    return base_dose;
}
```

### 5. Use Result Types for Operations That Can Fail

```al
function divide(a: float, b: float) -> Result<float, string> {
    if (b == 0) {
        return Error("Division by zero");
    }
    return Ok(a / b);
}
```

---

## Troubleshooting

### Issue: "asl: command not found"

**Solution:** Ensure AssertLang is installed and in your PATH:
```bash
pip install --upgrade assertlang
which asl  # Should show the path to asl
```

### Issue: "ModuleNotFoundError: No module named 'assertlang.runtime'"

**Solution:** The runtime library should be installed automatically with AssertLang. Try:
```bash
pip install --upgrade assertlang
python -c "from assertlang.runtime import Ok, Error, Result"  # Test import
```

### Issue: "NameError: name 'math' is not defined" in generated Python code

**Solution:** Upgrade to v0.1.6 or newer:
```bash
pip install --upgrade assertlang
asl --version  # Should be v0.1.6 or higher
```

### Issue: Generated code doesn't match expected behavior

**Solution:** Check the transpiled code:
```bash
# Regenerate with verbose output
asl build contract.al --lang python -o output.py
cat output.py  # Inspect generated code
```

---

## Next Steps

1. **Try the Examples** - See [examples/agent_coordination/](../examples/agent_coordination/) for complete working examples
2. **Read the Type System Docs** - See [docs/TYPE_SYSTEM.md](TYPE_SYSTEM.md) for advanced type features
3. **Explore Multi-Agent Coordination** - See how CrewAI and LangGraph agents coordinate using AL contracts
4. **Join the Community** - Open issues, ask questions, contribute: [GitHub Issues](https://github.com/AssertLang/AssertLang/issues)

---

## Support and Resources

- **Documentation:** [GitHub Wiki](https://github.com/AssertLang/AssertLang/wiki)
- **Examples:** [examples/](../examples/)
- **Issues:** [GitHub Issues](https://github.com/AssertLang/AssertLang/issues)
- **Discussions:** [GitHub Discussions](https://github.com/AssertLang/AssertLang/discussions)
- **Release Notes:** [CHANGELOG.md](../CHANGELOG.md)
- **v0.1.6 Release:** [Release v0.1.6](https://github.com/AssertLang/AssertLang/releases/tag/v0.1.6)

---

## Contributing

Found a bug? Have a feature request? Want to contribute?

- **Report Bugs:** [Open an issue](https://github.com/AssertLang/AssertLang/issues/new)
- **Request Features:** [Start a discussion](https://github.com/AssertLang/AssertLang/discussions)
- **Contribute Code:** See [CONTRIBUTING.md](../CONTRIBUTING.md) (if available)

---

**Ready to build deterministic multi-agent systems?** 🚀

```bash
pip install assertlang
asl build your_contract.al --lang python -o output.py
```

Welcome to AssertLang!
