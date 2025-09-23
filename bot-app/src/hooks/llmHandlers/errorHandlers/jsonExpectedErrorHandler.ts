import type { ErrorHandler } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';
import { JsonExpectedError } from '../../../types/Error';

export const jsonExpectedErrorHandler: ErrorHandler = {
  canHandle: (error) => error instanceof JsonExpectedError,
  handle: async (_error, { issueCorrection, CorrectionType }) => ({
    answerString: '',
    transientResponse: await issueCorrection(CorrectionType.JSON_EXPECTED)
  } as LlmResponse)
};
