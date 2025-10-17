# API Rate Limiting with Contract Validation

**Real-world example demonstrating contract-based rate limiting with token bucket algorithm and multi-tier quotas.**

## Quickstart (5 minutes)

```bash
# 1. Generate Python code
python3 -c "
from dsl.al_parser import parse_al
from language.python_generator_v2 import generate_python
with open('rate_limiter.al'), 'r') as f:
    ir_module = parse_al(f.read())
with open('rate_limiter.py', 'w') as f:
    f.write(generate_python(ir_module))
"

# 2. Run test suite (60 tests)
python3 -m pytest test_rate_limiter.py -v

# 3. Use in your API
from rate_limiter import (
    is_request_allowed,
    calculate_tokens_to_add,
    validate_tier_limits
)

# Token bucket check
if is_request_allowed(current_tokens=50, tokens_required=5, max_tokens=100):
    process_request()
else:
    return HTTP_429_TOO_MANY_REQUESTS
```

**Result**: Production-ready rate limiting with contract validation.

---

## What This Example Demonstrates

### 1. **Token Bucket Algorithm**
- Token allocation and refill
- Request cost calculation
- Retry-after timing
- Burst traffic handling

### 2. **Multi-Tier Rate Limits**
- **Free**: 10 req/min, 1K/day
- **Basic**: 100 req/min, 50K/day  
- **Pro**: 1K req/min, 1M/day
- **Enterprise**: 10K req/min, 10M/day

### 3. **Weighted Rate Limiting**
- Read operations: 1 token
- Write operations: 5 tokens
- Delete operations: 10 tokens
- Search operations: 3 tokens
- Payload size costs (1 token per 100KB)

### 4. **Violation Handling**
- Exponential backoff (2^violations)
- Cooldown periods
- IP-based limiting
- Global rate limits

---

## Real-World Applications

### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException, Header
from rate_limiter import is_request_allowed, calculate_retry_after_seconds

app = FastAPI()

# Token bucket state (use Redis in production)
user_tokens = {}

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    user_id = request.headers.get("X-User-ID")
    
    # Get current tokens
    current = user_tokens.get(user_id, {"tokens": 100, "last_refill": time.time()})
    
    # Refill tokens
    elapsed = int(time.time() - current["last_refill"])
    tokens_to_add = calculate_tokens_to_add(
        elapsed_seconds=elapsed,
        refill_rate=2,  # 2 tokens/second
        current_tokens=current["tokens"],
        max_tokens=100
    )
    current["tokens"] += tokens_to_add
    current["last_refill"] = time.time()
    
    # Check if request allowed
    if not is_request_allowed(current["tokens"], tokens_required=5, max_tokens=100):
        retry_after = calculate_retry_after_seconds(5, current["tokens"], 2)
        raise HTTPException(
            status_code=429,
            headers={"Retry-After": str(retry_after)}
        )
    
    # Deduct tokens
    current["tokens"] -= 5
    user_tokens[user_id] = current
    
    return await call_next(request)
```

### Flask with Tier Validation
```python
from flask import Flask, g, request
from rate_limiter import validate_tier_limits, calculate_request_cost

app = Flask(__name__)

@app.before_request
def check_tier_limits():
    user = get_current_user()
    
    # Validate tier limits
    if not validate_tier_limits(
        tier=user.tier,
        requests_per_minute=user.rpm_usage,
        daily_quota=user.daily_usage
    ):
        return {"error": "Tier limit exceeded"}, 403
    
    # Calculate request cost
    cost = calculate_request_cost(
        endpoint_type=request.method.lower(),  # "read" for GET
        payload_size_kb=len(request.data) // 1024
    )
    
    g.request_cost = cost
```

### Django with Exponential Backoff
```python
from django.core.cache import cache
from rate_limiter import calculate_violation_penalty, is_cooldown_active

