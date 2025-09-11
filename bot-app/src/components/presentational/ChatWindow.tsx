import React from 'react';
import ChatMessage from './ChatMessage';
import type { AppMessage } from '../../types/AppMessage';

interface ChatWindowProps {
  appMessages: AppMessage[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ appMessages }) => {
  return (
    <div className="w-full">
      {appMessages.map((appMessage, index) => (
        <ChatMessage key={index} persona={appMessage.persona} message={appMessage.message} />
      ))}
    </div>
  );
};

export default ChatWindow;