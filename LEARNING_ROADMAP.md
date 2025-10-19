# AssertLang Learning Roadmap
## A Systematic, Research-Based Curriculum for Teaching AssertLang

**Version:** 1.0
**Last Updated:** October 19, 2025
**Based On:** Educational research, cognitive load theory, and real-world validation (67/67 enterprise tests)

---

## Executive Summary

This roadmap provides a **systematic, pedagogically sound approach** to teaching AssertLang from absolute beginner to production deployment. It's based on:

1. **Cognitive Load Theory** - Reducing mental burden through scaffolding
2. **Worked Examples Method** - Learning from solutions before problem-solving
3. **Project-Based Learning** - Building real applications progressively
4. **Spaced Repetition** - Reinforcing concepts across multiple lessons
5. **Immediate Feedback** - Error-driven learning from compiler messages

**Target Outcomes:**
- ✅ Beginners can write production-ready AssertLang code
- ✅ Graduates can replicate testing agent's 680-line medical system
- ✅ Users understand when/why to use AssertLang vs other languages
- ✅ Developers can deploy to production environments confidently

---

## Research Foundation

### Pedagogical Principles Applied

#### 1. Cognitive Load Theory (Sweller, 1988; Updated 2024)

**Principle:** Novice programmers have limited working memory. Overwhelming them with syntax, logic, and problem-solving simultaneously causes learning failure.

**Application:**
- **Worked Examples First** - Show complete solutions before asking learners to code
- **Faded Scaffolding** - Start with fill-in-the-blanks, progress to blank slate
- **Chunking** - Group related concepts (e.g., all type system in one module)
- **Schema Building** - Explicitly connect new concepts to prior knowledge

**Evidence:** 2024 study shows worked examples reduce cognitive load by 35% vs problem-solving (Enhancing Teaching Strategies, MDPI Education Sciences)

#### 2. Active Learning (Freeman et al., 2014)

**Principle:** Students learn by doing, not just watching.

**Application:**
- **Immediate Practice** - Every concept has hands-on exercise within 3 minutes
- **Interactive Playground** - Live code execution with instant feedback
- **Build Real Projects** - 4 cumulative projects throughout curriculum
- **Pair Programming Simulations** - Collaborative problem-solving exercises

#### 3. Parsons Problems (Morrison et al., 2016)

**Principle:** Before writing code from scratch, learners benefit from assembling pre-written code blocks.

**Application:**
- **Early Lessons** - Give learners scrambled code blocks to arrange
- **Focus on Logic** - Removes syntax burden, focuses on control flow
- **Progressive Difficulty** - Add blank lines for learners to fill in

**Example:**
```
Arrange these lines to create a valid AssertLang function:
[ ] return Ok(result);
[ ] function divide(x: float, y: float) -> Result {
[ ]     return Error("Cannot divide by zero");
[ ]     let result = x / y;
[ ]     if (y == 0.0) {
[ ] }
[ ]     }
```

#### 4. Error-Driven Learning (Becker & Parker, 2011)

**Principle:** Compiler errors are learning opportunities, not failures.

**Application:**
- **Intentional Errors** - Lessons include broken code to fix
- **Error Message Explanations** - Teach how to read AL compiler errors
- **Common Mistakes Library** - Catalog of typical beginner errors
- **Fix-It Challenges** - Present buggy code and ask learners to debug

#### 5. Spaced Repetition (Ebbinghaus, 1885; Modern CS Ed 2024)

**Principle:** Revisiting concepts at increasing intervals improves retention.

**Application:**
- **Spiral Curriculum** - Introduce Result types early, deepen in 3 later modules
- **Cumulative Projects** - Each project uses ALL previously learned concepts
- **Review Modules** - Every 5 lessons, a synthesis/review lesson
- **Real-World Callbacks** - Reference earlier lessons in advanced topics

---

## Learning Objectives Framework

### Bloom's Taxonomy Applied to AssertLang

#### Level 1: Remember (Lessons 1-5)
- **Recognize** AL syntax vs other languages
- **Recall** basic types (int, float, string, bool)
- **List** when to use AssertLang vs Python/JavaScript

#### Level 2: Understand (Lessons 6-10)
- **Explain** why Result types prevent crashes
- **Describe** how transpilation works (AL → Python/JS)
- **Interpret** compiler error messages

#### Level 3: Apply (Lessons 11-18)
- **Use** math, str, list stdlib modules
- **Implement** classes with `__init__()` and methods
- **Execute** CLI commands (install, build, deploy)

#### Level 4: Analyze (Lessons 19-24)
- **Compare** AL contracts vs manual multi-language coding
- **Differentiate** when to use Ok() vs Error()
- **Examine** generated Python/JS code for quality

#### Level 5: Evaluate (Lessons 25-28)
- **Critique** existing validation logic for AL conversion
- **Judge** production-readiness (Python vs JS/TS)
- **Assess** when AssertLang adds value vs overhead

#### Level 6: Create (Lessons 29-32)
- **Design** multi-agent coordination contracts
- **Build** 680-line production application
- **Develop** framework-agnostic business logic

---

## Curriculum Structure

### Overview: 4 Stages, 32 Lessons, ~8 Hours

| Stage | Lessons | Time | Focus | Outcome |
|-------|---------|------|-------|---------|
| **Foundation** | 1-8 | 90 min | Syntax, types, control flow | Write basic functions |
| **Core Skills** | 9-18 | 150 min | OOP, stdlib, Result types | Write production code |
| **Production** | 19-24 | 120 min | CLI, deployment, debugging | Deploy real applications |
| **Mastery** | 25-32 | 180 min | Multi-agent, patterns, scale | Build enterprise systems |

---

## Stage 1: Foundation (Lessons 1-8)
### Goal: Write Basic AssertLang Functions with Confidence

**Learning Objectives:**
- Understand what AssertLang is and when to use it
- Write simple functions with parameters and return types
- Use basic control flow (if/else, loops)
- Understand strong typing

**Cognitive Load Strategy:** Maximum scaffolding, worked examples dominate

---

### Lesson 1: What is AssertLang? (8 minutes)

**Learning Objective:** Understand AssertLang's purpose and value proposition

**Content:**

#### 1.1 The Problem (2 min)
Show real-world pain point:
```
Scenario: You have a Python backend and JavaScript frontend.
Both need to validate email addresses identically.

Traditional approach:
✗ Write email validation twice
✗ Keep them in sync manually
✗ Debug subtle differences
✗ One breaks in production while the other works

AssertLang approach:
✓ Write validation once in AL
✓ Transpile to Python and JavaScript
✓ Guaranteed identical behavior
```

