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