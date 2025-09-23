import type { LlmHandler } from './types';

export const ramReadHandler: LlmHandler = {
  canHandle: (json) => !!json.required_ram_contents,
  handle: async (json, { requestRamRead }) => ({
    transientResponse: await requestRamRead(json.required_ram_contents)
  })
};
