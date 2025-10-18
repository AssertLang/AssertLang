/**
 * AssertLang SDK - Production-ready client library for MCP agents (Node.js).
 *
 * Features:
 * - Dynamic verb discovery with autocomplete
 * - Automatic retries with exponential backoff
 * - Connection pooling
 * - Circuit breaker pattern
 * - Timeout handling
 * - TypeScript support
 * - Request/response logging
 */

import axios from 'axios';
import { EventEmitter } from 'events';

/**
 * Circuit breaker states
 */
const CircuitState = {
  CLOSED: 'closed',       // Normal operation
  OPEN: 'open',          // Failing, reject requests
  HALF_OPEN: 'half_open' // Testing recovery
};

/**
 * Circuit breaker for fault tolerance
 */
class CircuitBreaker extends EventEmitter {
  constructor(threshold = 5, timeout = 60000) {
    super();
    this.threshold = threshold;
    this.timeout = timeout;
    this.failures = 0;
    this.lastFailureTime = 0;
    this.state = CircuitState.CLOSED;
  }

  async call(fn, ...args) {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime >= this.timeout) {
        this.state = CircuitState.HALF_OPEN;
        this.emit('state-change', CircuitState.HALF_OPEN);
      } else {
        throw new CircuitBreakerError('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn(...args);

      if (this.state === CircuitState.HALF_OPEN) {
        this.state = CircuitState.CLOSED;
        this.failures = 0;
        this.emit('state-change', CircuitState.CLOSED);
      }

      return result;
    } catch (error) {
      this.failures++;
      this.lastFailureTime = Date.now();

      if (this.failures >= this.threshold) {
        this.state = CircuitState.OPEN;
        this.emit('state-change', CircuitState.OPEN);
        this.emit('breaker-open', this.failures);
      }

      throw error;
    }
  }
}

/**
 * Custom errors
 */
class AgentError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AgentError';
  }
}

class ConnectionError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'ConnectionError';
  }
}

class TimeoutError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'TimeoutError';
  }
}

class VerbNotFoundError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'VerbNotFoundError';
  }
}

class InvalidParamsError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'InvalidParamsError';
  }
}

class CircuitBreakerError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'CircuitBreakerError';
  }
}

/**
 * Verb proxy for dynamic method calls
 */
class VerbProxy {
  constructor(client, verbPath = '') {
    this._client = client;
    this._verbPath = verbPath;

    return new Proxy(this, {
      get: (target, prop) => {
        if (prop in target || typeof prop === 'symbol') {
          return target[prop];
        }
        const newPath = target._verbPath ? `${target._verbPath}.${prop}` : prop;
        return new VerbProxy(target._client, newPath);
      },
      apply: (target, thisArg, args) => {
        const params = args[0] || {};
        const verbName = `${target._verbPath}@v1`;
        return target._client.callVerb(verbName, params);
      }
    });
  }
}

/**
 * Production-ready MCP agent client
 *
 * Features:
 * - Dynamic verb discovery
 * - Automatic retries with exponential backoff
 * - Circuit breaker pattern
 * - Connection pooling
 * - Timeout handling
 *
 * @example
 * const agent = new Agent('http://localhost:3000');
 * const result = await agent.user.create({ email: 'test@example.com', name: 'Test User' });
 * const user = await agent.user.get({ userId: '123' });
 */
