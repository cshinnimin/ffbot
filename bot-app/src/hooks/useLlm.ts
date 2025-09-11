import { useState, useCallback } from 'react';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';

// Converts AppMessage to LlmMessage
export function convertAppMessageToLlmMessage(appMessage: AppMessage): LlmMessage {
  return {
    role: appMessage.persona === 'User' ? 'user' : 'assistant',
    content: '{"message": "' + appMessage.message + '"}',
  };
}

export function useLlm() {
  const [llmMessages, setLlmMessages] = useState<LlmMessage[]>([]);

  const sendLlmMessage = useCallback((llmMessage: LlmMessage) => {
    setLlmMessages((prev) => [...prev, llmMessage]);
    // Here you would also trigger the LLM API call, etc.
  }, []);

  return { llmMessages, sendLlmMessage };
}
