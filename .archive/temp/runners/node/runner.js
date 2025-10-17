#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const net = require('net');

function outOk(data) {
  process.stdout.write(JSON.stringify({ ok: true, version: 'v1', data }) + '\n');
}

function outErr(code, message) {
  process.stdout.write(
    JSON.stringify({ ok: false, version: 'v1', error: { code, message } }) + '\n',
  );
}

function parseRequest() {
  const flagIndex = process.argv.indexOf('--json');
  if (flagIndex >= 0 && flagIndex + 1 < process.argv.length) {
    try {
      return JSON.parse(process.argv[flagIndex + 1] || '{}');
    } catch (err) {
      outErr('E_JSON', String(err && err.message ? err.message : err));
      process.exit(0);
    }
  }
  try {
    return JSON.parse(fs.readFileSync(0, 'utf8') || '{}');
  } catch (err) {
    outErr('E_JSON', String(err && err.message ? err.message : err));
    process.exit(0);
  }
}

function handleApply(req) {
  try {
    const target = req.target_dir || process.cwd();
    let writes = 0;
    for (const file of req.files || []) {
      const filePath = path.join(target, file.path);
      fs.mkdirSync(path.dirname(filePath), { recursive: true });
      fs.writeFileSync(filePath, file.content ?? '', 'utf8');
      if (typeof file.mode === 'number') {
        fs.chmodSync(filePath, file.mode);
      }
      writes += 1;
    }
    outOk({ writes, target });
  } catch (err) {
    outErr('E_FS', String(err && err.message ? err.message : err));
  }
}

function handleStart(req) {
  try {
    const cwd = req.cwd || process.cwd();
    const env = { ...process.env, ...(req.env || {}), PORT: String(req.port || 0) };
    const brewPaths = '/opt/homebrew/bin:/usr/local/bin';
    env.PATH = `${brewPaths}:${env.PATH || ''}`;

    const logPath = req.log_path || path.join(cwd, 'run.log');
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    fs.appendFileSync(logPath, `[runner] starting cmd: ${req.cmd} in ${cwd}\n`);

    const child = spawn('bash', ['-lc', req.cmd], {
      cwd,
      env,
      detached: true,
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    child.stdout.on('data', (chunk) => fs.appendFileSync(logPath, chunk));
    child.stderr.on('data', (chunk) => fs.appendFileSync(logPath, chunk));
    child.on('error', (err) =>
      fs.appendFileSync(logPath, `[runner] child error: ${String(err)}\n`),
    );
    child.on('exit', (code) =>
      fs.appendFileSync(logPath, `[runner] child exit code: ${code}\n`),
    );

    child.unref();
    outOk({ pid: child.pid });
  } catch (err) {
    outErr('E_RUNTIME', String(err && err.message ? err.message : err));
  }
}

function handleStop(req) {
  try {
    process.kill(Number(req.pid), 'SIGTERM');
    outOk({ stopped: true });
  } catch (err) {
    outErr('E_RUNTIME', String(err && err.message ? err.message : err));
  }
}

function handleHealth(req) {
  const host = req.host || '127.0.0.1';
  const port = Number(req.port || 0);
  const socket = net.createConnection({ host, port }, () => {
    socket.end();
    outOk({ ready: true });
  });
  socket.on('error', () => outOk({ ready: false }));
  socket.setTimeout(1000, () => {
    socket.destroy();
    outOk({ ready: false });
  });
}

const request = parseRequest();

switch (request.method) {
  case 'apply':
    handleApply(request);
    break;
  case 'start':
    handleStart(request);
    break;
  case 'stop':
    handleStop(request);
    break;
  case 'health':
    handleHealth(request);
    break;
  default:
    outErr('E_METHOD', 'unknown method');
}
