import type { LlmHandler } from './types';

export const locationByMonsterHandler: LlmHandler = {
  canHandle: (json) => !!json.required_services?.bestiary?.monster,
  handle: async (json, { requestLocationsByMonster }) => {
    const result = await requestLocationsByMonster(json.required_services.bestiary.monster);
    return { transientResponse: Array.isArray(result) ? result.join('\n') : result };
  }
};
