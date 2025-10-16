"""
Test suite for E-commerce Order System with Contract Validation

Demonstrates how contracts catch invalid inputs and enforce business rules.
"""

import pytest
import sys
from pathlib import Path

# Add project root and current directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from assertlang.runtime.contracts import ContractViolationError
from orders import (
    validate_order_inputs,
    validate_payment,
    validate_shipping,
    can_cancel_order,
    validate_refund,
    calculate_total_with_tax,
    apply_discount,
    can_transition_status,
    is_final_state,
    validate_item_count
)


class TestOrderInputValidation:
    """Test order creation input validation."""

    def test_valid_order_inputs(self):
        """Valid order inputs should pass."""
        result = validate_order_inputs(
            order_id="ORD-12345",
            customer_id="CUST-789",
            total_amount=99.99,
            item_count=3
        )
        assert result is True

    def test_empty_order_id_rejected(self):
        """Empty order ID should be rejected by precondition."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_order_inputs(
                order_id="",  # Invalid: empty
                customer_id="CUST-789",
                total_amount=99.99,
                item_count=3
            )
        assert "valid_order_id" in str(exc_info.value)

    def test_empty_customer_id_rejected(self):
        """Empty customer ID should be rejected by precondition."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_order_inputs(
                order_id="ORD-12345",
                customer_id="",  # Invalid: empty
                total_amount=99.99,
                item_count=3
            )
        assert "valid_customer_id" in str(exc_info.value)

    def test_negative_amount_rejected(self):
        """Negative total amount should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_order_inputs(
                order_id="ORD-12345",
                customer_id="CUST-789",
                total_amount=-50.00,  # Invalid: negative
                item_count=3
            )
        assert "positive_amount" in str(exc_info.value)

    def test_zero_items_rejected(self):
        """Zero items should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_order_inputs(
                order_id="ORD-12345",
                customer_id="CUST-789",
                total_amount=99.99,
                item_count=0  # Invalid: no items
            )
        assert "has_items" in str(exc_info.value)