#### 1.2 How It Works (3 min)
Visual diagram + live demo:
```
Write Once:          Transpile:              Use Everywhere:
contract.al    →     asl build         →     Python, JS, TS,
                     (2 seconds)             Go, Rust, C#
```

**Live Demo:**
- Show 10-line AL contract
- Run `asl build` command
- Show generated Python and JavaScript side-by-side
- Highlight: identical logic, different syntax

#### 1.3 When to Use AssertLang (2 min)
Decision matrix:
```
✓ USE AssertLang when:
  - Multiple languages need same logic
  - Building multi-agent AI systems (CrewAI, LangGraph)
  - Need guaranteed deterministic behavior
  - Migrating between frameworks

✗ DON'T use AssertLang for:
  - Single-language projects
  - UI rendering logic
  - Framework-specific features
```

#### 1.4 Your First Look (1 min)
Show complete AL function:
```al
function greet(name: string) -> string {
    return "Hello, " + name + "!";
}
```

Point out:
- Familiar C-style syntax
- Strong typing (`name: string`)
- Return type annotation (`-> string`)
- Simple, readable

**Exercise:** None (absorb information)

**Assessment:** Quiz
1. What problem does AssertLang solve? (multiple choice)
2. True/False: AssertLang is good for UI rendering
3. How many languages can AL transpile to? (answer: 6)

**Mastery Criteria:** 3/3 correct answers

---

### Lesson 2: Your First Function (10 minutes)

**Learning Objective:** Write a working AssertLang function

**Cognitive Strategy:** Worked example → guided practice → independent practice

#### 2.1 Anatomy of a Function (3 min)

**Worked Example:**
```al
function calculateTax(price: float) -> float {
    let taxRate = 0.08;
    let tax = price * taxRate;
    return tax;
}
```

**Explanation:**
- `function` keyword starts function definition
- `calculateTax` is the function name (camelCase)
- `(price: float)` is parameter with type
- `-> float` is return type
- `{ ... }` contains function body
- `let` declares variables
- `return` sends value back

#### 2.2 Try It Yourself (3 min)

**Faded Worked Example:**
```al
function __________(age: int) -> int {
    let nextYear = ____ + 1;
    return nextYear;
}
```

Fill in:
1. Function name: `calculateNextAge`
2. Expression: `age`

**Interactive:** Code editor with hints, instant feedback

#### 2.3 Build from Scratch (4 min)

**Challenge:** Create a function that doubles a number

Requirements:
- Name: `double`
- Parameter: `x` of type `int`
- Returns: `int`
- Logic: multiply input by 2

**Scaffold Provided:**
```al
function double(_______________) {
    // Your code here
}
```

**Solution:**
```al
function double(x: int) -> int {
    return x * 2;
}
```

**Interactive Test:** Auto-run with test cases
- `double(5)` → expect 10
- `double(-3)` → expect -6
- `double(0)` → expect 0

**Mastery Criteria:** All 3 tests pass

---

### Lesson 3: Understanding Types (12 minutes)

**Learning Objective:** Use AssertLang's type system correctly

#### 3.1 The Big Four Primitive Types (5 min)

**Worked Examples:**
```al
// int - whole numbers
let age: int = 25;
let score: int = -10;

// float - decimal numbers
let price: float = 99.99;
let temperature: float = -273.15;

// string - text
let name: string = "Alice";
let message: string = "Hello, world!";

// bool - true/false
let isActive: bool = true;
let hasPermission: bool = false;
```

**Key Point:** AssertLang is **strongly typed** - once a variable has a type, it can't change.

**Common Error to Learn From:**
```al
let age: int = 25;
age = "twenty-five";  // ❌ ERROR: Cannot assign string to int
```

Compiler says: `Type mismatch: expected int, got string`

#### 3.2 Type Inference (3 min)

You can omit types when they're obvious:
```al
// Explicit types
let age: int = 25;
let price: float = 99.99;

// Type inference (compiler figures it out)
let age = 25;        // Inferred as int
let price = 99.99;   // Inferred as float
```

**Best Practice:** Use explicit types for:
- Function parameters (always required)
- Function return types (always required)
- Public variables/fields

#### 3.3 List Type (2 min)

```al
let scores: list = [95, 87, 92, 88];
let names: list = ["Alice", "Bob", "Charlie"];
let mixed: list = [1, "two", 3.0, true];  // Valid!
```

**Note:** AL lists can contain mixed types (like Python, unlike TypeScript)

#### 3.4 Practice (2 min)

**Challenge:** Declare variables with correct types

```al
// 1. Store your age
let ___ = ___;

// 2. Store your height in meters
let ___ = ___;

// 3. Store your name
let ___ = ___;

// 4. Store if you're a student
let ___ = ___;

// 5. Store your grades
let ___ = [___, ___, ___];
```

**Mastery Criteria:** Correct types for 5/5 variables

---

### Lesson 4: Function Parameters (10 minutes)

**Learning Objective:** Create functions with multiple parameters

#### 4.1 Single Parameter Review (2 min)
```al
function greet(name: string) -> string {
    return "Hello, " + name;
}
```

#### 4.2 Multiple Parameters (3 min)

**Worked Example:**
```al
function calculateArea(width: float, height: float) -> float {
    let area = width * height;
    return area;
}

// Usage
let roomArea = calculateArea(10.5, 8.0);  // 84.0
```

**Pattern:**
- Parameters separated by commas
- Each has own type annotation
- Order matters when calling function

#### 4.3 Mixed Parameter Types (2 min)

```al
function formatCurrency(amount: float, symbol: string) -> string {
    return symbol + str(amount);
}

formatCurrency(99.99, "$");  // "$99.99"
```

**Note:** `str()` converts float to string

#### 4.4 Practice: Build a Calculator Function (3 min)

**Challenge:** Create `add` function
- Parameters: `x: float`, `y: float`
- Returns: `float`
- Logic: sum of x and y

**Test Cases:**
- `add(5.0, 3.0)` → 8.0
- `add(-2.0, 10.0)` → 8.0
- `add(0.0, 0.0)` → 0.0

**Bonus Challenge:** Create `subtract`, `multiply`, `divide` functions

**Mastery Criteria:** 3/3 test cases pass

---

### Lesson 5: Making Decisions with If/Else (15 minutes)

**Learning Objective:** Implement conditional logic

#### 5.1 Simple If Statement (3 min)

**Worked Example:**
```al
function checkAge(age: int) -> string {
    if (age >= 18) {
        return "Adult";
    }
    return "Minor";
}
```

**Pattern:**
- `if (condition)` - condition must be bool
- `{ ... }` - code block executes if true
- No `else` needed if you return early

