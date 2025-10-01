/**
 * Tool registry for dynamic tool loading and execution.
 *
 * Provides a central registry for all available tools, similar to
 * the Python implementation in tools/registry.py.
 */
import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createRequire } from 'module';
import { error, ok } from './envelope.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const require = createRequire(import.meta.url);

/**
 * Tool registry for discovering and executing tools.
 */
export class ToolRegistry {
  constructor() {
    // Point to the main Promptware tools directory
    // __dirname is promptware-js/, so dirname(__dirname) is Promptware/
    const promptwareRoot = dirname(__dirname);
    this.toolsDir = join(promptwareRoot, 'tools');
    this.schemasDir = join(promptwareRoot, 'schemas', 'tools');
    this._cache = new Map();
    this._schemaCache = new Map();
  }

  /**
   * Get tool implementation and schema by name.
   *
   * @param {string} toolName - Name of tool (e.g., 'http', 'storage')
   * @returns {Promise<object|null>} Tool object with handle function and schema
   */
  async getTool(toolName) {
    if (this._cache.has(toolName)) {
      return this._cache.get(toolName);
    }

    // Try to load from tools/<tool>/adapters/adapter_node.js
    const adapterPaths = [
      join(this.toolsDir, toolName, 'adapters', 'adapter_node.js'),
      join(this.toolsDir, toolName.replace('_', '-'), 'adapters', 'adapter_node.js')
    ];

    let toolModule = null;
    for (const adapterPath of adapterPaths) {
      try {
        // Use require to load CommonJS adapters
        toolModule = require(adapterPath);
        break;
      } catch (err) {
        // Try next path (tool may not have Node.js adapter or has missing dependencies)
        continue;
      }
    }

    if (!toolModule || !toolModule.handle) {
      return null;
    }

    // Load schema
    const schema = await this._loadSchema(toolName);

    const toolImpl = {
      handle: toolModule.handle,
      schema,
      version: toolModule.VERSION || 'v1',
      name: toolName
    };

    this._cache.set(toolName, toolImpl);
    return toolImpl;
  }

  /**
   * Load JSON schema for tool.
   *
   * @param {string} toolName - Tool name
   * @returns {Promise<object|null>} JSON schema or null
   */
  async _loadSchema(toolName) {
    if (this._schemaCache.has(toolName)) {
      return this._schemaCache.get(toolName);
    }

    const schemaPaths = [
      join(this.schemasDir, `${toolName}.v1.json`),
      join(this.schemasDir, `${toolName.replace('_', '-')}.v1.json`)
    ];

    for (const schemaPath of schemaPaths) {
      try {
        const schemaData = await readFile(schemaPath, 'utf-8');
        const schema = JSON.parse(schemaData);
        this._schemaCache.set(toolName, schema);
        return schema;
      } catch {
        // Try next path
      }
    }

    return null;
  }

  /**
   * Execute a tool with given parameters.
   *
   * @param {string} toolName - Name of tool to execute
   * @param {object} params - Parameters to pass to tool
   * @returns {Promise<object>} Tool response in envelope format
   */
  async executeTool(toolName, params) {
    const tool = await this.getTool(toolName);
    if (!tool) {
      return error('E_TOOL_NOT_FOUND', `Tool not found: ${toolName}`);
    }

    try {
      const result = await tool.handle(params);

      // Tools already return envelope format
      if (result && typeof result === 'object' && 'ok' in result) {
        return result;
      }

      // Wrap non-envelope responses
      return ok({ result });

    } catch (err) {
      return error('E_TOOL_EXECUTION', `Tool execution failed: ${err.message}`);
    }
  }
}

// Global registry instance
let _registry = null;

/**
 * Get the global tool registry instance.
 *
 * @returns {ToolRegistry} Global registry
 */
export function getRegistry() {
  if (!_registry) {
    _registry = new ToolRegistry();
  }
  return _registry;
}
