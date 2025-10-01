import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
app.use(express.json());

// Tool registry imports
// NOTE: Update this path to point to your promptware-js installation
import { getRegistry } from '../../../promptware-js/registry.js';
const toolRegistry = getRegistry();

// Tool executor setup
const configuredTools = ['storage'];

const toolExecutor = {
  hasTools: () => configuredTools.length > 0,
  executeTools: async (params) => {
    const results = {};

    for (const toolName of configuredTools) {
      try {
        // Map parameters to tool
        const toolParams = { ...params };
        const result = await toolRegistry.executeTool(toolName, toolParams);
        results[toolName] = result;
      } catch (error) {
        results[toolName] = {
          ok: false,
          error: { code: 'E_TOOL_EXEC', message: error.message }
        };
      }
    }

    return results;
  }
};

/**
 * Handler for user.create@v1
 *
 * @param {Object} params - Verb parameters
 * @returns {Object} Result object
 */
async function handleUserCreateV1(params) {
  if (!params.email) {
    return {
      error: { code: 'E_ARGS', message: 'Missing required parameter: email' }
    };
  }
  if (!params.name) {
    return {
      error: { code: 'E_ARGS', message: 'Missing required parameter: name' }
    };
  }

  // TODO: Implement actual handler logic
  // For now, return mock data
  return {
    user_id: "user_id_value",
    email: "email_value",
    name: "name_value",
    status: "status_value",
    created_at: "created_at_value"
  };
}

/**
 * Handler for user.get@v1
 *
 * @param {Object} params - Verb parameters
 * @returns {Object} Result object
 */
async function handleUserGetV1(params) {
  if (!params.user_id) {
    return {
      error: { code: 'E_ARGS', message: 'Missing required parameter: user_id' }
    };
  }

  // TODO: Implement actual handler logic
  // For now, return mock data
  return {
    user_id: "user_id_value",
    email: "email_value",
    name: "name_value",
    status: "status_value",
    created_at: "created_at_value"
  };
}

/**
 * Handler for user.list@v1
 *
 * @param {Object} params - Verb parameters
 * @returns {Object} Result object
 */
async function handleUserListV1(params) {
  if (!params.limit) {
    return {
      error: { code: 'E_ARGS', message: 'Missing required parameter: limit' }
    };
  }
  if (!params.offset) {
    return {
      error: { code: 'E_ARGS', message: 'Missing required parameter: offset' }
    };
  }

  // TODO: Implement actual handler logic
  // For now, return mock data
  return {
    users: [],
    total: 0
  };
}

// Main MCP endpoint
app.post('/mcp', async (req, res) => {
  try {
    const { jsonrpc, id, method, params } = req.body;

    if (!method) {
      return res.status(400).json({
        jsonrpc: '2.0',
        id: id || 1,
        error: { code: -32600, message: 'Invalid Request: missing method' }
      });
    }

    // Handle MCP protocol methods
    if (method === 'initialize') {
      return res.json({
        jsonrpc: '2.0',
        id,
        result: {
          protocolVersion: '0.1.0',
          capabilities: { tools: {}, prompts: {} },
          serverInfo: { name: 'user-service', version: 'v1' }
        }
      });
    }

    if (method === 'tools/list') {
      return res.json({
        jsonrpc: '2.0',
        id,
        result: { tools: [
  {
    "name": "user.create@v1",
    "description": "Execute user.create@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Parameter: email"
        },
        "name": {
          "type": "string",
          "description": "Parameter: name"
        }
      },
      "required": [
        "email",
        "name"
      ]
    }
  },
  {
    "name": "user.get@v1",
    "description": "Execute user.get@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "Parameter: user_id"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "user.list@v1",
    "description": "Execute user.list@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "Parameter: limit"
        },
        "offset": {
          "type": "integer",
          "description": "Parameter: offset"
        }
      },
      "required": [
        "limit",
        "offset"
      ]
    }
  }
] }
      });
    }

    if (method === 'tools/call') {
      const verbName = params?.name;
      const verbParams = params?.arguments || {};

      if (!verbName) {
        return res.status(400).json({
          jsonrpc: '2.0',
          id,
          error: { code: -32602, message: 'Invalid params: missing tool name' }
        });
      }

      // Execute tools first (if configured)
      let toolResults = {};
      let toolsExecuted = [];

      if (toolExecutor && toolExecutor.hasTools()) {
        toolResults = await toolExecutor.executeTools(verbParams);
        toolsExecuted = Object.keys(toolResults);
      }

      // Route to appropriate verb handler
      let verbResult = null;

      if (verbName === 'user.create@v1') {
        verbResult = await handleUserCreateV1(verbParams);
      }
      else if (verbName === 'user.get@v1') {
        verbResult = await handleUserGetV1(verbParams);
      }
      else if (verbName === 'user.list@v1') {
        verbResult = await handleUserListV1(verbParams);
      }
      else {
        return res.status(404).json({
          jsonrpc: '2.0',
          id,
          error: { code: -32601, message: `Method not found: ${verbName}` }
        });
      }

      // Check for errors
      if (verbResult && verbResult.error) {
        return res.status(400).json({
          jsonrpc: '2.0',
          id,
          error: { code: -32000, message: verbResult.error.message }
        });
      }

      // Determine mode
      const hasApiKey = !!process.env.ANTHROPIC_API_KEY;
      const mode = (hasApiKey && False) ? 'standalone_ai' : 'ide_integrated';

      // Build MCP-compliant response
      const responseData = {
        input_params: verbParams,
        tool_results: toolResults,
        metadata: {
          mode,
          agent_name: 'user-service',
          timestamp: new Date().toISOString(),
          tools_executed: toolsExecuted
        },
        ...verbResult
      };

      return res.json({
        jsonrpc: '2.0',
        id,
        result: responseData
      });
    }

    // Unknown method
    return res.status(404).json({
      jsonrpc: '2.0',
      id,
      error: { code: -32601, message: `Method not found: ${method}` }
    });

  } catch (error) {
    console.error('MCP endpoint error:', error);
    return res.status(500).json({
      jsonrpc: '2.0',
      id: req.body?.id || 1,
      error: { code: -32603, message: `Internal error: ${error.message}` }
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    agent: 'user-service',
    timestamp: new Date().toISOString()
  });
});

// List all exposed verbs
app.get('/verbs', (req, res) => {
  res.json({
    agent: 'user-service',
    verbs: ['user.create@v1', 'user.get@v1', 'user.list@v1']
  });
});

// Start server
const PORT = 23450;

app.listen(PORT, () => {
  console.log(`MCP server for agent: user-service`);
  console.log(`Port: ${PORT}`);
  console.log(`Exposed verbs: [user.create@v1, user.get@v1, user.list@v1]`);
  console.log(`Health check: http://127.0.0.1:${PORT}/health`);
  console.log(`MCP endpoint: http://127.0.0.1:${PORT}/mcp`);
});