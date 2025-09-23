import type { ErrorHandler } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';
import { FinalMessageContainsRamAddressesError } from '../../../types/Error';

export const ramAddressesErrorHandler: ErrorHandler = {
  canHandle: (error) => error instanceof FinalMessageContainsRamAddressesError,
  handle: async (_error, { issueCorrection, CorrectionType }) => ({
    answerString: '',
    transientResponse: await issueCorrection(CorrectionType.RAM_ADDRESSES_NOT_ALLOWED)
  } as LlmResponse)
};
