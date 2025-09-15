import { useCallback } from 'react';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getOllamaResponse } from '../api/ollamaApi';
import { useRamRequest } from './useRamRequest';
import { useLlmMessages } from '../references/LlmMessagesRef';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Converts AppMessage to LlmMessage
export function convertAppMessageToLlmMessage(appMessage: AppMessage): LlmMessage {
  return {
    role: appMessage.persona === 'User' ? 'user' : 'assistant',
    content: '{"message": "' + appMessage.message + '"}',
  };
}


export function useLlm() {
  // import the ref and actions we need from the new reference context
  const { llmMessagesRef, addLlmMessage, clearLlmMessages } = useLlmMessages();
  const { requestRamRead } = useRamRequest();

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    addLlmMessage(llmMessage.role, llmMessage.content);
    const response = await getOllamaResponse(llmMessagesRef.current, false);
    addLlmMessage('assistant', response.message.content);

    let responseContent = '';
    try {
      const ffbotResponse = JSON.parse(response.message.content);
      if (DEBUG_MODE) {
        console.log('useLlm - sendLlmMessage - ffbotResponse:');
        console.log(ffbotResponse);
      }

      if (ffbotResponse.required_ram_contents) {
        // is a Ram Read Request (RRR), delegate to ramReadRequest hook
        // for now, only one RRR is ever expected at a single time
        responseContent = await requestRamRead(ffbotResponse.required_ram_contents);
      } else if (ffbotResponse.answer) {
        responseContent = ffbotResponse.answer;
      } else {
        responseContent = response.message.content;
      }
    } catch (error) {
      if (DEBUG_MODE) {
        console.log('useLlm - sendLlmMessage - JSON parse error:');
        console.log(response.message.content);
      }

      return String(error).replace('Error: ', '');
    }

    return responseContent;
  }, [llmMessagesRef, addLlmMessage]);

  // Streaming LLM message
  // TODO: currently not used, but here for future use, may require modifications
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const sendLlmMessageStream = useCallback(async (llmMessage: LlmMessage, onChunk: (chunk: string) => void) => {
    llmMessagesRef.current.push(llmMessage);
    const conversation = [...llmMessagesRef.current];

    let fullResponse = '';
    await getOllamaResponse(conversation, true, (chunk) => {
      fullResponse += chunk;
      if (onChunk) onChunk(chunk);
    });

    // After streaming is done, update ref
    addLlmMessage(llmMessage.role, llmMessage.content);
    addLlmMessage('assistant', fullResponse);
    llmMessagesRef.current.push({
      role: 'assistant',
      content: fullResponse
    });

    return fullResponse;
  }, [llmMessagesRef, addLlmMessage]);

  return { llmMessagesRef, sendLlmMessage, sendLlmMessageStream, clearLlmMessages };
}