#### 5.2 If/Else (3 min)

```al
function getDiscount(age: int) -> float {
    if (age < 18) {
        return 0.10;  // 10% discount for minors
    } else {
        return 0.05;  // 5% discount for adults
    }
}
```

#### 5.3 If/Else If/Else Chain (4 min)

**Worked Example:**
```al
function gradeScore(score: int) -> string {
    if (score >= 90) {
        return "A";
    } else if (score >= 80) {
        return "B";
    } else if (score >= 70) {
        return "C";
    } else if (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}
```

#### 5.4 Comparison Operators (2 min)

```al
age >= 18   // Greater than or equal
score > 50  // Greater than
price <= 100  // Less than or equal
count < 10  // Less than
status == "active"  // Equal to
status != "inactive"  // Not equal to
```

#### 5.5 Logical Operators (3 min)

```al
// AND - both must be true
if (age >= 18 && hasLicense == true) {
    return "Can drive";
}

// OR - at least one must be true
if (isWeekend == true || isHoliday == true) {
    return "Day off";
}

// NOT - inverts bool
if (!isExpired) {
    return "Still valid";
}
```

**Practice:**

**Challenge:** Password strength checker

Requirements:
- Function name: `checkPasswordStrength`
- Parameter: `password: string`
- Returns: `string`
- Logic:
  - If length >= 12 → "Strong"
  - Else if length >= 8 → "Medium"
  - Else → "Weak"

**Hint:** Use `str.length(password)` to get length

**Mastery Criteria:** 3/3 test cases pass

---

### Lesson 6: Loops - Repeating Actions (15 minutes)

**Learning Objective:** Use for and while loops

#### 6.1 For Loop - Iterating Over Lists (5 min)

**Worked Example:**
```al
function sumScores(scores: list) -> int {
    let total = 0;
    for (score in scores) {
        total = total + score;
    }
    return total;
}

sumScores([95, 87, 92]);  // 274
```

**Pattern:**
- `for (item in list)` - iterate over each element
- `item` is current element (name it anything)
- Loop body executes once per element

#### 6.2 While Loop - Repeat Until Condition False (4 min)

```al
function countdown(n: int) -> int {
    while (n > 0) {
        n = n - 1;
    }
    return n;  // Always 0
}

countdown(5);  // Runs 5 times, returns 0
```

**Warning:** Ensure condition eventually becomes false, or loop runs forever!

#### 6.3 Building a List (3 min)

```al
function doubleNumbers(numbers: list) -> list {
    let result = [];
    for (num in numbers) {
        let doubled = num * 2;
        result.append(doubled);
    }
    return result;
}

doubleNumbers([1, 2, 3]);  // [2, 4, 6]
```

#### 6.4 Practice (3 min)

**Challenge:** Count evens

Requirements:
- Function: `countEvens(numbers: list) -> int`
- Count how many numbers are even
- Hint: `num % 2 == 0` checks if even

**Test Cases:**
- `countEvens([1, 2, 3, 4])` → 2
- `countEvens([1, 3, 5])` → 0
- `countEvens([2, 4, 6, 8])` → 4

**Mastery Criteria:** 3/3 tests pass

---

### Lesson 7: Comments and Documentation (8 minutes)

**Learning Objective:** Write clear, maintainable code

#### 7.1 Single-Line Comments (2 min)

```al
// This is a comment - compiler ignores it
function greet(name: string) -> string {
    return "Hello, " + name;  // Append name to greeting
}
```

#### 7.2 Multi-Line Comments (2 min)

```al
/*
 * Calculate the final price after applying discount
 * and adding tax.
 *
 * Parameters:
 *   price: Original price
 *   discount: Discount percentage (0.0 to 1.0)
 *   taxRate: Tax rate (0.0 to 1.0)
 */
function finalPrice(price: float, discount: float, taxRate: float) -> float {
    let discounted = price * (1.0 - discount);
    let withTax = discounted * (1.0 + taxRate);
    return withTax;
}
```

#### 7.3 When to Comment (2 min)

**Good comments:**
- Explain WHY, not WHAT
- Document complex business logic
- Warn about gotchas

**Bad comments:**
```al
// Adds x and y
function add(x: int, y: int) -> int {  // ❌ Obvious!
    return x + y;
}
```

**Good comments:**
```al
// Use 0.08 tax rate per California state law (2024)
let taxRate = 0.08;  // ✓ Explains context
```

#### 7.4 Practice (2 min)

Add helpful comments to this function:
```al
function calculateBMI(weight: float, height: float) -> float {
    let bmi = weight / (height * height);
    return bmi;
}
```

**Mastery Criteria:** Added at least 2 helpful comments

---

### Lesson 8: Foundation Review & Mini-Project (20 minutes)

**Learning Objective:** Synthesize Lessons 1-7 into working program

#### 8.1 Concept Review (5 min)

**Quiz:**
1. What are the 4 primitive types in AL?
2. How do you declare a function parameter?
3. What's the syntax for an if/else statement?
4. How do you iterate over a list?
5. When should you write comments?

**Mastery:** 4/5 correct

#### 8.2 Mini-Project: Grade Calculator (15 min)

**Requirements:**

Build a grade calculator with 3 functions:

**Function 1:** `calculateAverage(scores: list) -> float`
- Takes list of scores
- Returns average

**Function 2:** `determineLetterGrade(average: float) -> string`
- 90+ → "A"
- 80-89 → "B"
- 70-79 → "C"
- 60-69 → "D"
- Below 60 → "F"

**Function 3:** `formatResult(name: string, average: float, grade: string) -> string`
- Returns: "{name}: {average}% ({grade})"
- Example: "Alice: 87.5% (B)"

**Test Cases Provided:**
```al
let scores = [95, 87, 92, 78];
let avg = calculateAverage(scores);      // 88.0
let grade = determineLetterGrade(avg);   // "B"
let result = formatResult("Alice", avg, grade);  // "Alice: 88.0% (B)"
```

**Scaffolding:**
```al
function calculateAverage(scores: list) -> float {
    // Hint: Use a for loop to sum, then divide by count
    // Use list.length(scores) to get count
}

function determineLetterGrade(average: float) -> string {
    // Hint: Use if/else if chain
}

function formatResult(name: string, average: float, grade: string) -> string {
    // Hint: Concatenate strings with +
    // Convert float to string with str(average)
}
```

**Mastery Criteria:**
- ✅ All 3 functions implemented correctly
- ✅ All test cases pass
- ✅ Code includes helpful comments

**Graduation:** Can write basic AssertLang functions with types, control flow, and loops

---

## Stage 2: Core Skills (Lessons 9-18)
### Goal: Write Production-Ready AssertLang Code

