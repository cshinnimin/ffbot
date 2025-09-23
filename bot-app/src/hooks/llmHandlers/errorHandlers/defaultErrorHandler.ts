import type { ErrorHandler } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';

export const defaultErrorHandler: ErrorHandler = {
  canHandle: (_error) => true,
  handle: async (error) => {
    let answerString: string;

    if (error instanceof Error && error.message) {
      answerString = error.message;
    } else {
      answerString = String(error).replace('Error: ', '');
    }
    
    return { answerString, transientResponse: '' } as LlmResponse;
  }
};
