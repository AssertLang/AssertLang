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
  const tasks = Array.isArray(request.tasks) ? request.tasks : null;
  if (!tasks) {
    return error('E_ARGS', 'tasks must be an array');
  }
  const results = tasks.map((task, index) => ({ index, status: 'done', result: task }));
  return ok({ results });
}

module.exports = { VERSION, handle };
