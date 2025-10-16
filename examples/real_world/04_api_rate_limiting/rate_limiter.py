from __future__ import annotations

from assertlang.runtime.contracts import check_postcondition
from assertlang.runtime.contracts import check_precondition

def validate_rate_limit_config(requests_per_window: int, window_seconds: int, burst_size: int) -> bool:
    check_precondition(
    (requests_per_window > 0),
    "positive_requests",
    "requests_per_window > 0",
    "validate_rate_limit_config",
    context={"requests_per_window": requests_per_window, "window_seconds": window_seconds, "burst_size": burst_size}
)
    check_precondition(
    ((window_seconds > 0) and (window_seconds <= 86400)),
    "positive_window",
    "window_seconds > 0 and window_seconds <= 86400",
    "validate_rate_limit_config",
    context={"requests_per_window": requests_per_window, "window_seconds": window_seconds, "burst_size": burst_size}
)
    check_precondition(
    (burst_size >= requests_per_window),
    "valid_burst",
    "burst_size >= requests_per_window",
    "validate_rate_limit_config",
    context={"requests_per_window": requests_per_window, "window_seconds": window_seconds, "burst_size": burst_size}
)
    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
    (__result == True),
    "config_valid",
    "result == True",
    "validate_rate_limit_config",
    context=dict([("result", __result), ("requests_per_window", requests_per_window), ("window_seconds", window_seconds), ("burst_size", burst_size)])
)
    return __result


def is_request_allowed(current_token_count: int, tokens_required: int, max_tokens: int) -> bool:
    check_precondition(
    (current_token_count >= 0),
    "valid_current",
    "current_token_count >= 0",
    "is_request_allowed",
    context={"current_token_count": current_token_count, "tokens_required": tokens_required, "max_tokens": max_tokens}
)
    check_precondition(
    (tokens_required > 0),
    "valid_required",
    "tokens_required > 0",
    "is_request_allowed",
    context={"current_token_count": current_token_count, "tokens_required": tokens_required, "max_tokens": max_tokens}
)
    check_precondition(
    (max_tokens > 0),
    "valid_max",
    "max_tokens > 0",
    "is_request_allowed",
    context={"current_token_count": current_token_count, "tokens_required": tokens_required, "max_tokens": max_tokens}
)
    __result = None
    try:
        if (current_token_count < tokens_required):
            __result = False
            return __result
        if (current_token_count > max_tokens):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "decision_made",
    "result == True or result == False",
    "is_request_allowed",
    context=dict([("result", __result), ("current_token_count", current_token_count), ("tokens_required", tokens_required), ("max_tokens", max_tokens)])
)
    return __result


def calculate_tokens_to_add(elapsed_seconds: int, refill_rate: int, current_tokens: int, max_tokens: int) -> int:
    check_precondition(
    (elapsed_seconds >= 0),
    "valid_elapsed",
    "elapsed_seconds >= 0",
    "calculate_tokens_to_add",
    context={"elapsed_seconds": elapsed_seconds, "refill_rate": refill_rate, "current_tokens": current_tokens, "max_tokens": max_tokens}
)
    check_precondition(
    (refill_rate > 0),
    "positive_refill",
    "refill_rate > 0",
    "calculate_tokens_to_add",
    context={"elapsed_seconds": elapsed_seconds, "refill_rate": refill_rate, "current_tokens": current_tokens, "max_tokens": max_tokens}
)
    check_precondition(
    ((current_tokens >= 0) and (current_tokens <= max_tokens)),
    "valid_current",
    "current_tokens >= 0 and current_tokens <= max_tokens",
    "calculate_tokens_to_add",
    context={"elapsed_seconds": elapsed_seconds, "refill_rate": refill_rate, "current_tokens": current_tokens, "max_tokens": max_tokens}
)
    check_precondition(
    (max_tokens > 0),
    "positive_max",
    "max_tokens > 0",
    "calculate_tokens_to_add",
    context={"elapsed_seconds": elapsed_seconds, "refill_rate": refill_rate, "current_tokens": current_tokens, "max_tokens": max_tokens}
)
    __result = None
    try:
        tokens_to_add = (elapsed_seconds * refill_rate)
        potential_total = (current_tokens + tokens_to_add)
        if (potential_total > max_tokens):
            tokens_to_add = (max_tokens - current_tokens)
        __result = tokens_to_add
        return __result
    finally:
        check_postcondition(
    (__result >= 0),
    "valid_result",
    "result >= 0",
    "calculate_tokens_to_add",
    context=dict([("result", __result), ("elapsed_seconds", elapsed_seconds), ("refill_rate", refill_rate), ("current_tokens", current_tokens), ("max_tokens", max_tokens)])
)
    return __result


