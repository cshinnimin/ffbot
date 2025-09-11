
import React from 'react';
import ChatMessage from './ChatMessage';
import type { Message } from '../../types/Message';

interface ChatWindowProps {
  messages: Message[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  return (
    <div className="w-full">
      {messages.map((message, index) => (
        <ChatMessage key={index} persona={message.persona} message={message.message} />
      ))}
    </div>
  );
};

export default ChatWindow;