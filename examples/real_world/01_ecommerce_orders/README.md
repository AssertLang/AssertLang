# Example 1: E-commerce Order System with Contracts

**Complexity:** Beginner → Intermediate
**Time:** 15-20 minutes
**Languages:** Python, JavaScript

---

## What You'll Learn

- Writing contracts for business rule validation
- State machine validation with contracts
- Input validation patterns
- Testing contract-based code

---

## The Problem

E-commerce order systems need to enforce complex business rules:
- Orders can only transition through valid states (pending → paid → shipped → delivered)
- Refunds cannot exceed original amount
- Discounts must be between 0-100%
- Tax rates must be valid percentages
- Shipping info required before marking as shipped

**Without contracts:** These rules scattered across code, easy to miss, hard to maintain.

**With contracts:** Rules enforced automatically at function boundaries. Violations caught immediately with clear error messages.

---

## Quick Start

```bash
# Generate Python code from contracts
promptware build orders.pw -o orders.py

# Run tests
pytest test_orders.py -v

# All 48 tests should pass ✅
```

---

## The Contract File

**File:** `orders.pw` (187 lines)

### Structure

```pw
// 1. Input validation functions
function validate_order_inputs(...) -> bool {
    @requires valid_order_id: len(order_id) > 0
    @requires positive_amount: total_amount > 0.0
    // ...
}

// 2. Business logic functions
function calculate_total_with_tax(...) -> float {
    @requires positive_subtotal: subtotal >= 0.0
    @requires valid_tax_rate: tax_rate >= 0.0 && tax_rate <= 1.0
    @ensures total_includes_tax: result >= subtotal
    // ...
}

// 3. State machine validation
function can_transition_status(...) -> bool {
    @requires valid_current: len(current_status) > 0
    @ensures transition_decided: result == true || result == false
    // Complex state machine logic
}
```

---

## Key Patterns Demonstrated

### Pattern 1: Input Validation with Preconditions

```pw
function validate_payment(
    payment_method: string,
    transaction_id: string,
    amount: float
) -> bool {
    @requires valid_payment_method: len(payment_method) > 0
    @requires valid_transaction: len(transaction_id) > 0
    @requires positive_payment: amount > 0.0

    @ensures validation_complete: result == true || result == false

    return true;
}
```

**What this does:**
- Checks payment method is not empty
- Checks transaction ID exists
- Checks amount is positive
- Guarantees function returns boolean

**Python usage:**
```python
from orders import validate_payment

# ✅ Valid call
validate_payment("credit_card", "TXN-12345", 99.99)

# ❌ Raises ContractViolationError
validate_payment("", "TXN-12345", 99.99)  # Empty payment method
```

---

### Pattern 2: Business Rules with Postconditions

```pw
function apply_discount(
    original_price: float,
    discount_percent: float
) -> float {
    @requires positive_price: original_price > 0.0
    @requires valid_discount: discount_percent >= 0.0 && discount_percent <= 100.0

    @ensures discounted_price: result >= 0.0 && result <= original_price

    let discount_amount = original_price * (discount_percent / 100.0);
    let final_price = original_price - discount_amount;

    return final_price;
}
```

**What this does:**
- **Precondition:** Price must be positive, discount 0-100%
- **Business logic:** Calculate discount
- **Postcondition:** Result must be between 0 and original price

**Why postconditions matter:**
```python
# If your math is wrong, postcondition catches it:
result = apply_discount(100.0, 20.0)  # Should be 80.0

# Postcondition validates: result >= 0.0 && result <= 100.0
# If logic bug returns 120.0, contract violation raised!
```

---

### Pattern 3: State Machine Validation

```pw
function can_transition_status(
    current_status: string,
    new_status: string
) -> bool {
    @requires valid_current: len(current_status) > 0
    @requires valid_new: len(new_status) > 0

    @ensures transition_decided: result == true || result == false

    // State machine: pending -> payment_confirmed -> processing -> shipped -> delivered

    if (current_status == "pending") {
        if (new_status == "payment_confirmed" || new_status == "cancelled") {
            return true;
        }
    }

    if (current_status == "payment_confirmed") {
        if (new_status == "processing" || new_status == "cancelled") {
            return true;
        }
    }

    // ... more states ...

    return false;
}
```

**What this does:**
- Validates state transitions follow business rules
- Can't skip states (e.g., pending → shipped invalid)
- Can cancel before shipping
- Cannot go backwards

**Usage:**
```python
# ✅ Valid transitions
can_transition_status("pending", "payment_confirmed")  # True
can_transition_status("processing", "shipped")  # True

# ❌ Invalid transitions
can_transition_status("pending", "shipped")  # False - can't skip states
can_transition_status("shipped", "processing")  # False - can't go backwards
```

---

## Testing Strategy

### Test Categories

**1. Precondition Tests** (18 tests)
- Valid inputs pass
- Invalid inputs rejected with clear errors

**2. Business Logic Tests** (12 tests)
- Calculations correct
- Edge cases handled

**3. State Machine Tests** (9 tests)
- Valid transitions allowed
- Invalid transitions blocked

**4. End-to-End Scenarios** (4 tests)
- Complete workflows tested
- Multiple functions composed correctly

**Total: 48 tests, all passing ✅**

### Example Test

```python
def test_refund_exceeds_original_rejected(self):
    """Refund exceeding original amount should be rejected."""
    with pytest.raises(ContractViolationError) as exc_info:
        validate_refund(
            refund_amount=150.00,  # Invalid: exceeds original
            original_amount=100.00
        )
    assert "refund_not_exceeds" in str(exc_info.value)
```