def validate_quota_limit(used_quota: int, total_quota: int, warning_threshold: int) -> bool:
    check_precondition(
    (used_quota >= 0),
    "valid_used",
    "used_quota >= 0",
    "validate_quota_limit",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_threshold": warning_threshold}
)
    check_precondition(
    (total_quota > 0),
    "positive_total",
    "total_quota > 0",
    "validate_quota_limit",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_threshold": warning_threshold}
)
    check_precondition(
    ((warning_threshold > 0) and (warning_threshold <= total_quota)),
    "valid_threshold",
    "warning_threshold > 0 and warning_threshold <= total_quota",
    "validate_quota_limit",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_threshold": warning_threshold}
)
    __result = None
    try:
        if (used_quota > total_quota):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "quota_validated",
    "result == True or result == False",
    "validate_quota_limit",
    context=dict([("result", __result), ("used_quota", used_quota), ("total_quota", total_quota), ("warning_threshold", warning_threshold)])
)
    return __result


def is_quota_warning_threshold_reached(used_quota: int, total_quota: int, warning_percentage: int) -> bool:
    check_precondition(
    (used_quota >= 0),
    "valid_used",
    "used_quota >= 0",
    "is_quota_warning_threshold_reached",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_percentage": warning_percentage}
)
    check_precondition(
    (total_quota > 0),
    "positive_total",
    "total_quota > 0",
    "is_quota_warning_threshold_reached",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_percentage": warning_percentage}
)
    check_precondition(
    ((warning_percentage > 0) and (warning_percentage <= 100)),
    "valid_percentage",
    "warning_percentage > 0 and warning_percentage <= 100",
    "is_quota_warning_threshold_reached",
    context={"used_quota": used_quota, "total_quota": total_quota, "warning_percentage": warning_percentage}
)
    __result = None
    try:
        if ((used_quota * 100) >= (total_quota * warning_percentage)):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "threshold_checked",
    "result == True or result == False",
    "is_quota_warning_threshold_reached",
    context=dict([("result", __result), ("used_quota", used_quota), ("total_quota", total_quota), ("warning_percentage", warning_percentage)])
)
    return __result


def validate_tier_limits(tier: str, requests_per_minute: int, daily_quota: int) -> bool:
    check_precondition(
    (len(tier) > 0),
    "valid_tier",
    "len(tier) > 0",
    "validate_tier_limits",
    context={"tier": tier, "requests_per_minute": requests_per_minute, "daily_quota": daily_quota}
)
    check_precondition(
    (requests_per_minute > 0),
    "positive_requests",
    "requests_per_minute > 0",
    "validate_tier_limits",
    context={"tier": tier, "requests_per_minute": requests_per_minute, "daily_quota": daily_quota}
)
    check_precondition(
    (daily_quota > 0),
    "positive_quota",
    "daily_quota > 0",
    "validate_tier_limits",
    context={"tier": tier, "requests_per_minute": requests_per_minute, "daily_quota": daily_quota}
)
    __result = None
    try:
        if (tier == "free"):
            if (requests_per_minute > 10):
                __result = False
                return __result
            if (daily_quota > 1000):
                __result = False
                return __result
            __result = True
            return __result
        if (tier == "basic"):
            if (requests_per_minute > 100):
                __result = False
                return __result
            if (daily_quota > 50000):
                __result = False
                return __result
            __result = True
            return __result
        if (tier == "pro"):
            if (requests_per_minute > 1000):
                __result = False
                return __result
            if (daily_quota > 1000000):
                __result = False
                return __result
            __result = True
            return __result
        if (tier == "enterprise"):
            if (requests_per_minute > 10000):
                __result = False
                return __result
            if (daily_quota > 10000000):
                __result = False
                return __result
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "tier_validated",
    "result == True or result == False",
    "validate_tier_limits",
    context=dict([("result", __result), ("tier", tier), ("requests_per_minute", requests_per_minute), ("daily_quota", daily_quota)])
)
    return __result


