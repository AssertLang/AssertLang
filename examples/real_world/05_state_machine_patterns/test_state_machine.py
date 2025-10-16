"""
Test suite for State Machine Patterns with Contract Validation

Demonstrates how contracts validate state machines, transitions,
and state invariants.
"""

import pytest
import sys
from pathlib import Path

# Add project root and current directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from assertlang.runtime.contracts import ContractViolationError
from state_machine import (
    is_valid_state,
    can_transition,
    validate_state_data,
    check_entry_condition,
    check_exit_condition,
    is_terminal_state,
    can_retry_from_state,
    validate_transition_guard,
    count_transitions,
    validate_state_duration,
    check_state_timeout,
    validate_parallel_states,
    check_composite_state,
    validate_state_history,
    check_concurrent_transition,
    validate_state_invariant,
    check_rollback_allowed,
    validate_batch_transition,
    check_state_dependencies,
    validate_state_transition_path
)


class TestStateValidation:
    """Test state validation."""

    def test_valid_states(self):
        """All valid states should pass."""
        assert is_valid_state("idle") is True
        assert is_valid_state("active") is True
        assert is_valid_state("paused") is True
        assert is_valid_state("completed") is True
        assert is_valid_state("failed") is True
        assert is_valid_state("cancelled") is True

    def test_invalid_state_rejected(self):
        """Invalid states should be rejected."""
        assert is_valid_state("unknown") is False
        assert is_valid_state("pending") is False


class TestStateTransitions:
    """Test state transition validation."""

    def test_idle_transitions(self):
        """Idle can transition to active or cancelled."""
        assert can_transition("idle", "active") is True
        assert can_transition("idle", "cancelled") is True
        assert can_transition("idle", "paused") is False
        assert can_transition("idle", "completed") is False

    def test_active_transitions(self):
        """Active can transition to paused, completed, failed, or cancelled."""
        assert can_transition("active", "paused") is True
        assert can_transition("active", "completed") is True
        assert can_transition("active", "failed") is True
        assert can_transition("active", "cancelled") is True
        assert can_transition("active", "idle") is False

    def test_paused_transitions(self):
        """Paused can transition to active or cancelled."""
        assert can_transition("paused", "active") is True
        assert can_transition("paused", "cancelled") is True
        assert can_transition("paused", "completed") is False
        assert can_transition("paused", "failed") is False

    def test_terminal_states_no_transitions(self):
        """Terminal states cannot transition."""
        assert can_transition("completed", "idle") is False
        assert can_transition("completed", "active") is False
        assert can_transition("cancelled", "idle") is False
        assert can_transition("cancelled", "active") is False

    def test_failed_can_restart(self):
        """Failed can transition back to idle."""
        assert can_transition("failed", "idle") is True
        assert can_transition("failed", "active") is False


class TestStateDataValidation:
    """Test state-specific data validation."""

    def test_idle_requires_no_data(self):
        """Idle state requires no data."""
        assert validate_state_data("idle", False, False) is True

    def test_active_requires_valid_data(self):
        """Active state requires present and valid data."""
        assert validate_state_data("active", True, True) is True
        assert validate_state_data("active", False, True) is False
        assert validate_state_data("active", True, False) is False

    def test_paused_requires_present_data(self):
        """Paused state requires data present but not necessarily valid."""
        assert validate_state_data("paused", True, False) is True
        assert validate_state_data("paused", False, False) is False

    def test_completed_requires_valid_data(self):
        """Completed state requires present and valid data."""
        assert validate_state_data("completed", True, True) is True
        assert validate_state_data("completed", False, True) is False

    def test_failed_requires_no_data(self):
        """Failed state requires no specific data."""
        assert validate_state_data("failed", False, False) is True


class TestEntryConditions:
    """Test entry condition validation."""

    def test_idle_no_precondition(self):
        """Idle has no entry precondition."""
        assert check_entry_condition("idle", False) is True

    def test_active_requires_precondition(self):
        """Active requires entry precondition."""
        assert check_entry_condition("active", True) is True
        assert check_entry_condition("active", False) is False

    def test_completed_requires_precondition(self):
        """Completed requires entry precondition."""
        assert check_entry_condition("completed", True) is True
        assert check_entry_condition("completed", False) is False


class TestExitConditions:
    """Test exit condition validation."""

    def test_idle_no_cleanup(self):
        """Idle requires no cleanup."""
        assert check_exit_condition("idle", False) is True

    def test_active_requires_cleanup(self):
        """Active requires cleanup before exit."""
        assert check_exit_condition("active", True) is True
        assert check_exit_condition("active", False) is False

    def test_terminal_states_cannot_exit(self):
        """Terminal states cannot be exited."""
        assert check_exit_condition("completed", True) is False
        assert check_exit_condition("cancelled", True) is False


