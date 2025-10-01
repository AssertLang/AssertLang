/**
 * Tool envelope format utilities.
 *
 * All tools return responses in a standard envelope format:
 * - Success: { ok: true, version: "v1", data: {...} }
 * - Error: { ok: false, version: "v1", error: { code: "E_*", message: "..." } }
 */

const DEFAULT_VERSION = 'v1';

/**
 * Create success envelope.
 *
 * @param {object} data - Response data
 * @param {string} version - Tool version
 * @returns {object} Success envelope
 */
export function ok(data = {}, version = DEFAULT_VERSION) {
  return {
    ok: true,
    version,
    data
  };
}

/**
 * Create error envelope.
 *
 * @param {string} code - Error code (E_ARGS, E_NETWORK, E_RUNTIME, etc.)
 * @param {string} message - Error message
 * @param {object} details - Optional error details
 * @param {string} version - Tool version
 * @returns {object} Error envelope
 */
export function error(code, message, details = null, version = DEFAULT_VERSION) {
  const err = { code, message };
  if (details) {
    err.details = details;
  }
  return {
    ok: false,
    version,
    error: err
  };
}

/**
 * Validate request is an object.
 *
 * @param {*} req - Request to validate
 * @returns {object|null} Error envelope if invalid, null if valid
 */
export function validateRequest(req) {
  if (typeof req !== 'object' || req === null || Array.isArray(req)) {
    return error('E_SCHEMA', 'request must be an object');
  }
  return null;
}