def calculate_retry_after_seconds(tokens_needed: int, current_tokens: int, refill_rate: int) -> int:
    check_precondition(
    (tokens_needed > 0),
    "positive_needed",
    "tokens_needed > 0",
    "calculate_retry_after_seconds",
    context={"tokens_needed": tokens_needed, "current_tokens": current_tokens, "refill_rate": refill_rate}
)
    check_precondition(
    (current_tokens >= 0),
    "valid_current",
    "current_tokens >= 0",
    "calculate_retry_after_seconds",
    context={"tokens_needed": tokens_needed, "current_tokens": current_tokens, "refill_rate": refill_rate}
)
    check_precondition(
    (refill_rate > 0),
    "positive_refill",
    "refill_rate > 0",
    "calculate_retry_after_seconds",
    context={"tokens_needed": tokens_needed, "current_tokens": current_tokens, "refill_rate": refill_rate}
)
    __result = None
    try:
        tokens_short = (tokens_needed - current_tokens)
        if (tokens_short <= 0):
            __result = 0
            return __result
        seconds_needed = (tokens_short // refill_rate)
        if ((tokens_short % refill_rate) > 0):
            seconds_needed = (seconds_needed + 1)
        __result = seconds_needed
        return __result
    finally:
        check_postcondition(
    (__result >= 0),
    "valid_retry",
    "result >= 0",
    "calculate_retry_after_seconds",
    context=dict([("result", __result), ("tokens_needed", tokens_needed), ("current_tokens", current_tokens), ("refill_rate", refill_rate)])
)
    return __result


def is_burst_allowed(burst_size: int, normal_rate: int, requests_in_burst: int) -> bool:
    check_precondition(
    (burst_size > 0),
    "positive_burst",
    "burst_size > 0",
    "is_burst_allowed",
    context={"burst_size": burst_size, "normal_rate": normal_rate, "requests_in_burst": requests_in_burst}
)
    check_precondition(
    (normal_rate > 0),
    "positive_rate",
    "normal_rate > 0",
    "is_burst_allowed",
    context={"burst_size": burst_size, "normal_rate": normal_rate, "requests_in_burst": requests_in_burst}
)
    check_precondition(
    (requests_in_burst >= 0),
    "valid_requests",
    "requests_in_burst >= 0",
    "is_burst_allowed",
    context={"burst_size": burst_size, "normal_rate": normal_rate, "requests_in_burst": requests_in_burst}
)
    __result = None
    try:
        if (burst_size <= normal_rate):
            __result = False
            return __result
        if (requests_in_burst > burst_size):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "burst_decided",
    "result == True or result == False",
    "is_burst_allowed",
    context=dict([("result", __result), ("burst_size", burst_size), ("normal_rate", normal_rate), ("requests_in_burst", requests_in_burst)])
)
    return __result


def is_valid_time_window(window_start: int, window_end: int, current_time: int) -> bool:
    check_precondition(
    (window_start >= 0),
    "valid_start",
    "window_start >= 0",
    "is_valid_time_window",
    context={"window_start": window_start, "window_end": window_end, "current_time": current_time}
)
    check_precondition(
    (window_end >= 0),
    "valid_end",
    "window_end >= 0",
    "is_valid_time_window",
    context={"window_start": window_start, "window_end": window_end, "current_time": current_time}
)
    check_precondition(
    (current_time >= 0),
    "valid_current",
    "current_time >= 0",
    "is_valid_time_window",
    context={"window_start": window_start, "window_end": window_end, "current_time": current_time}
)
    __result = None
    try:
        if (window_end <= window_start):
            __result = False
            return __result
        if (current_time < window_start):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "window_validated",
    "result == True or result == False",
    "is_valid_time_window",
    context=dict([("result", __result), ("window_start", window_start), ("window_end", window_end), ("current_time", current_time)])
)
    return __result