**Learning Objectives:**
- Master Result type for error handling
- Use standard library (math, str, list)
- Create classes with methods
- Understand when code will break vs succeed

**Cognitive Load Strategy:** Reduce scaffolding, increase problem-solving

---

### Lesson 9: Result Types - Error Handling the AL Way (18 minutes)

**Learning Objective:** Handle errors without exceptions using Result types

#### 9.1 The Problem with Crashes (3 min)

**Bad code (in most languages):**
```python
def divide(x, y):
    return x / y  # CRASHES if y is 0!

result = divide(10, 0)  # 💥 ZeroDivisionError
```

**AssertLang approach:**
```al
function divide(x: float, y: float) -> Result {
    if (y == 0.0) {
        return Error("Cannot divide by zero");
    }
    return Ok(x / y);
}
```

**Key Insight:** Functions return `Result`, which can be either:
- `Ok(value)` - Success with a value
- `Error(message)` - Failure with error description

#### 9.2 Returning Success with Ok() (3 min)

**Pattern:**
```al
function sqrt(x: float) -> Result {
    if (x < 0.0) {
        return Error("Cannot take square root of negative number");
    }
    let result = math.sqrt(x);
    return Ok(result);
}
```

**Shorthand:**
```al
return Ok(math.sqrt(x));  // Can put expression directly in Ok()
```

#### 9.3 Returning Errors with Error() (3 min)

**Pattern:**
```al
function validateAge(age: int) -> Result {
    if (age < 0) {
        return Error("Age cannot be negative");
    }
    if (age > 150) {
        return Error("Age exceeds human lifespan");
    }
    return Ok(age);
}
```

**Best Practice:** Error messages should be:
- Clear and specific
- Actionable (user knows what to fix)
- Consistent in format

#### 9.4 Using Results - The Check Pattern (5 min)

**Worked Example:**
```al
function processPayment(amount: float) -> Result {
    // Try to process payment
    let result = chargeCard(amount);

    // Check if it succeeded
    if (result.is_ok()) {
        let transactionId = result.value;
        return Ok("Payment successful: " + transactionId);
    } else {
        let errorMsg = result.error;
        return Error("Payment failed: " + errorMsg);
    }
}
```

**Pattern:**
- `.is_ok()` - Returns true if Ok, false if Error
- `.is_error()` - Returns true if Error, false if Ok
- `.value` - Gets the value from Ok (only if is_ok() is true!)
- `.error` - Gets the message from Error (only if is_error() is true!)

#### 9.5 Common Mistake: Not Checking Results (2 min)

**WRONG:**
```al
let result = divide(10, 0);
let answer = result.value;  // ❌ CRASH! No value in Error result
```

**RIGHT:**
```al
let result = divide(10, 0);
if (result.is_ok()) {
    let answer = result.value;  // ✓ Safe - checked first
} else {
    // Handle error
}
```

#### 9.6 Practice (2 min)

**Challenge:** Safe square root

```al
function safeSqrt(x: float) -> Result {
    // If x < 0, return Error
    // Otherwise, return Ok with math.sqrt(x)
}
```

**Test Cases:**
- `safeSqrt(16.0)` → Ok(4.0)
- `safeSqrt(-9.0)` → Error("...")
- `safeSqrt(0.0)` → Ok(0.0)

**Mastery Criteria:** 3/3 tests pass

---

### Lesson 10: Math Module - Numbers Made Easy (15 minutes)

**Learning Objective:** Use math module for calculations

#### 10.1 Why Use math Module? (2 min)

AssertLang's math module provides consistent numeric operations across all target languages.

**Auto-Import (v0.1.6):** When you use `math.round()`, AL automatically adds:
```python
from assertlang.runtime import al_math as math
```

You don't need to import manually! ✨

#### 10.2 Basic Operations (4 min)

**Worked Examples:**
```al
function calculations(x: float, y: float) -> float {
    // Rounding
    let rounded = math.round(3.7);       // 4
    let floor = math.floor(3.7);         // 3
    let ceil = math.ceil(3.2);           // 4

    // Min/Max
    let minimum = math.min(x, y);        // Smaller of two
    let maximum = math.max(x, y);        // Larger of two

    // Absolute value
    let absolute = math.abs(-5.5);       // 5.5

    // Power
    let squared = math.pow(x, 2);        // x²
    let cubed = math.pow(x, 3);          // x³

    // Square root
    let root = math.sqrt(16);            // 4

    return rounded;
}
```

#### 10.3 Real-World Example: Dose Calculation (5 min)

**Scenario:** Medical dosing (from 67-test validation)

```al
function calculateDose(weight: float, age: int) -> Result {
    // Validate inputs
    if (weight <= 0) {
        return Error("Weight must be positive");
    }

    // Calculate base dose
    let baseDose = weight * 1.5;
    let rounded = math.round(baseDose);

    // Apply safety limits
    let minimum = math.max(rounded, 10);   // At least 10mg
    let safeDose = math.min(minimum, 100); // At most 100mg

    return Ok(safeDose);
}
```

**Test:**
- `calculateDose(50.0, 30)` → Ok(75.0)
- `calculateDose(10.0, 5)` → Ok(15.0) → applies min of 10
- `calculateDose(100.0, 50)` → Ok(100.0) → hits max cap

#### 10.4 Math Constants (2 min)

```al
function circleArea(radius: float) -> float {
    let pi = math.PI;  // 3.14159...
    return pi * math.pow(radius, 2);
}
```

#### 10.5 Practice (2 min)

**Challenge:** Temperature converter

```al
function celsiusToFahrenheit(celsius: float) -> float {
    // Formula: F = C * 9/5 + 32
    // Use math.round() for clean output
}
```

**Test Cases:**
- `celsiusToFahrenheit(0)` → 32.0
- `celsiusToFahrenheit(100)` → 212.0
- `celsiusToFahrenheit(-40)` → -40.0 (same in both!)

**Mastery Criteria:** 3/3 tests pass

---

### Lesson 11: String Module - Text Manipulation (15 minutes)

**Learning Objective:** Process and validate strings

#### 11.1 String Basics (3 min)

```al
let name = "Alice";
let length = str.length(name);  // 5

// Auto-imported in v0.1.6!
// from assertlang.runtime import al_str as str
```

#### 11.2 Common String Operations (5 min)

