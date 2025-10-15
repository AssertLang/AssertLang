const { ContractViolationError, shouldCheckPreconditions, shouldCheckPostconditions } = require('./contracts.js');

/**
 * @param {string} order_id
 * @param {string} customer_id
 * @param {number} total_amount
 * @param {number} item_count
 * @returns {boolean}
 */
function validate_order_inputs(order_id, customer_id, total_amount, item_count) {
    if (shouldCheckPreconditions()) {
        if (!((len(order_id) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_order_inputs',
                clause: 'valid_order_id',
                expression: '<expr> > 0',
                context: { order_id, customer_id, total_amount, item_count }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((len(customer_id) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_order_inputs',
                clause: 'valid_customer_id',
                expression: '<expr> > 0',
                context: { order_id, customer_id, total_amount, item_count }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((total_amount > 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_order_inputs',
                clause: 'positive_amount',
                expression: 'total_amount > 0.0',
                context: { order_id, customer_id, total_amount, item_count }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((item_count > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_order_inputs',
                clause: 'has_items',
                expression: 'item_count > 0',
                context: { order_id, customer_id, total_amount, item_count }
            });
        }
    }
    let __result;
    try {
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'validate_order_inputs',
                    clause: 'validation_result',
                    expression: 'result == True or result == False',
                    context: { result: __result, order_id: order_id, customer_id: customer_id, total_amount: total_amount, item_count: item_count }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {string} payment_method
 * @param {string} transaction_id
 * @param {number} amount
 * @returns {boolean}
 */
function validate_payment(payment_method, transaction_id, amount) {
    if (shouldCheckPreconditions()) {
        if (!((len(payment_method) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_payment',
                clause: 'valid_payment_method',
                expression: '<expr> > 0',
                context: { payment_method, transaction_id, amount }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((len(transaction_id) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_payment',
                clause: 'valid_transaction',
                expression: '<expr> > 0',
                context: { payment_method, transaction_id, amount }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((amount > 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_payment',
                clause: 'positive_payment',
                expression: 'amount > 0.0',
                context: { payment_method, transaction_id, amount }
            });
        }
    }
    let __result;
    try {
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'validate_payment',
                    clause: 'validation_complete',
                    expression: 'result == True or result == False',
                    context: { result: __result, payment_method: payment_method, transaction_id: transaction_id, amount: amount }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {string} tracking_number
 * @param {string} carrier
 * @param {string} address
 * @returns {boolean}
 */
function validate_shipping(tracking_number, carrier, address) {
    if (shouldCheckPreconditions()) {
        if (!((len(tracking_number) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_shipping',
                clause: 'valid_tracking',
                expression: '<expr> > 0',
                context: { tracking_number, carrier, address }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((len(carrier) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_shipping',
                clause: 'valid_carrier',
                expression: '<expr> > 0',
                context: { tracking_number, carrier, address }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((len(address) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_shipping',
                clause: 'valid_address',
                expression: '<expr> > 0',
                context: { tracking_number, carrier, address }
            });
        }
    }
    let __result;
    try {
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'validate_shipping',
                    clause: 'validation_complete',
                    expression: 'result == True or result == False',
                    context: { result: __result, tracking_number: tracking_number, carrier: carrier, address: address }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {string} status
 * @param {boolean} is_shipped
 * @returns {boolean}
 */
function can_cancel_order(status, is_shipped) {
    if (shouldCheckPreconditions()) {
        if (!((len(status) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'can_cancel_order',
                clause: 'valid_status',
                expression: '<expr> > 0',
                context: { status, is_shipped }
            });
        }
    }
    let __result;
    try {
        if ((is_shipped === true)) {
            return false;
        }
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'can_cancel_order',
                    clause: 'cancellation_possible',
                    expression: 'result == True or result == False',
                    context: { result: __result, status: status, is_shipped: is_shipped }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {number} refund_amount
 * @param {number} original_amount
 * @returns {boolean}
 */
function validate_refund(refund_amount, original_amount) {
    if (shouldCheckPreconditions()) {
        if (!((refund_amount > 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_refund',
                clause: 'positive_refund',
                expression: 'refund_amount > 0.0',
                context: { refund_amount, original_amount }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((original_amount > 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_refund',
                clause: 'positive_original',
                expression: 'original_amount > 0.0',
                context: { refund_amount, original_amount }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((refund_amount <= original_amount))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_refund',
                clause: 'refund_not_exceeds',
                expression: 'refund_amount <= original_amount',
                context: { refund_amount, original_amount }
            });
        }
    }
    let __result;
    try {
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!((__result === true))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'validate_refund',
                    clause: 'refund_valid',
                    expression: 'result == True',
                    context: { result: __result, refund_amount: refund_amount, original_amount: original_amount }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {number} subtotal
 * @param {number} tax_rate
 * @returns {number}
 */
function calculate_total_with_tax(subtotal, tax_rate) {
    if (shouldCheckPreconditions()) {
        if (!((subtotal >= 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'calculate_total_with_tax',
                clause: 'positive_subtotal',
                expression: 'subtotal >= 0.0',
                context: { subtotal, tax_rate }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!(((tax_rate >= 0.0) && (tax_rate <= 1.0)))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'calculate_total_with_tax',
                clause: 'valid_tax_rate',
                expression: 'tax_rate >= 0.0 and tax_rate <= 1.0',
                context: { subtotal, tax_rate }
            });
        }
    }
    let __result;
    try {
        const tax_amount = (subtotal * tax_rate);
        const total = (subtotal + tax_amount);
        __result = total;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!((__result >= subtotal))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'calculate_total_with_tax',
                    clause: 'total_includes_tax',
                    expression: 'result >= subtotal',
                    context: { result: __result, subtotal: subtotal, tax_rate: tax_rate }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {number} original_price
 * @param {number} discount_percent
 * @returns {number}
 */
function apply_discount(original_price, discount_percent) {
    if (shouldCheckPreconditions()) {
        if (!((original_price > 0.0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'apply_discount',
                clause: 'positive_price',
                expression: 'original_price > 0.0',
                context: { original_price, discount_percent }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!(((discount_percent >= 0.0) && (discount_percent <= 100.0)))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'apply_discount',
                clause: 'valid_discount',
                expression: 'discount_percent >= 0.0 and discount_percent <= 100.0',
                context: { original_price, discount_percent }
            });
        }
    }
    let __result;
    try {
        const discount_amount = (original_price * (discount_percent / 100.0));
        const final_price = (original_price - discount_amount);
        __result = final_price;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result >= 0.0) && (__result <= original_price)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'apply_discount',
                    clause: 'discounted_price',
                    expression: 'result >= 0.0 and result <= original_price',
                    context: { result: __result, original_price: original_price, discount_percent: discount_percent }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {string} current_status
 * @param {string} new_status
 * @returns {boolean}
 */
function can_transition_status(current_status, new_status) {
    if (shouldCheckPreconditions()) {
        if (!((len(current_status) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'can_transition_status',
                clause: 'valid_current',
                expression: '<expr> > 0',
                context: { current_status, new_status }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((len(new_status) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'can_transition_status',
                clause: 'valid_new',
                expression: '<expr> > 0',
                context: { current_status, new_status }
            });
        }
    }
    let __result;
    try {
        if ((current_status === "pending")) {
            if (((new_status === "payment_confirmed") || (new_status === "cancelled"))) {
                return true;
            }
        }
        if ((current_status === "payment_confirmed")) {
            if (((new_status === "processing") || (new_status === "cancelled"))) {
                return true;
            }
        }
        if ((current_status === "processing")) {
            if (((new_status === "shipped") || (new_status === "cancelled"))) {
                return true;
            }
        }
        if ((current_status === "shipped")) {
            if ((new_status === "delivered")) {
                return true;
            }
        }
        if ((current_status === "delivered")) {
            if ((new_status === "refunded")) {
                return true;
            }
        }
        __result = false;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'can_transition_status',
                    clause: 'transition_decided',
                    expression: 'result == True or result == False',
                    context: { result: __result, current_status: current_status, new_status: new_status }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {string} status
 * @returns {boolean}
 */
function is_final_state(status) {
    if (shouldCheckPreconditions()) {
        if (!((len(status) > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'is_final_state',
                clause: 'valid_status',
                expression: '<expr> > 0',
                context: { status }
            });
        }
    }
    let __result;
    try {
        if ((((status === "delivered") || (status === "cancelled")) || (status === "refunded"))) {
            return true;
        }
        __result = false;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'is_final_state',
                    clause: 'is_boolean',
                    expression: 'result == True or result == False',
                    context: { result: __result, status: status }
                });
            }
        }
    }
    return __result;
}


/**
 * @param {number} item_count
 * @param {number} max_items_per_order
 * @returns {boolean}
 */
function validate_item_count(item_count, max_items_per_order) {
    if (shouldCheckPreconditions()) {
        if (!((item_count > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_item_count',
                clause: 'positive_count',
                expression: 'item_count > 0',
                context: { item_count, max_items_per_order }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((max_items_per_order > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'validate_item_count',
                clause: 'positive_max',
                expression: 'max_items_per_order > 0',
                context: { item_count, max_items_per_order }
            });
        }
    }
    let __result;
    try {
        if ((item_count > max_items_per_order)) {
            return false;
        }
        __result = true;
    } finally {
        if (shouldCheckPostconditions()) {
            if (!(((__result === true) || (__result === false)))) {
                throw new ContractViolationError({
                    type: 'postcondition',
                    function: 'validate_item_count',
                    clause: 'count_valid',
                    expression: 'result == True or result == False',
                    context: { result: __result, item_count: item_count, max_items_per_order: max_items_per_order }
                });
            }
        }
    }
    return __result;
}
