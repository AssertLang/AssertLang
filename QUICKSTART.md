# Quickstart: Your First Contract in 5 Minutes

**Get from zero to working contract-based validation in under 5 minutes.**

---

## What You'll Build

A simple order validation function with contracts that automatically catch invalid inputs at runtime.

**Before contracts:**
```python
def process_order(total, discount):
    final = total - discount
    return final  # Bug: discount could exceed total!
```

**After contracts:**
```python
def process_order(total, discount):
    # Contract catches: discount > total
    # Contract catches: negative values
    final = total - discount
    return final  # ✓ Guaranteed valid
```

---

## Step 1: Install (30 seconds)

```bash
pip install promptware
```

✓ **Success**: Run `promptware --version` (should show version 2.3.0+)

---

## Step 2: Create Your First Contract (2 minutes)

Create `order.pw`:

```pw
function calculate_total(
    price: float,
    quantity: int,
    discount: float
) -> float {
    @requires price_positive: price > 0.0
    @requires quantity_positive: quantity > 0
    @requires valid_discount: discount >= 0.0 && discount <= price * quantity

    @ensures positive_result: result >= 0.0
    @ensures discount_applied: result == (price * quantity) - discount

    let subtotal = price * quantity;
    let final_total = subtotal - discount;

    return final_total;
}
```

**What this does:**
- `@requires` = Preconditions (checked before function runs)
- `@ensures` = Postconditions (checked after function returns)
- **Automatic validation**: Invalid inputs caught immediately

---

## Step 3: Generate Python Code (1 minute)

```bash
promptware build order.pw -o order.py
```

✓ **Success**: Creates `order.py` with contract validation embedded

**Generated code** (simplified view):
```python
def calculate_total(price: float, quantity: int, discount: float) -> float:
    # Precondition checks (auto-generated)
    check_precondition(price > 0.0, "price_positive")
    check_precondition(quantity > 0, "quantity_positive")
    check_precondition(discount >= 0.0 and discount <= price * quantity, "valid_discount")

    # Your logic
    subtotal = price * quantity
    final_total = subtotal - discount

    # Postcondition checks (auto-generated)
    check_postcondition(result >= 0.0, "positive_result")
    check_postcondition(result == (price * quantity) - discount, "discount_applied")

    return final_total
```

---

## Step 4: See It Work (1 minute)

Create `test_order.py`:

```python
from order import calculate_total

# ✓ Valid input
print(calculate_total(price=10.0, quantity=5, discount=5.0))
# Output: 45.0

# ❌ Invalid input (discount exceeds total)
try:
    calculate_total(price=10.0, quantity=5, discount=60.0)
except Exception as e:
    print(f"Contract caught error: {e}")
    # Output: Contract violation: valid_discount failed
    #         Expected: discount <= price * quantity
    #         Got: 60.0 > 50.0
```

Run it:
```bash
python test_order.py
```

✓ **Success**: See validation working automatically!

---

## What Just Happened?

1. **You wrote contracts** - Declarative rules about valid inputs/outputs
2. **Promptware generated code** - Contract checks embedded in Python
3. **Runtime validation** - Invalid inputs caught with clear error messages

**No manual validation code needed.** Contracts compile to runtime checks.

---

## Next Steps (Choose Your Path)

### Learn by Example 🎯
- **[E-commerce Orders](examples/real_world/01_ecommerce_orders/)** - State machines, refunds
- **[Multi-Agent AI](examples/real_world/02_multi_agent_research/)** - CrewAI contracts
- **[Data Pipelines](examples/real_world/03_data_processing_workflow/)** - LangGraph validation
- **[Rate Limiting](examples/real_world/04_api_rate_limiting/)** - Token bucket algorithm
- **[State Machines](examples/real_world/05_state_machine_patterns/)** - Generic patterns

### Explore by Use Case 📚
- **Agent Coordination** → [Multi-Agent Research Example](examples/real_world/02_multi_agent_research/)
- **State Validation** → [State Machine Patterns](examples/real_world/05_state_machine_patterns/)
- **API Safety** → [Rate Limiting Example](examples/real_world/04_api_rate_limiting/)
- **Data Quality** → [Data Processing Example](examples/real_world/03_data_processing_workflow/)

### Dive Deeper 📖
- **[Contract Syntax](docs/reference/contract-syntax.md)** - Complete language reference
- **[Python Integration](docs/guides/languages/python-guide.md)** - Python-specific patterns
- **[CLI Commands](docs/reference/cli-commands.md)** - All `promptware` commands

---

## Common Questions

**Q: When should I use contracts?**
A: Whenever a function has invariants that must hold. State machines, validation logic, business rules, API boundaries.

**Q: Does this work with existing code?**
A: Yes! Generate Python/JavaScript/Go from contracts, import like normal modules.

**Q: Performance impact?**
A: Negligible (~1-2µs per check). Disable in production with `PROMPTWARE_DISABLE_CONTRACTS=1`.

**Q: Which languages supported?**
A: Python (100%), JavaScript (95%), Go (70%), Rust (60%). TypeScript and C# coming soon.

**Q: Can I use with CrewAI/LangGraph/AutoGen?**
A: Yes! See [Multi-Agent Example](examples/real_world/02_multi_agent_research/) and [Data Pipeline Example](examples/real_world/03_data_processing_workflow/).

---

## Get Help

- **[GitHub Issues](https://github.com/Promptware-dev/promptware/issues)** - Bug reports, feature requests
- **[Examples](examples/real_world/)** - 5 production-ready examples with tests
- **[Documentation](docs/)** - Complete guides and reference

---

## What's Next?

You've mastered the basics! Now explore:

1. **Real-World Examples** - See contracts in production scenarios
2. **Advanced Patterns** - State machines, invariants, composition
3. **Framework Integration** - CrewAI, LangGraph, Airflow, FastAPI

**Pro Tip**: Start with the [E-commerce Orders example](examples/real_world/01_ecommerce_orders/) - it's the most beginner-friendly and shows common patterns.

---

**Time to First Contract**: < 5 minutes ✓
**Next**: [Choose an example](examples/real_world/) →