def should_reset_rate_limit(last_reset_time: int, current_time: int, reset_interval: int) -> bool:
    check_precondition(
    (last_reset_time >= 0),
    "valid_last_reset",
    "last_reset_time >= 0",
    "should_reset_rate_limit",
    context={"last_reset_time": last_reset_time, "current_time": current_time, "reset_interval": reset_interval}
)
    check_precondition(
    (current_time >= 0),
    "valid_current",
    "current_time >= 0",
    "should_reset_rate_limit",
    context={"last_reset_time": last_reset_time, "current_time": current_time, "reset_interval": reset_interval}
)
    check_precondition(
    (reset_interval > 0),
    "positive_interval",
    "reset_interval > 0",
    "should_reset_rate_limit",
    context={"last_reset_time": last_reset_time, "current_time": current_time, "reset_interval": reset_interval}
)
    __result = None
    try:
        time_since_reset = (current_time - last_reset_time)
        if (time_since_reset >= reset_interval):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "reset_decided",
    "result == True or result == False",
    "should_reset_rate_limit",
    context=dict([("result", __result), ("last_reset_time", last_reset_time), ("current_time", current_time), ("reset_interval", reset_interval)])
)
    return __result


def validate_concurrent_requests(active_requests: int, max_concurrent: int) -> bool:
    check_precondition(
    (active_requests >= 0),
    "valid_active",
    "active_requests >= 0",
    "validate_concurrent_requests",
    context={"active_requests": active_requests, "max_concurrent": max_concurrent}
)
    check_precondition(
    (max_concurrent > 0),
    "positive_max",
    "max_concurrent > 0",
    "validate_concurrent_requests",
    context={"active_requests": active_requests, "max_concurrent": max_concurrent}
)
    __result = None
    try:
        if (active_requests >= max_concurrent):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "concurrent_validated",
    "result == True or result == False",
    "validate_concurrent_requests",
    context=dict([("result", __result), ("active_requests", active_requests), ("max_concurrent", max_concurrent)])
)
    return __result


def calculate_request_cost(endpoint_type: str, payload_size_kb: int) -> int:
    check_precondition(
    (len(endpoint_type) > 0),
    "valid_endpoint",
    "len(endpoint_type) > 0",
    "calculate_request_cost",
    context={"endpoint_type": endpoint_type, "payload_size_kb": payload_size_kb}
)
    check_precondition(
    (payload_size_kb >= 0),
    "valid_size",
    "payload_size_kb >= 0",
    "calculate_request_cost",
    context={"endpoint_type": endpoint_type, "payload_size_kb": payload_size_kb}
)
    __result = None
    try:
        base_cost = 1
        if (endpoint_type == "read"):
            base_cost = 1
        if (endpoint_type == "write"):
            base_cost = 5
        if (endpoint_type == "delete"):
            base_cost = 10
        if (endpoint_type == "search"):
            base_cost = 3
        size_cost = (payload_size_kb // 100)
        if ((payload_size_kb % 100) > 0):
            size_cost = (size_cost + 1)
        total_cost = (base_cost + size_cost)
        __result = total_cost
        return __result
    finally:
        check_postcondition(
    (__result > 0),
    "positive_cost",
    "result > 0",
    "calculate_request_cost",
    context=dict([("result", __result), ("endpoint_type", endpoint_type), ("payload_size_kb", payload_size_kb)])
)
    return __result


def validate_ip_rate_limit(requests_from_ip: int, max_requests_per_ip: int, time_window_seconds: int) -> bool:
    check_precondition(
    (requests_from_ip >= 0),
    "valid_requests",
    "requests_from_ip >= 0",
    "validate_ip_rate_limit",
    context={"requests_from_ip": requests_from_ip, "max_requests_per_ip": max_requests_per_ip, "time_window_seconds": time_window_seconds}
)
    check_precondition(
    (max_requests_per_ip > 0),
    "positive_max",
    "max_requests_per_ip > 0",
    "validate_ip_rate_limit",
    context={"requests_from_ip": requests_from_ip, "max_requests_per_ip": max_requests_per_ip, "time_window_seconds": time_window_seconds}
)
    check_precondition(
    (time_window_seconds > 0),
    "positive_window",
    "time_window_seconds > 0",
    "validate_ip_rate_limit",
    context={"requests_from_ip": requests_from_ip, "max_requests_per_ip": max_requests_per_ip, "time_window_seconds": time_window_seconds}
)
    __result = None
    try:
        if (requests_from_ip > max_requests_per_ip):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "ip_limit_validated",
    "result == True or result == False",
    "validate_ip_rate_limit",
    context=dict([("result", __result), ("requests_from_ip", requests_from_ip), ("max_requests_per_ip", max_requests_per_ip), ("time_window_seconds", time_window_seconds)])
)
    return __result


