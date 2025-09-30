const VERSION = 'v1';

async function handle(request) {
  const op = request && request.op !== undefined ? String(request.op) : 'undefined';
  return { ok: true, version: VERSION, data: { result: op } };
}

module.exports = { VERSION, handle };