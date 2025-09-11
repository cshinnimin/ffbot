
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useAppMessages } from '../../context/AppMessagesContext';

function ChatContainer() {
  const { appMessages, addAppMessage } = useAppMessages();

  return (
    <ChatLayout>
      <ChatWindow appMessages={appMessages} />
      <ChatInput onSend={addAppMessage} />
    </ChatLayout>
  );
}

export default ChatContainer;