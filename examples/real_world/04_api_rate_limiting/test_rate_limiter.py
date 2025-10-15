"""
Test suite for API Rate Limiting with Contract Validation

Demonstrates how contracts validate rate limits, quotas, and
token bucket algorithm implementations.
"""

import pytest
import sys
from pathlib import Path

# Add project root and current directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from promptware.runtime.contracts import ContractViolationError
from rate_limiter import (
    validate_rate_limit_config,
    is_request_allowed,
    calculate_tokens_to_add,
    validate_quota_limit,
    is_quota_warning_threshold_reached,
    validate_tier_limits,
    calculate_retry_after_seconds,
    is_burst_allowed,
    is_valid_time_window,
    should_reset_rate_limit,
    validate_concurrent_requests,
    calculate_request_cost,
    validate_ip_rate_limit,
    is_cooldown_active,
    validate_global_rate_limit,
    calculate_violation_penalty
)


class TestRateLimitConfig:
    """Test rate limit configuration validation."""

    def test_valid_config(self):
        """Valid rate limit config should pass."""
        result = validate_rate_limit_config(
            requests_per_window=100,
            window_seconds=60,
            burst_size=150
        )
        assert result is True

    def test_negative_requests_rejected(self):
        """Negative requests per window should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_rate_limit_config(
                requests_per_window=0,  # Invalid
                window_seconds=60,
                burst_size=150
            )
        assert "positive_requests" in str(exc_info.value)

    def test_excessive_window_rejected(self):
        """Window > 24 hours should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_rate_limit_config(
                requests_per_window=100,
                window_seconds=90000,  # > 86400 (24 hours)
                burst_size=150
            )
        assert "positive_window" in str(exc_info.value)

    def test_burst_smaller_than_rate_rejected(self):
        """Burst size smaller than rate should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_rate_limit_config(
                requests_per_window=100,
                window_seconds=60,
                burst_size=50  # Invalid: < requests_per_window
            )
        assert "valid_burst" in str(exc_info.value)


class TestTokenBucketAlgorithm:
    """Test token bucket algorithm validation."""

    def test_request_allowed_with_enough_tokens(self):
        """Request should be allowed with sufficient tokens."""
        result = is_request_allowed(
            current_token_count=10,
            tokens_required=5,
            max_tokens=100
        )
        assert result is True

    def test_request_rejected_insufficient_tokens(self):
        """Request should be rejected without enough tokens."""
        result = is_request_allowed(
            current_token_count=3,
            tokens_required=5,
            max_tokens=100
        )
        assert result is False

    def test_request_rejected_exceeds_max(self):
        """Request should be rejected if current exceeds max."""
        result = is_request_allowed(
            current_token_count=150,
            tokens_required=5,
            max_tokens=100
        )
        assert result is False

    def test_calculate_tokens_to_add(self):
        """Calculate tokens based on elapsed time."""
        result = calculate_tokens_to_add(
            elapsed_seconds=10,
            refill_rate=2,
            current_tokens=50,
            max_tokens=100
        )
        assert result == 20  # 10 seconds * 2 tokens/sec

    def test_tokens_capped_at_max(self):
        """Token refill should be capped at max."""
        result = calculate_tokens_to_add(
            elapsed_seconds=100,
            refill_rate=2,
            current_tokens=90,
            max_tokens=100
        )
        assert result == 10  # Capped: 90 + 10 = 100 max


class TestQuotaManagement:
    """Test quota validation."""

    def test_valid_quota_usage(self):
        """Valid quota usage should pass."""
        result = validate_quota_limit(
            used_quota=500,
            total_quota=1000,
            warning_threshold=800
        )
        assert result is True

    def test_exceeded_quota_rejected(self):
        """Exceeded quota should be rejected."""
        result = validate_quota_limit(
            used_quota=1100,
            total_quota=1000,
            warning_threshold=800
        )
        assert result is False

    def test_warning_threshold_not_reached(self):
        """Below warning threshold should return False."""
        result = is_quota_warning_threshold_reached(
            used_quota=700,
            total_quota=1000,
            warning_percentage=80  # 80% = 800
        )
        assert result is False

    def test_warning_threshold_reached(self):
        """At or above warning threshold should return True."""
        result = is_quota_warning_threshold_reached(
            used_quota=850,
            total_quota=1000,
            warning_percentage=80  # 80% = 800
        )
        assert result is True

    def test_warning_threshold_exact(self):
        """Exactly at threshold should return True."""
        result = is_quota_warning_threshold_reached(
            used_quota=800,
            total_quota=1000,
            warning_percentage=80
        )
        assert result is True


class TestTierLimits:
    """Test tier-based rate limit validation."""

    def test_free_tier_valid(self):
        """Free tier within limits should pass."""
        result = validate_tier_limits(
            tier="free",
            requests_per_minute=10,
            daily_quota=1000
        )
        assert result is True

    def test_free_tier_exceeded_rpm(self):
        """Free tier exceeding RPM should fail."""
        result = validate_tier_limits(
            tier="free",
            requests_per_minute=15,  # > 10
            daily_quota=1000
        )
        assert result is False

    def test_free_tier_exceeded_quota(self):
        """Free tier exceeding daily quota should fail."""
        result = validate_tier_limits(
            tier="free",
            requests_per_minute=10,
            daily_quota=2000  # > 1000
        )
        assert result is False

    def test_basic_tier_valid(self):
        """Basic tier within limits should pass."""
        result = validate_tier_limits(
            tier="basic",
            requests_per_minute=100,
            daily_quota=50000
        )
        assert result is True

    def test_basic_tier_exceeded(self):
        """Basic tier exceeding limits should fail."""
        result = validate_tier_limits(
            tier="basic",
            requests_per_minute=150,  # > 100
            daily_quota=50000
        )
        assert result is False

    def test_pro_tier_valid(self):
        """Pro tier within limits should pass."""
        result = validate_tier_limits(
            tier="pro",
            requests_per_minute=1000,
            daily_quota=1000000
        )
        assert result is True

    def test_enterprise_tier_valid(self):
        """Enterprise tier within limits should pass."""
        result = validate_tier_limits(
            tier="enterprise",
            requests_per_minute=10000,
            daily_quota=10000000
        )
        assert result is True

    def test_unknown_tier_rejected(self):
        """Unknown tier should be rejected."""
        result = validate_tier_limits(
            tier="premium",  # Unknown tier
            requests_per_minute=100,
            daily_quota=50000
        )
        assert result is False


class TestRetryLogic:
    """Test retry-after calculation."""

    def test_retry_after_calculation(self):
        """Calculate retry-after seconds."""
        result = calculate_retry_after_seconds(
            tokens_needed=10,
            current_tokens=5,
            refill_rate=1
        )
        assert result == 5  # Need 5 more tokens, 1/sec = 5 seconds

    def test_retry_after_with_remainder(self):
        """Retry calculation should round up."""
        result = calculate_retry_after_seconds(
            tokens_needed=10,
            current_tokens=4,
            refill_rate=2
        )
        assert result == 3  # Need 6 tokens, 2/sec = 3 seconds

    def test_no_retry_if_enough_tokens(self):
        """No retry needed if already have enough tokens."""
        result = calculate_retry_after_seconds(
            tokens_needed=10,
            current_tokens=15,
            refill_rate=1
        )
        assert result == 0


class TestBurstAllowance:
    """Test burst traffic validation."""

    def test_burst_allowed(self):
        """Burst within limits should be allowed."""
        result = is_burst_allowed(
            burst_size=150,
            normal_rate=100,
            requests_in_burst=120
        )
        assert result is True

    def test_burst_size_too_small_rejected(self):
        """Burst size <= normal rate should be rejected."""
        result = is_burst_allowed(
            burst_size=100,
            normal_rate=100,
            requests_in_burst=50
        )
        assert result is False

    def test_burst_exceeded_rejected(self):
        """Requests exceeding burst size should be rejected."""
        result = is_burst_allowed(
            burst_size=150,
            normal_rate=100,
            requests_in_burst=200  # Exceeds burst
        )
        assert result is False


class TestTimeWindows:
    """Test time window validation."""

    def test_valid_time_window(self):
        """Valid time window should pass."""
        result = is_valid_time_window(
            window_start=1000,
            window_end=2000,
            current_time=1500
        )
        assert result is True

    def test_end_before_start_rejected(self):
        """Window end before start should be rejected."""
        result = is_valid_time_window(
            window_start=2000,
            window_end=1000,  # Before start
            current_time=1500
        )
        assert result is False

    def test_current_before_start_rejected(self):
        """Current time before window start should be rejected."""
        result = is_valid_time_window(
            window_start=2000,
            window_end=3000,
            current_time=1500  # Before window
        )
        assert result is False


class TestRateLimitReset:
    """Test rate limit reset logic."""

    def test_reset_needed(self):
        """Reset should be needed after interval elapsed."""
        result = should_reset_rate_limit(
            last_reset_time=1000,
            current_time=2000,
            reset_interval=900
        )
        assert result is True  # 1000 seconds elapsed > 900

    def test_reset_not_needed(self):
        """Reset should not be needed before interval."""
        result = should_reset_rate_limit(
            last_reset_time=1000,
            current_time=1500,
            reset_interval=900
        )
        assert result is False  # Only 500 seconds elapsed

    def test_reset_exact_interval(self):
        """Reset should trigger at exact interval."""
        result = should_reset_rate_limit(
            last_reset_time=1000,
            current_time=1900,
            reset_interval=900
        )
        assert result is True  # Exactly 900 seconds


class TestConcurrentRequests:
    """Test concurrent request limit validation."""

    def test_concurrent_within_limit(self):
        """Concurrent requests within limit should pass."""
        result = validate_concurrent_requests(
            active_requests=50,
            max_concurrent=100
        )
        assert result is True

    def test_concurrent_at_limit_rejected(self):
        """Concurrent requests at limit should be rejected."""
        result = validate_concurrent_requests(
            active_requests=100,
            max_concurrent=100
        )
        assert result is False

    def test_concurrent_exceeds_limit_rejected(self):
        """Concurrent requests exceeding limit should be rejected."""
        result = validate_concurrent_requests(
            active_requests=150,
            max_concurrent=100
        )
        assert result is False


class TestWeightedRateLimiting:
    """Test weighted request cost calculation."""

    def test_read_request_cost(self):
        """Read requests should cost 1 token."""
        result = calculate_request_cost(
            endpoint_type="read",
            payload_size_kb=0
        )
        assert result == 1

    def test_write_request_cost(self):
        """Write requests should cost 5 tokens."""
        result = calculate_request_cost(
            endpoint_type="write",
            payload_size_kb=0
        )
        assert result == 5

    def test_delete_request_cost(self):
        """Delete requests should cost 10 tokens."""
        result = calculate_request_cost(
            endpoint_type="delete",
            payload_size_kb=0
        )
        assert result == 10

    def test_search_request_cost(self):
        """Search requests should cost 3 tokens."""
        result = calculate_request_cost(
            endpoint_type="search",
            payload_size_kb=0
        )
        assert result == 3

    def test_large_payload_cost(self):
        """Large payloads should add cost."""
        result = calculate_request_cost(
            endpoint_type="read",
            payload_size_kb=250  # 250KB = 3 additional tokens (100KB each)
        )
        assert result == 4  # 1 (base) + 3 (size)

    def test_payload_cost_rounding(self):
        """Payload cost should round up."""
        result = calculate_request_cost(
            endpoint_type="read",
            payload_size_kb=150  # 150KB = 2 tokens (rounds up)
        )
        assert result == 3  # 1 (base) + 2 (size)


class TestIPRateLimiting:
    """Test IP-based rate limiting."""

    def test_ip_within_limit(self):
        """IP requests within limit should pass."""
        result = validate_ip_rate_limit(
            requests_from_ip=50,
            max_requests_per_ip=100,
            time_window_seconds=60
        )
        assert result is True

    def test_ip_exceeds_limit(self):
        """IP requests exceeding limit should fail."""
        result = validate_ip_rate_limit(
            requests_from_ip=150,
            max_requests_per_ip=100,
            time_window_seconds=60
        )
        assert result is False


class TestCooldownPeriod:
    """Test cooldown period validation."""

    def test_cooldown_active(self):
        """Cooldown should be active within period."""
        result = is_cooldown_active(
            last_violation_time=1000,
            current_time=1300,
            cooldown_seconds=600
        )
        assert result is True  # 300 seconds < 600

    def test_cooldown_expired(self):
        """Cooldown should expire after period."""
        result = is_cooldown_active(
            last_violation_time=1000,
            current_time=1700,
            cooldown_seconds=600
        )
        assert result is False  # 700 seconds >= 600


class TestGlobalRateLimiting:
    """Test global rate limit validation."""

    def test_global_within_limit(self):
        """Global requests within limit should pass."""
        result = validate_global_rate_limit(
            total_requests=50000,
            max_global_requests=100000,
            time_window_seconds=60
        )
        assert result is True

    def test_global_exceeds_limit(self):
        """Global requests exceeding limit should fail."""
        result = validate_global_rate_limit(
            total_requests=150000,
            max_global_requests=100000,
            time_window_seconds=60
        )
        assert result is False


class TestViolationPenalty:
    """Test exponential backoff penalty calculation."""

    def test_zero_violations(self):
        """Zero violations should have no multiplier."""
        result = calculate_violation_penalty(
            violation_count=0,
            base_penalty_seconds=60
        )
        assert result == 60  # 60 * 1

    def test_one_violation(self):
        """One violation should double penalty."""
        result = calculate_violation_penalty(
            violation_count=1,
            base_penalty_seconds=60
        )
        assert result == 120  # 60 * 2

    def test_three_violations(self):
        """Three violations should multiply by 8."""
        result = calculate_violation_penalty(
            violation_count=3,
            base_penalty_seconds=60
        )
        assert result == 480  # 60 * 8

    def test_five_violations(self):
        """Five violations should multiply by 32."""
        result = calculate_violation_penalty(
            violation_count=5,
            base_penalty_seconds=60
        )
        assert result == 1920  # 60 * 32

    def test_ten_violations_capped(self):
        """Ten violations should cap at 1024."""
        result = calculate_violation_penalty(
            violation_count=10,
            base_penalty_seconds=60
        )
        assert result == 61440  # 60 * 1024

    def test_excessive_violations_capped(self):
        """More than 10 violations should cap at 1024."""
        result = calculate_violation_penalty(
            violation_count=15,
            base_penalty_seconds=60
        )
        assert result == 61440  # 60 * 1024 (capped)


class TestEndToEndScenarios:
    """Test complete rate limiting scenarios."""

    def test_successful_request_flow(self):
        """Test successful request processing."""
        # Validate config
        assert validate_rate_limit_config(100, 60, 150) is True

        # Check token availability
        assert is_request_allowed(50, 5, 100) is True

        # Process request with weight
        cost = calculate_request_cost("read", 0)
        assert cost == 1

        # Check quota
        assert validate_quota_limit(500, 1000, 800) is True

    def test_rate_limit_exceeded_flow(self):
        """Test rate limit exceeded scenario."""
        # Request rejected (insufficient tokens)
        assert is_request_allowed(2, 5, 100) is False

        # Calculate retry-after
        retry_seconds = calculate_retry_after_seconds(5, 2, 1)
        assert retry_seconds == 3

        # Violation penalty applied
        penalty = calculate_violation_penalty(1, 60)
        assert penalty == 120

    def test_tier_upgrade_flow(self):
        """Test tier limit validation across tiers."""
        # Free tier limits
        assert validate_tier_limits("free", 10, 1000) is True
        assert validate_tier_limits("free", 50, 1000) is False

        # Basic tier allows more
        assert validate_tier_limits("basic", 50, 10000) is True

        # Pro tier allows even more
        assert validate_tier_limits("pro", 500, 500000) is True

    def test_burst_traffic_handling(self):
        """Test burst traffic scenario."""
        # Normal config
        assert validate_rate_limit_config(100, 60, 150) is True

        # Burst allowed
        assert is_burst_allowed(150, 100, 120) is True

        # Too many requests in burst
        assert is_burst_allowed(150, 100, 200) is False

    def test_quota_warning_flow(self):
        """Test quota warning scenario."""
        # Below warning threshold
        assert is_quota_warning_threshold_reached(700, 1000, 80) is False

        # Approaching threshold
        assert is_quota_warning_threshold_reached(850, 1000, 80) is True

        # Quota exceeded
        assert validate_quota_limit(1100, 1000, 800) is False


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
