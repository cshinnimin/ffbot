import { useCallback } from 'react';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getOllamaResponse } from '../api/ollamaApi';
import { useRamRequest } from './useRamRequest';
import { useLlmMessages } from '../context/LlmMessagesContext';

// Converts AppMessage to LlmMessage
export function convertAppMessageToLlmMessage(appMessage: AppMessage): LlmMessage {
  return {
    role: appMessage.persona === 'User' ? 'user' : 'assistant',
    content: '{"message": "' + appMessage.message + '"}',
  };
}

export function useLlm() {
  // import the state and actions we need from context
  const { llmMessages, addLlmMessage, clearLlmMessages } = useLlmMessages();
  const { requestRamRead } = useRamRequest();

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    let conversation = [...llmMessages, llmMessage];
    const response = await getOllamaResponse(conversation, false);

    // register updates to context
    addLlmMessage(llmMessage.role, llmMessage.content);
    addLlmMessage('assistant', response.message.content);
    // note that updates to the context will not be available until after this
    // entire process completes, we need to pass the building conversation
    // into any additonal hooks or functions that need it:
    conversation = [...conversation, { 
      role: 'assistant', 
      content: response.message.content 
    }];

    let responseContent = '';
    try {
      const ffbotResponse = JSON.parse(response.message.content);

      if (ffbotResponse.required_ram_contents) {
        // is a Ram Read Request (RRR), delegate to ramReadRequest hook
        // for now, only one RRR is ever expected at a single time
        responseContent = await requestRamRead(conversation, ffbotResponse.required_ram_contents);
      } else if (ffbotResponse.answer) {
        responseContent = ffbotResponse.answer;
      } else {
        responseContent = response.message.content;
      }
    } catch (e) {
      // if response is not JSON, just return the raw content
      return response.message.content;
    }

    return responseContent;
  }, [llmMessages, addLlmMessage]);

  // Streaming LLM message
  // TODO: currently not used, but here for future use, may require modifications
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const sendLlmMessageStream = useCallback(async (llmMessage: LlmMessage, onChunk: (chunk: string) => void) => {
    const conversation = [...llmMessages, llmMessage];

    let fullResponse = '';
    await getOllamaResponse(conversation, true, (chunk) => {
      fullResponse += chunk;
      if (onChunk) onChunk(chunk);
    });

    // After streaming is done, update state
    addLlmMessage(llmMessage.role, llmMessage.content);
    addLlmMessage('assistant', fullResponse);

    return fullResponse;
  }, [llmMessages, addLlmMessage]);

  return { llmMessages, sendLlmMessage, sendLlmMessageStream, clearLlmMessages };
}