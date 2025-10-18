/**
 * MCP Client for calling AssertLang services over HTTP.
 *
 * Provides both a reusable client class and a simple function-based API.
 */
import { HTTPTransport } from './transport.js';

export class MCPClient {
  /**
   * Initialize MCP client.
   *
   * @param {string} address - Base URL of MCP service
   * @param {object} options - Client options
   * @param {number} options.timeout - Request timeout in milliseconds
   * @param {number} options.retries - Number of retry attempts
   * @param {number} options.backoffFactor - Exponential backoff multiplier
   */
  constructor(address, options = {}) {
    this.address = address;
    this.transport = new HTTPTransport({
      baseUrl: address,
      timeout: options.timeout || 30000,
      retries: options.retries !== undefined ? options.retries : 3,
      backoffFactor: options.backoffFactor || 2.0
    });

    this._initialized = false;
    this._serverInfo = null;
    this._availableTools = null;
  }

  /**
   * Initialize connection to MCP server.
   *
   * Returns server capabilities and information.
   *
   * @returns {Promise<object>} Server info
   */
  async initialize() {
    const result = await this.transport.request('initialize', {});
    this._initialized = true;
    this._serverInfo = result.serverInfo || {};
    return result;
  }

  /**
   * List all available tools/verbs from the server.
   *
   * @returns {Promise<Array>} List of tool definitions
   */
  async listTools() {
    const result = await this.transport.request('tools/list', {});
    const tools = result.tools || [];
    this._availableTools = {};
    for (const tool of tools) {
      this._availableTools[tool.name] = tool;
    }
    return tools;
  }

  /**
   * Call an MCP verb/tool.
   *
   * @param {string} verb - Verb name (e.g., "user.get@v1")
   * @param {object} args - Verb arguments/parameters
   * @param {number} requestId - Optional JSON-RPC request ID
   * @returns {Promise<object>} Result object
   */
  async call(verb, args, requestId = null) {
    const params = {
      name: verb,
      arguments: args
    };

    const result = await this.transport.request(
      'tools/call',
      params,
      requestId || 1
    );

    return result;
  }

  /**
   * Get cached server info (from initialize call).
   *
   * @returns {object|null} Server info or null
   */
  getServerInfo() {
    return this._serverInfo;
  }

  /**
   * Get schema for a specific tool.
   *
   * @param {string} toolName - Tool name
   * @returns {object|null} Tool schema or null
   */
  getToolSchema(toolName) {
    if (!this._availableTools) {
      return null;
    }
    return this._availableTools[toolName] || null;
  }
}

/**
 * Simple function to call an MCP verb.
 *
 * Convenience wrapper that creates a client, calls the verb, and cleans up.
 *
 * @param {string} service - Service name (for documentation)
 * @param {string} verb - Verb name
 * @param {object} params - Verb parameters
 * @param {string} address - Service address
 * @param {number} timeout - Request timeout in milliseconds
 * @param {number} retries - Number of retry attempts
 * @returns {Promise<object>} Result from verb execution
 */
export async function callVerb({
  service,
  verb,
  params,
  address = 'http://localhost:23450',
  timeout = 30000,
  retries = 3
}) {
  const client = new MCPClient(address, { timeout, retries });
  return await client.call(verb, params);
}