**Worked Examples:**
```al
function stringOperations(text: string) -> string {
    // Length
    let len = str.length(text);

    // Case conversion
    let upper = str.upper(text);           // "HELLO"
    let lower = str.lower(text);           // "hello"

    // Checking contents
    let hasAt = str.contains(text, "@");   // true if @ present
    let startsWithHi = str.starts_with(text, "Hi");
    let endsWithExclaim = str.ends_with(text, "!");

    // Whitespace
    let trimmed = str.trim("  hello  ");   // "hello"

    // Replace
    let replaced = str.replace(text, "o", "0");  // "hell0"

    // Split
    let words = str.split(text, " ");      // ["Hello", "world"]

    return upper;
}
```

#### 11.3 Real-World: Email Validation (4 min)

**Scenario:** Validate email format

```al
function validateEmail(email: string) -> Result {
    // Check minimum length
    if (str.length(email) < 5) {
        return Error("Email too short");
    }

    // Must contain @
    if (!str.contains(email, "@")) {
        return Error("Email must contain @");
    }

    // Must contain dot after @
    let parts = str.split(email, "@");
    if (list.length(parts) != 2) {
        return Error("Email must have exactly one @");
    }

    let domain = list.last(parts);
    if (!str.contains(domain, ".")) {
        return Error("Domain must contain a dot");
    }

    return Ok(email);
}
```

**Test:**
- `validateEmail("alice@example.com")` → Ok
- `validateEmail("alice")` → Error (no @)
- `validateEmail("@.com")` → Error (too short)

#### 11.4 Practice (3 min)

**Challenge:** Password validator

Requirements:
- At least 8 characters
- Contains both uppercase and lowercase
- Hint: Compare `str.upper(password)` with `str.lower(password)`

```al
function validatePassword(password: string) -> Result {
    // Your code here
}
```

**Mastery Criteria:** 3/3 tests pass

---

### Lesson 12: List Module - Working with Collections (15 minutes)

**Learning Objective:** Manipulate lists effectively

#### 12.1 List Operations (5 min)

```al
function listOperations(items: list) -> list {
    // Length
    let count = list.length(items);      // Number of items

    // Access
    let first = list.first(items);       // First item
    let last = list.last(items);         // Last item

    // Checking
    let hasItem = list.contains(items, "target");  // true/false

    // Transformation
    let reversed = list.reverse(items);  // Reverse order

    // Note: list.append() adds to end (mutable!)
    items.append("new item");

    return items;
}
```

#### 12.2 Real-World: Shopping Cart (5 min)

```al
function calculateTotal(prices: list) -> Result {
    if (list.length(prices) == 0) {
        return Error("Cart is empty");
    }

    let total = 0.0;
    for (price in prices) {
        total = total + price;
    }

    let rounded = math.round(total * 100.0) / 100.0;  // Round to cents
    return Ok(rounded);
}

function findMostExpensive(prices: list) -> Result {
    if (list.length(prices) == 0) {
        return Error("No prices to compare");
    }

    let maxPrice = list.first(prices);
    for (price in prices) {
        maxPrice = math.max(maxPrice, price);
    }

    return Ok(maxPrice);
}
```

#### 12.3 Practice (5 min)

**Challenge:** Grade statistics

```al
// 1. Function to count passing grades (>= 60)
function countPassing(grades: list) -> int {
    // Your code
}

// 2. Function to get highest grade
function getHighestGrade(grades: list) -> Result {
    // Return Error if list empty
    // Otherwise return Ok with highest grade
}
```

**Test Cases:**
- `countPassing([95, 55, 72, 48, 83])` → 3
- `getHighestGrade([95, 55, 72])` → Ok(95)
- `getHighestGrade([])` → Error

**Mastery Criteria:** All tests pass

---

### Lesson 13: Classes - Your First Object (20 minutes)

**Learning Objective:** Create classes with `__init__()` and methods

#### 13.1 Why Classes? (3 min)

**Without classes:**
```al
let userName = "Alice";
let userEmail = "alice@example.com";
let userAge = 25;

function formatUser(name: string, email: string, age: int) -> string {
    return name + " (" + email + ")";
}

formatUser(userName, userEmail, userAge);  // Tedious!
```

**With classes:**
```al
class User {
    name: string;
    email: string;
    age: int;

    function __init__(name: string, email: string, age: int) {
        self.name = name;
        self.email = email;
        self.age = age;
    }

    function format() -> string {
        return self.name + " (" + self.email + ")";
    }
}

let user = User("Alice", "alice@example.com", 25);
user.format();  // Clean!
```

#### 13.2 Class Anatomy (5 min)

**Worked Example:**
```al
class BankAccount {
    // 1. Fields (properties)
    accountNumber: string;
    balance: float;
    owner: string;

    // 2. Constructor (called when creating instance)
    function __init__(accountNumber: string, owner: string) {
        self.accountNumber = accountNumber;
        self.balance = 0.0;         // Start with $0
        self.owner = owner;
    }

    // 3. Methods (functions that work on the object)
    function deposit(amount: float) -> Result {
        if (amount <= 0) {
            return Error("Deposit amount must be positive");
        }
        self.balance = self.balance + amount;
        return Ok(self.balance);
    }

    function getBalance() -> float {
        return self.balance;
    }
}

// Creating an instance
let account = BankAccount("12345", "Alice");

// Calling methods
account.deposit(100.0);    // Ok(100.0)
account.getBalance();      // 100.0
```

**Key Points:**
- `class` keyword starts definition
- Fields declared at top (with types)
- `function __init__()` is constructor (note: double underscore!)
- `self` refers to the instance
- Methods are functions inside the class

#### 13.3 Common Mistakes (3 min)

**WRONG:**
```al
class User {
    function init(name: string) {  // ❌ Wrong! Use __init__
        self.name = name;
    }
}
```

**RIGHT:**
```al
class User {
    function __init__(name: string) {  // ✓ Double underscore
        self.name = name;
    }
}
```

**WRONG:**
```al
class User {
    function __init__(name: string) {
        name = name;  // ❌ Wrong! Use self.name
    }
}
```

**RIGHT:**
```al
class User {
    function __init__(name: string) {
        self.name = name;  // ✓ self.fieldName
    }
}
```

#### 13.4 Practice: Create a Product Class (9 min)

**Challenge:**

Build a Product class for an e-commerce system:

**Fields:**
- `name: string`
- `price: float`
- `stock: int`

**Constructor:**
- Takes name, price, initial stock

**Methods:**
- `getInfo() -> string` - Returns "{name}: ${price} ({stock} in stock)"
- `purchase(quantity: int) -> Result` - Decreases stock, returns Error if not enough
- `restock(quantity: int) -> Result` - Adds to stock, returns Error if quantity <= 0

