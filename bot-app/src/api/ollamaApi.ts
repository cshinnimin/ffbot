// Utility for communicating with the Ollama LLM API
// supporting both streaming and non-streaming responses

import type { LlmMessage } from '../types/LlmMessage';

export async function getOllamaResponse(
  conversation: LlmMessage[],
  stream: boolean = false,
  onStreamChunk?: (chunk: string) => void
): Promise<any> {
  try {
    // Read port from VITE_LLM_PORT in .env, default to 11434
    const port = import.meta.env.VITE_LLM_PORT || '11434';
    const model = import.meta.env.VITE_LLM_MODEL || 'llama3.2:3b';
    const temperature = import.meta.env.VITE_LLM_TEMPERATURE || '0.4';
    const keep_alive = import.meta.env.VITE_LLM_KEEP_ALIVE || '30m';

    const url = `http://localhost:${port}/api/chat`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: model,
        messages: conversation,
        stream,
        options: {
          temperature: Number(temperature),
        },
        keep_alive: keep_alive
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
