const VERSION = 'v1';

function handle(request) {
const yaml = require('js-yaml');

function ok(data) {
  return { ok: true, version: VERSION, data };
}

function error(code, message) {
  return { ok: false, version: VERSION, error: { code, message } };
}

  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be an object');
  }
  const from = request.from;
  const to = request.to;
  if ((from !== 'json' && from !== 'yaml') || (to !== 'json' && to !== 'yaml')) {
    return error('E_ARGS', 'from/to must be json or yaml');
  }
  const content = request.content ?? '';
  let data;
  try {
    if (from === 'json') {
      data = JSON.parse(String(content || '{}'));
    } else {
      data = yaml.load(String(content || '')) || {};
    }
  } catch (err) {
    return error('E_RUNTIME', String(err));
  }
  try {
    if (to === 'json') {
      const json = JSON.stringify(data, null, 2);
      return ok({ content: json });
    }
    const yamlContent = yaml.dump(data, { sortKeys: false });
    return ok({ content: yamlContent });
  } catch (err) {
    return error('E_RUNTIME', String(err));
  }
}

module.exports = { VERSION, handle };
