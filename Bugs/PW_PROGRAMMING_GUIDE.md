# PW Programming Language - Complete Guide for Agents

**Date:** 2025-10-08
**Author:** COORDINATOR Agent
**Purpose:** Teach all CC-Agents how to code in raw PW (not just API definitions)

---

## Introduction

**PW (Promptware) is a REAL programming language** - not just a DSL for API definitions. It has:
- C-style syntax
- Functions, classes, control flow
- Type system (string, int, float, bool, arrays, maps)
- Cross-compilation to Python, Go, Rust, Node.js, C#

**You should write ALL code solutions in .pw first, then compile to target language.**

---

## Complete PW Syntax Reference

### 1. Comments

```pw
// Single-line comment

/*
  Multi-line comment
  Spans multiple lines
*/

# Python-style comment (also supported)
```

### 2. Variables

```pw
// Variable declaration with `let`
let name = "John";
let age = 30;
let price = 99.99;
let is_active = true;

// Type inference from value
let count = 0;        // int
let message = "Hi";   // string
let rate = 0.05;      // float
```

### 3. Types

**Primitive Types:**
- `string` - Text
- `int` - Integer numbers
- `float` - Floating-point numbers
- `bool` - true/false
- `void` - No return value

**Collection Types:**
- `array` - List of values
- `array<T>` - Typed array
- `map` - Key-value dictionary
- `map<K,V>` - Typed map

**Optional Types:**
- `string?` - Optional string
- `int?` - Optional integer

**Examples:**
```pw
let name: string = "Alice";
let age: int = 25;
let score: float = 95.5;
let active: bool = true;

let numbers: array<int> = [1, 2, 3, 4, 5];
let users: map<string, int> = {"alice": 1, "bob": 2};
```

### 4. Functions

**Basic Function:**
```pw
function functionName(param1: type, param2: type) -> returnType {
    // function body
    return value;
}
```

**Examples:**
```pw
// Simple function
function add(x: int, y: int) -> int {
    return x + y;
}

// Function with local variables
function calculate_tax(price: float, tax_rate: float) -> float {
    let tax = price * tax_rate;
    return price + tax;
}

// Function returning nothing
function log_message(message: string) -> void {
    // No return statement needed
}

// Function with multiple parameters
function create_user(name: string, age: int, email: string) -> map {
    return {
        name: name,
        age: age,
        email: email,
        created: true
    };
}
```

### 5. Control Flow

**If Statements:**
```pw
if (condition) {
    // code when true
}

if (condition) {
    // code when true
} else {
    // code when false
}

if (condition1) {
    // code when condition1 true
} else if (condition2) {
    // code when condition2 true
} else {
    // code when all false
}
```

**Examples:**
```pw
function max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function classify_age(age: int) -> string {
    if (age < 18) {
        return "minor";
    } else if (age < 65) {
        return "adult";
    } else {
        return "senior";
    }
}
```

**While Loops:**
```pw
while (condition) {
    // loop body
}
```

**Example:**
```pw
function count_to_n(n: int) -> int {
    let counter = 0;
    while (counter < n) {
        counter = counter + 1;
    }
    return counter;
}
```

**For Loops (C-style):**
```pw
for (let i = 0; i < 10; i = i + 1) {
    // loop body
}
```

**Example:**
```pw
function sum_to_n(n: int) -> int {
    let sum = 0;
    for (let i = 1; i <= n; i = i + 1) {
        sum = sum + i;
    }
    return sum;
}

function factorial(n: int) -> int {
    let result = 1;
    for (let i = 2; i <= n; i = i + 1) {
        result = result * i;
    }
    return result;
}
```

**For-In Loops:**
```pw
for (item in collection) {
    // process item
}
```

**Example:**
```pw
function sum_array(numbers: array<int>) -> int {
    let sum = 0;
    for (num in numbers) {
        sum = sum + num;
    }
    return sum;
}

function find_user(users: array, target_id: int) -> map {
    for (user in users) {
        if (user.id == target_id) {
            return user;
        }
    }
    return {};
}
```

