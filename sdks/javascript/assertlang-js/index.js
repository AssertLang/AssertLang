/**
 * AssertLang Node.js Client Library
 *
 * Provides MCP client for calling AssertLang services over HTTP.
 */

export { MCPClient, callVerb } from './client.js';
export {
  MCPError,
  ConnectionError,
  TimeoutError,
  ServiceUnavailableError,
  InvalidVerbError,
  InvalidParamsError,
  ProtocolError
} from './exceptions.js';
