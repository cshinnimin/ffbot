export type HandlerDeps = {
  requestRamRead: (arg: any) => Promise<string>;
  requestRamWrite: (lua: any, answer: any) => Promise<any>;
  requestMonstersByLocation: (location: any) => Promise<string | string[]>;
  requestLocationsByMonster: (monsters: string[]) => Promise<Record<string, string[]>>;
};

// the LLM handler must return an `answerString` if the LLM included an `answer` 
// in it's response (indicating it has come up with a final answer), or a
// `transientResponse` otherwise (indicating it has requested more information
// from one of the Request hooks)
import type { LlmResponse } from '../../types/LlmResponse';

// HandlerResult is now LlmResponse for clarity and type safety
export type HandlerResult = LlmResponse;

export type LlmHandler = {
  canHandle: (json: any) => boolean;
  handle: (json: any, deps: HandlerDeps) => Promise<LlmResponse>;
};
