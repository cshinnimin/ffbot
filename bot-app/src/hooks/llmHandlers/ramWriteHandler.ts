import type { LlmHandler } from './types';

export const ramWriteHandler: LlmHandler = {
  canHandle: (json) => !!json.lua_script,
  handle: async (json, { requestRamWrite }) => ({
    answerString: await requestRamWrite(json.lua_script, json.answer)
  })
};
