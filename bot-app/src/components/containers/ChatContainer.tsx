
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';

function ChatContainer() {
  const { appMessages, addAppMessage } = useAppMessages();

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