**Loop Control:**
```pw
// Break - exit loop early
for (let i = 0; i < 100; i = i + 1) {
    if (found) {
        break;  // Exit loop
    }
}

// Continue - skip to next iteration
for (let i = 0; i < 100; i = i + 1) {
    if (skip_this) {
        continue;  // Skip rest of loop body
    }
    // Process
}
```

**Example:**
```pw
function find_first_positive(numbers: array<int>) -> int {
    for (num in numbers) {
        if (num > 0) {
            return num;  // Early return
        }
    }
    return -1;  // Not found
}

function count_evens(numbers: array<int>) -> int {
    let count = 0;
    for (num in numbers) {
        if (num % 2 != 0) {
            continue;  // Skip odd numbers
        }
        count = count + 1;
    }
    return count;
}

### 6. Classes

**Class Definition:**
```pw
class ClassName {
    // Properties
    property1: type;
    property2: type;

    // Constructor
    constructor(param1: type, param2: type) {
        self.property1 = param1;
        self.property2 = param2;
    }

    // Methods
    function methodName(param: type) -> returnType {
        // method body
        return value;
    }
}
```

**Complete Example:**
```pw
class TodoItem {
    id: int;
    title: string;
    description: string;
    completed: bool;
    priority: int;

    constructor(
        id: int,
        title: string,
        description: string,
        priority: int
    ) {
        self.id = id;
        self.title = title;
        self.description = description;
        self.completed = false;
        self.priority = priority;
    }

    function mark_completed() -> void {
        self.completed = true;
    }

    function mark_incomplete() -> void {
        self.completed = false;
    }

    function update_title(new_title: string) -> void {
        self.title = new_title;
    }

    function to_map() -> map {
        return {
            id: self.id,
            title: self.title,
            description: self.description,
            completed: self.completed,
            priority: self.priority
        };
    }
}
```

**Using Classes:**
```pw
function create_todo_example() -> TodoItem {
    // Create instance
    let todo = TodoItem(
        1,
        "Write documentation",
        "Complete the API docs",
        1
    );

    // Call methods
    todo.mark_completed();
    todo.update_title("Updated title");

    return todo;
}
```

### 7. Arrays

**Array Creation:**
```pw
// Empty array
let numbers = [];

// Array with values
let numbers = [1, 2, 3, 4, 5];

// Typed array
let names: array<string> = ["Alice", "Bob", "Charlie"];
```

**Array Operations:**
```pw
// Access element
let first = numbers[0];

// Concatenation
let combined = array1 + array2;

// Length (conceptual - use fixed bounds in loops)
let size = 0;
while (size < 100) {
    if (size < numbers.length) {
        // Process numbers[size]
    }
    size = size + 1;
}
```

**Example:**
```pw
function find_max(numbers: array<int>) -> int {
    let max_val = numbers[0];
    let index = 1;

    while (index < 100) {
        if (index < numbers.length) {
            if (numbers[index] > max_val) {
                max_val = numbers[index];
            }
        }
        index = index + 1;
    }

    return max_val;
}
```

### 8. Maps/Dictionaries

**Map Creation:**
```pw
// Empty map
let user = {};

// Map with values
let user = {
    name: "Alice",
    age: 30,
    email: "alice@example.com"
};

// Typed map
let scores: map<string, int> = {
    "alice": 95,
    "bob": 87,
    "charlie": 92
};
```

**Map Access:**
```pw
let name = user.name;
let age = user["age"];
```

**Example:**
```pw
function create_user_profile(
    name: string,
    age: int,
    email: string
) -> map {
    return {
        name: name,
        age: age,
        email: email,
        created_at: "2025-10-08",
        is_active: true
    };
}
```

### 9. Operators

**Arithmetic:**
```pw
+ (addition)
- (subtraction)
* (multiplication)
/ (division)
% (modulo)
```

**Comparison:**
```pw
== (equal)
!= (not equal)
> (greater than)
< (less than)
>= (greater than or equal)
<= (less than or equal)
```

**Logical:**
```pw
&& (and)
|| (or)
! (not)
```

**Examples:**
```pw
let sum = a + b;
let is_equal = x == y;
let is_valid = age >= 18 && age < 65;
let should_process = is_active && !is_deleted;
```

### 10. String Operations

```pw
// String concatenation
let full_name = first_name + " " + last_name;

