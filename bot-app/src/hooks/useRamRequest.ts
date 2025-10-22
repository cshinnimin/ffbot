import { getLlmResponse } from '../api/llmApi';
import { getRamValuesMap, sendLuaScript } from '../api/nesApi';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useCallback } from 'react';
import { RamContentsError } from '../types/Error';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

export function useRamRequest() {
	// import llmMessages
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

		const response = await getLlmResponse(llmMessagesRef.current);
		addLlmMessage('assistant', response);
		if (DEBUG_MODE) {
			console.log('%cuseRamRequest - requestRamRead - response:', 'color: #ec9ba4; font-size: 14px; font-weight: bold;');
			console.log(response);
		}

		return response;
	}, [llmMessagesRef, addLlmMessage]);

	const requestRamWrite = useCallback(async (lua_script: string, message: string): Promise<string> => {
		if (!lua_script) {
			throw new RamContentsError('No Lua script specified.');
		}

		if (DEBUG_MODE) {
			console.log('%cuseRamRequest - requestRamWrite - lua_script:', 'color: #ec9ba4; font-size: 14px; font-weight: bold;');
			console.log(lua_script);
			console.log('%cuseRamRequest - requestRamWrite - message:', 'color: #ec9ba4; font-size: 14px; font-weight: bold;');
			console.log(message);
		}

		// Call sendLuaScript to write to NES RAM
		await sendLuaScript(lua_script);

		return message;
    }, [llmMessagesRef, addLlmMessage]);

    return { requestRamRead, requestRamWrite };
}
