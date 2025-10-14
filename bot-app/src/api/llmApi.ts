// Utility for communicating with the LLM API
// supporting both streaming and non-streaming responses

import type { LlmMessage } from '../types/LlmMessage';

export async function getLlmResponse(
  conversation: LlmMessage[],
  stream: boolean = false,
  onStreamChunk?: (chunk: string) => void
): Promise<any> {
  try {
    const url = import.meta.env.VITE_LLM_URL || 'http://localhost:11434/api/chat';
    const model = import.meta.env.VITE_LLM_MODEL || 'llama3.2:3b';
    const temperature = Number(import.meta.env.VITE_LLM_TEMPERATURE || '0.4');
    const keep_alive = import.meta.env.VITE_LLM_KEEP_ALIVE || '30m';
    const api_key = import.meta.env.VITE_LLM_API_KEY || ''; 
    const delay = Number(import.meta.env.VITE_LLM_THROTTLE_DELAY || '0'); 

    if (delay) {
      await sleep(delay);
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "Authorization": `Bearer ${api_key}`
      },
      body: JSON.stringify({
        model: model,
        messages: conversation,
        stream,
        // options: {
        //   temperature: temperature,
        // },
        // keep_alive: keep_alive
        temperature: temperature
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

export function parseResponse(response: any) {
  if (response.error?.message) {
    // error format for openai.com
    return '{ "answer": "' + response.error.message + '" }';
  } else if (response.choices) {
    // response format for openrouter.ai
    return response.choices[0].message.content;
  } else if (response.message?.content) {
    // response format for Ollama local LLMs
    return response.message.content;
  }

  return {};
}

const sleep = (ms: number) => new Promise(res => setTimeout(res, ms));
