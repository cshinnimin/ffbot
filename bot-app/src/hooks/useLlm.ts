import type { HandlerDeps, LlmHandler } from './llmHandlers/types';
import { ramReadHandler } from './llmHandlers/ramReadHandler';
import { ramWriteHandler } from './llmHandlers/ramWriteHandler';
import { monsterByLocationHandler } from './llmHandlers/monsterByLocationHandler';
import { locationByMonsterHandler } from './llmHandlers/locationByMonsterHandler';
import { answerHandler } from './llmHandlers/answerHandler';
import { useCallback } from 'react';
import { dispatch } from './llmHandlers/dispatch';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getLlmResponse, parseResponse } from '../api/llmApi';
import { useRamRequest } from './useRamRequest';
import { useBestiaryRequest } from './useBestiaryRequest';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useTraining, CorrectionType } from './useTraining';
import { JsonUtils } from '../utils/json';
import { 
  FinalMessageContainsRamAddressesError, 
  FinalMessageContainsSquareBracketsError, 
  JsonExpectedError 
} from '../types/Error';

const DEBUG_MODE = import.meta.env.VITE_DEBUG_MODE === 'true';

// Converts AppMessage to LlmMessage
export function convertAppMessageToLlmMessage(appMessage: AppMessage): LlmMessage {
  return {
    role: appMessage.persona === 'User' ? 'user' : 'assistant',
    content: '{"message": "' + appMessage.message + '"}',
  };
}

export function useLlm() {
  // import the ref and actions we need from the new reference context
  const { llmMessagesRef, addLlmMessage, clearLlmMessages } = useLlmMessages();
  const { requestRamRead, requestRamWrite } = useRamRequest();
  const { requestMonstersByLocation, requestLocationsByMonster } = useBestiaryRequest();
  const { issueCorrection } = useTraining();

  // import handlers for the different types of responses we
  // have trained the LLM to use
  const handlerDeps: HandlerDeps = {
    requestRamRead,
    requestRamWrite,
    requestMonstersByLocation,
    requestLocationsByMonster
  };
  const handlers: LlmHandler[] = [
    ramReadHandler,
    ramWriteHandler,
    monsterByLocationHandler,
    locationByMonsterHandler,
    answerHandler
  ];

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    addLlmMessage(llmMessage.role, llmMessage.content);
    const response = await getLlmResponse(llmMessagesRef.current, false);
    addLlmMessage('assistant', parseResponse(response));

    let answerString = ''; // main loop will continue until LLM has settled on a final answer
    let transientResponse = parseResponse(response);
    while (!answerString) {
      try {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - transientResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(transientResponse);
        }

        const ffbotResponseJson = JsonUtils.parse(transientResponse);
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - ffbotResponseJson:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(ffbotResponseJson);
        }

        // Use dispatch utility to handle LLM response
        const result = await dispatch(ffbotResponseJson, handlers, handlerDeps);
        if (typeof result.transientResponse !== 'undefined') 
          transientResponse = result.transientResponse;
        if (typeof result.answerString !== 'undefined') 
          answerString = result.answerString;

        if (answerString.includes('0x00')) {
          answerString = ''; // clear final response, LLM requires a correction
          throw new FinalMessageContainsRamAddressesError('');
        }
        if (answerString.includes('[')) {
          answerString = ''; // clear final response, LLM requires a correction
          throw new FinalMessageContainsSquareBracketsError('');
        }
      } catch (error) {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - error caught - transientResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(transientResponse);
        }

        switch (true) {
          case error instanceof JsonExpectedError:
            // Issue corrective training to the LLM for JSON errors, 
            // then retry parsing the new response at the top of the loop
            transientResponse = await issueCorrection(CorrectionType.JSON_EXPECTED);
            break;
          case error instanceof FinalMessageContainsRamAddressesError:
            transientResponse = await issueCorrection(CorrectionType.RAM_ADDRESSES_NOT_ALLOWED);
            break;
          case error instanceof FinalMessageContainsSquareBracketsError:
            transientResponse = await issueCorrection(CorrectionType.SQUARE_BRACKETS_NOT_ALLOWED);
            break;
          default:
            // in the default exception case we return the error string
            // and terminate the loop by setting answerString
            if (error instanceof Error && error.message) {
              // if error is of type Error (or inherits from Error), read error.message
              answerString = error.message;
            } else {
              // otherwise, cast to string and remove "Error: " prefix if present
              answerString = String(error).replace('Error: ', '');
            }
        }
      }
    }

    return answerString;
  }, [llmMessagesRef, addLlmMessage, issueCorrection, requestRamRead]);

  // Streaming LLM message
  // TODO: currently not used, but here for future use, may require modifications
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const sendLlmMessageStream = useCallback(async (llmMessage: LlmMessage, onChunk: (chunk: string) => void) => {
    llmMessagesRef.current.push(llmMessage);
    const conversation = [...llmMessagesRef.current];

    let fullResponse = '';
    await getLlmResponse(conversation, true, (chunk) => {
      fullResponse += chunk;
      if (onChunk) onChunk(chunk);
    });

    // After streaming is done, update ref
    addLlmMessage(llmMessage.role, llmMessage.content);
    addLlmMessage('assistant', fullResponse);
    llmMessagesRef.current.push({
      role: 'assistant',
      content: fullResponse
    });

    return fullResponse;
  }, [llmMessagesRef, addLlmMessage]);

  return { llmMessagesRef, sendLlmMessage, sendLlmMessageStream, clearLlmMessages };
}