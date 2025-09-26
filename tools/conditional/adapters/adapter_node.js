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
  const left = String(request.left ?? '');
  const op = request.op;
  const right = String(request.right ?? '');
  if (typeof op !== 'string') {
    return error('E_ARGS', 'op is required');
  }
  if (op === '==') {
    return ok({ pass: left === right });
  }
  if (op === '!=') {
    return ok({ pass: left !== right });
  }
  if (op === 'regex') {
    try {
      const re = new RegExp(right);
      return ok({ pass: re.test(left) });
    } catch (err) {
      return error('E_RUNTIME', String(err));
    }
  }
  return error('E_ARGS', `unsupported operator: ${op}`);
}

module.exports = { VERSION, handle };
