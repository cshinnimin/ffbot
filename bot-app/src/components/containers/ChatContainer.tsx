import React from 'react';
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';
import { useLlm, convertAppMessageToLlmMessage } from '../../hooks/useLlm';
import { useLlmMessages } from '../../references/LlmMessagesRef';
import falconTrainingMessage from '../../assets/symlinks/training/falcon_3b.md?raw';

function ChatContainer() {
  // first import what we need from context/state
  const { appMessages, addAppMessage } = useAppMessages();
  // second, import what we need from hooks
  const { sendLlmMessage } = useLlm();

  // Spinner state
  const [spinnerOn, setFullSpinner] = React.useState(false);
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
  const handleRestartLlm = async () => {
    setFullSpinner(true);

    try {
      clearLlmMessages();

      const startTime = Date.now();
      const llmResponse = await sendLlmMessage({ role: 'user', content: falconTrainingMessage });
      const endTime = Date.now();

      const elapsedMs = endTime - startTime;
      const minutes = Math.floor(elapsedMs / 60000);
      const seconds = Math.floor((elapsedMs % 60000) / 1000);
      let timeString = '';
      if (minutes > 0 || seconds > 0) {
        timeString = ` Training took ${minutes > 0 ? minutes + ' minute' + (minutes !== 1 ? 's' : '') + ' and ' : ''}${seconds} second${seconds !== 1 ? 's' : ''}.`;
      }

      addAppMessage('Bot', llmResponse + timeString);
    } finally {
      setFullSpinner(false);
    }
  };

  return (
    <ChatLayout spinnerOn={spinnerOn}>
      <ChatWindow appMessages={appMessages} />
      <ChatInput
        onSend={handleSend}
        onRestartLlm={handleRestartLlm}
        inputSpinnerOn={inputSpinnerOn}
      />
    </ChatLayout>
  );
}

export default ChatContainer;