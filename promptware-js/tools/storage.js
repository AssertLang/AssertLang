/**
 * Storage tool adapter for Node.js.
 *
 * Provides filesystem operations: get, put, list, delete.
 */
import { readFile, writeFile, unlink, mkdir } from 'fs/promises';
import { dirname } from 'path';
import { glob } from 'glob';
import { ok, error } from '../envelope.js';

export const VERSION = 'v1';

/**
 * Handle storage operation.
 *
 * @param {object} request - Request parameters
 * @param {string} request.backend - Storage backend (only 'fs' supported)
 * @param {string} request.op - Operation: get, put, list, delete
 * @param {object} request.params - Operation parameters
 * @param {string} request.params.path - File/directory path
 * @param {string} request.params.content - Content to write (for put)
 * @param {string} request.params.glob - Glob pattern (for list)
 * @returns {object} Envelope with operation result
 */
export async function handle(request) {
  if (typeof request !== 'object' || request === null) {
    return error('E_SCHEMA', 'request must be an object');
  }

  const backend = request.backend || 'fs';
  if (backend !== 'fs') {
    return error('E_UNSUPPORTED', `unsupported backend: ${backend}`);
  }

  const op = request.op;
  const params = request.params || {};
  const pathValue = params.path;

  if (!pathValue) {
    return error('E_ARGS', 'path is required');
  }

  try {
    switch (op) {
      case 'put': {
        const content = params.content || '';
        const dir = dirname(pathValue);
        await mkdir(dir, { recursive: true });
        await writeFile(pathValue, String(content), 'utf-8');
        return ok({ written: true });
      }

      case 'get': {
        try {
          const content = await readFile(pathValue, 'utf-8');
          return ok({ content });
        } catch (err) {
          if (err.code === 'ENOENT') {
            return error('E_RUNTIME', 'file not found');
          }
          throw err;
        }
      }

      case 'list': {
        const pattern = params.glob || '*';
        const fullPattern = `${pathValue}/${pattern}`;
        const items = await glob(fullPattern);
        return ok({ items });
      }

      case 'delete': {
        try {
          await unlink(pathValue);
          return ok({ deleted: true });
        } catch (err) {
          if (err.code === 'ENOENT') {
            // File doesn't exist, consider it deleted
            return ok({ deleted: true });
          }
          throw err;
        }
      }

      default:
        return error('E_ARGS', `unsupported op: ${op}`);
    }
  } catch (err) {
    return error('E_RUNTIME', err.message);
  }
}
