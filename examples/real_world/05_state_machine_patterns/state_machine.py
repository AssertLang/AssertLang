from __future__ import annotations

from assertlang.runtime.contracts import check_postcondition
from assertlang.runtime.contracts import check_precondition

def is_valid_state(state: str) -> bool:
    check_precondition(
    (len(state) > 0),
    "non_empty_state",
    "len(state) > 0",
    "is_valid_state",
    context={"state": state}
)
    __result = None
    try:
        if (state == "idle"):
            __result = True
            return __result
        if (state == "active"):
            __result = True
            return __result
        if (state == "paused"):
            __result = True
            return __result
        if (state == "completed"):
            __result = True
            return __result
        if (state == "failed"):
            __result = True
            return __result
        if (state == "cancelled"):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "validation_complete",
    "result == True or result == False",
    "is_valid_state",
    context=dict([("result", __result), ("state", state)])
)
    return __result


def can_transition(from_state: str, to_state: str) -> bool:
    check_precondition(
    (len(from_state) > 0),
    "valid_from",
    "len(from_state) > 0",
    "can_transition",
    context={"from_state": from_state, "to_state": to_state}
)
    check_precondition(
    (len(to_state) > 0),
    "valid_to",
    "len(to_state) > 0",
    "can_transition",
    context={"from_state": from_state, "to_state": to_state}
)
    __result = None
    try:
        if (from_state == "idle"):
            if ((to_state == "active") or (to_state == "cancelled")):
                __result = True
                return __result
            __result = False
            return __result
        if (from_state == "active"):
            if ((((to_state == "paused") or (to_state == "completed")) or (to_state == "failed")) or (to_state == "cancelled")):
                __result = True
                return __result
            __result = False
            return __result
        if (from_state == "paused"):
            if ((to_state == "active") or (to_state == "cancelled")):
                __result = True
                return __result
            __result = False
            return __result
        if (from_state == "completed"):
            __result = False
            return __result
        if (from_state == "failed"):
            if (to_state == "idle"):
                __result = True
                return __result
            __result = False
            return __result
        if (from_state == "cancelled"):
            __result = False
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "transition_decided",
    "result == True or result == False",
    "can_transition",
    context=dict([("result", __result), ("from_state", from_state), ("to_state", to_state)])
)
    return __result


def validate_state_data(state: str, data_present: bool, data_valid: bool) -> bool:
    check_precondition(
    (len(state) > 0),
    "valid_state",
    "len(state) > 0",
    "validate_state_data",
    context={"state": state, "data_present": data_present, "data_valid": data_valid}
)
    __result = None
    try:
        if (state == "idle"):
            __result = True
            return __result
        if (state == "active"):
            if (data_present == False):
                __result = False
                return __result
            if (data_valid == False):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "paused"):
            if (data_present == False):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "completed"):
            if (data_present == False):
                __result = False
                return __result
            if (data_valid == False):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "failed"):
            __result = True
            return __result
        if (state == "cancelled"):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "data_validated",
    "result == True or result == False",
    "validate_state_data",
    context=dict([("result", __result), ("state", state), ("data_present", data_present), ("data_valid", data_valid)])
)
    return __result


def check_entry_condition(target_state: str, precondition_met: bool) -> bool:
    check_precondition(
    (len(target_state) > 0),
    "valid_target",
    "len(target_state) > 0",
    "check_entry_condition",
    context={"target_state": target_state, "precondition_met": precondition_met}
)
    __result = None
    try:
        if (target_state == "idle"):
            __result = True
            return __result
        if (target_state == "active"):
            if (precondition_met == False):
                __result = False
                return __result
            __result = True
            return __result
        if (target_state == "paused"):
            __result = True
            return __result
        if (target_state == "completed"):
            if (precondition_met == False):
                __result = False
                return __result
            __result = True
            return __result
        if (target_state == "failed"):
            __result = True
            return __result
        if (target_state == "cancelled"):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "entry_checked",
    "result == True or result == False",
    "check_entry_condition",
    context=dict([("result", __result), ("target_state", target_state), ("precondition_met", precondition_met)])
)
    return __result


