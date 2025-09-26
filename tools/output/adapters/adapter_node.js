const VERSION = 'v1';

function handle(request) {
const fs = require('fs');
const path = require('path');

function ok(data) {
  return { ok: true, version: VERSION, data };
}

function error(code, message) {
  return { ok: false, version: VERSION, error: { code, message } };
}

  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be an object');
  }
  const target = request.target;
  if (target !== 'stdout' && target !== 'file') {
    return error('E_ARGS', 'target must be stdout or file');
  }
  const content = request.content ?? '';
  if (target === 'stdout') {
    console.log(String(content));
    return ok({ written: true });
  }
  const filePath = request.path;
  if (typeof filePath !== 'string' || !filePath) {
    return error('E_ARGS', 'path is required for file target');
  }
  const resolved = path.resolve(filePath);
  fs.mkdirSync(path.dirname(resolved), { recursive: true });
  fs.writeFileSync(resolved, String(content), 'utf-8');
  return ok({ written: true, path: resolved });
}

module.exports = { VERSION, handle };
