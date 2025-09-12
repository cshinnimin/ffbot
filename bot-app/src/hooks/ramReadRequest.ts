import { getOllamaResponse } from '../api/ollamaApi';
import { getRamValuesMap } from '../api/nesApi';
import type { LlmMessage } from '../types/LlmMessage';
import { useLlmMessages } from '../context/LlmMessagesContext';

import { useCallback } from 'react';

export function useRamRequest() {
	const { llmMessages, addLlmMessage } = useLlmMessages();

	const requestRamRead = useCallback(async (conversation: LlmMessage[], required_ram_contents: string[]): Promise<string> => {
		if (!required_ram_contents) {
			throw new Error('No RAM contents specified.');
		}

		// Fetch RAM values from nesApi
		const ramValuesMap = await getRamValuesMap(required_ram_contents);

		// Compose a message to send to the LLM
		const ramReadResponseMessage: LlmMessage = {
			role: 'user',
			content: JSON.stringify({ ram_contents: ramValuesMap }),
		};

		//const conversation = [...llmMessages, ramReadResponseMessage];
        conversation = [...conversation, ramReadResponseMessage];
		const response = await getOllamaResponse(conversation, false);

		const responseJson = JSON.parse(response.message.content);

		// Register the RAM read response message for context update
		addLlmMessage(ramReadResponseMessage.role, ramReadResponseMessage.content);

		// Register the LLM's answer for context update
		addLlmMessage('assistant', responseJson.answer);

		return responseJson.answer;
	}, [llmMessages, addLlmMessage]);

	return { requestRamRead };
}
