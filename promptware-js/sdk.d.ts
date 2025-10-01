/**
 * TypeScript definitions for Promptware SDK
 */

import { EventEmitter } from 'events';
import { AxiosInstance, AxiosRequestConfig } from 'axios';

// Configuration
export interface AgentConfig {
  baseUrl: string;
  timeout?: number;
  maxRetries?: number;
  retryDelay?: number;
  retryBackoff?: number;
  circuitBreakerThreshold?: number;
  circuitBreakerTimeout?: number;
  enableLogging?: boolean;
  httpAgent?: any;
  httpsAgent?: any;
}

// Circuit Breaker
export enum CircuitState {
  CLOSED = 'closed',
  OPEN = 'open',
  HALF_OPEN = 'half_open'
}

// Errors
export class AgentError extends Error {
  name: 'AgentError';
}

export class ConnectionError extends AgentError {
  name: 'ConnectionError';
}

export class TimeoutError extends AgentError {
  name: 'TimeoutError';
}

export class VerbNotFoundError extends AgentError {
  name: 'VerbNotFoundError';
}

export class InvalidParamsError extends AgentError {
  name: 'InvalidParamsError';
}

export class CircuitBreakerError extends AgentError {
  name: 'CircuitBreakerError';
}

// Verb Schema
export interface VerbParameter {
  name: string;
  type: string;
  description?: string;
}

export interface VerbSchema {
  name: string;
  description?: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, any>;
    required?: string[];
  };
}

// Agent
export class Agent extends EventEmitter {
  constructor(baseUrl: string, options?: Partial<AgentConfig>);

  // Health checks
  health(): Promise<{
    status: string;
    uptime_seconds?: number;
    timestamp: string;
  }>;

  ready(): Promise<{
    status: string;
    checks?: Record<string, string>;
    timestamp: string;
  }>;

  // Discovery
  discover(forceRefresh?: boolean): Promise<VerbSchema[]>;
  listVerbs(): Promise<string[]>;
  getVerbSchema(verbName: string): Promise<VerbSchema | null>;

  // Verb calls
  callVerb(
    verbName: string,
    params?: Record<string, any>,
    options?: {
      timeout?: number;
    }
  ): Promise<any>;

  // Lifecycle
  close(): void;

  // Events
  on(event: 'circuit-breaker-state', listener: (state: CircuitState) => void): this;
  on(event: string, listener: (...args: any[]) => void): this;
}

// Allow dynamic property access
export interface Agent {
  [key: string]: any;
}

// Convenience function
export function callVerb(
  baseUrl: string,
  verbName: string,
  params?: Record<string, any>,
  options?: Partial<AgentConfig>
): Promise<any>;

// Default export
export default Agent;
