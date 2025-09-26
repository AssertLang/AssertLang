
'use strict';
const VERSION='v1';
const fs = require('fs');
const path = require('path');

let _validator = undefined;
function _loadValidator() {
  if (_validator !== undefined) return _validator;
  try {
    const Ajv = require('ajv');
    let addFormats = null; try { addFormats = require('ajv-formats'); } catch (_e) { /* optional */ }
    const ajv = new Ajv({ allErrors: true, strict: false });
    if (addFormats) addFormats(ajv);
    const schemaPath = path.join(__dirname, '..', 'schema.v1.json');
    const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
    const requestSchema = (schema.properties && schema.properties.request) || schema.request || schema;
    _validator = ajv.compile(requestSchema);
  } catch (e) {
    _validator = null; // Ajv not available; skip deep validation
  }
  return _validator;
}

function capabilities() {
  return { tool: 'mytool', versions: ['v1'], features: ['validation','envelope','idempotency'] };
}

function ok(data) { return { ok: true, version: VERSION, data: data||{} }; }
function error(code, message, details) {
  const err={ code, message }; if (details) err.details=details; return { ok:false, version: VERSION, error: err };
}

function validateRequest(req) {
  if (typeof req !== 'object' || req === null) return error('E_SCHEMA','request must be an object');
  const validate = _loadValidator();
  if (validate) {
    const valid = validate(req);
    if (!valid) return error('E_SCHEMA','schema validation failed', { errors: validate.errors });
  }
  return null;
}

exports.capabilities = capabilities;
exports.handle = function(req) {
  const e = validateRequest(req); if (e) return e;
  const _idempotencyKey = req.idempotency_key;
  try {
    // TODO: implement tool logic using req.data per schema
    return ok({});
  } catch (ex) {
    return error('E_RUNTIME', String((ex && ex.message) || ex));
  }
};
