const VERSION = 'v1';

function ok(data) {
  return { ok: true, version: VERSION, data };
}

function error(code, message) {
  return { ok: false, version: VERSION, error: { code, message } };
}

function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be an object');
  }
  const items = Array.isArray(request.items) ? request.items : null;
  if (!items) {
    return error('E_ARGS', 'items must be a list');
  }
  return ok({ iterations: items.length });
}

module.exports = { VERSION, handle };
