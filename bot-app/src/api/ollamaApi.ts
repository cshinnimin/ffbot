// Utility for communicating with the Ollama LLM API
// supporting both streaming and non-streaming responses

import type { LlmMessage } from '../types/LlmMessage';

export async function getOllamaResponse(
  conversation: LlmMessage[],
  stream: boolean = false,
  onStreamChunk?: (chunk: string) => void
): Promise<any> {
  try {
    const response = await fetch('http://localhost:11434/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'falcon3:3b',
        messages: conversation,
        stream,
        options: {
          temperature: 0.4,
        },
      }),
    });

    if (stream) {
      if (!response.body) {
        throw new Error('No response body for streaming');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let result = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        result += chunk;
        if (onStreamChunk) onStreamChunk(chunk);
      }

      return JSON.parse(result);
    } else {
      const data = await response.json();
      return data;
    }
  } catch (error) {
    console.error('Error generating response:', error);
    return null;
  }
}
