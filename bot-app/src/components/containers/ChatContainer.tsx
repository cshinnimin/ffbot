
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';
import { useLlm, convertAppMessageToLlmMessage } from '../../hooks/useLlm';


function ChatContainer() {
  // first import what we need from context/state
  const { appMessages, addAppMessage } = useAppMessages();

  // second, import what we need from hooks
  const { sendLlmMessage } = useLlm();

  // now define any behaviours we need
  const handleSend = async (message: string) => {
    // messages from ChatInput are always from the User
    const appMessage = { persona: 'User' as const, message };
    addAppMessage('User', message); // add message to appMessages in store

    const llmResponse = await sendLlmMessage(convertAppMessageToLlmMessage(appMessage));
    addAppMessage('Bot', llmResponse);
  };

  return (
    <ChatLayout>
      <ChatWindow appMessages={appMessages} />
      <ChatInput onSend={handleSend} />
    </ChatLayout>
  );
}

export default ChatContainer;