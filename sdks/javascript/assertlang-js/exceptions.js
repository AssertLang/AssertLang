/**
 * Exception classes for AssertLang MCP client.
 */

export class MCPError extends Error {
  constructor(message, code = null) {
    super(message);
    this.name = 'MCPError';
    this.code = code;
  }
}

export class ConnectionError extends MCPError {
  constructor(message) {
    super(message);
    this.name = 'ConnectionError';
  }
}

export class TimeoutError extends MCPError {
  constructor(message) {
    super(message);
    this.name = 'TimeoutError';
  }
}

export class ServiceUnavailableError extends MCPError {
  constructor(message, code = null) {
    super(message, code);
    this.name = 'ServiceUnavailableError';
  }
}

export class InvalidVerbError extends MCPError {
  constructor(verb, message = null) {
    super(message || `Verb not found: ${verb}`, -32601);
    this.name = 'InvalidVerbError';
    this.verb = verb;
  }
}

export class InvalidParamsError extends MCPError {
  constructor(message, validationErrors = {}) {
    super(message, -32602);
    this.name = 'InvalidParamsError';
    this.validationErrors = validationErrors;
  }
}

export class ProtocolError extends MCPError {
  constructor(message) {
    super(message);
    this.name = 'ProtocolError';
  }
}
