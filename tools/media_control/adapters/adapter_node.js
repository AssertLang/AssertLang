const VERSION = 'v1';

async function handle(request) {
  return { ok: true, version: VERSION, data: { ok: true } };
}

module.exports = { VERSION, handle };