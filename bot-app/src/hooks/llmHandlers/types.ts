export type HandlerDeps = {
  requestRamRead: (arg: any) => Promise<string>;
  requestRamWrite: (lua: any, answer: any) => Promise<any>;
  requestMonstersByLocation: (location: any) => Promise<string | string[]>;
  requestLocationsByMonster: (monster: any) => Promise<string | string[]>;
};

// the LLM handler must return an `answerString` if the LLM included an `answer` 
// in it's response (indicating it has come up with a final answer), or a
// `transientResponse` otherwise (indicating it has requested more information
// from one of the Request hooks)
export type HandlerResult = { transientResponse?: string; answerString?: any };

export type LlmHandler = {
  canHandle: (json: any) => boolean;
  handle: (json: any, deps: HandlerDeps) => Promise<HandlerResult>;
};
