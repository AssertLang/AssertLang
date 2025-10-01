/**
 * Test that Node.js tools actually execute and return correct results.
 */
import { getRegistry } from './promptware-js/registry.js';

const registry = getRegistry();

async function runTests() {
  console.log('Node.js Tool Execution Tests');
  console.log('='.repeat(50));

  const tests = [
    {
      name: 'http - GET request',
      tool: 'http',
      params: { url: 'https://httpbin.org/get', method: 'GET', timeout_sec: 5 },
      validate: (result) => result.ok && result.data.status === 200
    },
    {
      name: 'auth - API key header',
      tool: 'auth',
      params: { type: 'apiKey', token: 'test123', header: 'Authorization', prefix: 'Bearer ' },
      validate: (result) => result.ok && result.data.headers.Authorization === 'Bearer test123'
    },
    {
      name: 'conditional - equality check',
      tool: 'conditional',
      params: { left: 'foo', op: '==', right: 'foo' },
      validate: (result) => result.ok && result.data.pass === true
    },
    {
      name: 'logger - log message',
      tool: 'logger',
      params: { level: 'info', message: 'Test log', context: { foo: 'bar' } },
      validate: (result) => result.ok && result.data.logged === true
    },
    {
      name: 'transform - JSON to YAML',
      tool: 'transform',
      params: { from: 'json', to: 'yaml', content: '{"key":"value"}' },
      validate: (result) => result.ok && result.data.content.includes('key: value')
    }
  ];

  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    try {
      const result = await registry.executeTool(test.tool, test.params);

      if (test.validate(result)) {
        console.log(`✓ ${test.name}`);
        passed++;
      } else {
        console.log(`✗ ${test.name} - validation failed`);
        console.log(`  Result:`, JSON.stringify(result, null, 2));
        failed++;
      }
    } catch (error) {
      console.log(`✗ ${test.name} - ${error.message}`);
      failed++;
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log(`Results: ${passed}/${tests.length} tests passed`);

  process.exit(failed > 0 ? 1 : 0);
}

runTests();
