import type { ErrorHandler } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';
import { FinalMessageContainsSquareBracketsError } from '../../../types/Error';

export const squareBracketsErrorHandler: ErrorHandler = {
  canHandle: (error) => error instanceof FinalMessageContainsSquareBracketsError,
  handle: async (_error, { issueCorrection, CorrectionType }) => ({
    answerString: '',
    transientResponse: await issueCorrection(CorrectionType.SQUARE_BRACKETS_NOT_ALLOWED)
  } as LlmResponse)
};
