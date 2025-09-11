import { useState, useCallback } from 'react';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getOllamaResponse } from '../api/ollamaApi';

// Converts AppMessage to LlmMessage
export function convertAppMessageToLlmMessage(appMessage: AppMessage): LlmMessage {
  return {
    role: appMessage.persona === 'User' ? 'user' : 'assistant',
    content: '{"message": "' + appMessage.message + '"}',
  };
}

export function useLlm() {
  const [llmMessages, setLlmMessages] = useState<LlmMessage[]>([]);

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    const conversation = [...llmMessages, llmMessage];
    const response = await getOllamaResponse(conversation, false);

    setLlmMessages((prev) => [...prev, {
        role: 'assistant', content: response.message.content
    }]);

    // TODO: later we will need to return JSON.parse(response.message.content).message
    return response.message.content;
  }, []);

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
    setLlmMessages((prev) => [...prev, {
      role: 'assistant', content: fullResponse
    }]);

    return fullResponse;
  }, []);

  return { llmMessages, sendLlmMessage, sendLlmMessageStream };
}