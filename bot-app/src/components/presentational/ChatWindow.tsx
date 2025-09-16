import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import type { AppMessage } from '../../types/AppMessage';

interface ChatWindowProps {
  appMessages: AppMessage[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ appMessages }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [appMessages]);

  return (
    <div className="w-full overflow-y-auto" ref={containerRef} style={{ maxHeight: '100%' }}>
      {appMessages.map((appMessage, index) => (
        <ChatMessage key={index} persona={appMessage.persona} message={appMessage.message} />
      ))}
    </div>
  );
};

export default ChatWindow;