**Scaffolding:**
```al
class Product {
    name: string;
    price: float;
    stock: int;

    function __init__(__________, __________, __________) {
        // Initialize fields
    }

    function getInfo() -> string {
        // Format and return info string
    }

    function purchase(quantity: int) -> Result {
        // Check if enough stock
        // If yes, decrease stock and return Ok
        // If no, return Error
    }

    function restock(quantity: int) -> Result {
        // Validate quantity > 0
        // Add to stock
        // Return Ok with new stock level
    }
}
```

**Test Cases:**
```al
let laptop = Product("Laptop", 999.99, 5);
laptop.getInfo();        // "Laptop: $999.99 (5 in stock)"
laptop.purchase(2);      // Ok - stock becomes 3
laptop.purchase(10);     // Error - not enough stock
laptop.restock(5);       // Ok - stock becomes 8
```

**Mastery Criteria:**
- All fields initialized correctly
- All methods implemented
- All test cases pass

---

### Lesson 14: Methods and self (12 minutes)

**Learning Objective:** Understand method behavior and self reference

#### 14.1 What is self? (3 min)

`self` is a reference to the current instance of the class.

**Example:**
```al
class Counter {
    count: int;

    function __init__() {
        self.count = 0;  // self.count refers to THIS counter's count
    }

    function increment() {
        self.count = self.count + 1;  // Modify this instance
    }

    function getCount() -> int {
        return self.count;  // Return this instance's count
    }
}

let counter1 = Counter();
let counter2 = Counter();

counter1.increment();  // counter1.count = 1
counter2.increment();  // counter2.count = 1
counter2.increment();  // counter2.count = 2

counter1.getCount();  // 1 (independent!)
counter2.getCount();  // 2
```

**Key Insight:** Each instance has its own `self`, so state is independent.

#### 14.2 Methods Can Call Other Methods (3 min)

```al
class Calculator {
    history: list;

    function __init__() {
        self.history = [];
    }

    function add(x: float, y: float) -> float {
        let result = x + y;
        self.recordOperation("add", result);  // Call another method!
        return result;
    }

    function recordOperation(op: string, result: float) {
        let entry = op + ": " + str(result);
        self.history.append(entry);
    }

    function getHistory() -> list {
        return self.history;
    }
}
```

#### 14.3 Methods with Result Return Types (3 min)

```al
class Validator {
    minLength: int;

    function __init__(minLength: int) {
        self.minLength = minLength;
    }

    function validate(text: string) -> Result {
        if (str.length(text) < self.minLength) {
            return Error("Text too short, minimum " + str(self.minLength));
        }
        return Ok(text);
    }
}
```

#### 14.4 Practice (3 min)

**Challenge:** Temperature tracker

```al
class TemperatureTracker {
    readings: list;

    function __init__() {
        self.readings = [];
    }

    function addReading(temp: float) {
        // Add temp to readings list
    }

    function getAverage() -> Result {
        // If no readings, return Error
        // Otherwise calculate and return Ok with average
        // Hint: Use list.length() and a for loop
    }

    function getMax() -> Result {
        // Return highest reading, or Error if none
        // Hint: Use math.max() in a loop
    }
}
```

**Mastery Criteria:** All methods work correctly

---

### Lesson 15: Combining Classes and Results (15 minutes)

**Learning Objective:** Build robust classes with error handling

#### 15.1 Why Classes Need Results (2 min)

Many operations can fail:
- Withdrawing more money than account balance
- Accessing out-of-bounds list index
- Invalid constructor parameters

**Pattern:** Methods that can fail return `Result`

#### 15.2 Worked Example: Safe Bank Account (8 min)

```al
class BankAccount {
    accountNumber: string;
    balance: float;
    owner: string;

    function __init__(accountNumber: string, owner: string, initialDeposit: float) {
        self.accountNumber = accountNumber;
        self.owner = owner;
        self.balance = initialDeposit;
    }

    function deposit(amount: float) -> Result {
        // Validate
        if (amount <= 0) {
            return Error("Deposit must be positive");
        }

        // Update
        self.balance = self.balance + amount;

        // Return success with new balance
        return Ok(self.balance);
    }

    function withdraw(amount: float) -> Result {
        // Validate amount
        if (amount <= 0) {
            return Error("Withdrawal must be positive");
        }

        // Check sufficient funds
        if (amount > self.balance) {
            return Error("Insufficient funds: balance is " + str(self.balance));
        }

        // Update
        self.balance = self.balance - amount;

        // Return success
        return Ok(self.balance);
    }

    function transfer(other: BankAccount, amount: float) -> Result {
        // Try to withdraw
        let withdrawResult = self.withdraw(amount);
        if (withdrawResult.is_error()) {
            return withdrawResult;  // Forward the error
        }

        // Try to deposit
        let depositResult = other.deposit(amount);
        if (depositResult.is_error()) {
            // Uh oh, deposit failed! Refund the withdrawal
            self.deposit(amount);
            return Error("Transfer failed: " + depositResult.error);
        }

        return Ok("Transferred " + str(amount));
    }
}
```

**Test Cases:**
```al
let alice = BankAccount("001", "Alice", 1000.0);
let bob = BankAccount("002", "Bob", 500.0);

alice.withdraw(200.0);     // Ok(800.0)
alice.withdraw(1000.0);    // Error - insufficient funds
alice.transfer(bob, 300.0); // Ok - Alice: 500, Bob: 800
```

#### 15.3 Practice: User Registration System (5 min)

**Challenge:**

Build a User class with validation:

```al
class User {
    username: string;
    email: string;
    age: int;

    function __init__(username: string, email: string, age: int) -> Result {
        // Validate username length >= 3
        // Validate email contains @
        // Validate age >= 13
        // If any fail, return Error
        // Otherwise set fields and return Ok
    }

    function changeEmail(newEmail: string) -> Result {
        // Validate new email
        // Update if valid
    }

    function changePassword(oldPassword: string, newPassword: string) -> Result {
        // Validate old password matches
        // Validate new password strength (>= 8 chars)
        // Update if valid
    }
}
```

**Note:** Constructors can return Result!

**Mastery Criteria:** All validation works correctly

---

### Lesson 16: Core Skills Review & Project (25 minutes)

**Learning Objective:** Synthesize Lessons 9-15

#### 16.1 Concept Quiz (5 min)

1. When should a function return Result?
2. Name 3 math module functions
3. How do you check if a string contains a character?
4. What's the syntax for a class constructor?
5. What does `self` refer to?

**Mastery:** 4/5 correct

#### 16.2 Project: E-Commerce Shopping Cart (20 min)

**Requirements:**

Build a shopping cart system with:

**Product Class:**
- Fields: name, price, sku
- Method: `getInfo() -> string`

**CartItem Class:**
- Fields: product, quantity
- Method: `getSubtotal() -> float`