def check_exit_condition(source_state: str, cleanup_done: bool) -> bool:
    check_precondition(
    (len(source_state) > 0),
    "valid_source",
    "len(source_state) > 0",
    "check_exit_condition",
    context={"source_state": source_state, "cleanup_done": cleanup_done}
)
    __result = None
    try:
        if (source_state == "idle"):
            __result = True
            return __result
        if (source_state == "active"):
            if (cleanup_done == False):
                __result = False
                return __result
            __result = True
            return __result
        if (source_state == "paused"):
            __result = True
            return __result
        if (source_state == "completed"):
            __result = False
            return __result
        if (source_state == "failed"):
            __result = True
            return __result
        if (source_state == "cancelled"):
            __result = False
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "exit_checked",
    "result == True or result == False",
    "check_exit_condition",
    context=dict([("result", __result), ("source_state", source_state), ("cleanup_done", cleanup_done)])
)
    return __result


def is_terminal_state(state: str) -> bool:
    check_precondition(
    (len(state) > 0),
    "valid_state",
    "len(state) > 0",
    "is_terminal_state",
    context={"state": state}
)
    __result = None
    try:
        if ((state == "completed") or (state == "cancelled")):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "terminal_checked",
    "result == True or result == False",
    "is_terminal_state",
    context=dict([("result", __result), ("state", state)])
)
    return __result


def can_retry_from_state(state: str) -> bool:
    check_precondition(
    (len(state) > 0),
    "valid_state",
    "len(state) > 0",
    "can_retry_from_state",
    context={"state": state}
)
    __result = None
    try:
        if (state == "failed"):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "retry_decided",
    "result == True or result == False",
    "can_retry_from_state",
    context=dict([("result", __result), ("state", state)])
)
    return __result


def validate_transition_guard(from_state: str, to_state: str, guard_condition: bool) -> bool:
    check_precondition(
    (len(from_state) > 0),
    "valid_from",
    "len(from_state) > 0",
    "validate_transition_guard",
    context={"from_state": from_state, "to_state": to_state, "guard_condition": guard_condition}
)
    check_precondition(
    (len(to_state) > 0),
    "valid_to",
    "len(to_state) > 0",
    "validate_transition_guard",
    context={"from_state": from_state, "to_state": to_state, "guard_condition": guard_condition}
)
    __result = None
    try:
        if (guard_condition == False):
            __result = False
            return __result
        if ((from_state == "active") and (to_state == "completed")):
            __result = True
            return __result
        if ((from_state == "paused") and (to_state == "active")):
            __result = True
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "guard_validated",
    "result == True or result == False",
    "validate_transition_guard",
    context=dict([("result", __result), ("from_state", from_state), ("to_state", to_state), ("guard_condition", guard_condition)])
)
    return __result


def count_transitions(transition_count: int, max_transitions: int) -> bool:
    check_precondition(
    (transition_count >= 0),
    "valid_count",
    "transition_count >= 0",
    "count_transitions",
    context={"transition_count": transition_count, "max_transitions": max_transitions}
)
    check_precondition(
    (max_transitions > 0),
    "positive_max",
    "max_transitions > 0",
    "count_transitions",
    context={"transition_count": transition_count, "max_transitions": max_transitions}
)
    __result = None
    try:
        if (transition_count >= max_transitions):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "count_validated",
    "result == True or result == False",
    "count_transitions",
    context=dict([("result", __result), ("transition_count", transition_count), ("max_transitions", max_transitions)])
)
    return __result


def validate_state_duration(time_in_state: int, min_duration: int, max_duration: int) -> bool:
    check_precondition(
    (time_in_state >= 0),
    "valid_time",
    "time_in_state >= 0",
    "validate_state_duration",
    context={"time_in_state": time_in_state, "min_duration": min_duration, "max_duration": max_duration}
)
    check_precondition(
    (min_duration >= 0),
    "valid_min",
    "min_duration >= 0",
    "validate_state_duration",
    context={"time_in_state": time_in_state, "min_duration": min_duration, "max_duration": max_duration}
)
    check_precondition(
    (max_duration >= min_duration),
    "valid_max",
    "max_duration >= min_duration",
    "validate_state_duration",
    context={"time_in_state": time_in_state, "min_duration": min_duration, "max_duration": max_duration}
)
    __result = None
    try:
        if (time_in_state < min_duration):
            __result = False
            return __result
        if (time_in_state > max_duration):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "duration_validated",
    "result == True or result == False",
    "validate_state_duration",
    context=dict([("result", __result), ("time_in_state", time_in_state), ("min_duration", min_duration), ("max_duration", max_duration)])
)
    return __result