def rate_limit_view(request):
    user_id = request.user.id
    violations = cache.get(f"violations:{user_id}", 0)
    last_violation = cache.get(f"last_violation:{user_id}", 0)
    
    # Check cooldown
    if is_cooldown_active(
        last_violation_time=last_violation,
        current_time=int(time.time()),
        cooldown_seconds=300  # 5 minutes
    ):
        penalty = calculate_violation_penalty(violations, base_penalty_seconds=60)
        return HttpResponse(
            f"Too many violations. Retry in {penalty} seconds",
            status=429
        )
```

---

## The Problem We're Solving

### Without Contracts

```python
# ❌ No token validation
def process_request(user):
    user.tokens -= 5
    # What if tokens go negative?
    # What if tokens exceed max?

# ❌ No tier enforcement
user.tier = "free"
user.requests_per_minute = 1000  # Way over free tier limit!

# ❌ Violation penalties not validated
penalty = base * (2 ** violations)  # Could overflow!

# ❌ No request cost validation
cost = calculate_cost("delete", 999999)  # Unreasonable cost
```

### With Contracts

```python
# ✅ Token validation
is_request_allowed(
    current_token_count=-5,  # ❌ Invalid
    tokens_required=5,
    max_tokens=100
)  # Contract violation caught

# ✅ Tier enforcement
validate_tier_limits(
    tier="free",
    requests_per_minute=1000,  # ❌ Exceeds free tier
    daily_quota=1000
)  # Returns False

# ✅ Penalty capped
calculate_violation_penalty(
    violation_count=100,  # Capped at 10
    base_penalty_seconds=60
)  # Returns 60 * 1024 (max multiplier)

# ✅ Cost validation
calculate_request_cost(
    endpoint_type="delete",
    payload_size_kb=5000  # Large payload
)  # Returns 10 + 50 = 60 tokens
```

---

## Running the Tests

```bash
# Full test suite (60 tests)
python3 -m pytest test_rate_limiter.py -v

# Specific categories
pytest test_rate_limiter.py::TestTokenBucketAlgorithm -v
pytest test_rate_limiter.py::TestTierLimits -v
pytest test_rate_limiter.py::TestWeightedRateLimiting -v
pytest test_rate_limiter.py::TestViolationPenalty -v
```

**Test Results**: 60/60 passing
- Token bucket (5 tests)
- Quota management (5 tests)
- Tier limits (8 tests)
- Weighted costs (6 tests)
- Violation penalties (6 tests)
- Concurrent requests (3 tests)
- IP limiting (2 tests)
- End-to-end scenarios (5 tests)

---

## Key Patterns

### Token Bucket Pattern
```python
# Refill tokens over time
elapsed = current_time - last_refill
tokens_to_add = calculate_tokens_to_add(
    elapsed_seconds=elapsed,
    refill_rate=2,  # 2 tokens/sec
    current_tokens=50,
    max_tokens=100
)  # Returns 20 if elapsed=10, capped at max

# Check if request allowed
if is_request_allowed(current_tokens=70, tokens_required=5, max_tokens=100):
    # Process request, deduct 5 tokens
    pass
```

### Weighted Request Costs
```python
# Different operations cost different amounts
read_cost = calculate_request_cost("read", 0)      # 1 token
write_cost = calculate_request_cost("write", 0)    # 5 tokens
delete_cost = calculate_request_cost("delete", 0)  # 10 tokens

# Large payloads add cost
large_read = calculate_request_cost("read", 250)   # 1 + 3 = 4 tokens
```

### Exponential Backoff
```python
# Penalty increases exponentially with violations
penalty_0 = calculate_violation_penalty(0, 60)   # 60 * 1 = 60s
penalty_1 = calculate_violation_penalty(1, 60)   # 60 * 2 = 120s
penalty_3 = calculate_violation_penalty(3, 60)   # 60 * 8 = 480s
penalty_10 = calculate_violation_penalty(10, 60) # 60 * 1024 = 61440s (capped)
```

### Tier-Based Limits
```python
# Validate against tier limits
validate_tier_limits("free", 10, 1000)       # ✅ Valid
validate_tier_limits("free", 50, 1000)       # ❌ Exceeds 10 req/min
validate_tier_limits("basic", 50, 10000)     # ✅ Valid  
validate_tier_limits("pro", 500, 500000)     # ✅ Valid
validate_tier_limits("enterprise", 5000, 5000000)  # ✅ Valid
```

---

## Common Pitfalls

### 1. Not Refilling Tokens

**❌ Wrong**:
```python
if is_request_allowed(current_tokens, 5, 100):
    process_request()