**ShoppingCart Class:**
- Field: items (list of CartItem)
- Methods:
  - `addItem(product: Product, quantity: int) -> Result`
  - `removeItem(sku: string) -> Result`
  - `getTotal() -> float`
  - `checkout() -> Result` (validates cart not empty)

**Test Case:**
```al
let cart = ShoppingCart();
let laptop = Product("Laptop", 999.99, "LAP001");
let mouse = Product("Mouse", 29.99, "MOU001");

cart.addItem(laptop, 1);         // Ok
cart.addItem(mouse, 2);          // Ok
cart.getTotal();                 // 1059.97
cart.checkout();                 // Ok - ready to process
```

**Scaffolding Provided:** Class stubs

**Mastery Criteria:**
- All classes implemented
- All methods work correctly
- Uses Result for error handling
- Uses math module for calculations
- All test cases pass

**Graduation:** Can write production-ready AssertLang with OOP, stdlib, and error handling

---

## Stage 3: Production (Lessons 17-24)
### Goal: Deploy Real AssertLang Applications

**Learning Objectives:**
- Install and use AssertLang CLI
- Transpile to multiple languages
- Understand v0.1.6 auto-import
- Debug transpiled code
- Deploy to production

**Cognitive Load Strategy:** Real-world scenarios, practical deployment

---

### Lesson 17: Installing AssertLang CLI (10 minutes)

**Learning Objective:** Set up development environment

#### 17.1 Installation (3 min)

**Command:**
```bash
pip install assertlang
```

**Verify:**
```bash
asl --version
```

Expected output: `AssertLang 0.1.6` (or newer)

#### 17.2 Your First Transpilation (5 min)

**Step 1:** Create file `hello.al`
```al
function greet(name: string) -> string {
    return "Hello, " + name + "!";
}
```

**Step 2:** Transpile to Python
```bash
asl build hello.al --lang python -o hello.py
```

**Step 3:** Inspect output
```bash
cat hello.py
```

You'll see:
```python
# Generated by AssertLang v0.1.6
# Source: hello.al
# DO NOT EDIT - Regenerate from source instead

from assertlang.runtime import Ok, Error, Result

def greet(name):
    return "Hello, " + name + "!"
```

**Step 4:** Use it!
```python
from hello import greet
print(greet("Alice"))  # "Hello, Alice!"
```

#### 17.3 Transpile to JavaScript (2 min)

```bash
asl build hello.al --lang javascript -o hello.js
```

Output:
```javascript
// Generated by AssertLang v0.1.6
// Source: hello.al
// DO NOT EDIT - Regenerate from source instead

function greet(name) {
    return "Hello, " + name + "!";
}

module.exports = { greet };
```

**Mastery Criteria:** Successfully transpile and run code

---

### Lesson 18: v0.1.6 Auto-Import Magic (12 minutes)

**Learning Objective:** Understand how auto-import works

#### 18.1 The Problem Before v0.1.6 (3 min)

**Generated code (v0.1.5):**
```python
# Generated by AssertLang v0.1.5
from assertlang.runtime import Ok, Error, Result

def calculate(x):
    return math.round(x)  # ❌ NameError: math not defined!
```

**Manual fix required:**
```python
from assertlang.runtime import Ok, Error, Result, al_math as math  # 😞
```

#### 18.2 v0.1.6 Solution: Smart Detection (4 min)

**AL Code:**
```al
function calculate(x: float) -> float {
    let rounded = math.round(x);
    let maximum = math.max(rounded, 10);
    return maximum;
}
```

**Generated Python (v0.1.6):**
```python
# Generated by AssertLang v0.1.6
# Source: calculate.al

from assertlang.runtime import Ok, Error, Result, al_math as math  # ✨ Auto!

def calculate(x):
    rounded = math.round(x)
    maximum = math.max(rounded, 10)
    return maximum
```

**How it works:**
1. Compiler scans your AL code for `math.*`, `str.*`, `list.*`
2. Detects which modules you use
3. Auto-adds imports only for what you need
4. **Zero manual fixes required!**

#### 18.3 What Gets Auto-Imported (3 min)

```al
// Uses math module
function calc1(x: float) -> float {
    return math.round(x);
}
// Generated: from assertlang.runtime import ..., al_math as math

// Uses str module
function calc2(text: string) -> int {
    return str.length(text);
}
// Generated: from assertlang.runtime import ..., al_str as str

// Uses multiple modules
function calc3(items: list, threshold: float) -> string {
    let count = list.length(items);
    let rounded = math.round(threshold);
    let result = str.upper("result");
    return result;
}
// Generated: from assertlang.runtime import ..., al_math as math, al_str as str, al_list as list
```

#### 18.4 Practice (2 min)

**Challenge:** Predict imports

For each AL function, predict which modules get auto-imported:

```al
// 1.
function process(x: float) -> float {
    return math.sqrt(x);
}

// 2.
function validate(email: string) -> bool {
    return str.contains(email, "@");
}

// 3.
function analyze(data: list) -> float {
    let sum = 0.0;
    for (item in data) {
        sum = sum + item;
    }
    return math.round(sum / list.length(data));
}
```

**Answers:**
1. `al_math as math`
2. `al_str as str`
3. `al_math as math, al_list as list`

**Mastery Criteria:** Correctly predict 3/3

---

### Lessons 19-24: Continue with CLI usage, debugging, deployment patterns, multi-language transpilation, production checklist, and final project...

---

## Stage 4: Mastery (Lessons 25-32)
### Goal: Build Enterprise-Grade Multi-Agent Systems

**Learning Objectives:**
- Design contracts for multi-agent coordination
- Integrate with CrewAI, LangGraph, AutoGen
- Handle complex state machines
- Scale to 680+ line systems
- Apply best practices from 67-test validation

**Cognitive Load Strategy:** Expert-level problem solving, architectural thinking

---

### Lessons 25-32: Cover multi-agent patterns, framework integration, advanced Result patterns, state machines, medical dosing case study, performance optimization, production deployment, and capstone project...

---

## Assessment Framework

### Skill Level Definitions

#### Beginner (Stage 1 Complete)
**Can:**
- Write functions with parameters and return types
- Use if/else and loops
- Understand type system basics

**Cannot yet:**
- Handle errors properly
- Use standard library
- Create classes

**Assessment:** Grade calculator mini-project

---

#### Intermediate (Stage 2 Complete)
**Can:**
- Handle errors with Result types
- Use math, str, list modules
- Create classes with methods
- Write production-ready validation logic

**Cannot yet:**
- Deploy to production
- Debug transpiled code
- Integrate with frameworks

