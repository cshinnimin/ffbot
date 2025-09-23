import type { LlmResponse } from '../../../types/LlmResponse';

export type ErrorHandlerContext = {
  issueCorrection: (type: any) => Promise<string>;
  CorrectionType: any;
};

export type ErrorHandler = {
  canHandle: (error: unknown) => boolean;
  handle: (error: unknown, context: ErrorHandlerContext) => Promise<LlmResponse>;
};
