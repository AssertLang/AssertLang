const fs = require('fs');
const path = require('path');

const VERSION = 'v1';

async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return { ok: false, version: VERSION, error: { code: 'E_SCHEMA', message: 'request must be an object' } };
  }
  const taskId = request.task_id;
  if (typeof taskId !== 'string') {
    return { ok: false, version: VERSION, error: { code: 'E_ARGS', message: 'task_id must be a string' } };
  }
  const base = path.join('.mcpd', taskId);
  const logs = [];
  if (fs.existsSync(base)) {
    const walk = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          walk(fullPath);
        } else if (entry.name.endsWith('.log')) {
          try {
            const content = fs.readFileSync(fullPath, 'utf-8');
            const lines = content.split('\n');
            logs.push({ file: fullPath, last: lines.slice(-1) });
          } catch (err) {
            // skip files that can't be read
          }
        }
      }
    };
    walk(base);
  }
  return { ok: true, version: VERSION, data: { errors: [], summary: '', logs } };
}

module.exports = { VERSION, handle };