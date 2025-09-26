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
  return ok({ thrown: Boolean(request.thrown) });
}

module.exports = { VERSION, handle };
