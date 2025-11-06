import React from 'react';
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';
import { useLlm, convertAppMessageToLlmMessage } from '../../hooks/useLlm';
import { useLlmMessages } from '../../references/LlmMessagesRef';
import trainingMessage from '../../assets/symlinks/training/chat-completion/initial-instructions.md?raw';

function ChatContainer() {
  // first import what we need from context/state
  const { appMessages, addAppMessage, clearAppMessages } = useAppMessages();
  
  // second, import what we need from hooks
  const { sendLlmMessage } = useLlm();

  // Spinner state
  const [fullSpinnerOn, setFullSpinner] = React.useState(false);
  const [inputSpinnerOn, setInputSpinner] = React.useState(false);

  // now define any behaviours we need
  const handleSend = async (message: string) => {
    setInputSpinner(true);

    try {
      // messages from ChatInput are always from the User
      const appMessage = { persona: 'User' as const, message };
      addAppMessage('User', message); // add message to appMessages in store

      const llmResponse = await sendLlmMessage(convertAppMessageToLlmMessage(appMessage));
      addAppMessage('Bot', llmResponse);
    } finally {
      setInputSpinner(false);
    }
  };

  const { clearLlmMessages } = useLlmMessages();
  const handleNewConversation = async () => {
    setFullSpinner(true);

    try {
      clearLlmMessages();
      clearAppMessages();

      const charNames = await getCharacterNames();
      const finalTrainingMessage = trainingMessage
        .replaceAll('<character_1>', charNames.character1)
        .replaceAll('<character_2>', charNames.character2)
        .replaceAll('<character_3>', charNames.character3)
        .replaceAll('<character_4>', charNames.character4);

      const startTime = Date.now();
      const llmResponse = await sendLlmMessage({ role: 'user', content: finalTrainingMessage });
      const endTime = Date.now();

      const elapsedMs = endTime - startTime;
      const minutes = Math.floor(elapsedMs / 60000);
      const seconds = Math.floor((elapsedMs % 60000) / 1000);

      let timeString = '';
      if (minutes > 0 || seconds > 0) {
        timeString = ` Training took ${minutes > 0 ? minutes + ' minute' + (minutes !== 1 ? 's' : '') + ' and ' : ''}${seconds} second${seconds !== 1 ? 's' : ''}.`;
      }

      debugger;
      addAppMessage('Bot', llmResponse + timeString);
    } finally {
      setFullSpinner(false);
    }
  };

  return (
    <ChatLayout spinnerOn={fullSpinnerOn}>
      <ChatWindow appMessages={appMessages} />
      <ChatInput
        onSend={handleSend}
        onRestartLlm={handleNewConversation}
        inputSpinnerOn={inputSpinnerOn}
        fullSpinnerOn={fullSpinnerOn}
      />
    </ChatLayout>
  );
}

/**
 * Private function to look up and add character names to training. The LLMs seem to 
 * be very poor at the reasoning task required to look up character names and associate
 * those names to the character numbers in the training data.
 * 
 * This text will be appended to Section 5: Hints in the training message.
 */
import { getRamValuesMap } from '../../api/nesApi';

async function getCharacterNames() {
  const ramValuesMap = await getRamValuesMap([
    "0x006102", "0x006103", "0x006104", "0x006105",
    "0x006142", "0x006143", "0x006144", "0x006145",
    "0x006182", "0x006183", "0x006184", "0x006185",
    "0x0061C2", "0x0061C3", "0x0061C4", "0x0061C5",
  ]);

  const char1Name = ramValuesMap["0x006102"] + ramValuesMap["0x006103"] +
    ramValuesMap["0x006104"] + ramValuesMap["0x006105"];
  const char2Name = ramValuesMap["0x006142"] + ramValuesMap["0x006143"] +
    ramValuesMap["0x006144"] + ramValuesMap["0x006145"];
  const char3Name = ramValuesMap["0x006182"] + ramValuesMap["0x006183"] +
    ramValuesMap["0x006184"] + ramValuesMap["0x006185"];
  const char4Name = ramValuesMap["0x0061C2"] + ramValuesMap["0x0061C3"] +
    ramValuesMap["0x0061C4"] + ramValuesMap["0x0061C5"];
  
  return {
    character1: char1Name,
    character2: char2Name,
    character3: char3Name,
    character4: char4Name
  }
}

export default ChatContainer;