// String in conditionals
if (status == "active") {
    // ...
}

// String comparison
if (name == "admin") {
    // Handle admin
}

// Empty string check
if (text != "") {
    // Text has content
}
```

**Note:** PW strings are primitives. For advanced operations (.length, .substring, .toUpperCase), compile to target language and use native string methods.

### 11. Error Handling

**Try/Catch:**
```pw
try {
    // Risky code that might fail
    let result = divide(10, 0);
} catch (error) {
    // Handle the error
    return -1;
}
```

**Example:**
```pw
function safe_divide(a: int, b: int) -> float {
    try {
        if (b == 0) {
            throw "Division by zero";
        }
        return a / b;
    } catch (error) {
        return 0.0;
    }
}

function parse_user_input(input: string) -> map {
    try {
        // Attempt to process input
        if (input == "") {
            throw "Empty input";
        }
        return {
            success: true,
            data: input
        };
    } catch (error) {
        return {
            success: false,
            error: error
        };
    }
}
```

### 12. Null Values

```pw
// Null assignment
let user = null;
let data: string? = null;  // Optional type

// Null check
if (user != null) {
    // User exists
}

// Default with null check
function get_name(user: map) -> string {
    if (user == null) {
        return "Unknown";
    }
    return user.name;
}
```

**Null translates to:**
- Python: `None`
- Go: `nil`
- Rust: `None`
- TypeScript: `null`
- C#: `null`

---

## Common Patterns

### Pattern 1: Data Validation

```pw
function validate_email(email: string) -> bool {
    // Simple validation
    let has_at = false;
    let has_dot = false;

    // Check for @ and .
    if (email != "") {
        has_at = true;  // Simplified
        has_dot = true;  // Simplified
    }

    return has_at && has_dot;
}

function validate_age(age: int) -> bool {
    return age >= 0 && age <= 150;
}

function validate_user(name: string, age: int, email: string) -> map {
    let errors = [];

    if (name == "") {
        errors = errors + ["Name is required"];
    }

    if (!validate_age(age)) {
        errors = errors + ["Invalid age"];
    }

    if (!validate_email(email)) {
        errors = errors + ["Invalid email"];
    }

    return {
        valid: errors == [],
        errors: errors
    };
}
```

### Pattern 2: Data Transformation

```pw
function calculate_discount(price: float, discount_percent: float) -> float {
    let discount_amount = price * (discount_percent / 100.0);
    return price - discount_amount;
}

function apply_tax(price: float, tax_rate: float) -> float {
    let tax_amount = price * tax_rate;
    return price + tax_amount;
}

function calculate_final_price(
    base_price: float,
    discount: float,
    tax_rate: float
) -> float {
    let after_discount = calculate_discount(base_price, discount);
    let final_price = apply_tax(after_discount, tax_rate);
    return final_price;
}
```

### Pattern 3: List Processing

```pw
function filter_active_users(users: array) -> array {
    let active = [];
    let index = 0;

    while (index < 100) {
        if (index < users.length) {
            let user = users[index];
            if (user.is_active) {
                active = active + [user];
            }
        }
        index = index + 1;
    }

    return active;
}

function sum_prices(items: array) -> float {
    let total = 0.0;
    let index = 0;

    while (index < 100) {
        if (index < items.length) {
            total = total + items[index].price;
        }
        index = index + 1;
    }

    return total;
}
```

### Pattern 4: Builder Pattern

```pw
class UserBuilder {
    name: string;
    age: int;
    email: string;
    role: string;

    constructor() {
        self.name = "";
        self.age = 0;
        self.email = "";
        self.role = "user";
    }

    function set_name(name: string) -> UserBuilder {
        self.name = name;
        return self;
    }

    function set_age(age: int) -> UserBuilder {
        self.age = age;
        return self;
    }

    function set_email(email: string) -> UserBuilder {
        self.email = email;
        return self;
    }