class TestTerminalStates:
    """Test terminal state identification."""

    def test_terminal_states(self):
        """Completed and cancelled are terminal."""
        assert is_terminal_state("completed") is True
        assert is_terminal_state("cancelled") is True

    def test_non_terminal_states(self):
        """Other states are not terminal."""
        assert is_terminal_state("idle") is False
        assert is_terminal_state("active") is False
        assert is_terminal_state("paused") is False
        assert is_terminal_state("failed") is False


class TestRetryLogic:
    """Test retry capability."""

    def test_failed_can_retry(self):
        """Failed state can be retried."""
        assert can_retry_from_state("failed") is True

    def test_other_states_cannot_retry(self):
        """Other states cannot be retried."""
        assert can_retry_from_state("idle") is False
        assert can_retry_from_state("active") is False
        assert can_retry_from_state("completed") is False


class TestTransitionGuards:
    """Test guard condition validation."""

    def test_guard_false_blocks_transition(self):
        """False guard blocks any transition."""
        assert validate_transition_guard("active", "completed", False) is False

    def test_guard_true_allows_transition(self):
        """True guard allows transition."""
        assert validate_transition_guard("active", "completed", True) is True
        assert validate_transition_guard("paused", "active", True) is True


class TestTransitionCounting:
    """Test transition count limits."""

    def test_within_limit(self):
        """Transition count within limit should pass."""
        assert count_transitions(5, 10) is True

    def test_at_limit_rejected(self):
        """Transition count at limit should be rejected."""
        assert count_transitions(10, 10) is False

    def test_exceeds_limit_rejected(self):
        """Transition count exceeding limit should be rejected."""
        assert count_transitions(15, 10) is False


class TestStateDuration:
    """Test state duration validation."""

    def test_valid_duration(self):
        """Duration within range should pass."""
        assert validate_state_duration(500, 100, 1000) is True

    def test_below_minimum_rejected(self):
        """Duration below minimum should be rejected."""
        assert validate_state_duration(50, 100, 1000) is False

    def test_above_maximum_rejected(self):
        """Duration above maximum should be rejected."""
        assert validate_state_duration(1500, 100, 1000) is False

    def test_at_boundaries(self):
        """Duration at exact boundaries should pass."""
        assert validate_state_duration(100, 100, 1000) is True
        assert validate_state_duration(1000, 100, 1000) is True


class TestStateTimeout:
    """Test state timeout detection."""

    def test_timeout_not_reached(self):
        """Time below timeout should return False."""
        assert check_state_timeout(50, 100) is False

    def test_timeout_reached(self):
        """Time at or above timeout should return True."""
        assert check_state_timeout(100, 100) is True
        assert check_state_timeout(150, 100) is True


class TestParallelStates:
    """Test parallel state validation."""

    def test_different_states_allowed(self):
        """Different parallel states should be allowed."""
        assert validate_parallel_states("idle", "active") is True
        assert validate_parallel_states("paused", "failed") is True

    def test_same_state_rejected(self):
        """Same state in parallel should be rejected."""
        assert validate_parallel_states("active", "active") is False

    def test_conflicting_states_rejected(self):
        """Conflicting parallel states should be rejected."""
        assert validate_parallel_states("completed", "active") is False
        assert validate_parallel_states("active", "completed") is False


class TestCompositeStates:
    """Test composite (hierarchical) state validation."""

    def test_active_composite_states(self):
        """Active parent can have processing/waiting/executing children."""
        assert check_composite_state("active", "processing") is True
        assert check_composite_state("active", "waiting") is True
        assert check_composite_state("active", "executing") is True
        assert check_composite_state("active", "idle") is False

    def test_paused_composite_states(self):
        """Paused parent can have suspended/interrupted children."""
        assert check_composite_state("paused", "suspended") is True
        assert check_composite_state("paused", "interrupted") is True
        assert check_composite_state("paused", "processing") is False

    def test_invalid_parent_rejected(self):
        """Invalid parent states should be rejected."""
        assert check_composite_state("idle", "processing") is False
        assert check_composite_state("completed", "executing") is False


class TestStateHistory:
    """Test state history validation."""

    def test_returnable_transitions(self):
        """Returnable transitions should be validated."""
        assert validate_state_history("active", "paused", True) is True
        assert validate_state_history("paused", "active", True) is True

    def test_non_returnable_transitions(self):
        """Non-returnable transitions should always pass."""
        assert validate_state_history("idle", "completed", False) is True
        assert validate_state_history("active", "failed", False) is True


