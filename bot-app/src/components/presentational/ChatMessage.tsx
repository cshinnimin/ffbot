import React from 'react';

interface ChatMessageProps {
  persona: 'User' | 'Bot';
  message: string;
  // Add other props as needed, e.g. avatar, etc.
}

const ChatMessage: React.FC<ChatMessageProps> = ({ persona, message }) => {
  const chatClass = persona === 'User' ? 'chat chat-start' : 'chat chat-end';
  const headerText = persona === 'Bot' ? 'FFBot' : 'Adventurer';

  const avatarSrc = persona === 'User' ? '/images/user-avatar.png' : '/images/ffbot-avatar.png';
  return (
    <div className={chatClass}>
      <div className="chat-image avatar">
        <div className="w-10 rounded-full">
          <img
            alt={persona === 'User' ? 'Adventurer Avatar' : 'Final Fantasy Bot Avatar'}
            src={avatarSrc}
          />
        </div>
      </div>
      <div className="chat-header">
        {headerText}
      </div>
      <div className="chat-bubble">{message}</div>
    </div>
  );
};

export default ChatMessage;