class TestPaymentValidation:
    """Test payment information validation."""

    def test_valid_payment(self):
        """Valid payment info should pass."""
        result = validate_payment(
            payment_method="credit_card",
            transaction_id="TXN-98765",
            amount=99.99
        )
        assert result is True

    def test_empty_payment_method_rejected(self):
        """Empty payment method should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_payment(
                payment_method="",  # Invalid
                transaction_id="TXN-98765",
                amount=99.99
            )
        assert "valid_payment_method" in str(exc_info.value)

    def test_empty_transaction_id_rejected(self):
        """Empty transaction ID should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_payment(
                payment_method="credit_card",
                transaction_id="",  # Invalid
                amount=99.99
            )
        assert "valid_transaction" in str(exc_info.value)

    def test_negative_payment_amount_rejected(self):
        """Negative payment amount should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_payment(
                payment_method="credit_card",
                transaction_id="TXN-98765",
                amount=-99.99  # Invalid
            )
        assert "positive_payment" in str(exc_info.value)


class TestShippingValidation:
    """Test shipping information validation."""

    def test_valid_shipping(self):
        """Valid shipping info should pass."""
        result = validate_shipping(
            tracking_number="TRACK-12345",
            carrier="UPS",
            address="123 Main St, City, ST 12345"
        )
        assert result is True

    def test_empty_tracking_rejected(self):
        """Empty tracking number should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_shipping(
                tracking_number="",  # Invalid
                carrier="UPS",
                address="123 Main St"
            )
        assert "valid_tracking" in str(exc_info.value)

    def test_empty_carrier_rejected(self):
        """Empty carrier should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_shipping(
                tracking_number="TRACK-12345",
                carrier="",  # Invalid
                address="123 Main St"
            )
        assert "valid_carrier" in str(exc_info.value)


class TestCancellation:
    """Test order cancellation logic."""

    def test_can_cancel_unshipped_order(self):
        """Unshipped orders can be cancelled."""
        result = can_cancel_order(
            status="processing",
            is_shipped=False
        )
        assert result is True

    def test_cannot_cancel_shipped_order(self):
        """Shipped orders cannot be cancelled."""
        result = can_cancel_order(
            status="shipped",
            is_shipped=True
        )
        assert result is False


class TestRefundValidation:
    """Test refund amount validation."""

    def test_valid_refund(self):
        """Valid refund amount should pass."""
        result = validate_refund(
            refund_amount=50.00,
            original_amount=100.00
        )
        assert result is True

    def test_full_refund(self):
        """Full refund should be allowed."""
        result = validate_refund(
            refund_amount=100.00,
            original_amount=100.00
        )
        assert result is True

    def test_refund_exceeds_original_rejected(self):
        """Refund exceeding original amount should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_refund(
                refund_amount=150.00,  # Invalid: exceeds original
                original_amount=100.00
            )
        assert "refund_not_exceeds" in str(exc_info.value)

    def test_negative_refund_rejected(self):
        """Negative refund should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_refund(
                refund_amount=-50.00,  # Invalid
                original_amount=100.00
            )
        assert "positive_refund" in str(exc_info.value)


class TestTaxCalculation:
    """Test tax calculation with postconditions."""

    def test_calculate_tax(self):
        """Tax calculation should work correctly."""
        # 10% tax on $100
        result = calculate_total_with_tax(
            subtotal=100.00,
            tax_rate=0.10
        )
        assert result == 110.00

    def test_zero_tax(self):
        """Zero tax rate should work."""
        result = calculate_total_with_tax(
            subtotal=100.00,
            tax_rate=0.0
        )
        assert result == 100.00

    def test_invalid_tax_rate_rejected(self):
        """Tax rate > 1.0 should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            calculate_total_with_tax(
                subtotal=100.00,
                tax_rate=1.5  # Invalid: > 1.0
            )
        assert "valid_tax_rate" in str(exc_info.value)

    def test_negative_tax_rejected(self):
        """Negative tax rate should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            calculate_total_with_tax(
                subtotal=100.00,
                tax_rate=-0.10  # Invalid
            )
        assert "valid_tax_rate" in str(exc_info.value)


class TestDiscountApplication:
    """Test discount application with constraints."""

    def test_apply_discount(self):
        """Discount should reduce price correctly."""
        # 20% off $100
        result = apply_discount(
            original_price=100.00,
            discount_percent=20.0
        )
        assert result == 80.00

    def test_full_discount(self):
        """100% discount should result in zero."""
        result = apply_discount(
            original_price=100.00,
            discount_percent=100.0
        )
        assert result == 0.00

    def test_no_discount(self):
        """0% discount should keep original price."""
        result = apply_discount(
            original_price=100.00,
            discount_percent=0.0
        )
        assert result == 100.00

    def test_discount_exceeds_100_rejected(self):
        """Discount > 100% should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            apply_discount(
                original_price=100.00,
                discount_percent=150.0  # Invalid
            )
        assert "valid_discount" in str(exc_info.value)

    def test_negative_discount_rejected(self):
        """Negative discount should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            apply_discount(
                original_price=100.00,
                discount_percent=-10.0  # Invalid
            )
        assert "valid_discount" in str(exc_info.value)


class TestStateTransitions:
    """Test state machine transition validation."""

    def test_pending_to_payment_confirmed(self):
        """Pending can transition to payment_confirmed."""
        result = can_transition_status("pending", "payment_confirmed")
        assert result is True

    def test_pending_to_cancelled(self):
        """Pending can transition to cancelled."""
        result = can_transition_status("pending", "cancelled")
        assert result is True

    def test_payment_confirmed_to_processing(self):
        """Payment confirmed can transition to processing."""
        result = can_transition_status("payment_confirmed", "processing")
        assert result is True

    def test_processing_to_shipped(self):
        """Processing can transition to shipped."""
        result = can_transition_status("processing", "shipped")
        assert result is True

    def test_shipped_to_delivered(self):
        """Shipped can transition to delivered."""
        result = can_transition_status("shipped", "delivered")
        assert result is True

    def test_delivered_to_refunded(self):
        """Delivered can transition to refunded."""
        result = can_transition_status("delivered", "refunded")
        assert result is True

    def test_invalid_transition_rejected(self):
        """Invalid transitions should be rejected."""
        # Can't go from pending directly to shipped
        result = can_transition_status("pending", "shipped")
        assert result is False

    def test_cannot_transition_from_delivered_to_shipped(self):
        """Cannot go backwards from delivered to shipped."""
        result = can_transition_status("delivered", "shipped")
        assert result is False

    def test_shipped_cannot_cancel(self):
        """Shipped orders cannot be cancelled."""
        result = can_transition_status("shipped", "cancelled")
        assert result is False


class TestFinalStates:
    """Test final state detection."""

    def test_delivered_is_final(self):
        """Delivered is a final state."""
        result = is_final_state("delivered")
        assert result is True

    def test_cancelled_is_final(self):
        """Cancelled is a final state."""
        result = is_final_state("cancelled")
        assert result is True

    def test_refunded_is_final(self):
        """Refunded is a final state."""
        result = is_final_state("refunded")
        assert result is True

    def test_pending_not_final(self):
        """Pending is not a final state."""
        result = is_final_state("pending")
        assert result is False

    def test_processing_not_final(self):
        """Processing is not a final state."""
        result = is_final_state("processing")
        assert result is False


class TestItemCount:
    """Test item count validation."""

    def test_valid_item_count(self):
        """Valid item count should pass."""
        result = validate_item_count(
            item_count=5,
            max_items_per_order=10
        )
        assert result is True

    def test_at_max_items(self):
        """Item count at max should pass."""
        result = validate_item_count(
            item_count=10,
            max_items_per_order=10
        )
        assert result is True

    def test_exceeds_max_items(self):
        """Item count exceeding max should fail."""
        result = validate_item_count(
            item_count=15,
            max_items_per_order=10
        )
        assert result is False


class TestEndToEndScenarios:
    """Test complete order workflows."""

    def test_successful_order_flow(self):
        """Test complete successful order flow."""
        # 1. Validate order inputs
        assert validate_order_inputs("ORD-001", "CUST-001", 100.00, 2) is True

        # 2. Check initial state transition
        assert can_transition_status("pending", "payment_confirmed") is True

        # 3. Validate payment
        assert validate_payment("credit_card", "TXN-001", 100.00) is True

        # 4. Process order
        assert can_transition_status("payment_confirmed", "processing") is True

        # 5. Ship order
        assert can_transition_status("processing", "shipped") is True
        assert validate_shipping("TRACK-001", "UPS", "123 Main St") is True

        # 6. Deliver order
        assert can_transition_status("shipped", "delivered") is True
        assert is_final_state("delivered") is True

    def test_cancelled_order_flow(self):
        """Test order cancellation flow."""
        # 1. Create order
        assert validate_order_inputs("ORD-002", "CUST-002", 50.00, 1) is True

        # 2. Cancel before payment
        assert can_cancel_order("pending", False) is True
        assert can_transition_status("pending", "cancelled") is True
        assert is_final_state("cancelled") is True

    def test_refund_flow(self):
        """Test refund flow."""
        # 1. Order delivered
        assert is_final_state("delivered") is True

        # 2. Initiate refund
        assert can_transition_status("delivered", "refunded") is True

        # 3. Validate refund amount
        assert validate_refund(75.00, 100.00) is True

        # 4. Refund completed
        assert is_final_state("refunded") is True

    def test_pricing_flow(self):
        """Test pricing calculations."""
        # 1. Original price
        original = 100.00

        # 2. Apply 20% discount
        discounted = apply_discount(original, 20.0)
        assert discounted == 80.00

        # 3. Add 10% tax
        final_price = calculate_total_with_tax(discounted, 0.10)
        assert final_price == 88.00


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
