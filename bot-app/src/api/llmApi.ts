// Utility for communicating with the LLM API
// supporting both streaming and non-streaming responses

import type { LlmMessage } from '../types/LlmMessage';

export async function getLlmResponse(
  conversation: LlmMessage[]
): Promise<any> {
  try {
    const flaskUrl = '/llm/get_response';
    const response = await fetch(flaskUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: conversation
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error generating response:', error);
    return null;
  }
}

export function parseResponse(response: any) {
  if (!response) {
    return '{ "answer": "The LLM did not return a response." }';
  }

  if (response.error?.message) {
    // error format for openai.com and openrouter.ai
    return '{ "answer": "' + response.error.message + '" }';
  } else if (response.choices) {
    // response format for openai.com and openrouter.ai
    return response.choices[0].message.content;
  } else if (response.message?.content) {
    // response format for Ollama local LLMs
    return response.message.content;
  }

  return {};
}