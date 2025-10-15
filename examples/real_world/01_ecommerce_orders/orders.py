from __future__ import annotations

from promptware.runtime.contracts import check_postcondition
from promptware.runtime.contracts import check_precondition

def validate_order_inputs(order_id: str, customer_id: str, total_amount: float, item_count: int) -> bool:
    check_precondition(
    (len(order_id) > 0),
    "valid_order_id",
    "len(order_id) > 0",
    "validate_order_inputs",
    context={"order_id": order_id, "customer_id": customer_id, "total_amount": total_amount, "item_count": item_count}
)
    check_precondition(
    (len(customer_id) > 0),
    "valid_customer_id",
    "len(customer_id) > 0",
    "validate_order_inputs",
    context={"order_id": order_id, "customer_id": customer_id, "total_amount": total_amount, "item_count": item_count}
)
    check_precondition(
    (total_amount > 0.0),
    "positive_amount",
    "total_amount > 0.0",
    "validate_order_inputs",
    context={"order_id": order_id, "customer_id": customer_id, "total_amount": total_amount, "item_count": item_count}
)
    check_precondition(
    (item_count > 0),
    "has_items",
    "item_count > 0",
    "validate_order_inputs",
    context={"order_id": order_id, "customer_id": customer_id, "total_amount": total_amount, "item_count": item_count}
)
    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "validation_result",
    "result == True or result == False",
    "validate_order_inputs",
    context=dict([("result", __result), ("order_id", order_id), ("customer_id", customer_id), ("total_amount", total_amount), ("item_count", item_count)])
)
    return __result


def validate_payment(payment_method: str, transaction_id: str, amount: float) -> bool:
    check_precondition(
    (len(payment_method) > 0),
    "valid_payment_method",
    "len(payment_method) > 0",
    "validate_payment",
    context={"payment_method": payment_method, "transaction_id": transaction_id, "amount": amount}
)
    check_precondition(
    (len(transaction_id) > 0),
    "valid_transaction",
    "len(transaction_id) > 0",
    "validate_payment",
    context={"payment_method": payment_method, "transaction_id": transaction_id, "amount": amount}
)
    check_precondition(
    (amount > 0.0),
    "positive_payment",
    "amount > 0.0",
    "validate_payment",
    context={"payment_method": payment_method, "transaction_id": transaction_id, "amount": amount}
)
    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "validation_complete",
    "result == True or result == False",
    "validate_payment",
    context=dict([("result", __result), ("payment_method", payment_method), ("transaction_id", transaction_id), ("amount", amount)])
)
    return __result


def validate_shipping(tracking_number: str, carrier: str, address: str) -> bool:
    check_precondition(
    (len(tracking_number) > 0),
    "valid_tracking",
    "len(tracking_number) > 0",
    "validate_shipping",
    context={"tracking_number": tracking_number, "carrier": carrier, "address": address}
)
    check_precondition(
    (len(carrier) > 0),
    "valid_carrier",
    "len(carrier) > 0",
    "validate_shipping",
    context={"tracking_number": tracking_number, "carrier": carrier, "address": address}
)
    check_precondition(
    (len(address) > 0),
    "valid_address",
    "len(address) > 0",
    "validate_shipping",
    context={"tracking_number": tracking_number, "carrier": carrier, "address": address}
)
    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "validation_complete",
    "result == True or result == False",
    "validate_shipping",
    context=dict([("result", __result), ("tracking_number", tracking_number), ("carrier", carrier), ("address", address)])
)
    return __result


def can_cancel_order(status: str, is_shipped: bool) -> bool:
    check_precondition(
    (len(status) > 0),
    "valid_status",
    "len(status) > 0",
    "can_cancel_order",
    context={"status": status, "is_shipped": is_shipped}
)
    __result = None
    try:
        if (is_shipped == True):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "cancellation_possible",
    "result == True or result == False",
    "can_cancel_order",
    context=dict([("result", __result), ("status", status), ("is_shipped", is_shipped)])
)
    return __result


def validate_refund(refund_amount: float, original_amount: float) -> bool:
    check_precondition(
    (refund_amount > 0.0),
    "positive_refund",
    "refund_amount > 0.0",
    "validate_refund",
    context={"refund_amount": refund_amount, "original_amount": original_amount}
)
    check_precondition(
    (original_amount > 0.0),
    "positive_original",
    "original_amount > 0.0",
    "validate_refund",
    context={"refund_amount": refund_amount, "original_amount": original_amount}
)
    check_precondition(
    (refund_amount <= original_amount),
    "refund_not_exceeds",
    "refund_amount <= original_amount",
    "validate_refund",
    context={"refund_amount": refund_amount, "original_amount": original_amount}
)
    __result = None
    try:
        __result = True
        return __result
    finally:
        check_postcondition(
    (__result == True),
    "refund_valid",
    "result == True",
    "validate_refund",
    context=dict([("result", __result), ("refund_amount", refund_amount), ("original_amount", original_amount)])
)
    return __result