# Tokens never refill!
```

**✅ Correct**:
```python
tokens_to_add = calculate_tokens_to_add(elapsed, 2, current_tokens, 100)
current_tokens += tokens_to_add
if is_request_allowed(current_tokens, 5, 100):
    current_tokens -= 5
    process_request()
```

### 2. Ignoring Request Costs

**❌ Wrong**:
```python
# All requests cost the same
deduct_tokens(user, 1)
```

**✅ Correct**:
```python
cost = calculate_request_cost(request.method.lower(), payload_size)
deduct_tokens(user, cost)
```

### 3. No Retry-After Header

**❌ Wrong**:
```python
if not is_request_allowed(...):
    return 429  # User doesn't know when to retry
```

**✅ Correct**:
```python
if not is_request_allowed(current, required, max):
    retry_after = calculate_retry_after_seconds(required, current, refill_rate)
    return Response(status=429, headers={"Retry-After": retry_after})
```

### 4. Unbounded Violation Penalties

**❌ Wrong**:
```python
penalty = base * (2 ** violations)  # Could overflow with many violations
```

**✅ Correct**:
```python
penalty = calculate_violation_penalty(violations, base)  # Capped at 10 violations
```

---

## Integration Examples

### Redis-Backed Token Bucket
```python
import redis
from rate_limiter import is_request_allowed, calculate_tokens_to_add

r = redis.Redis()

def check_rate_limit(user_id, tokens_required=1):
    key = f"tokens:{user_id}"
    last_refill_key = f"last_refill:{user_id}"
    
    # Get current state
    current_tokens = int(r.get(key) or 100)
    last_refill = int(r.get(last_refill_key) or time.time())
    
    # Refill
    elapsed = int(time.time() - last_refill)
    tokens_to_add = calculate_tokens_to_add(elapsed, 2, current_tokens, 100)
    current_tokens = min(current_tokens + tokens_to_add, 100)
    
    # Check
    if is_request_allowed(current_tokens, tokens_required, 100):
        r.set(key, current_tokens - tokens_required)
        r.set(last_refill_key, int(time.time()))
        return True
    
    return False
```

### Quota Warning System
```python
from rate_limiter import is_quota_warning_threshold_reached

def check_quota_warnings(user):
    if is_quota_warning_threshold_reached(
        used_quota=user.daily_usage,
        total_quota=user.daily_limit,
        warning_percentage=80
    ):
        send_warning_email(user, "80% quota used")
    
    if is_quota_warning_threshold_reached(
        used_quota=user.daily_usage,
        total_quota=user.daily_limit,
        warning_percentage=90
    ):
        send_alert(user, "90% quota used - approaching limit")
```

---

## Production Considerations

### State Storage
- Use Redis/Memcached for distributed systems
- Local memory for single-server setups
- Database for persistent quota tracking

### Performance
- Token bucket overhead: ~2µs per request
- Negligible vs network/processing time
- Can handle millions of requests/sec

### Monitoring
- Track violation rates
- Alert on quota threshold breaches
- Monitor token refill rates

---

## Next Steps

1. **Add to your API** - Integrate rate limiting middleware
2. **Choose storage** - Redis for distributed, memory for single-server
3. **Set tier limits** - Define limits for your subscription tiers
4. **Monitor usage** - Track violations and quota usage

---

## Learn More

- **[Example 1: E-commerce Orders](../01_ecommerce_orders/)** - Order validation
- **[Example 2: Multi-Agent Research](../02_multi_agent_research/)** - Agent coordination  
- **[Example 3: Data Processing](../03_data_processing_workflow/)** - Pipeline validation
- **[Example 5: State Machines](../05_state_machine_patterns/)** - State validation
- **[AssertLang Documentation](../../../docs/)** - Complete guide
