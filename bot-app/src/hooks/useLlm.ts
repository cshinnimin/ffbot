import { useCallback } from 'react';
import type { AppMessage } from '../types/AppMessage';
import type { LlmMessage } from '../types/LlmMessage';
import { getOllamaResponse } from '../api/ollamaApi';
import { useRamRequest } from './useRamRequest';
import { useLlmMessages } from '../references/LlmMessagesRef';
import { JsonExpectedError } from '../types/Error';
import { useTraining, CorrectionType } from './useTraining';

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
  const { requestRamRead } = useRamRequest();
  const { issueCorrection } = useTraining();

  // Non-streaming LLM message
  const sendLlmMessage = useCallback(async (llmMessage: LlmMessage) => {
    addLlmMessage(llmMessage.role, llmMessage.content);
    const response = await getOllamaResponse(llmMessagesRef.current, false);
    addLlmMessage('assistant', response.message.content);

    let responseContent = '';
    let ffbotResponse = response.message.content;
    while (!responseContent) {
      try {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - ffbotResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(ffbotResponse);
        }

        const ffbotResponseJson = JSON.parse(ffbotResponse);
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - ffbotResponseJson:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(ffbotResponseJson);
        }

        if (ffbotResponseJson.required_ram_contents) {
          // is a Ram Read Request (RRR), delegate to ramReadRequest hook
          //responseContent = await requestRamRead(ffbotResponseJson.required_ram_contents);
          ffbotResponse = await requestRamRead(ffbotResponseJson.required_ram_contents);
        } else if (ffbotResponseJson.answer) {
          responseContent = ffbotResponseJson.answer;
        } else {
          // if we received JSON from the LLM but it had an unknown format,
          // terminate the loop by setting a generic responseContent
          responseContent = 'I am Error.'; // throwback to Zelda 2
        }
      } catch (error) {
        if (DEBUG_MODE) {
          console.log('%cuseLlm - sendLlmMessage - error caught - ffbotResponse:', 'color: #81aca6; font-size: 14px; font-weight: bold;');
          console.log(ffbotResponse);
        }

        switch (true) {
          case error instanceof JsonExpectedError:
            // Issue corrective training to the LLM for JSON errors, 
            // then retry parsing the new response at the top of the loop
            ffbotResponse = await issueCorrection(CorrectionType.JSON_EXPECTED);
            break;
          default:
            // in the default exception case we return the error string
            // and terminate the loop by setting responseContent
            responseContent = String(error).replace('Error: ', '');
        }
      }
    }

    return responseContent;
  }, [llmMessagesRef, addLlmMessage, issueCorrection, requestRamRead]);

  // Streaming LLM message
  // TODO: currently not used, but here for future use, may require modifications
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const sendLlmMessageStream = useCallback(async (llmMessage: LlmMessage, onChunk: (chunk: string) => void) => {
    llmMessagesRef.current.push(llmMessage);
    const conversation = [...llmMessagesRef.current];

    let fullResponse = '';
    await getOllamaResponse(conversation, true, (chunk) => {
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