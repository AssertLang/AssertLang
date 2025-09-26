const VERSION = 'v1';

function ok(data) {
  return { ok: true, version: VERSION, data };
}

function error(code, message) {
  return { ok: false, version: VERSION, error: { code, message } };
}

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be an object');
  }
  const base = request.base;
  const path = request.path;
  if (typeof base !== 'string' || typeof path !== 'string') {
    return error('E_ARGS', 'base and path are required strings');
  }
  let url;
  try {
    url = new URL(path, base);
  } catch (err) {
    return error('E_ARGS', `invalid URL components: ${String(err)}`);
  }
  const params = request.params || {};
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.set(key, String(value));
    }
  });
  const method = (request.method || 'GET').toUpperCase();
  const headers = request.headers || {};
  let bodyValue = request.body;
  if (bodyValue !== undefined && bodyValue !== null && typeof bodyValue !== 'string') {
    bodyValue = JSON.stringify(bodyValue);
    if (!headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }
  }
  const controller = new AbortController();
  const timeout = (request.timeout_sec ?? 30) * 1000;
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const resp = await fetch(url.toString(), { method, headers, body: bodyValue ?? null, signal: controller.signal });
    const text = await resp.text();
    let jsonPayload = null;
    try {
      jsonPayload = JSON.parse(text);
    } catch (err) {
      jsonPayload = null;
    }
    const headerPairs = {};
    resp.headers.forEach((value, key) => { headerPairs[key] = value; });
    return ok({ status: resp.status, headers: headerPairs, text, json: jsonPayload });
  } catch (err) {
    return error('E_NETWORK', String(err));
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { VERSION, handle };
