
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import { useMessages } from '../../context/MessagesContext';

function ChatContainer() {
  const { messages, addMessage } = useMessages();

  return (
    <ChatLayout>
      <ChatWindow messages={messages} />
      <ChatInput onSend={addMessage} />
    </ChatLayout>
  );
}

export default ChatContainer;