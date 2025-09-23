import type { LlmHandler } from './types';

export const answerHandler: LlmHandler = {
  canHandle: (json) => !!json.answer,
  handle: async (json) => ({ answerString: json.answer })
};