def is_cooldown_active(last_violation_time: int, current_time: int, cooldown_seconds: int) -> bool:
    check_precondition(
    (last_violation_time >= 0),
    "valid_last_violation",
    "last_violation_time >= 0",
    "is_cooldown_active",
    context={"last_violation_time": last_violation_time, "current_time": current_time, "cooldown_seconds": cooldown_seconds}
)
    check_precondition(
    (current_time >= 0),
    "valid_current",
    "current_time >= 0",
    "is_cooldown_active",
    context={"last_violation_time": last_violation_time, "current_time": current_time, "cooldown_seconds": cooldown_seconds}
)
    check_precondition(
    (cooldown_seconds > 0),
    "positive_cooldown",
    "cooldown_seconds > 0",
    "is_cooldown_active",
    context={"last_violation_time": last_violation_time, "current_time": current_time, "cooldown_seconds": cooldown_seconds}
)
    __result = None
    try:
        time_since_violation = (current_time - last_violation_time)
        if (time_since_violation < cooldown_seconds):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "cooldown_checked",
    "result == True or result == False",
    "is_cooldown_active",
    context=dict([("result", __result), ("last_violation_time", last_violation_time), ("current_time", current_time), ("cooldown_seconds", cooldown_seconds)])
)
    return __result


def validate_global_rate_limit(total_requests: int, max_global_requests: int, time_window_seconds: int) -> bool:
    check_precondition(
    (total_requests >= 0),
    "valid_total",
    "total_requests >= 0",
    "validate_global_rate_limit",
    context={"total_requests": total_requests, "max_global_requests": max_global_requests, "time_window_seconds": time_window_seconds}
)
    check_precondition(
    (max_global_requests > 0),
    "positive_max",
    "max_global_requests > 0",
    "validate_global_rate_limit",
    context={"total_requests": total_requests, "max_global_requests": max_global_requests, "time_window_seconds": time_window_seconds}
)
    check_precondition(
    (time_window_seconds > 0),
    "positive_window",
    "time_window_seconds > 0",
    "validate_global_rate_limit",
    context={"total_requests": total_requests, "max_global_requests": max_global_requests, "time_window_seconds": time_window_seconds}
)
    __result = None
    try:
        if (total_requests > max_global_requests):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "global_limit_validated",
    "result == True or result == False",
    "validate_global_rate_limit",
    context=dict([("result", __result), ("total_requests", total_requests), ("max_global_requests", max_global_requests), ("time_window_seconds", time_window_seconds)])
)
    return __result


def calculate_violation_penalty(violation_count: int, base_penalty_seconds: int) -> int:
    check_precondition(
    (violation_count >= 0),
    "valid_count",
    "violation_count >= 0",
    "calculate_violation_penalty",
    context={"violation_count": violation_count, "base_penalty_seconds": base_penalty_seconds}
)
    check_precondition(
    (base_penalty_seconds > 0),
    "positive_base",
    "base_penalty_seconds > 0",
    "calculate_violation_penalty",
    context={"violation_count": violation_count, "base_penalty_seconds": base_penalty_seconds}
)
    __result = None
    try:
        multiplier = 1
        if (violation_count == 0):
            multiplier = 1
        if (violation_count == 1):
            multiplier = 2
        if (violation_count == 2):
            multiplier = 4
        if (violation_count == 3):
            multiplier = 8
        if (violation_count == 4):
            multiplier = 16
        if (violation_count == 5):
            multiplier = 32
        if (violation_count == 6):
            multiplier = 64
        if (violation_count == 7):
            multiplier = 128
        if (violation_count == 8):
            multiplier = 256
        if (violation_count == 9):
            multiplier = 512
        if (violation_count >= 10):
            multiplier = 1024
        penalty = (base_penalty_seconds * multiplier)
        __result = penalty
        return __result
    finally:
        check_postcondition(
    (__result > 0),
    "positive_penalty",
    "result > 0",
    "calculate_violation_penalty",
    context=dict([("result", __result), ("violation_count", violation_count), ("base_penalty_seconds", base_penalty_seconds)])
)
    return __result
