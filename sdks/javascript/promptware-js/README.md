# @promptware/client

Node.js client library for calling AssertLang MCP services over HTTP.

## Installation

```bash
npm install @promptware/client
```

## Quick Start

### Simple Function Call

```javascript
import { callVerb } from '@promptware/client';

const result = await callVerb({
  service: 'user-service',
  verb: 'user.get@v1',
  params: { user_id: '123' },
  address: 'http://localhost:23450'
});

console.log(result);
```

### Reusable Client

```javascript
import { MCPClient } from '@promptware/client';

const client = new MCPClient('http://localhost:23450');

// Initialize connection (optional but recommended)
const serverInfo = await client.initialize();
console.log(`Connected to: ${serverInfo.serverInfo.name}`);

// List available tools
const tools = await client.listTools();
tools.forEach(tool => {
  console.log(`- ${tool.name}: ${tool.description}`);
});

// Call verbs
const result = await client.call('user.get@v1', { user_id: '123' });
console.log(result);
```

## API Reference

### `callVerb(options)`

Simple function for one-off verb calls.

```javascript
await callVerb({
  service: 'user-service',    // Service name (documentation only)
  verb: 'user.get@v1',        // Verb name
  params: { user_id: '123' }, // Verb parameters
  address: 'http://localhost:23450', // Service URL
  timeout: 30000,             // Request timeout in ms
  retries: 3                  // Number of retry attempts
});
```

**Returns:** Result object with keys:
- `input_params`: Echo of input parameters
- `tool_results`: Results from tool execution
- `metadata`: Execution metadata
- ...verb-specific return values...

### `MCPClient`

Reusable client for multiple calls.

#### Constructor

```javascript
const client = new MCPClient(address, options);
```

**Options:**
- `timeout` (number): Request timeout in milliseconds (default: 30000)
- `retries` (number): Retry attempts (default: 3)
- `backoffFactor` (number): Exponential backoff multiplier (default: 2.0)

#### Methods

##### `initialize()`

Initialize connection and get server capabilities.

```javascript
const result = await client.initialize();
// Returns:
// {
//   protocolVersion: '0.1.0',
//   capabilities: { tools: {}, prompts: {} },
//   serverInfo: { name: 'service-name', version: 'v1' }
// }
```

##### `listTools()`

List all available tools/verbs.

```javascript
const tools = await client.listTools();
// Returns: Array of tool definitions
```

##### `call(verb, arguments, requestId)`

Call an MCP verb.

```javascript
const result = await client.call('user.get@v1', { user_id: '123' });
```

##### `getServerInfo()`

Get cached server info from `initialize()`.

```javascript
const info = client.getServerInfo();
// Returns null if initialize() not called yet
```

##### `getToolSchema(toolName)`

Get schema for a specific tool.

```javascript
const schema = client.getToolSchema('user.get@v1');
```

## Error Handling

### Exception Hierarchy

```
MCPError (base)
├── ConnectionError        // Failed to connect
├── TimeoutError          // Request timed out
├── ServiceUnavailableError // 5xx server error
├── InvalidVerbError      // Verb not found
├── InvalidParamsError    // Invalid parameters
└── ProtocolError         // MCP protocol violation
```

### Example

```javascript
import {
  callVerb,
  InvalidVerbError,
  InvalidParamsError,
  TimeoutError,
  ConnectionError
} from '@promptware/client';

try {
  const result = await callVerb({
    service: 'user-service',
    verb: 'user.get@v1',
    params: { user_id: '123' },
    address: 'http://localhost:23450',
    timeout: 5000,
    retries: 3
  });
  console.log(result);
} catch (error) {
  if (error instanceof InvalidVerbError) {
    console.error(`Verb not found: ${error.verb}`);
  } else if (error instanceof InvalidParamsError) {
    console.error(`Invalid params: ${error.validationErrors}`);
  } else if (error instanceof TimeoutError) {
    console.error('Request timed out');
  } else if (error instanceof ConnectionError) {
    console.error(`Connection failed: ${error.message}`);
  }
}
```

## Retry Logic

The client automatically retries transient failures:

- **Retry on:**
  - Connection errors
  - 5xx server errors
  - Timeout errors

- **Don't retry on:**
  - 4xx client errors (bad params, verb not found)
  - Successful responses

**Exponential backoff:**
```
Attempt 1: immediate
Attempt 2: 1s delay
Attempt 3: 2s delay
Attempt 4: 4s delay (if retries=3)
```

## Service-to-Service Communication

Example: Order service calling user service

```javascript
import { MCPClient } from '@promptware/client';

async function createOrder(userId, items, total) {
  // Validate user first
  const userClient = new MCPClient('http://user-service:23450');
  const user = await userClient.call('user.get@v1', { user_id: userId });

  if (user.status !== 'active') {
    throw new Error('User is not active');
  }

  // Create order
  const orderClient = new MCPClient('http://order-service:23451');
  const order = await orderClient.call('order.create@v1', {
    user_id: userId,
    items,
    total_amount: total
  });

  return order;
}
```

## Response Format

All verb calls return an object with this structure:

```javascript
{
  input_params: {
    // Echo of your input parameters
    user_id: '123'
  },
  tool_results: {
    // Results from tool execution
    http: {
      ok: true,
      data: { status: 200, ... }
    }
  },
  metadata: {
    mode: 'ide_integrated',  // or 'standalone_ai'
    agent_name: 'user-service',
    timestamp: '2025-09-30T...',
    tools_executed: ['http']
  },
  // Verb-specific return values
  user_id: '123',
  name: 'John Doe',
  email: 'john@example.com'
}
```

## Examples

See the Python examples for equivalent functionality:
- Simple calls
- Reusable clients
- Error handling
- Service-to-service communication

## License

MIT
