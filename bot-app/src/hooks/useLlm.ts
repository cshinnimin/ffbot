import { jsonExpectedErrorHandler } from './llmHandlers/errorHandlers/jsonExpectedErrorHandler';
import { ramAddressesErrorHandler } from './llmHandlers/errorHandlers/ramAddressesErrorHandler';
import { squareBracketsErrorHandler } from './llmHandlers/errorHandlers/squareBracketsErrorHandler';
import { defaultErrorHandler } from './llmHandlers/errorHandlers/defaultErrorHandler';
import { bestiaryRequestInvalidFormatErrorHandler } from './llmHandlers/errorHandlers/bestiaryRequestInvalidFormatErrorHandler';
import { dispatchError as dispatchErrorHandler } from './llmHandlers/errorHandlers/dispatchErrorHandler';
import type { HandlerDeps, LlmHandler } from './llmHandlers/types';
import { ramReadHandler } from './llmHandlers/ramReadHandler';
import { ramWriteHandler } from './llmHandlers/ramWriteHandler';
import { monsterByLocationHandler } from './llmHandlers/monsterByLocationHandler';
import { locationByMonsterHandler } from './llmHandlers/locationByMonsterHandler';
import { answerHandler } from './llmHandlers/answerHandler';
import { useCallback } from 'react';
import { dispatchLlmHandler } from './llmHandlers/dispatchLlmHandler';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getLlmResponse } from '../api/llmApi';
import type { LlmResponse } from '../types/LlmResponse';
import { useRamRequest } from './useRamRequest';
import { useBestiaryRequest } from './useBestiaryRequest';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { useTraining, CorrectionType } from './useTraining';
import { JsonUtils } from '../utils/json';
import { validateLlmAnswerString } from '../validators/LlmResponseValidator';

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

  // import error handlers
  const errorHandlers = [
    jsonExpectedErrorHandler,
    ramAddressesErrorHandler,
    squareBracketsErrorHandler,
    bestiaryRequestInvalidFormatErrorHandler,
    defaultErrorHandler,
  ];
  const errorHandlerContext = { issueCorrection, CorrectionType };

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    addLlmMessage(llmMessage.role, llmMessage.content);
    const response = await getLlmResponse(llmMessagesRef.current);
    // getLlmResponse now returns the assistant's answer string directly
    addLlmMessage('assistant', response);

    // Use LlmResponse type to track both answerString and transientResponse
    let llmResponse: LlmResponse = {
      answerString: '',
      transientResponse: response
    };

    while (!llmResponse.answerString) {
      try {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - transientResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(llmResponse.transientResponse);
        }

        const ffbotResponseJson = JsonUtils.parse(llmResponse.transientResponse);
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - ffbotResponseJson:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(ffbotResponseJson);
        }

        // Use handler dispatcher to handle LLM response
        llmResponse = await dispatchLlmHandler(ffbotResponseJson, handlers, handlerDeps);

        // Perform validations on the answerString
        validateLlmAnswerString(llmResponse.answerString);
      } catch (error) {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - error caught - transientResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(llmResponse.transientResponse);
        }

        llmResponse = await dispatchErrorHandler(error, errorHandlers, errorHandlerContext);
      }
    }

    return llmResponse.answerString;
  }, [llmMessagesRef, addLlmMessage, issueCorrection, requestRamRead]);

  return { llmMessagesRef, sendLlmMessage, clearLlmMessages };
}