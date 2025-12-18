import { useCallback } from "react";
import { useLlmMessages } from '../references/LlmMessagesRef';
import { getLlmResponse } from "../api/llmApi";
import { getMonstersByLocation, getLocationsByMonster } from "../api/nesApi";
import { BestiaryRequestInvalidFormatError } from "../types/Error";

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

export function useBestiaryRequest() {
  // import llmMessages
	const { llmMessagesRef, addLlmMessage } = useLlmMessages();
  

  
  const requestMonstersByLocation = useCallback(async (location: string): Promise<string[]> => {
    // Check if location starts and ends with parentheses
    if (!(location.startsWith('(') && location.endsWith(')'))) {
      throw new BestiaryRequestInvalidFormatError('I cannot seem to retrieve the required information from the bestiary.');
    }

    // Fetch monsters from backend
    const monsters = await getMonstersByLocation(location);
    addLlmMessage('user', JSON.stringify({monsters: monsters}));

    if (DEBUG_MODE) {
      console.log('%cuseBestiaryRequest - requestMonstersByLocation - llmMessagesRef.current:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(llmMessagesRef.current);
    }
    
    const response = await getLlmResponse(llmMessagesRef.current);
    addLlmMessage('assistant', response);

    if (DEBUG_MODE) {
      console.log('%cuseBestiary - requestMonstersByLocation - response:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(response);
    }

    return response;
  }, [addLlmMessage]);

  /**
   * Request locations by monster names.
   *
   */
  const requestLocationsByMonster = useCallback(async (monsters: string[]): Promise<Record<string, string[]>> => {

    // Fetch locations from backend
    const locationsObj = await getLocationsByMonster(monsters);

    addLlmMessage('user', JSON.stringify({ locations: locationsObj }));

    if (DEBUG_MODE) {
      console.log('%cuseBestiaryRequest - requestLocationsByMonster - llmMessagesRef.current:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(llmMessagesRef.current);
    }

    const response = await getLlmResponse(llmMessagesRef.current);
    addLlmMessage('assistant', response);

    if (DEBUG_MODE) {
      console.log('%cuseBestiary - requestLocationsByMonster - response:', 'color: #888888; font-size: 14px; font-weight: bold;');
      console.log(response);
    }

    return response;
  }, [addLlmMessage]);

  return {
    requestMonstersByLocation,
    requestLocationsByMonster,
  };
}