def check_state_timeout(time_in_state: int, timeout_seconds: int) -> bool:
    check_precondition(
    (time_in_state >= 0),
    "valid_time",
    "time_in_state >= 0",
    "check_state_timeout",
    context={"time_in_state": time_in_state, "timeout_seconds": timeout_seconds}
)
    check_precondition(
    (timeout_seconds > 0),
    "positive_timeout",
    "timeout_seconds > 0",
    "check_state_timeout",
    context={"time_in_state": time_in_state, "timeout_seconds": timeout_seconds}
)
    __result = None
    try:
        if (time_in_state >= timeout_seconds):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "timeout_checked",
    "result == True or result == False",
    "check_state_timeout",
    context=dict([("result", __result), ("time_in_state", time_in_state), ("timeout_seconds", timeout_seconds)])
)
    return __result


def validate_parallel_states(state_a: str, state_b: str) -> bool:
    check_precondition(
    (len(state_a) > 0),
    "valid_a",
    "len(state_a) > 0",
    "validate_parallel_states",
    context={"state_a": state_a, "state_b": state_b}
)
    check_precondition(
    (len(state_b) > 0),
    "valid_b",
    "len(state_b) > 0",
    "validate_parallel_states",
    context={"state_a": state_a, "state_b": state_b}
)
    __result = None
    try:
        if (state_a == state_b):
            __result = False
            return __result
        if ((state_a == "completed") and (state_b == "active")):
            __result = False
            return __result
        if ((state_a == "active") and (state_b == "completed")):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "parallel_validated",
    "result == True or result == False",
    "validate_parallel_states",
    context=dict([("result", __result), ("state_a", state_a), ("state_b", state_b)])
)
    return __result


def check_composite_state(parent_state: str, child_state: str) -> bool:
    check_precondition(
    (len(parent_state) > 0),
    "valid_parent",
    "len(parent_state) > 0",
    "check_composite_state",
    context={"parent_state": parent_state, "child_state": child_state}
)
    check_precondition(
    (len(child_state) > 0),
    "valid_child",
    "len(child_state) > 0",
    "check_composite_state",
    context={"parent_state": parent_state, "child_state": child_state}
)
    __result = None
    try:
        if (parent_state == "active"):
            if (((child_state == "processing") or (child_state == "waiting")) or (child_state == "executing")):
                __result = True
                return __result
            __result = False
            return __result
        if (parent_state == "paused"):
            if ((child_state == "suspended") or (child_state == "interrupted")):
                __result = True
                return __result
            __result = False
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "composite_validated",
    "result == True or result == False",
    "check_composite_state",
    context=dict([("result", __result), ("parent_state", parent_state), ("child_state", child_state)])
)
    return __result


def validate_state_history(previous_state: str, current_state: str, can_return: bool) -> bool:
    check_precondition(
    (len(previous_state) > 0),
    "valid_previous",
    "len(previous_state) > 0",
    "validate_state_history",
    context={"previous_state": previous_state, "current_state": current_state, "can_return": can_return}
)
    check_precondition(
    (len(current_state) > 0),
    "valid_current",
    "len(current_state) > 0",
    "validate_state_history",
    context={"previous_state": previous_state, "current_state": current_state, "can_return": can_return}
)
    __result = None
    try:
        if (can_return == False):
            __result = True
            return __result
        if ((previous_state == "active") and (current_state == "paused")):
            __result = True
            return __result
        if ((previous_state == "paused") and (current_state == "active")):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "history_validated",
    "result == True or result == False",
    "validate_state_history",
    context=dict([("result", __result), ("previous_state", previous_state), ("current_state", current_state), ("can_return", can_return)])
)
    return __result


def check_concurrent_transition(active_transitions: int, max_concurrent: int) -> bool:
    check_precondition(
    (active_transitions >= 0),
    "valid_active",
    "active_transitions >= 0",
    "check_concurrent_transition",
    context={"active_transitions": active_transitions, "max_concurrent": max_concurrent}
)
    check_precondition(
    (max_concurrent > 0),
    "positive_max",
    "max_concurrent > 0",
    "check_concurrent_transition",
    context={"active_transitions": active_transitions, "max_concurrent": max_concurrent}
)
    __result = None
    try:
        if (active_transitions >= max_concurrent):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "concurrent_validated",
    "result == True or result == False",
    "check_concurrent_transition",
    context=dict([("result", __result), ("active_transitions", active_transitions), ("max_concurrent", max_concurrent)])
)
    return __result


