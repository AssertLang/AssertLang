/**
 * Simple test for Node.js MCP client
 *
 * Tests against the Python user service from the demo.
 */
import { MCPClient, callVerb } from './index.js';

async function testSimpleCall() {
  console.log('=== Test 1: Simple Call ===');

  try {
    const result = await callVerb({
      service: 'user-service',
      verb: 'user.get@v1',
      params: { user_id: '123' },
      address: 'http://localhost:23450',
      timeout: 5000
    });

    console.log('✓ Simple call succeeded');
    console.log(`  Metadata mode: ${result.metadata.mode}`);
    console.log(`  Agent name: ${result.metadata.agent_name}`);
    return true;
  } catch (error) {
    console.error('✗ Simple call failed:', error.message);
    return false;
  }
}

async function testMCPClient() {
  console.log('\n=== Test 2: MCPClient ===');

  const client = new MCPClient('http://localhost:23450', { timeout: 5000 });

  try {
    // Initialize
    const serverInfo = await client.initialize();
    console.log(`✓ Connected to: ${serverInfo.serverInfo.name}`);

    // List tools
    const tools = await client.listTools();
    console.log(`✓ Found ${tools.length} tools`);
    console.log(`  Tools: ${tools.map(t => t.name).join(', ')}`);

    // Call verb
    const result = await client.call('user.get@v1', { user_id: '456' });
    console.log('✓ Verb call succeeded');
    console.log(`  Tools executed: ${result.metadata.tools_executed.join(', ')}`);

    return true;
  } catch (error) {
    console.error('✗ MCPClient test failed:', error.message);
    return false;
  }
}

async function testErrorHandling() {
  console.log('\n=== Test 3: Error Handling ===');

  const client = new MCPClient('http://localhost:23450', { timeout: 5000, retries: 1 });

  try {
    // Call non-existent verb
    await client.call('unknown.verb@v1', { param: 'value' });
    console.error('✗ Should have thrown InvalidVerbError');
    return false;
  } catch (error) {
    if (error.name === 'InvalidVerbError') {
      console.log('✓ InvalidVerbError thrown correctly');
      return true;
    } else {
      console.error('✗ Wrong error type:', error.name);
      return false;
    }
  }
}

async function testCrossLanguage() {
  console.log('\n=== Test 4: Cross-Language (Node.js → Python) ===');

  try {
    // Node.js client calling Python server
    const result = await callVerb({
      service: 'user-service',
      verb: 'user.create@v1',
      params: {
        email: 'test@example.com',
        name: 'Test User from Node.js'
      },
      address: 'http://localhost:23450'
    });

    console.log('✓ Cross-language call succeeded');
    console.log(`  Created user: ${result.name || 'name_value'}`);
    console.log(`  Email: ${result.email || 'email_value'}`);
    return true;
  } catch (error) {
    console.error('✗ Cross-language call failed:', error.message);
    return false;
  }
}

async function runTests() {
  console.log('Node.js MCP Client Tests');
  console.log('========================\n');
  console.log('NOTE: Start Python user service first:');
  console.log('  cd examples/demo');
  console.log('  python3 user_service_server.py\n');

  const results = [];

  results.push(await testSimpleCall());
  results.push(await testMCPClient());
  results.push(await testErrorHandling());
  results.push(await testCrossLanguage());

  const passed = results.filter(r => r).length;
  const total = results.length;

  console.log('\n========================');
  console.log(`Results: ${passed}/${total} tests passed`);

  if (passed === total) {
    console.log('✓ All tests passed!');
    process.exit(0);
  } else {
    console.log('✗ Some tests failed');
    process.exit(1);
  }
}

runTests();
