import type { HandlerDeps, LlmHandler } from './types';

export async function dispatch(
  ffbotResponseJson: any,
  handlers: LlmHandler[],
  handlerDeps: HandlerDeps
): Promise<{ transientResponse?: string; answerString?: any }> {
  for (const handler of handlers) {
    if (handler.canHandle(ffbotResponseJson)) {
      return handler.handle(ffbotResponseJson, handlerDeps);
    }
  }
  // fallback: unknown format
  return { answerString: 'I am Error.' };
}
