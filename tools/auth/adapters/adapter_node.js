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
  const authType = request.type;
  const token = request.token;
  if (typeof authType !== 'string' || typeof token !== 'string') {
    return error('E_ARGS', 'type and token are required strings');
  }
  if (authType !== 'apiKey' && authType !== 'jwt') {
    return error('E_UNSUPPORTED', `unsupported auth type: ${authType}`);
  }
  const headerName = typeof request.header === 'string' && request.header.trim() ? request.header : 'Authorization';
  const prefix = typeof request.prefix === 'string' ? request.prefix : 'Bearer ';
  const value = prefix ? `${prefix}${token}` : token;
  return ok({ headers: { [headerName]: value } });
}

module.exports = { VERSION, handle };
