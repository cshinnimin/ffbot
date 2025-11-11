import { useCallback } from 'react';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { getLlmResponse } from '../api/llmApi';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Define the enum-like object for correction types
export const CorrectionType = {
  JSON_EXPECTED: 'JSON_EXPECTED',
  RAM_ADDRESSES_NOT_ALLOWED: 'RAM_ADDRESSES_NOT_ALLOWED',
  SQUARE_BRACKETS_NOT_ALLOWED: 'SQUARE_BRACKETS_NOT_ALLOWED',
  BESTIARY_REQUEST_INVALID_FORMAT: 'BESTIARY_REQUEST_INVALID_FORMAT'
} as const;
type CorrectionType = typeof CorrectionType[keyof typeof CorrectionType];

// Map CorrectionType to corrective instructions for the LLM
const CORRECTION_MAP: Record<CorrectionType, string> = {
  [CorrectionType.JSON_EXPECTED]: 'You failed to follow instructions. Please respond in valid JSON format as specified previously.',
  [CorrectionType.RAM_ADDRESSES_NOT_ALLOWED]: 'You failed to follow instructions. Please request ram values from the RRM as specified previously',
  [CorrectionType.SQUARE_BRACKETS_NOT_ALLOWED]: 'You failed to follow instructions. Please perform the math inside the square brackets as specified previously.',
  [CorrectionType.BESTIARY_REQUEST_INVALID_FORMAT]: 'The bestiary request has an invalid format. If providing a location, make sure you include brackets in your location value'
};

export function useTraining() {
    const { llmMessagesRef, addLlmMessage } = useLlmMessages();

    const MAX_ATTEMPTS = Number((import.meta as any).env?.LLM_MAX_ATTEMPTS || '5');
    let trainingAttempts = 0;

    /**
     * A function used to issue a corrective training message to the LLM
     * when it has made a mistake, e.g., not responding in JSON format
     */
    const issueCorrection = useCallback(async (correction: CorrectionType) => {
        if (trainingAttempts >= MAX_ATTEMPTS) {
          if (DEBUG_MODE) {
            console.log('%cuseTraining - max attempts reached:', 'color: #8e86ae; font-size: 14px; font-weight: bold;');
          }

          return '{ "answer": "The maximum number of training attempts has been reached." }';
        }
        
        trainingAttempts++;
        addLlmMessage('user', CORRECTION_MAP[correction]);

        if (DEBUG_MODE) {
          console.log('%cuseTraining - useTraining - llmMessagesRef.current:', 'color: #8e86ae; font-size: 14px; font-weight: bold;');
          console.log(llmMessagesRef.current);
		    }

        const response = await getLlmResponse(llmMessagesRef.current);
        addLlmMessage('assistant', response);
        if (DEBUG_MODE) {
          console.log('%cuseTraining - useTraining - response:', 'color: #8e86ae; font-size: 14px; font-weight: bold;');
          console.log(response);
        }

        return response;
    }, []);

    return { issueCorrection };
}
