import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const ramReadHandler: LlmHandler = {
  canHandle: (json: any): boolean => !!json.required_ram_contents,
  handle: async (json: any, { requestRamRead }: { requestRamRead: (arg: any) => Promise<string> }): Promise<LlmResponse> => {
    return {
      answerString: '',
      transientResponse: await requestRamRead(json.required_ram_contents)
    } as LlmResponse;
  }
};