    function set_role(role: string) -> UserBuilder {
        self.role = role;
        return self;
    }

    function build() -> map {
        return {
            name: self.name,
            age: self.age,
            email: self.email,
            role: self.role
        };
    }
}

// Usage
function create_admin_user() -> map {
    let builder = UserBuilder();
    return builder
        .set_name("Admin")
        .set_age(35)
        .set_email("admin@example.com")
        .set_role("admin")
        .build();
}
```

---

## Best Practices for Agents

### 1. Always Type Your Functions

```pw
// ✅ GOOD - Explicit types
function calculate_total(price: float, quantity: int) -> float {
    return price * quantity;
}

// ❌ BAD - Missing types (won't compile)
function calculate_total(price, quantity) {
    return price * quantity;
}
```

### 2. Use Meaningful Names

```pw
// ✅ GOOD
function calculate_user_discount(user_age: int, is_member: bool) -> float {
    if (is_member) {
        return 0.15;
    } else if (user_age >= 65) {
        return 0.10;
    } else {
        return 0.0;
    }
}

// ❌ BAD
function calc(a: int, b: bool) -> float {
    if (b) {
        return 0.15;
    }
    return 0.0;
}
```

### 3. Keep Functions Small and Focused

```pw
// ✅ GOOD - Single responsibility
function validate_email(email: string) -> bool {
    return email != "" && email != "invalid";
}

function validate_age(age: int) -> bool {
    return age >= 0 && age <= 150;
}

function validate_user(email: string, age: int) -> bool {
    return validate_email(email) && validate_age(age);
}

// ❌ BAD - Too much in one function
function validate_everything(email: string, age: int, name: string, address: string) -> bool {
    // 50 lines of validation logic...
}
```

### 4. Use Classes for Related Data and Behavior

```pw
// ✅ GOOD - Class encapsulates behavior
class ShoppingCart {
    items: array;
    total: float;

    constructor() {
        self.items = [];
        self.total = 0.0;
    }

    function add_item(item: map) -> void {
        self.items = self.items + [item];
        self.total = self.total + item.price;
    }

    function get_total() -> float {
        return self.total;
    }
}

// ❌ BAD - Functions with loose data
function add_item_to_cart(items: array, item: map) -> array {
    return items + [item];
}

function calculate_cart_total(items: array) -> float {
    // Calculate total...
}
```

### 5. Handle Edge Cases

```pw
// ✅ GOOD - Handles zero denominator
function divide(numerator: int, denominator: int) -> float {
    if (denominator != 0) {
        return numerator / denominator;
    } else {
        return 0.0;  // Or return error
    }
}

// ❌ BAD - No error handling
function divide(numerator: int, denominator: int) -> float {
    return numerator / denominator;  // Will crash if denominator is 0
}
```

---

## Complete Example: Task Manager

```pw
// ============================================================================
// Task Manager - Complete PW Application
// ============================================================================

class Task {
    id: int;
    title: string;
    description: string;
    status: string;
    priority: int;
    created_at: string;

    constructor(id: int, title: string, description: string, priority: int) {
        self.id = id;
        self.title = title;
        self.description = description;
        self.status = "pending";
        self.priority = priority;
        self.created_at = "2025-10-08";
    }

    function complete() -> void {
        self.status = "completed";
    }

    function cancel() -> void {
        self.status = "cancelled";
    }

    function update_priority(new_priority: int) -> void {
        self.priority = new_priority;
    }

    function to_json() -> map {
        return {
            id: self.id,
            title: self.title,
            description: self.description,
            status: self.status,
            priority: self.priority,
            created_at: self.created_at
        };
    }
}

class TaskManager {
    tasks: array;
    next_id: int;

    constructor() {
        self.tasks = [];
        self.next_id = 1;
    }

    function create_task(
        title: string,
        description: string,
        priority: int
    ) -> Task {
        let task = Task(self.next_id, title, description, priority);
        self.tasks = self.tasks + [task];
        self.next_id = self.next_id + 1;
        return task;
    }

