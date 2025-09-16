import { getOllamaResponse } from '../api/ollamaApi';
import { getRamValuesMap } from '../api/nesApi';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useCallback } from 'react';
import { RamContentsError } from '../types/Error';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

export function useRamRequest() {
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();

	const requestRamRead = useCallback(async (required_ram_contents: string[]): Promise<string> => {
		if (!required_ram_contents) {
			throw new RamContentsError('No RAM contents specified.');
		}

		// Fetch RAM values from nesApi
		const ramValuesMap = await getRamValuesMap(required_ram_contents);

		addLlmMessage('user', JSON.stringify({ ram_contents: ramValuesMap }));

		if (DEBUG_MODE) {
			console.log('%cuseRamRequest - requestRamRead - llmMessagesRef.current:', 'color: #ec9ba4; font-size: 14px; font-weight: bold;');
			console.log(llmMessagesRef.current);
		}

		const response = await getOllamaResponse(llmMessagesRef.current, false);
		addLlmMessage('assistant', response.message.content);
		if (DEBUG_MODE) {
			console.log('%cuseRamRequest - requestRamRead - response:', 'color: #ec9ba4; font-size: 14px; font-weight: bold;');
			console.log(response.message.content);
		}

		return response.message.content;
	}, [llmMessagesRef, addLlmMessage]);

	return { requestRamRead };
}
