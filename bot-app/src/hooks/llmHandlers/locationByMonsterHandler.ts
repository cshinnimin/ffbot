import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const locationByMonsterHandler: LlmHandler = {
  canHandle: (json: any): boolean => !!json.required_services?.bestiary?.monster,
  handle: async (json: any, { requestLocationsByMonster }: { requestLocationsByMonster: (monster: any) => Promise<string | string[]> }): Promise<LlmResponse> => {
    const result = await requestLocationsByMonster(json.required_services.bestiary.monster);
    return {
      answerString: '',
      transientResponse: Array.isArray(result) ? result.join('\n') : result
    } as LlmResponse;
  }
};
