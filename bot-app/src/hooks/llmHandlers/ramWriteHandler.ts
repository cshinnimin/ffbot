import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const ramWriteHandler: LlmHandler = {
  canHandle: (json: any): boolean => !!json.lua_script,
  handle: async (json: any, { requestRamWrite }: { requestRamWrite: (lua: any, answer: any) => Promise<any> }): Promise<LlmResponse> => {
    return {
      answerString: await requestRamWrite(json.lua_script, json.answer),
      transientResponse: ''
    } as LlmResponse;
  }
};
