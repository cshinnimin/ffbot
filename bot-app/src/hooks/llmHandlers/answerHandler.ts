import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const answerHandler: LlmHandler = {
  canHandle: (json: any): boolean => !!json.answer,
  handle: async (json: any): Promise<LlmResponse> => {
  return { answerString: json.answer ?? '', transientResponse: '' } as LlmResponse;
  }
};
