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
  const cases = request.cases;
  if (typeof cases !== 'object' || cases === null) {
    return error('E_ARGS', 'cases must be an object');
  }
  const value = String(request.value ?? '');
  const selected = Object.prototype.hasOwnProperty.call(cases, value) ? value : 'default';
  return ok({ selected });
}

module.exports = { VERSION, handle };
