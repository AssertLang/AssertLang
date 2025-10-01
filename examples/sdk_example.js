/**
 * Example: Using the Promptware Node.js SDK
 *
 * Demonstrates all SDK features:
 * - Dynamic verb discovery
 * - Automatic retries
 * - Circuit breaker
 * - Health checks
 * - Error handling
 */

import {
  Agent,
  callVerb,
  VerbNotFoundError,
  InvalidParamsError,
  ConnectionError,
  CircuitBreakerError,
} from '../promptware-js/sdk.js';

async function basicUsage() {
  console.log('=== Basic Usage ===\n');

  // Create agent client
  const agent = new Agent('http://localhost:3000');

  // Health check
  const health = await agent.health();
  console.log('Health:', health);

  // List available verbs
  const verbs = await agent.listVerbs();
  console.log('\nAvailable verbs:', verbs);

  // Call verb with dot notation (assumes @v1)
  try {
    const result = await agent.user.create({
      email: 'alice@example.com',
      name: 'Alice Johnson'
    });
    console.log('\nUser created:', result);
  } catch (error) {
    if (error instanceof VerbNotFoundError) {
      console.log('\nNote: user.create@v1 verb not found - using mock agent');
    }
  }
}

async function errorHandling() {
  console.log('\n=== Error Handling ===\n');

  const agent = new Agent('http://localhost:3000');

  // Verb not found
  try {
    await agent.nonexistent.verb();
  } catch (error) {
    if (error instanceof VerbNotFoundError) {
      console.log('Verb not found:', error.message);
    }
  }

  // Invalid parameters
  try {
    await agent.user.create();  // Missing required params
  } catch (error) {
    if (error instanceof InvalidParamsError) {
      console.log('Invalid parameters:', error.message);
    }
  }

  // Connection error
  try {
    const badAgent = new Agent('http://localhost:9999', { timeout: 5000 });
    await badAgent.health();
  } catch (error) {
    if (error instanceof ConnectionError) {
      console.log('Connection failed:', error.message);
    }
  }
}

async function withRetries() {
  console.log('\n=== Automatic Retries ===\n');

  const agent = new Agent('http://localhost:3000', {
    maxRetries: 5,
    retryDelay: 2000,
    timeout: 60000
  });

  // Will automatically retry on network errors
  try {
    const result = await agent.user.get({ userId: '123' });
    console.log('User retrieved (with retries):', result);
  } catch (error) {
    if (error instanceof VerbNotFoundError) {
      console.log('Note: user.get@v1 verb not found - using mock agent');
    }
  }
}

async function circuitBreakerExample() {
  console.log('\n=== Circuit Breaker ===\n');

  const agent = new Agent('http://localhost:3000', {
    circuitBreakerThreshold: 3,  // Open after 3 failures
    circuitBreakerTimeout: 10000  // Try again after 10 seconds
  });

  // Listen to circuit breaker events
  agent.on('circuit-breaker-state', (state) => {
    console.log(`[Circuit Breaker] State: ${state}`);
  });

  // Simulate failures
  const badAgent = new Agent('http://localhost:9999', {
    circuitBreakerThreshold: 2,
    timeout: 2000
  });

  for (let i = 0; i < 5; i++) {
    try {
      await badAgent.health();
    } catch (error) {
      if (error instanceof CircuitBreakerError) {
        console.log(`Attempt ${i+1}: Circuit breaker is OPEN - service unavailable`);
        break;
      } else if (error instanceof ConnectionError) {
        console.log(`Attempt ${i+1}: Connection failed`);
      }
    }
  }
}

async function verbDiscovery() {
  console.log('\n=== Verb Discovery ===\n');

  const agent = new Agent('http://localhost:3000');

  // Discover all verbs
  const verbs = await agent.discover();
  console.log(`Discovered ${verbs.length} verbs:`);

  for (const verb of verbs) {
    console.log(`\nVerb: ${verb.name}`);
    console.log(`  Description: ${verb.description || 'N/A'}`);

    // Show parameters
    const inputSchema = verb.inputSchema || {};
    const properties = inputSchema.properties || {};
    const required = inputSchema.required || [];

    if (Object.keys(properties).length > 0) {
      console.log('  Parameters:');
      for (const [paramName, paramSchema] of Object.entries(properties)) {
        const requiredStr = required.includes(paramName) ? ' (required)' : '';
        const paramType = paramSchema.type || 'unknown';
        console.log(`    - ${paramName}: ${paramType}${requiredStr}`);
      }
    }
  }
}

async function productionConfig() {
  console.log('\n=== Production Configuration ===\n');

  const agent = new Agent('http://localhost:3000', {
    timeout: 60000,
    maxRetries: 5,
    retryDelay: 2000,
    retryBackoff: 2.0,
    circuitBreakerThreshold: 10,
    circuitBreakerTimeout: 120000,
    enableLogging: true
  });

  // Monitor circuit breaker
  agent.on('circuit-breaker-state', (state) => {
    console.log(`[Production] Circuit breaker state: ${state}`);
  });

  // Use in production with proper error handling
  try {
    // Health check before processing
    const health = await agent.health();
    if (health.status !== 'alive') {
      throw new Error('Service not healthy');
    }

    // Process requests
    const result = await agent.user.create({
      email: 'production@example.com',
      name: 'Production User'
    });
    console.log('Production request successful:', result);

  } catch (error) {
    if (error instanceof VerbNotFoundError) {
      console.log('Note: user.create@v1 verb not found - using mock agent');
    } else {
      console.log('Production error:', error.message);
    }
  } finally {
    agent.close();
  }
}

async function convenienceFunction() {
  console.log('\n=== Convenience Function ===\n');

  // One-off verb call
  try {
    const result = await callVerb(
      'http://localhost:3000',
      'user.get@v1',
      { userId: '123' }
    );
    console.log('One-off call result:', result);
  } catch (error) {
    if (error instanceof VerbNotFoundError) {
      console.log('Note: user.get@v1 verb not found - using mock agent');
    }
  }
}

// Main execution
(async () => {
  console.log('Promptware SDK Examples\n');
  console.log('Make sure you have an agent running on http://localhost:3000');
  console.log('Or use: promptware generate test.pw --lang python && cd generated/test && python test_server.py\n');

  try {
    await basicUsage();
    await errorHandling();
    await withRetries();
    await circuitBreakerExample();
    await verbDiscovery();
    await productionConfig();
    await convenienceFunction();

    console.log('\n=== All Examples Complete ===');
  } catch (error) {
    console.error('\nUnexpected error:', error);
  }
})();