class TestConcurrentTransitions:
    """Test concurrent transition limits."""

    def test_within_concurrent_limit(self):
        """Concurrent transitions within limit should pass."""
        assert check_concurrent_transition(5, 10) is True

    def test_at_concurrent_limit_rejected(self):
        """Concurrent transitions at limit should be rejected."""
        assert check_concurrent_transition(10, 10) is False

    def test_exceeds_concurrent_limit_rejected(self):
        """Concurrent transitions exceeding limit should be rejected."""
        assert check_concurrent_transition(15, 10) is False


class TestStateInvariants:
    """Test state invariant validation."""

    def test_idle_invariant(self):
        """Idle must have no resources."""
        assert validate_state_invariant("idle", False, 0) is True
        assert validate_state_invariant("idle", True, 0) is False
        assert validate_state_invariant("idle", False, 1) is False

    def test_active_invariant(self):
        """Active must have allocated resources."""
        assert validate_state_invariant("active", True, 5) is True
        assert validate_state_invariant("active", False, 5) is False
        assert validate_state_invariant("active", True, 0) is False

    def test_paused_invariant(self):
        """Paused must have allocated resources."""
        assert validate_state_invariant("paused", True, 3) is True
        assert validate_state_invariant("paused", False, 3) is False

    def test_completed_invariant(self):
        """Completed must have no allocated resources."""
        assert validate_state_invariant("completed", False, 0) is True
        assert validate_state_invariant("completed", True, 0) is False


class TestRollbackValidation:
    """Test rollback capability."""

    def test_rollback_from_failed_to_active(self):
        """Can rollback from failed to active."""
        assert check_rollback_allowed("failed", "active") is True

    def test_rollback_from_failed_to_paused(self):
        """Can rollback from failed to paused."""
        assert check_rollback_allowed("failed", "paused") is True

    def test_rollback_from_other_states_rejected(self):
        """Cannot rollback from non-failed states."""
        assert check_rollback_allowed("active", "idle") is False
        assert check_rollback_allowed("completed", "active") is False


class TestBatchTransitions:
    """Test batch transition validation."""

    def test_valid_batch_transition(self):
        """Transitions <= states should pass."""
        assert validate_batch_transition(10, 10) is True
        assert validate_batch_transition(10, 5) is True

    def test_too_many_transitions_rejected(self):
        """Transitions > states should be rejected."""
        assert validate_batch_transition(10, 15) is False


class TestStateDependencies:
    """Test state dependency validation."""

    def test_active_requires_dependency(self):
        """Active state requires dependency satisfied."""
        assert check_state_dependencies("active", True) is True
        assert check_state_dependencies("active", False) is False

    def test_other_states_no_dependency(self):
        """Other states have no dependency requirement."""
        assert check_state_dependencies("idle", False) is True
        assert check_state_dependencies("paused", False) is True


class TestTransitionPaths:
    """Test transition path validation."""

    def test_same_state_no_intermediates(self):
        """Same start and end requires no intermediates."""
        assert validate_state_transition_path("idle", "idle", 0) is True
        assert validate_state_transition_path("idle", "idle", 1) is False

    def test_idle_to_completed_requires_intermediates(self):
        """Idle to completed requires at least one intermediate."""
        assert validate_state_transition_path("idle", "completed", 1) is True
        assert validate_state_transition_path("idle", "completed", 2) is True
        assert validate_state_transition_path("idle", "completed", 0) is False


class TestEndToEndScenarios:
    """Test complete state machine scenarios."""

    def test_successful_workflow(self):
        """Test complete successful workflow."""
        assert is_valid_state("idle") is True
        assert can_transition("idle", "active") is True
        assert check_entry_condition("active", True) is True

        assert validate_state_data("active", True, True) is True
        assert validate_state_invariant("active", True, 5) is True

        assert can_transition("active", "completed") is True
        assert check_entry_condition("completed", True) is True
        assert check_exit_condition("active", True) is True

        assert is_terminal_state("completed") is True

    def test_workflow_with_pause(self):
        """Test workflow with pause and resume."""
        assert can_transition("idle", "active") is True
        assert can_transition("active", "paused") is True
        assert validate_state_history("active", "paused", True) is True

        assert can_transition("paused", "active") is True
        assert validate_state_history("paused", "active", True) is True

    def test_workflow_with_failure_and_retry(self):
        """Test workflow with failure and retry."""
        assert can_transition("active", "failed") is True
        assert can_retry_from_state("failed") is True

        assert check_rollback_allowed("failed", "active") is True
        assert can_transition("failed", "idle") is True

    def test_composite_state_workflow(self):
        """Test composite state workflow."""
        assert is_valid_state("active") is True
        assert check_composite_state("active", "processing") is True
        assert check_composite_state("active", "waiting") is True
        assert check_composite_state("active", "executing") is True

    def test_parallel_states_workflow(self):
        """Test parallel states."""
        assert validate_parallel_states("idle", "active") is True
        assert validate_parallel_states("active", "active") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
