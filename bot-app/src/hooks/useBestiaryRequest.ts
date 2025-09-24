import { useCallback, useMemo } from "react";
import { useLlmMessages } from '../references/LlmMessagesRef';
import bestiaryData from '../../public/symlinks/ramdisk/bestiary.json';
import { getLlmResponse, parseResponse } from "../api/llmApi";
import { BestiaryRequestInvalidFormatError } from "../types/Error";

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Types for the bestiary data
export type BestiaryMap = Record<string, string[]>;
export type ReverseBestiaryMap = Record<string, string[]>;

export function useBestiaryRequest() {
  // import llmMessages
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();
  
  // Build maps only once for the app lifecycle, bestiary
  // information does not change like RAM information does
  // ( useMemo() caches the information )
  const { bestiary, reverseBestiary } = useMemo(() => {
    const bestiary: BestiaryMap = bestiaryData as BestiaryMap;
    const reverseBestiary: ReverseBestiaryMap = {};

    // Helper to normalize monster names for the reverse bestiary keys:
    // lowercase, remove spaces and symbols
    const normalize = (name: string) => name.toLowerCase().replace(/[^a-z0-9]/g, "");

    for (const [loc, monsters] of Object.entries(bestiary)) {
      for (const monster of monsters) {
        const key = normalize(monster);
        if (!reverseBestiary[key]) reverseBestiary[key] = [];
        reverseBestiary[key].push(loc);
      }
    }
    return { bestiary, reverseBestiary };
  }, []);

  
  const requestMonstersByLocation = useCallback(async (location: string): Promise<string[]> => {
    // Check if location starts and ends with parentheses
    if (!(location.startsWith('(') && location.endsWith(')'))) {
      throw new BestiaryRequestInvalidFormatError('I cannot seem to retrieve the required information from the bestiary.');
    }

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

  /**
   * Request locations by monster names.
   *
   */
  const requestLocationsByMonster = useCallback(async (monsters: string[]): Promise<Record<string, string[]>> => {

    // Strip trailing 's' from entries unless 'cerebus' or 'chaos', since no other
    // monsters in the game end with S
    const normalizedMonsters = monsters.map(monster => {
      if ((monster.toLowerCase() !== 'cerebus' && monster.toLowerCase() !== 'chaos') && monster.endsWith('s')) {
        return monster.slice(0, -1);
      }
      return monster;
    });

    const locationsObj: Record<string, string[]> = {};
    for (let i = 0; i < monsters.length; i++) {
      const monster = normalizedMonsters[i];
      const locations = reverseBestiary[monster] || ["monster not found"];
      locationsObj[monster] = locations;
    }

    addLlmMessage('user', JSON.stringify({ locations: locationsObj }));

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
  }, [addLlmMessage, reverseBestiary]);

  return {
    requestMonstersByLocation,
    requestLocationsByMonster,
  };
}
