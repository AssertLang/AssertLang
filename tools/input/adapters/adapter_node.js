const fs = require('fs');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  if (request.source !== 'file') {
    return { ok: false, version: VERSION, error: { code: 'E_UNSUPPORTED', message: 'only file source supported' } };
  }
  const filePath = request.path;
  if (typeof filePath !== 'string') {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'path must be a string' } };
  }
  const encoding = request.encoding || 'utf-8';
  try {
    const content = fs.readFileSync(filePath, encoding);
    return { ok: true, version: VERSION, data: { content } };
  } catch (err) {
    if (err.code === 'ENOENT') {
      return { ok: false, version: VERSION, error: { code: 'E_RUNTIME', message: 'file not found' } };
    }
    return { ok: false, version: VERSION, error: { code: 'E_RUNTIME', message: err.message } };
  }
}

module.exports = { VERSION, handle };