**Assessment:** E-commerce cart project

---

#### Advanced (Stage 3 Complete)
**Can:**
- Use CLI to transpile code
- Deploy to production environments
- Debug across languages
- Understand v0.1.6 features

**Cannot yet:**
- Design multi-agent systems
- Integrate with AI frameworks
- Build large-scale applications

**Assessment:** Multi-language deployment project

---

#### Expert (Stage 4 Complete)
**Can:**
- Design multi-agent contracts
- Integrate with CrewAI/LangGraph/AutoGen
- Build 680+ line production systems
- Apply all best practices

**Assessment:** Medical dosing system capstone (replicate testing agent's work)

---

## Learning Outcomes Validation

### Can graduates replicate testing agent's 680-line medical system?

**After Stage 1:** ❌ No (lacks stdlib, classes, error handling)

**After Stage 2:** ⚠️ Partially (has concepts, lacks deployment knowledge)

**After Stage 3:** ✅ Mostly (can write and deploy, lacks multi-agent patterns)

**After Stage 4:** ✅✅ Yes! (Complete mastery)

---

## Teaching Methodology

### Instructional Design Principles

#### 1. Worked Examples → Faded Scaffolding → Independent Practice

**Lesson structure:**
1. **Watch:** Worked example with explanation (3 min)
2. **Try:** Faded example with fill-in-the-blanks (3 min)
3. **Build:** Independent practice from scratch (6 min)
4. **Test:** Auto-graded test cases (instant feedback)

**Example progression:**

**Stage 1 (Worked):**
```al
// Complete solution shown
function calculateTax(price: float) -> float {
    let taxRate = 0.08;
    let tax = price * taxRate;
    return tax;
}
```

**Stage 2 (Faded):**
```al
// Some blanks for learner to fill
function calculateDiscount(price: float) -> float {
    let discountRate = ______;  // Fill in: 0.10
    let discount = price * ______;  // Fill in: discountRate
    return ______;  // Fill in: discount
}
```

**Stage 3 (Independent):**
```
Challenge: Create a function calculateShipping(weight: float) -> float
- If weight < 5, shipping is $5
- Otherwise, shipping is weight * $2
- Write the complete function
```

#### 2. Parsons Problems for Control Flow

**Instead of:**
```
Write an if/else statement to check if age >= 18
```

**Use:**
```
Arrange these lines in the correct order:
[ ] return "Adult";
[ ] if (age >= 18) {
[ ] } else {
[ ] return "Minor";
[ ] }
```

**Benefits:**
- Focuses on logic, not syntax
- Reduces cognitive load
- 35% faster learning (research-proven)

#### 3. Error-Driven Learning

**Include intentional errors:**

```al
// Fix This Code:
function divide(x: float, y: float) -> float {
    return x / y;
}

// Hint: What happens if y is 0?
```

**Expected learning:**
- Recognize need for validation
- Discover Result types organically
- Learn from compiler messages

#### 4. Immediate Feedback

**Every exercise has:**
- ✅ Auto-run test cases
- 📊 Instant pass/fail
- 💡 Hints if struggling
- 🎯 Clear success criteria

**Example:**
```
Your Output:  "Hello Alice!"
Expected:     "Hello, Alice!"
              ^^^^^^^^^^^^^
Test Failed: Missing comma
Hint: Remember to include punctuation
```

#### 5. Spaced Repetition

**Result types introduced 5 times:**
1. Lesson 9: Basic Ok/Error syntax
2. Lesson 10: Math operations with Result
3. Lesson 13: Class methods returning Result
4. Lesson 15: Complex error handling patterns
5. Lesson 22: Production error handling best practices

**Each time:** Deeper understanding, more complex scenarios

---

## Accessibility & Inclusivity

### Multiple Learning Paths

#### Visual Learners
- Diagrams for every concept
- Syntax highlighting
- Side-by-side before/after examples

#### Kinesthetic Learners
- Interactive code editor
- Immediate execution
- Hands-on projects

#### Auditory Learners
- Video explanations (optional)
- Narrated walkthroughs
- Discussion forums

### Language Support
- Simple, clear English (no jargon without explanation)
- Glossary of terms
- Non-native speaker friendly

### Pace Options
- Self-paced progression
- Optional "deep dive" sections
- "Express path" for experienced programmers

---

## Success Metrics

### Completion Rates
- **Target:** 70% complete all 32 lessons
- **Benchmark:** Industry average is 10-15% for MOOCs

### Mastery Assessment
- **Target:** 90% pass capstone project (680-line medical system)
- **Benchmark:** Testing agent achieved 67/67 tests (100%)

### Time to Competency
- **Target:** 8 hours from beginner to production-ready
- **Benchmark:** Rust Book is ~20 hours

### User Satisfaction
- **Target:** Net Promoter Score > 50
- **Measure:** "Would you recommend AssertLang to a colleague?"

---

## Curriculum Maintenance

### Quarterly Updates
- Align with latest AssertLang version
- Add new features (v0.1.7, v0.2.0)
- Update examples with community contributions

### Community Feedback
- Track where learners get stuck (analytics)
- A/B test lesson structures
- Incorporate user suggestions

### Industry Alignment
- Update medical example with latest guidelines
- Add new framework integrations (AutoGen, etc.)
- Reflect production best practices

---

## Next Steps

### Phase 1: Build Foundation Lessons (Weeks 1-2)
- Implement Lessons 1-8
- Create interactive exercises
- Build auto-grading system

### Phase 2: Core Skills (Weeks 3-4)
- Implement Lessons 9-16
- Add stdlib interactive demos
- Create shopping cart project

### Phase 3: Production Path (Weeks 5-6)
- Implement Lessons 17-24
- Build CLI integration
- Create deployment guides

### Phase 4: Mastery Content (Weeks 7-8)
- Implement Lessons 25-32
- Recreate medical system project
- Add framework integration guides

### Phase 5: Polish & Launch (Week 9)
- User testing
- Bug fixes
- Marketing materials

---

## Conclusion

This roadmap provides a **systematic, research-based curriculum** for teaching AssertLang that:

✅ **Reduces cognitive load** through worked examples and scaffolding
✅ **Enables practice** with immediate feedback and auto-grading
✅ **Builds progressively** from basics to enterprise applications
✅ **Validates mastery** through real-world projects (680-line medical system)
✅ **Ensures success** with clear learning objectives and assessments

**Outcome:** Graduates can confidently write production-ready AssertLang code and deploy multi-agent systems, matching the testing agent's validation results.

---

**Document Version:** 1.0
**Last Updated:** October 19, 2025
**Next Review:** After Phase 1 implementation (Lessons 1-8)
