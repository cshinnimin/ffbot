import { getOllamaResponse } from '../api/ollamaApi';
import { getRamValuesMap } from '../api/nesApi';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useCallback } from 'react';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

export function useRamRequest() {
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();

	const requestRamRead = useCallback(async (required_ram_contents: string[]): Promise<string> => {
		if (!required_ram_contents) {
			throw new Error('No RAM contents specified.');
		}

		let ramValuesMap;
		try {
			// Fetch RAM values from nesApi
			ramValuesMap = await getRamValuesMap(required_ram_contents);
		} catch (error) {
			throw new Error('Access to game memory failed.');
		}

		addLlmMessage('user', JSON.stringify({ ram_contents: ramValuesMap }));

		if (DEBUG_MODE) {
			console.log('useRamRequest - requestRamRead - llmMessagesRef.current:');
			console.log(llmMessagesRef.current);
		}

		const response = await getOllamaResponse(llmMessagesRef.current, false);
		const responseJson = JSON.parse(response.message.content);

		addLlmMessage('assistant', responseJson.answer);

		return responseJson.answer;
	}, [llmMessagesRef, addLlmMessage]);

	return { requestRamRead };
}