    function get_task(id: int) -> map {
        let index = 0;
        while (index < 1000) {
            if (index < self.tasks.length) {
                let task = self.tasks[index];
                if (task.id == id) {
                    return task.to_json();
                }
            }
            index = index + 1;
        }
        return {};
    }

    function get_all_tasks() -> array {
        let result = [];
        let index = 0;

        while (index < 1000) {
            if (index < self.tasks.length) {
                result = result + [self.tasks[index].to_json()];
            }
            index = index + 1;
        }

        return result;
    }

    function get_pending_tasks() -> array {
        let pending = [];
        let index = 0;

        while (index < 1000) {
            if (index < self.tasks.length) {
                let task = self.tasks[index];
                if (task.status == "pending") {
                    pending = pending + [task.to_json()];
                }
            }
            index = index + 1;
        }

        return pending;
    }

    function complete_task(id: int) -> bool {
        let index = 0;
        while (index < 1000) {
            if (index < self.tasks.length) {
                let task = self.tasks[index];
                if (task.id == id) {
                    task.complete();
                    return true;
                }
            }
            index = index + 1;
        }
        return false;
    }

    function get_stats() -> map {
        let total = 0;
        let completed = 0;
        let pending = 0;
        let cancelled = 0;
        let index = 0;

        while (index < 1000) {
            if (index < self.tasks.length) {
                total = total + 1;
                let task = self.tasks[index];

                if (task.status == "completed") {
                    completed = completed + 1;
                } else if (task.status == "pending") {
                    pending = pending + 1;
                } else if (task.status == "cancelled") {
                    cancelled = cancelled + 1;
                }
            }
            index = index + 1;
        }

        return {
            total: total,
            completed: completed,
            pending: pending,
            cancelled: cancelled
        };
    }
}

// Main application
function main() -> map {
    let manager = TaskManager();

    // Create some tasks
    let task1 = manager.create_task(
        "Write documentation",
        "Complete API docs",
        1
    );

    let task2 = manager.create_task(
        "Fix bug",
        "Handle edge case in parser",
        3
    );

    let task3 = manager.create_task(
        "Add feature",
        "Implement class support",
        2
    );

    // Complete a task
    let completed = manager.complete_task(1);

    // Get statistics
    let stats = manager.get_stats();

    return stats;
}
```

---

## Compilation

**Compile to any language:**

```bash
# Python
promptware build task_manager.pw --lang python -o task_manager.py

# Go
promptware build task_manager.pw --lang go -o task_manager.go

# Rust
promptware build task_manager.pw --lang rust -o task_manager.rs

# Node.js
promptware build task_manager.pw --lang nodejs -o task_manager.ts

# C#
promptware build task_manager.pw --lang csharp -o TaskManager.cs
```

---

## Workflow for Agents

**When given a coding task:**

1. **Design in PW first** - Think in language-agnostic terms
2. **Write complete .pw code** - Use full language features
3. **Test compilation** - `promptware validate your_code.pw`
4. **Generate target** - `promptware build your_code.pw --lang python`
5. **Report .pw file** - Give user the universal source

**Example:**

```
User: "Build a calculator"

Agent workflow:
1. Write calculator.pw (178 lines)
2. Validate: promptware validate calculator.pw ✅
3. Generate Python: promptware build calculator.pw --lang python
4. Return calculator.pw to user (they can compile to any language)
```

---

## Summary

**PW is a REAL programming language with:**
- ✅ Functions with type signatures
- ✅ Classes with constructors and methods
- ✅ Control flow (if/else, while loops)
- ✅ Arrays and maps
- ✅ Operators (arithmetic, comparison, logical)
- ✅ Type system (primitives + collections + optionals)
- ✅ Cross-compilation to 5 languages

**Agents should:**
1. Code in PW for ALL solutions
2. Use proper types, functions, and classes
3. Follow best practices
4. Return .pw files as universal IR

**This is the future of multi-agent code generation.**

---

**Created by:** COORDINATOR Agent
**For:** All CC-Agents specialists
**Purpose:** Universal coding standard
**Status:** Production guide for promptware v2.1.0b1
