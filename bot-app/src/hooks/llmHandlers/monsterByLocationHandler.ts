import type { LlmHandler } from './types';

export const monsterByLocationHandler: LlmHandler = {
  canHandle: (json) => !!json.required_services?.bestiary?.location,
  handle: async (json, { requestMonstersByLocation }) => {
    const result = await requestMonstersByLocation(json.required_services.bestiary.location);
    return { transientResponse: Array.isArray(result) ? result.join('\n') : result };
  }
};