def validate_state_invariant(state: str, resource_allocated: bool, resource_count: int) -> bool:
    check_precondition(
    (len(state) > 0),
    "valid_state",
    "len(state) > 0",
    "validate_state_invariant",
    context={"state": state, "resource_allocated": resource_allocated, "resource_count": resource_count}
)
    check_precondition(
    (resource_count >= 0),
    "valid_count",
    "resource_count >= 0",
    "validate_state_invariant",
    context={"state": state, "resource_allocated": resource_allocated, "resource_count": resource_count}
)
    __result = None
    try:
        if (state == "idle"):
            if (resource_allocated == True):
                __result = False
                return __result
            if (resource_count > 0):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "active"):
            if (resource_allocated == False):
                __result = False
                return __result
            if (resource_count == 0):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "paused"):
            if (resource_allocated == False):
                __result = False
                return __result
            __result = True
            return __result
        if (state == "completed"):
            if (resource_allocated == True):
                __result = False
                return __result
            __result = True
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "invariant_validated",
    "result == True or result == False",
    "validate_state_invariant",
    context=dict([("result", __result), ("state", state), ("resource_allocated", resource_allocated), ("resource_count", resource_count)])
)
    return __result


def check_rollback_allowed(current_state: str, previous_state: str) -> bool:
    check_precondition(
    (len(current_state) > 0),
    "valid_current",
    "len(current_state) > 0",
    "check_rollback_allowed",
    context={"current_state": current_state, "previous_state": previous_state}
)
    check_precondition(
    (len(previous_state) > 0),
    "valid_previous",
    "len(previous_state) > 0",
    "check_rollback_allowed",
    context={"current_state": current_state, "previous_state": previous_state}
)
    __result = None
    try:
        if (current_state == "failed"):
            if ((previous_state == "active") or (previous_state == "paused")):
                __result = True
                return __result
            __result = False
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "rollback_decided",
    "result == True or result == False",
    "check_rollback_allowed",
    context=dict([("result", __result), ("current_state", current_state), ("previous_state", previous_state)])
)
    return __result


def validate_batch_transition(states_count: int, transitions_count: int) -> bool:
    check_precondition(
    (states_count > 0),
    "valid_states",
    "states_count > 0",
    "validate_batch_transition",
    context={"states_count": states_count, "transitions_count": transitions_count}
)
    check_precondition(
    (transitions_count >= 0),
    "valid_transitions",
    "transitions_count >= 0",
    "validate_batch_transition",
    context={"states_count": states_count, "transitions_count": transitions_count}
)
    __result = None
    try:
        if (transitions_count > states_count):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "batch_validated",
    "result == True or result == False",
    "validate_batch_transition",
    context=dict([("result", __result), ("states_count", states_count), ("transitions_count", transitions_count)])
)
    return __result


def check_state_dependencies(state: str, dependency_satisfied: bool) -> bool:
    check_precondition(
    (len(state) > 0),
    "valid_state",
    "len(state) > 0",
    "check_state_dependencies",
    context={"state": state, "dependency_satisfied": dependency_satisfied}
)
    __result = None
    try:
        if (state == "active"):
            if (dependency_satisfied == False):
                __result = False
                return __result
            __result = True
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "dependencies_checked",
    "result == True or result == False",
    "check_state_dependencies",
    context=dict([("result", __result), ("state", state), ("dependency_satisfied", dependency_satisfied)])
)
    return __result


def validate_state_transition_path(start_state: str, end_state: str, intermediate_states: int) -> bool:
    check_precondition(
    (len(start_state) > 0),
    "valid_start",
    "len(start_state) > 0",
    "validate_state_transition_path",
    context={"start_state": start_state, "end_state": end_state, "intermediate_states": intermediate_states}
)
    check_precondition(
    (len(end_state) > 0),
    "valid_end",
    "len(end_state) > 0",
    "validate_state_transition_path",
    context={"start_state": start_state, "end_state": end_state, "intermediate_states": intermediate_states}
)
    check_precondition(
    (intermediate_states >= 0),
    "valid_intermediate",
    "intermediate_states >= 0",
    "validate_state_transition_path",
    context={"start_state": start_state, "end_state": end_state, "intermediate_states": intermediate_states}
)
    __result = None
    try:
        if (start_state == end_state):
            if (intermediate_states > 0):
                __result = False
                return __result
            __result = True
            return __result
        if ((start_state == "idle") and (end_state == "completed")):
            if (intermediate_states < 1):
                __result = False
                return __result
            __result = True
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "path_validated",
    "result == True or result == False",
    "validate_state_transition_path",
    context=dict([("result", __result), ("start_state", start_state), ("end_state", end_state), ("intermediate_states", intermediate_states)])
)
    return __result
