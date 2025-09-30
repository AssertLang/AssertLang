const fs = require('fs');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  const artifact = request.artifact;
  if (typeof artifact !== 'string' || !fs.existsSync(artifact)) {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'artifact missing' } };
  }
  const tool = request.tool;
  const version = request.version;
  return { ok: true, version: VERSION, data: { url: `https://market.local/${tool}:${version}` } };
}

module.exports = { VERSION, handle };