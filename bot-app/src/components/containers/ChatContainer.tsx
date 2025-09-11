import React from 'react';
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';
import { useLlm, convertAppMessageToLlmMessage } from '../../hooks/useLlm';
import { useLlmMessages } from '../../context/LlmMessagesContext';
import falconTrainingMessage from '../../assets/training/falcon_3b.md?raw';

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

  const handleRestartLlm = () => {
    
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