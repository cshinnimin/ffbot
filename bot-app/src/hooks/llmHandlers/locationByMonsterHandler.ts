
import type { LlmHandler } from './types';
import type { LlmResponse } from '../../types/LlmResponse';

export const locationByMonsterHandler: LlmHandler = {
  canHandle: (json: any): boolean => {
    // Now expect plural: monsters
    return !!json.required_services?.bestiary?.monsters;
  },
  handle: async (json: any, { requestLocationsByMonster }: { requestLocationsByMonster: (monsters: string[]) => Promise<Record<string, string[]>> }): Promise<LlmResponse> => {
    // Now expect plural: monsters
    let monsters: string[] = [];
    if (Array.isArray(json.required_services.bestiary.monsters)) {
      monsters = json.required_services.bestiary.monsters;
    } else if (typeof json.required_services.bestiary.monsters === 'string') {
      monsters = [json.required_services.bestiary.monsters];
    }

    const result = await requestLocationsByMonster(monsters);

    return {
      answerString: '',
      transientResponse: Array.isArray(result) ? result.join('\n') : result
    } as LlmResponse;
  }
};
