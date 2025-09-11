
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';

function ChatContainer() {
  // first set up what we need from context/state
  const { appMessages, addAppMessage } = useAppMessages();

  // now define any behaviours we need
  const handleSend = (message: string) => {
    // messages from ChatInput are always from the User
    addAppMessage('User', message);
  };

  return (
    <ChatLayout>
      <ChatWindow appMessages={appMessages} />
      <ChatInput onSend={handleSend} />
    </ChatLayout>
  );
}

export default ChatContainer;