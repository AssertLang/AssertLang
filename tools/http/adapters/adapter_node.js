const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  const method = (request.method || 'GET').toUpperCase();
  const url = request.url;
  if (!url) {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'url is required' } };
  }
  const headers = request.headers || {};
  const body = request.body ?? null;
  const controller = new AbortController();
  const timeout = (request.timeout_sec ?? 30) * 1000;
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const resp = await fetch(url, { method, headers, body, signal: controller.signal });
    const text = await resp.text();
    const headerPairs = {};
    resp.headers.forEach((value, key) => { headerPairs[key] = value; });
    return { ok: true, version: VERSION, data: { status: resp.status, headers: headerPairs, body: text } };
  } catch (err) {
    return { ok: false, version: VERSION, error: { code: 'E_NETWORK', message: String(err) } };
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { VERSION, handle };
