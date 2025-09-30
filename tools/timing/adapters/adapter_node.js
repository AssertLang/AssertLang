const VERSION = 'v1';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  if (request.op !== 'sleep') {
    return { ok: false, version: VERSION, error: { code: 'E_UNSUPPORTED', message: 'only sleep supported' } };
  }
  const ms = request.ms;
  if (typeof ms !== 'number' || ms < 0) {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'ms must be a non-negative integer' } };
  }
  const start = Date.now();
  await sleep(ms);
  const elapsed = Date.now() - start;
  return { ok: true, version: VERSION, data: { elapsed_ms: elapsed } };
}

module.exports = { VERSION, handle };