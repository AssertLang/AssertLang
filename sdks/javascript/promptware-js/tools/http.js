/**
 * HTTP tool adapter for Node.js.
 *
 * Makes HTTP requests with configurable method, headers, body, and timeout.
 */
import axios from 'axios';
import { ok, error } from '../envelope.js';

export const VERSION = 'v1';

/**
 * Handle HTTP request.
 *
 * @param {object} request - Request parameters
 * @param {string} request.url - URL to request
 * @param {string} request.method - HTTP method (GET, POST, etc.)
 * @param {object} request.headers - Request headers
 * @param {string|object} request.body - Request body
 * @param {number} request.timeout_sec - Timeout in seconds
 * @returns {object} Envelope with { status, headers, body }
 */
export function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be a JSON object');
  }

  const method = request.method || 'GET';
  const url = request.url;

  if (!url) {
    return error('E_ARGS', 'url is required');
  }

  const headers = request.headers || {};
  const body = request.body;
  const timeout = (request.timeout_sec || 30) * 1000; // Convert to ms

  return axios({
    method,
    url,
    headers,
    data: body,
    timeout,
    validateStatus: () => true // Don't throw on any status code
  })
    .then(response => {
      return ok({
        status: response.status,
        headers: response.headers,
        body: response.data
      });
    })
    .catch(err => {
      if (err.code === 'ECONNABORTED') {
        return error('E_NETWORK', `Request timed out after ${timeout}ms`);
      }
      return error('E_NETWORK', err.message);
    });
}
