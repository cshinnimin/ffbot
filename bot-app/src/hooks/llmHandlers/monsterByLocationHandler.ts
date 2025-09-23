import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const monsterByLocationHandler: LlmHandler = {
  canHandle: (json: any): boolean => !!json.required_services?.bestiary?.location,
  handle: async (json: any, { requestMonstersByLocation }: { requestMonstersByLocation: (location: any) => Promise<string | string[]> }): Promise<LlmResponse> => {
    const result = await requestMonstersByLocation(json.required_services.bestiary.location);
    return {
      answerString: '',
      transientResponse: Array.isArray(result) ? result.join('\n') : result
    } as LlmResponse;
  }
};
