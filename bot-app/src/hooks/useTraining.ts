import { useCallback } from 'react';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { getOllamaResponse, parseResponse } from '../api/ollamaApi';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Define the enum-like object for correction types
export const CorrectionType = {
  JSON_EXPECTED: 'JSON_EXPECTED',
  RAM_ADDRESSES_NOT_ALLOWED: 'RAM_ADDRESSES_NOT_ALLOWED',
  SQUARE_BRACKETS_NOT_ALLOWED: 'SQUARE_BRACKETS_NOT_ALLOWED'
} as const;
type CorrectionType = typeof CorrectionType[keyof typeof CorrectionType];

// Map CorrectionType to corrective instructions for the LLM
const CORRECTION_MAP: Record<CorrectionType, string> = {
  [CorrectionType.JSON_EXPECTED]: 'You failed to follow instructions. Please respond in valid JSON format as specified previously.',
  [CorrectionType.RAM_ADDRESSES_NOT_ALLOWED]: 'You failed to follow instructions. Please request ram values from the RRM as specified previously',
  [CorrectionType.SQUARE_BRACKETS_NOT_ALLOWED]: 'You failed to follow instructions. Please perform the math inside the square brackets as specified previously.'
};

export function useTraining() {
    const { llmMessagesRef, addLlmMessage } = useLlmMessages();

    /**
     * A function used to issue a corrective training message to the LLM
     * when it has made a mistake, e.g., not responding in JSON format
     */
    const issueCorrection = useCallback(async (correction: CorrectionType) => {
        addLlmMessage('user', CORRECTION_MAP[correction]);

        if (DEBUG_MODE) {
          console.log('%cuseTraining - useTraining - llmMessagesRef.current:', 'color: #8e86ae; font-size: 14px; font-weight: bold;');
          console.log(llmMessagesRef.current);
		    }

        const response = await getOllamaResponse(llmMessagesRef.current, false);
        addLlmMessage('assistant', parseResponse(response));
        if (DEBUG_MODE) {
        console.log('%cuseTraining - useTraining - response:', 'color: #8e86ae; font-size: 14px; font-weight: bold;');
        console.log(parseResponse(response));
      }

      return parseResponse(response);
    }, []);

    return { issueCorrection };
}
