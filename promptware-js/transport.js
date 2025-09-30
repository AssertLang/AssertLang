/**
 * HTTP transport layer for MCP client.
 *
 * Handles low-level HTTP communication with retry logic and timeouts.
 */
import axios from 'axios';
import {
  ConnectionError,
  TimeoutError,
  ServiceUnavailableError,
  ProtocolError,
  InvalidVerbError,
  InvalidParamsError,
  MCPError
} from './exceptions.js';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export class HTTPTransport {
  /**
   * Initialize HTTP transport.
   *
   * @param {string} baseUrl - Base URL of MCP service
   * @param {number} timeout - Request timeout in milliseconds
   * @param {number} retries - Number of retry attempts
   * @param {number} backoffFactor - Multiplier for exponential backoff
   * @param {number} initialDelay - Initial delay in milliseconds
   */
  constructor({
    baseUrl,
    timeout = 30000,
    retries = 3,
    backoffFactor = 2.0,
    initialDelay = 1000
  }) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.timeout = timeout;
    this.retries = retries;
    this.backoffFactor = backoffFactor;
    this.initialDelay = initialDelay;

    this.client = axios.create({
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });
  }

  /**
   * Send JSON-RPC request with retry logic.
   *
   * @param {string} method - JSON-RPC method name
   * @param {object} params - Method parameters
   * @param {number} requestId - JSON-RPC request ID
   * @returns {Promise<object>} Response data
   */
  async request(method, params = {}, requestId = 1) {
    const payload = {
      jsonrpc: '2.0',
      id: requestId,
      method,
      params
    };

    let lastException = null;
    let delay = this.initialDelay;

    for (let attempt = 0; attempt < this.retries; attempt++) {
      try {
        const response = await this.client.post(`${this.baseUrl}/mcp`, payload);

        // Check HTTP status
        if (response.status >= 500) {
          lastException = new ServiceUnavailableError(
            `Service returned ${response.status}: ${response.data}`
          );
          if (attempt < this.retries - 1) {
            await sleep(delay);
            delay *= this.backoffFactor;
            continue;
          }
          throw lastException;
        }

        const data = response.data;

        // Validate JSON-RPC structure
        if (!data.jsonrpc || data.jsonrpc !== '2.0') {
          throw new ProtocolError('Invalid JSON-RPC response: missing jsonrpc field');
        }

        if (data.id === undefined || data.id !== requestId) {
          throw new ProtocolError('Invalid JSON-RPC response: ID mismatch');
        }

        // Check for JSON-RPC error
        if (data.error) {
          const error = data.error;
          const code = error.code || -32000;
          const message = error.message || 'Unknown error';

          // These are not retriable (client errors)
          if (code === -32601) {
            throw new InvalidVerbError(params.name || 'unknown', message);
          } else if (code === -32602) {
            throw new InvalidParamsError(message);
          } else {
            throw new MCPError(message, code);
          }
        }

        // Return result
        if (data.result === undefined) {
          throw new ProtocolError('Invalid JSON-RPC response: missing result field');
        }

        return data.result;

      } catch (error) {
        // Re-throw our own exceptions immediately
        if (error instanceof MCPError) {
          throw error;
        }

        // Handle axios errors
        if (error.code === 'ECONNABORTED') {
          lastException = new TimeoutError(`Request timed out after ${this.timeout}ms`);
        } else if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
          lastException = new ConnectionError(`Failed to connect to ${this.baseUrl}: ${error.message}`);
        } else if (error.response && error.response.status >= 500) {
          lastException = new ServiceUnavailableError(
            `Service returned ${error.response.status}`
          );
        } else if (error.response && error.response.status === 404) {
          // 404 might be a method not found error
          lastException = new InvalidVerbError('unknown', error.message);
        } else {
          // Unknown error - wrap it
          lastException = new ConnectionError(error.message);
        }

        // Retry on transient failures
        if (attempt < this.retries - 1) {
          await sleep(delay);
          delay *= this.backoffFactor;
          continue;
        }

        throw lastException;
      }
    }

    // Should never reach here
    throw lastException || new ConnectionError('All retry attempts failed');
  }
}
