import { FinalMessageContainsRamAddressesError, FinalMessageContainsSquareBracketsError } from '../types/Error';

/**
 * Validates the answerString of an LlmResponse.
 * Throws an error if the answerString contains invalid patterns.
 * Extend this function to add more validation rules as needed.
 */
export function validateLlmAnswerString(answerString: string): void {
  if (!answerString) return;
  if (answerString.includes('0x00')) {
    throw new FinalMessageContainsRamAddressesError('');
  }
  if (answerString.includes('[')) {
    throw new FinalMessageContainsSquareBracketsError('');
  }
  // Add more validation rules here as needed
}
