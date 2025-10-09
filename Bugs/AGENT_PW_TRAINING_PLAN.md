# Agent PW Training Plan - CC-Agents System

**Date:** 2025-10-08
**Status:** Ready to deploy
**Purpose:** Train all 11 specialist agents to code in PW as primary language

---

## Training Objectives

By completion, each agent should:
1. **Code solutions in .pw first** (not Python/Go/etc)
2. **Use full PW language features** (classes, loops, error handling)
3. **Learn PW idioms** via Python → PW conversion
4. **Report .pw artifacts** to users (universal source)
5. **Provide feedback** to PW developer (David) on limitations

---

## Training Method: Learn by Converting

**Recommended by David (PW creator):**

### Step 1: Write in Familiar Language
```python
# Example: Write Python solution
def calculate_discount(price, percent):
    discount = price * (percent / 100)
    return price - discount

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def apply_discount(self, percent):
        return calculate_discount(self.price, percent)
```

### Step 2: Convert to PW
```bash
# Use reverse parser
cd /Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/promptware
python3 -c "
from reverse_parsers.python_parser import PythonReverseParser

parser = PythonReverseParser()
agent = parser.parse_file('your_solution.py')
print(agent)
"
```

### Step 3: Study PW Output
```pw
// Observe PW idioms
function calculate_discount(price: float, percent: float) -> float {
    let discount = price * (percent / 100.0);
    return price - discount;
}

class Product {
    name: string;
    price: float;

    constructor(name: string, price: float) {
        self.name = name;
        self.price = price;
    }

    function apply_discount(percent: float) -> float {
        return calculate_discount(self.price, percent);
    }
}
```

### Step 4: Build Pattern Library
- Note differences (`: type` annotations, `self.` required, etc.)
- Collect common patterns
- Build intuition for writing PW directly

---

## Training Exercises by Agent

### SECURITY (Yuki Tanaka)
**Exercise:** Authentication system

**Python version:**
```python
def hash_password(password):
    # Hashing logic
    return hashed

def verify_password(password, hashed):
    # Verification logic
    return is_valid

class AuthManager:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        hashed = hash_password(password)
        self.users[username] = hashed
        return True

    def login(self, username, password):
        if username not in self.users:
            return False
        return verify_password(password, self.users[username])
```

**Task:** Convert to PW, study output, write improved version directly in PW

### CODER (Alex Rivera)
**Exercise:** Algorithm implementation

**Python version:**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Task:** Convert to PW, note loop patterns, write sorting algorithm in PW

### DATA (Sarah Kim)
**Exercise:** Data processing pipeline

**Python version:**
```python
class DataProcessor:
    def __init__(self):
        self.data = []

    def load(self, items):
        self.data = items

    def filter(self, condition):
        return [item for item in self.data if condition(item)]

    def transform(self, func):
        return [func(item) for item in self.data]

    def aggregate(self, func):
        result = None
        for item in self.data:
            result = func(result, item) if result else item
        return result
```

**Task:** Convert to PW, learn for-in loops, write analytics in PW

### BACKEND (Priya Sharma)
**Exercise:** API server

**Python version:**
```python
class APIServer:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler):
        self.routes[path] = handler

    def handle_request(self, path, data):
        if path not in self.routes:
            return {"error": "Not found"}
        return self.routes[path](data)
```

**Task:** Convert to PW, study maps, write REST API in PW

### FRONTEND (Riley Chen)
**Exercise:** Form validation

**Python version:**
```python
def validate_email(email):
    return "@" in email and "." in email

def validate_form(data):
    errors = []

    if not data.get("name"):
        errors.append("Name required")

    if not validate_email(data.get("email", "")):
        errors.append("Invalid email")

    if data.get("age", 0) < 18:
        errors.append("Must be 18+")

    return {"valid": len(errors) == 0, "errors": errors}
```

**Task:** Convert to PW, learn validation patterns, write form handler in PW

### DEVOPS (Jamal Washington)
**Exercise:** Deployment script

**Python version:**
```python
class DeploymentManager:
    def __init__(self):
        self.services = []

    def add_service(self, name, port):
        self.services.append({"name": name, "port": port, "status": "stopped"})

    def start_service(self, name):
        for service in self.services:
            if service["name"] == name:
                service["status"] = "running"
                return True
        return False

    def get_status(self):
        running = sum(1 for s in self.services if s["status"] == "running")
        return {"total": len(self.services), "running": running}
```

**Task:** Convert to PW, learn class patterns, write config manager in PW

### DATABASE (Marcus Chen)
**Exercise:** Query builder

**Python version:**
```python
class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.conditions = []

    def where(self, field, value):
        self.conditions.append((field, value))
        return self

    def build(self):
        query = f"SELECT * FROM {self.table}"
        if self.conditions:
            where_clauses = [f"{f} = {v}" for f, v in self.conditions]
            query += " WHERE " + " AND ".join(where_clauses)
        return query
```

**Task:** Convert to PW, learn builder pattern, write ORM in PW

### DOCS (Emma O'Brien)
**Exercise:** Documentation generator

