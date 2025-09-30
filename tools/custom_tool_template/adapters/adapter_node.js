const fs = require('fs');
const path = require('path');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  const name = request.name;
  if (typeof name !== 'string') {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'name must be a string' } };
  }
  const filePath = path.join('schemas', 'tools', `${name}.v1.json`);
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, '{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}', 'utf-8');
  }
  return { ok: true, version: VERSION, data: { paths: [filePath] } };
}

module.exports = { VERSION, handle };