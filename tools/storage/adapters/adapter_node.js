const VERSION = 'v1';
const fs = require('fs');
const path = require('path');

function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  const backend = request.backend || 'fs';
  if (backend !== 'fs') {
    return { ok: false, version: VERSION, error: { code: 'E_UNSUPPORTED', message: `unsupported backend: ${backend}` } };
  }
  const op = request.op;
  const params = request.params || {};
  const p = params.path;
  if (!p) {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'path is required' } };
  }
  const target = path.resolve(p);
  try {
    if (op === 'put') {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, String(params.content ?? ''), 'utf-8');
      return { ok: true, version: VERSION, data: { written: true } };
    }
    if (op === 'get') {
      const content = fs.readFileSync(target, 'utf-8');
      return { ok: true, version: VERSION, data: { content } };
    }
    if (op === 'list') {
      const glob = params.glob || '';
      const dir = fs.existsSync(target) ? fs.readdirSync(target) : [];
      return { ok: true, version: VERSION, data: { items: dir.map((file) => path.join(target, file)) } };
    }
    if (op === 'delete') {
      if (fs.existsSync(target)) fs.rmSync(target);
      return { ok: true, version: VERSION, data: { deleted: true } };
    }
  } catch (err) {
    return { ok: false, version: VERSION, error: { code: 'E_RUNTIME', message: String(err) } };
  }
  return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: `unsupported op: ${op}` } };
}

module.exports = { VERSION, handle };