**Python version:**
```python
class DocGenerator:
    def __init__(self):
        self.sections = []

    def add_section(self, title, content):
        self.sections.append({"title": title, "content": content})

    def generate(self):
        doc = "# Documentation\n\n"
        for section in self.sections:
            doc += f"## {section['title']}\n\n{section['content']}\n\n"
        return doc
```

**Task:** Convert to PW, learn string operations, write markdown generator in PW

### TESTER (Raj Patel)
**Exercise:** Test runner

**Python version:**
```python
class TestRunner:
    def __init__(self):
        self.tests = []
        self.results = []

    def add_test(self, name, func):
        self.tests.append({"name": name, "func": func})

    def run(self):
        for test in self.tests:
            try:
                test["func"]()
                self.results.append({"name": test["name"], "passed": True})
            except Exception as e:
                self.results.append({"name": test["name"], "passed": False, "error": str(e)})

    def report(self):
        passed = sum(1 for r in self.results if r["passed"])
        return {"total": len(self.results), "passed": passed, "failed": len(self.results) - passed}
```

**Task:** Convert to PW, learn try/catch, write assertion library in PW

### ARCHITECT (Dr. Elena Vasquez)
**Exercise:** System design DSL

**Python version:**
```python
class Component:
    def __init__(self, name, component_type):
        self.name = name
        self.type = component_type
        self.dependencies = []

    def depends_on(self, component):
        self.dependencies.append(component)

class System:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def validate(self):
        # Check for circular dependencies
        return {"valid": True, "errors": []}
```

**Task:** Convert to PW, learn graph structures, write architecture validator in PW

### AI (Dr. Amara Okafor)
**Exercise:** ML pipeline

**Python version:**
```python
class MLPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, name, transform):
        self.steps.append({"name": name, "transform": transform})

    def execute(self, data):
        result = data
        for step in self.steps:
            result = step["transform"](result)
        return result
```

**Task:** Convert to PW, learn pipeline patterns, write data transformer in PW

---

## Training Timeline

### Week 1: Foundation (All Agents)
- **Day 1-2:** Read PW_PROGRAMMING_GUIDE.md
- **Day 3-4:** Complete conversion exercises (Python → PW)
- **Day 5:** Write first solution directly in PW

### Week 2: Practice (All Agents)
- **Day 1-3:** Take real tasks, solve in PW first
- **Day 4-5:** Review peer PW code, provide feedback

### Week 3: Mastery (All Agents)
- **Day 1-5:** All new code in PW, compile to target as needed

---

## Success Metrics

**Agent is proficient when:**
- [ ] Codes solutions in .pw first (no Python intermediary)
- [ ] Uses classes, loops, error handling correctly
- [ ] Can read/write PW fluently
- [ ] Returns .pw artifacts to users
- [ ] Provides constructive feedback to PW developer

---

## Common PW Patterns (Reference)

### Pattern 1: CRUD Operations
```pw
class ItemManager {
    items: array;
    next_id: int;

    constructor() {
        self.items = [];
        self.next_id = 1;
    }

    function create(name: string) -> map {
        let item = {id: self.next_id, name: name};
        self.items = self.items + [item];
        self.next_id = self.next_id + 1;
        return item;
    }

    function get(id: int) -> map {
        for (item in self.items) {
            if (item.id == id) {
                return item;
            }
        }
        return null;
    }

    function update(id: int, name: string) -> bool {
        for (item in self.items) {
            if (item.id == id) {
                item.name = name;
                return true;
            }
        }
        return false;
    }

    function delete(id: int) -> bool {
        let new_items = [];
        let found = false;

        for (item in self.items) {
            if (item.id == id) {
                found = true;
                continue;
            }
            new_items = new_items + [item];
        }

        if (found) {
            self.items = new_items;
        }

        return found;
    }
}
```

### Pattern 2: Validation
```pw
function validate_input(data: map) -> map {
    let errors = [];

    if (data.name == "") {
        errors = errors + ["Name required"];
    }

    if (data.age < 0) {
        errors = errors + ["Age must be positive"];
    }

    return {
        valid: errors == [],
        errors: errors
    };
}
```

### Pattern 3: Error Handling
```pw
function safe_operation(input: string) -> map {
    try {
        if (input == "") {
            throw "Empty input";
        }

        // Process input
        let result = process(input);

        return {
            success: true,
            data: result
        };
    } catch (error) {
        return {
            success: false,
            error: error
        };
    }
}
```

---

## Support Resources

- **PW_PROGRAMMING_GUIDE.md** - Complete language reference
- **PW_AS_IR_ARCHITECTURE.md** - Architectural benefits
- **promptware/examples/** - Real working code
- **David (user)** - PW developer, accepts feedback

---

## Feedback Template for PW Issues

```markdown
## PW Feedback Report

**Agent:** [Your agent name]
**Date:** [Date]
**PW Version:** 2.1.0b1

### Issue Description
[What doesn't work as expected]

### PW Code Attempted
```pw
[Your PW code]
```

### Error/Behavior
[What happened]

### Expected Behavior
[What should happen]

### Suggested Fix
[How to fix - optional]

### Impact
[How this affects agent workflow]
```

---

**Status:** Ready for deployment
**Maintainer:** COORDINATOR agent
**Last Updated:** 2025-10-08
