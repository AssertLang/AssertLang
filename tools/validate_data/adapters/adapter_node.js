const Ajv = require('ajv');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }

  const fmt = request.format;
  const schema = request.schema;
  const content = request.content;

  if (fmt !== 'json') {
    return { ok: false, version: VERSION, error: { code: 'E_UNSUPPORTED', message: `unsupported format: ${fmt}` } };
  }
  if (typeof schema !== 'object' || schema === null || typeof content !== 'string') {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'schema must be an object and content must be a string' } };
  }

  let data;
  try {
    data = JSON.parse(content);
  } catch (exc) {
    return { ok: true, version: VERSION, data: { valid: false, issues: [`json decode failed: ${exc.message}`] } };
  }

  const ajv = new Ajv();
  let validate;
  try {
    validate = ajv.compile(schema);
  } catch (exc) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: `invalid schema: ${exc.message}` } };
  }

  const valid = validate(data);
  if (!valid) {
    const issues = validate.errors.map(err => `${err.instancePath} ${err.message}`);
    return { ok: true, version: VERSION, data: { valid: false, issues } };
  }

  return { ok: true, version: VERSION, data: { valid: true, issues: [] } };
}

module.exports = { VERSION, handle };