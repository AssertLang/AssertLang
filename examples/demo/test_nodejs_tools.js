/**
 * Test Node.js tool execution.
 *
 * Tests that the Node.js tool registry actually executes real tools.
 */
import { getRegistry } from '../../promptware-js/registry.js';

const registry = getRegistry();

async function testHttpTool() {
  console.log('=== Test 1: HTTP Tool ===');

  const result = await registry.executeTool('http', {
    url: 'https://httpbin.org/get',
    method: 'GET',
    timeout_sec: 5
  });

  if (result.ok) {
    console.log('✓ HTTP tool succeeded');
    console.log(`  Status: ${result.data.status}`);
    console.log(`  Response headers: ${Object.keys(result.data.headers).length} headers`);
  } else {
    console.log('✗ HTTP tool failed:',result.error.message);
  }

  return result.ok;
}

async function testStorageTool() {
  console.log('\n=== Test 2: Storage Tool ===');

  // Write file
  const writeResult = await registry.executeTool('storage', {
    backend: 'fs',
    op: 'put',
    params: {
      path: '/tmp/promptware-test.txt',
      content: 'Hello from Node.js tool!'
    }
  });

  if (!writeResult.ok) {
    console.log('✗ Storage write failed:', writeResult.error.message);
    return false;
  }

  console.log('✓ Storage write succeeded');

  // Read file
  const readResult = await registry.executeTool('storage', {
    backend: 'fs',
    op: 'get',
    params: {
      path: '/tmp/promptware-test.txt'
    }
  });

  if (!readResult.ok) {
    console.log('✗ Storage read failed:', readResult.error.message);
    return false;
  }

  console.log('✓ Storage read succeeded');
  console.log(`  Content: "${readResult.data.content}"`);

  // Cleanup
  await registry.executeTool('storage', {
    backend: 'fs',
    op: 'delete',
    params: { path: '/tmp/promptware-test.txt' }
  });

  return true;
}

async function testToolNotFound() {
  console.log('\n=== Test 3: Tool Not Found ===');

  const result = await registry.executeTool('nonexistent_tool', {});

  if (!result.ok && result.error.code === 'E_TOOL_NOT_FOUND') {
    console.log('✓ Correctly returned E_TOOL_NOT_FOUND');
    return true;
  } else {
    console.log('✗ Should have returned E_TOOL_NOT_FOUND');
    return false;
  }
}

async function runTests() {
  console.log('Node.js Tool Registry Tests');
  console.log('===========================\n');

  const results = [];

  results.push(await testHttpTool());
  results.push(await testStorageTool());
  results.push(await testToolNotFound());

  const passed = results.filter(r => r).length;
  const total = results.length;

  console.log('\n===========================');
  console.log(`Results: ${passed}/${total} tests passed`);

  if (passed === total) {
    console.log('✓ All tool registry tests passed!');
    process.exit(0);
  } else {
    console.log('✗ Some tests failed');
    process.exit(1);
  }
}

runTests();
