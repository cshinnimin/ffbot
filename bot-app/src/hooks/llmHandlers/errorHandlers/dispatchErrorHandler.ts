import type { ErrorHandler, ErrorHandlerContext } from './types';
import type { LlmResponse } from '../../../types/LlmResponse';

export async function dispatchError(
  error: unknown,
  handlers: ErrorHandler[],
  context: ErrorHandlerContext
): Promise<LlmResponse> {
  for (const handler of handlers) {
    if (handler.canHandle(error)) {
      const result = await handler.handle(error, context);
      // Normalize to always return a complete LlmResponse
      return {
        answerString: result.answerString ?? '',
        transientResponse: result.transientResponse ?? ''
      } as LlmResponse;
    }
  }
  
  // fallback should never be hit if defaultErrorHandler is included
  return { answerString: 'Unknown error', transientResponse: '' } as LlmResponse;
}