class Agent extends EventEmitter {
  constructor(baseUrl, options = {}) {
    super();

    this.config = {
      baseUrl: baseUrl.replace(/\/$/, ''),
      timeout: options.timeout || 30000,
      maxRetries: options.maxRetries || 3,
      retryDelay: options.retryDelay || 1000,
      retryBackoff: options.retryBackoff || 2.0,
      circuitBreakerThreshold: options.circuitBreakerThreshold || 5,
      circuitBreakerTimeout: options.circuitBreakerTimeout || 60000,
      enableLogging: options.enableLogging || false,
    };

    // HTTP client with connection pooling
    this.http = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
      // Connection pooling
      maxRedirects: 5,
      httpAgent: options.httpAgent,
      httpsAgent: options.httpsAgent,
    });

    // Circuit breaker
    this.circuitBreaker = new CircuitBreaker(
      this.config.circuitBreakerThreshold,
      this.config.circuitBreakerTimeout
    );

    // Forward circuit breaker events
    this.circuitBreaker.on('state-change', (state) => {
      this.emit('circuit-breaker-state', state);
    });

    // Cache
    this._verbsCache = null;
    this._serverInfo = null;

    // Return proxy for dynamic verb calls
    return new Proxy(this, {
      get: (target, prop) => {
        if (prop in target || typeof prop === 'symbol' || prop.startsWith('_')) {
          return target[prop];
        }
        return new VerbProxy(target, prop);
      }
    });
  }

  /**
   * Check agent health status
   */
  async health() {
    try {
      const response = await this.http.get('/health');
      return response.data;
    } catch (error) {
      throw new ConnectionError(`Health check failed: ${error.message}`);
    }
  }

  /**
   * Check agent readiness status
   */
  async ready() {
    try {
      const response = await this.http.get('/ready');
      return response.data;
    } catch (error) {
      throw new ConnectionError(`Readiness check failed: ${error.message}`);
    }
  }

  /**
   * Discover available verbs from agent
   *
   * @param {boolean} forceRefresh - Force refresh from server
   * @returns {Promise<Array>} List of verb definitions
   */
  async discover(forceRefresh = false) {
    if (this._verbsCache && !forceRefresh) {
      return this._verbsCache;
    }

    try {
      const response = await this._makeRequest('tools/list', {});
      const tools = response.result?.tools || [];
      this._verbsCache = tools;
      return tools;
    } catch (error) {
      if (this.config.enableLogging) {
        console.error('Verb discovery failed:', error);
      }
      return [];
    }
  }

  /**
   * Get list of all verb names
   */
  async listVerbs() {
    const verbs = await this.discover();
    return verbs.map(v => v.name);
  }

  /**
   * Get schema for a specific verb
   */
  async getVerbSchema(verbName) {
    const verbs = await this.discover();
    return verbs.find(v => v.name === verbName) || null;
  }

  /**
   * Call a verb with parameters
   *
   * @param {string} verbName - Verb name (e.g., "user.create@v1")
   * @param {Object} params - Verb parameters
   * @param {Object} options - Call options
   * @returns {Promise<*>} Verb result
   */
  async callVerb(verbName, params = {}, options = {}) {
    return this._callWithRetry(verbName, params, options);
  }

  /**
   * Execute verb call with retry logic
   * @private
   */
  async _callWithRetry(verbName, params, options) {
    let delay = this.config.retryDelay;
    let lastError;

    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        return await this.circuitBreaker.call(
          this._executeCall.bind(this),
          verbName,
          params,
          options
        );
      } catch (error) {
        lastError = error;

        // Don't retry on circuit breaker errors
        if (error instanceof CircuitBreakerError) {
          throw new ConnectionError('Circuit breaker is open - service unavailable');
        }

        // Don't retry on HTTP errors (4xx, 5xx)
        if (error.response && error.response.status >= 400) {
          throw this._handleHttpError(error);
        }

        // Retry on network errors
        if (attempt < this.config.maxRetries) {
          if (this.config.enableLogging) {
            console.warn(`Attempt ${attempt + 1} failed, retrying in ${delay}ms:`, error.message);
          }

          await this._sleep(delay);
          delay *= this.config.retryBackoff;
        }
      }
    }

    throw new ConnectionError(`Failed after ${this.config.maxRetries + 1} attempts: ${lastError.message}`);
  }

  /**
   * Execute the actual verb call
   * @private
   */
  async _executeCall(verbName, params, options) {
    const response = await this._makeRequest(
      'tools/call',
      {
        name: verbName,
        arguments: params,
      },
      options.timeout
    );

    if (response.error) {
      const { code, message } = response.error;

      if (code === -32601) {
        throw new VerbNotFoundError(`Verb not found: ${verbName}`);
      } else if (code === -32602) {
        throw new InvalidParamsError(message);
      } else {
        throw new AgentError(`Agent error (${code}): ${message}`);
      }
    }

    return response.result || {};
  }

  /**
   * Make JSON-RPC request to agent
   * @private
   */
  async _makeRequest(method, params, timeout) {
    const payload = {
      jsonrpc: '2.0',
      id: Date.now(),
      method,
      params,
    };

    if (this.config.enableLogging) {
      console.log('Request:', method, 'with params:', params);
    }

    const response = await this.http.post('/mcp', payload, {
      timeout: timeout || this.config.timeout,
    });

    if (this.config.enableLogging) {
      console.log('Response:', response.data);
    }

    return response.data;
  }

  /**
   * Convert HTTP errors to appropriate exceptions
   * @private
   */
  _handleHttpError(error) {
    if (error.code === 'ECONNABORTED') {
      return new TimeoutError(`Request timed out: ${error.message}`);
    } else if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return new ConnectionError(`Connection failed: ${error.message}`);
    } else if (error.response) {
      return new AgentError(`HTTP ${error.response.status}: ${error.response.statusText}`);
    } else {
      return new AgentError(`HTTP error: ${error.message}`);
    }
  }

  /**
   * Sleep helper
   * @private
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Close HTTP session and release resources
   */
  close() {
    // Axios doesn't need explicit cleanup
  }
}

/**
 * Convenience function for one-off verb calls
 *
 * @example
 * const result = await callVerb(
 *   'http://localhost:3000',
 *   'user.create@v1',
 *   { email: 'test@example.com', name: 'Test' }
 * );
 */
async function callVerb(baseUrl, verbName, params, options = {}) {
  const agent = new Agent(baseUrl, options);
  try {
    return await agent.callVerb(verbName, params);
  } finally {
    agent.close();
  }
}

// Exports
export {
  Agent,
  callVerb,
  AgentError,
  ConnectionError,
  TimeoutError,
  VerbNotFoundError,
  InvalidParamsError,
  CircuitBreakerError,
  CircuitState,
};

export default Agent;
