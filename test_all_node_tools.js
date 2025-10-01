/**
 * Test that all 38 Node.js tool adapters can be loaded.
 */
import { getRegistry } from './promptware-js/registry.js';
import { readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const registry = getRegistry();

async function discoverTools() {
  const toolsDir = join(__dirname, 'tools');
  const entries = readdirSync(toolsDir, { withFileTypes: true });

  return entries
    .filter(e => e.isDirectory() && !e.name.startsWith('_'))
    .map(e => e.name)
    .sort();
}

async function testAllTools() {
  console.log('Testing All Node.js Tool Adapters');
  console.log('=' .repeat(50));

  const tools = await discoverTools();
  console.log(`\nDiscovered ${tools.length} tools\n`);

  let loaded = 0;
  let failed = [];

  for (const toolName of tools) {
    try {
      const tool = await registry.getTool(toolName);
      if (tool && tool.handle) {
        loaded++;
        console.log(`✓ ${toolName.padEnd(25)} - loaded`);
      } else {
        failed.push({ tool: toolName, error: 'No handle function' });
        console.log(`✗ ${toolName.padEnd(25)} - no handle function`);
      }
    } catch (error) {
      failed.push({ tool: toolName, error: error.message });
      console.log(`✗ ${toolName.padEnd(25)} - ${error.message}`);
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log(`Results: ${loaded}/${tools.length} tools loaded successfully`);

  if (failed.length > 0) {
    console.log(`\nFailed tools:`);
    failed.forEach(f => console.log(`  - ${f.tool}: ${f.error}`));
  }

  process.exit(failed.length > 0 ? 1 : 0);
}

testAllTools();
