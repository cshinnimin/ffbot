
import { useState } from 'react'
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import type { Message } from '../../types/Message';


function ChatContainer() {
  // Define state at the top of the function component
  // State to hold the list of chat messages
  const [messages, setMessages] = useState<Message[]>([
    {
      persona: 'User',
      message: 'Hello, this is a hardcoded message!'
    }
  ]);

  // Next come the handlers which represent actions that can be taken
  // Handler to add a new message to the chat
  const addMessage = (userMessage: string) => {
    setMessages(prevMessages => prevMessages.concat(
      {
        persona: 'User',
        message: userMessage
      }
    ));
  };

  // Render the chat layout, window, and input components
  return (
    <ChatLayout>
      <ChatWindow messages={messages} />
  <ChatInput onSend={addMessage} />
    </ChatLayout>
  );
}

export default ChatContainer;