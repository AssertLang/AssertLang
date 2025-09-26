const VERSION = 'v1';

function handle(request) {
  const level = (request.level || 'info').toUpperCase();
  const message = request.message || '';
  const context = request.context || {};
  console.log(`[${level}] ${message} ${JSON.stringify(context)}`);
  return { ok: true, version: VERSION, data: { logged: true } };
}

module.exports = { VERSION, handle };
