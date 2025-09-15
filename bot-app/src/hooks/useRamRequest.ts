import { getOllamaResponse } from '../api/ollamaApi';
import { getRamValuesMap } from '../api/nesApi';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useCallback } from 'react';
import { JsonExpectedError, RamContentsError } from '../types/Error';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

export function useRamRequest() {
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();

	const requestRamRead = useCallback(async (required_ram_contents: string[]): Promise<string> => {
		if (!required_ram_contents) {
			throw new RamContentsError('No RAM contents specified.');
		}

		let ramValuesMap;
		try {
			// Fetch RAM values from nesApi
			ramValuesMap = await getRamValuesMap(required_ram_contents);
		} catch (error) {
			throw new RamContentsError('Access to game memory failed.');
		}

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

		let responseJson;
		try {
			responseJson = JSON.parse(response.message.content);
		} catch (error) {
			throw new JsonExpectedError('I need to recall my training.');
		}

		// we have already validated the content string is in JSON format,
		// but consumers expect the format to be a string, so return that
		return response.message.content;
	}, [llmMessagesRef, addLlmMessage]);

	return { requestRamRead };
}
