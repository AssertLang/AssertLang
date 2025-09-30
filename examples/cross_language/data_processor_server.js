const express = require('express');
const app = express();

// Agent state (in-memory for demo)
const agentState = {
  agentName: 'data-processor',
  startedAt: new Date().toISOString(),
  requestsHandled: 0
};

// Middleware
app.use(express.json());

/**
 * Handler for data.transform@v1
 *
 * Parameters: input, format
 * Returns: output, status
 */
function handle_data_transform_v1(params) {
  if (!params.input) {
    return { error: { code: "E_ARGS", message: "Missing required parameter: input" } };
  }
  if (!params.format) {
    return { error: { code: "E_ARGS", message: "Missing required parameter: format" } };
  }

  agentState.requestsHandled++;

  // TODO: Implement actual handler logic
  return { output: "output_value", status: "status_value" };
}

/**
 * Handler for data.validate@v1
 *
 * Parameters: data, schema
 * Returns: valid, errors
 */
function handle_data_validate_v1(params) {
  if (!params.data) {
    return { error: { code: "E_ARGS", message: "Missing required parameter: data" } };
  }
  if (!params.schema) {
    return { error: { code: "E_ARGS", message: "Missing required parameter: schema" } };
  }

  agentState.requestsHandled++;

  // TODO: Implement actual handler logic
  return { valid: true, errors: [] };
}

// Main MCP endpoint - handles JSON-RPC requests
app.post('/mcp', (req, res) => {
  try {
    const { method, params = {} } = req.body;

    if (!method) {
      return res.status(400).json({
        ok: false,
        version: 'v1',
        error: {
          code: 'E_ARGS',
          message: "Missing 'method' in request"
        }
      });
    }

    let result;
    switch (method) {
    case "data.transform@v1":
      result = handle_data_transform_v1(params);
      break;
    case "data.validate@v1":
      result = handle_data_validate_v1(params);
      break;
      default:
        return res.status(404).json({
          ok: false,
          version: 'v1',
          error: {
            code: 'E_METHOD',
            message: `Unknown method: ${method}`
          }
        });
    }

    // Check for errors in result
    if (result.error) {
      return res.status(400).json({
        ok: false,
        version: 'v1',
        error: result.error
      });
    }

    // Success response
    res.json({
      ok: true,
      version: 'v1',
      data: result
    });
  } catch (error) {
    res.status(500).json({
      ok: false,
      version: 'v1',
      error: {
        code: 'E_RUNTIME',
        message: error.message
      }
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    agent: 'data-processor',
    uptime: agentState.requestsHandled
  });
});

// List all exposed verbs
app.get('/verbs', (req, res) => {
  res.json({
    agent: 'data-processor',
    verbs: ['"data.transform@v1"', '"data.validate@v1"']
  });
});

// Start server
const PORT = 23500;
app.listen(PORT, () => {
  console.log(`Starting MCP server for agent: data-processor`);
  console.log(`Port: ${PORT}`);
  console.log(`Exposed verbs: ['data.transform@v1', 'data.validate@v1']`);
  console.log(`Health check: http://127.0.0.1:${PORT}/health`);
  console.log(`MCP endpoint: http://127.0.0.1:${PORT}/mcp`);
});