**What this tests:**
- Contract catches business rule violation
- Error message includes clause name
- Developer knows exactly what failed

---

## Running the Example

### Step 1: Generate Code

```bash
# Generate Python
promptware build orders.pw -o orders.py

# Generate JavaScript (coming soon)
promptware build orders.pw --lang javascript -o orders.js
```

### Step 2: Run Tests

```bash
# Run all tests
pytest test_orders.py -v

# Run specific test class
pytest test_orders.py::TestStateTransitions -v

# Run with coverage
pytest test_orders.py --cov=orders --cov-report=html
```

### Step 3: Use in Your Code

```python
from orders import (
    validate_order_inputs,
    validate_payment,
    can_transition_status,
    calculate_total_with_tax
)

# Validate order creation
if validate_order_inputs("ORD-001", "CUST-001", 99.99, 2):
    print("Order inputs valid!")

# Check state transition
if can_transition_status("pending", "payment_confirmed"):
    # Update order status in database
    pass
```

---

## Contract Benefits Demonstrated

### 1. **Early Error Detection**

**Without contracts:**
```python
def apply_discount(price, discount):
    return price * (discount / 100)  # Bug: should subtract!

result = apply_discount(100, 20)  # Returns 20, not 80 😱
# Bug discovered in production when customer complains
```

**With contracts:**
```pw
@ensures discounted_price: result >= 0.0 && result <= original_price

# Postcondition fails immediately during testing:
# ContractViolationError: discounted_price violated
#   Expected: result >= 0.0 && result <= original_price
#   Got: result = 20.0 (original = 100.0)
```

### 2. **Self-Documenting Code**

Contracts explain:
- **What function expects** (preconditions)
- **What function guarantees** (postconditions)
- **Business rules** (constraints on inputs/outputs)

### 3. **Fearless Refactoring**

Change implementation, contracts ensure behavior unchanged:
```python
# Refactor discount calculation
# Tests still pass = refactoring safe ✅
```

### 4. **Clear Error Messages**

**Without contracts:**
```
ValueError: invalid literal for int() with base 10: ''
```

**With contracts:**
```
ContractViolationError in validate_payment()

Precondition 'valid_transaction' failed:
  Expected: len(transaction_id) > 0
  Received: len(transaction_id) = 0

Context:
  payment_method = "credit_card"
  transaction_id = ""
  amount = 99.99

Suggestion: Ensure transaction_id is non-empty before calling validate_payment()
```

---

## Real-World Applications

This example demonstrates patterns for:

### E-commerce Platforms
- Order lifecycle management
- Payment processing validation
- Refund policy enforcement

### SaaS Applications
- Subscription state transitions
- Billing validation
- Discount code validation

### Workflow Systems
- State machine validation
- Business rule enforcement
- Process step validation

---

## Common Pitfalls (and how contracts help)

### Pitfall 1: Off-by-One Errors

```pw
@requires valid_discount: discount_percent >= 0.0 && discount_percent <= 100.0
```

Catches: `discount_percent = 101.0` ✅

### Pitfall 2: Negative Values

```pw
@requires positive_amount: total_amount > 0.0
```

Catches: `total_amount = -10.0` ✅

### Pitfall 3: Empty Strings

```pw
@requires valid_order_id: len(order_id) > 0
```

Catches: `order_id = ""` ✅

### Pitfall 4: Invalid State Transitions

```pw
@ensures transition_decided: result == true || result == false
```

Logic must return boolean. Catches type errors ✅

---

## Next Steps

### Extend This Example

1. **Add More States:**
   - Add "on_hold", "backordered" states
   - Update `can_transition_status` with new rules

2. **Add Invariants:**
   - Add class invariants for Order object
   - Ensure consistency across state changes

3. **Add More Business Rules:**
   - Minimum order amount
   - Maximum discount per customer tier
   - Shipping cost calculation

### Try Other Examples

- **Example 2:** Multi-Agent Research Pipeline (CrewAI)
- **Example 3:** Data Processing Workflow (LangGraph)
- **Example 4:** API Rate Limiting
- **Example 5:** State Machine Patterns

---

## File Structure

```
01_ecommerce_orders/
├── orders.pw              # Contract definitions (187 lines)
├── orders.py              # Generated Python code (357 lines)
├── test_orders.py         # Test suite (48 tests)
├── README.md              # This file
└── data/
    ├── valid_orders.json  # (coming soon)
    └── invalid_orders.json
```

---

## Key Takeaways

1. **Contracts catch bugs early** - Before they reach production
2. **Preconditions validate inputs** - Guard against invalid data
3. **Postconditions validate outputs** - Ensure correct results
4. **State machines need validation** - Contracts perfect for this
5. **Tests validate contracts work** - 48/48 passing ✅

---

## Questions?

- **Contracts not triggering?** Check `PROMPTWARE_VALIDATE` environment variable
- **Need more examples?** See other real-world examples in `examples/`
- **Want to contribute?** See `CONTRIBUTING.md`

---

## Learn More

- [Contract Syntax Guide](https://docs.promptware.dev/guides/contracts)
- [Preconditions Deep Dive](https://docs.promptware.dev/guides/preconditions)
- [State Machine Patterns](https://docs.promptware.dev/cookbook/state-machines)
- [Testing with Contracts](https://docs.promptware.dev/guides/testing)

---

**Example 1 Complete** ✅
**Next:** Try modifying the contracts and see what breaks!
