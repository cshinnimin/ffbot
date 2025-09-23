import type { ErrorHandler } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';
import { BestiaryRequestInvalidFormatError } from '../../../types/Error';

export const bestiaryRequestInvalidFormatErrorHandler: ErrorHandler = {
  canHandle: (error) => error instanceof BestiaryRequestInvalidFormatError,
  handle: async (_error, { issueCorrection, CorrectionType }) => ({
    answerString: '',
    transientResponse: await issueCorrection(CorrectionType.BESTIARY_REQUEST_INVALID_FORMAT)
  } as LlmResponse)
};
