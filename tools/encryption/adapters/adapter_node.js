const crypto = require('crypto');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  if (request.op !== 'hash' || request.alg !== 'sha256') {
    return { ok: false, version: VERSION, error: { code: 'E_UNSUPPORTED', message: 'only sha256 hash supported' } };
  }
  const data = request.data;
  if (typeof data !== 'string') {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'data must be a string' } };
  }
  const digest = crypto.createHash('sha256').update(data, 'utf-8').digest('hex');
  return { ok: true, version: VERSION, data: { result: digest } };
}

module.exports = { VERSION, handle };