def calculate_total_with_tax(subtotal: float, tax_rate: float) -> float:
    check_precondition(
    (subtotal >= 0.0),
    "positive_subtotal",
    "subtotal >= 0.0",
    "calculate_total_with_tax",
    context={"subtotal": subtotal, "tax_rate": tax_rate}
)
    check_precondition(
    ((tax_rate >= 0.0) and (tax_rate <= 1.0)),
    "valid_tax_rate",
    "tax_rate >= 0.0 and tax_rate <= 1.0",
    "calculate_total_with_tax",
    context={"subtotal": subtotal, "tax_rate": tax_rate}
)
    __result = None
    try:
        tax_amount = (subtotal * tax_rate)
        total = (subtotal + tax_amount)
        __result = total
        return __result
    finally:
        check_postcondition(
    (__result >= subtotal),
    "total_includes_tax",
    "result >= subtotal",
    "calculate_total_with_tax",
    context=dict([("result", __result), ("subtotal", subtotal), ("tax_rate", tax_rate)])
)
    return __result


def apply_discount(original_price: float, discount_percent: float) -> float:
    check_precondition(
    (original_price > 0.0),
    "positive_price",
    "original_price > 0.0",
    "apply_discount",
    context={"original_price": original_price, "discount_percent": discount_percent}
)
    check_precondition(
    ((discount_percent >= 0.0) and (discount_percent <= 100.0)),
    "valid_discount",
    "discount_percent >= 0.0 and discount_percent <= 100.0",
    "apply_discount",
    context={"original_price": original_price, "discount_percent": discount_percent}
)
    __result = None
    try:
        discount_amount = (original_price * (discount_percent / 100.0))
        final_price = (original_price - discount_amount)
        __result = final_price
        return __result
    finally:
        check_postcondition(
    ((__result >= 0.0) and (__result <= original_price)),
    "discounted_price",
    "result >= 0.0 and result <= original_price",
    "apply_discount",
    context=dict([("result", __result), ("original_price", original_price), ("discount_percent", discount_percent)])
)
    return __result


def can_transition_status(current_status: str, new_status: str) -> bool:
    check_precondition(
    (len(current_status) > 0),
    "valid_current",
    "len(current_status) > 0",
    "can_transition_status",
    context={"current_status": current_status, "new_status": new_status}
)
    check_precondition(
    (len(new_status) > 0),
    "valid_new",
    "len(new_status) > 0",
    "can_transition_status",
    context={"current_status": current_status, "new_status": new_status}
)
    __result = None
    try:
        if (current_status == "pending"):
            if ((new_status == "payment_confirmed") or (new_status == "cancelled")):
                __result = True
                return __result
        if (current_status == "payment_confirmed"):
            if ((new_status == "processing") or (new_status == "cancelled")):
                __result = True
                return __result
        if (current_status == "processing"):
            if ((new_status == "shipped") or (new_status == "cancelled")):
                __result = True
                return __result
        if (current_status == "shipped"):
            if (new_status == "delivered"):
                __result = True
                return __result
        if (current_status == "delivered"):
            if (new_status == "refunded"):
                __result = True
                return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "transition_decided",
    "result == True or result == False",
    "can_transition_status",
    context=dict([("result", __result), ("current_status", current_status), ("new_status", new_status)])
)
    return __result


def is_final_state(status: str) -> bool:
    check_precondition(
    (len(status) > 0),
    "valid_status",
    "len(status) > 0",
    "is_final_state",
    context={"status": status}
)
    __result = None
    try:
        if (((status == "delivered") or (status == "cancelled")) or (status == "refunded")):
            __result = True
            return __result
        __result = False
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "is_boolean",
    "result == True or result == False",
    "is_final_state",
    context=dict([("result", __result), ("status", status)])
)
    return __result


def validate_item_count(item_count: int, max_items_per_order: int) -> bool:
    check_precondition(
    (item_count > 0),
    "positive_count",
    "item_count > 0",
    "validate_item_count",
    context={"item_count": item_count, "max_items_per_order": max_items_per_order}
)
    check_precondition(
    (max_items_per_order > 0),
    "positive_max",
    "max_items_per_order > 0",
    "validate_item_count",
    context={"item_count": item_count, "max_items_per_order": max_items_per_order}
)
    __result = None
    try:
        if (item_count > max_items_per_order):
            __result = False
            return __result
        __result = True
        return __result
    finally:
        check_postcondition(
    ((__result == True) or (__result == False)),
    "count_valid",
    "result == True or result == False",
    "validate_item_count",
    context=dict([("result", __result), ("item_count", item_count), ("max_items_per_order", max_items_per_order)])
)
    return __result
