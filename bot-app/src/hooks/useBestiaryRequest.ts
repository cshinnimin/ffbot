import { useCallback } from "react";
import { useLlmMessages } from '../references/LlmMessagesRef';
import bestiaryData from '../../public/symlinks/ramdisk/bestiary.json';
import { getLlmResponse, parseResponse } from "../api/llmApi";

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Types for the bestiary data
export type BestiaryMap = Record<string, string[]>;
export type ReverseBestiaryMap = Record<string, string[]>;

export function useBestiaryRequest() {
  // import llmMessages
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();
  
  // Build maps synchronously at module load
  const bestiary: BestiaryMap = bestiaryData as BestiaryMap;
  const reverseBestiary: ReverseBestiaryMap = {};
  for (const [loc, monsters] of Object.entries(bestiary)) {
    for (const monster of monsters) {
      if (!reverseBestiary[monster]) reverseBestiary[monster] = [];
      reverseBestiary[monster].push(loc);
    }
  }

  // Returns a promise to match the async pattern of requestRamRead
  const requestMonstersByLocation = useCallback(async (location: string): Promise<string[]> => {
    const monsters = bestiary[location] || ["no monsters here"];
    addLlmMessage('user', JSON.stringify({monsters: monsters}));

    if (DEBUG_MODE) {
      console.log('%cuseBestiaryRequest - requestMonstersByLocation - llmMessagesRef.current:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(llmMessagesRef.current);
    }
    
    const response = await getLlmResponse(llmMessagesRef.current, false);
    addLlmMessage('assistant', parseResponse(response));
    
    if (DEBUG_MODE) {
        console.log('%cuseBestiary - requestMonstersByLocation - response:', 'color: #888888; font-size: 14px; font-weight: bold;');
        console.log(parseResponse(response));
    }
    
    return parseResponse(response);
  }, [addLlmMessage]);

  const requestLocationsByMonster = useCallback(async (monster: string): Promise<string[]> => {
    const locations = reverseBestiary[monster] || ["no locations found"];
    addLlmMessage('user', JSON.stringify({locations: locations}));

    if (DEBUG_MODE) {
      console.log('%cuseBestiaryRequest - requestLocationsByMonster - llmMessagesRef.current:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(llmMessagesRef.current);
    }

    const response = await getLlmResponse(llmMessagesRef.current, false);
    addLlmMessage('assistant', parseResponse(response));

    if (DEBUG_MODE) {
        console.log('%cuseBestiary - requestLocationsByMonster - response:', 'color: #888888; font-size: 14px; font-weight: bold;');
        console.log(parseResponse(response));
    }

    return parseResponse(response);
  }, [addLlmMessage]);

  return {
    requestMonstersByLocation,
    requestLocationsByMonster,
  };
}
