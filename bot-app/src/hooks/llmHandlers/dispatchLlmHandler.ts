import type { HandlerDeps, LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export async function dispatchLlmHandler(
  ffbotResponseJson: any,
  handlers: LlmHandler[],
  handlerDeps: HandlerDeps
): Promise<LlmResponse> {
  for (const handler of handlers) {
    if (handler.canHandle(ffbotResponseJson)) {
      // Always return a full LlmResponse
      const result = await handler.handle(ffbotResponseJson, handlerDeps);
      return {
        answerString: result.answerString ?? '',
        transientResponse: result.transientResponse ?? ''
      };
    }
  }

  // fallback: unknown format, "I am Error" throwback to Zelda 2
  return { answerString: 'I am Error.', transientResponse: '' };
}
