import React from 'react';

interface ChatMessageProps {
  persona: 'User' | 'Bot';
  message: string;
  // Add other props as needed, e.g. avatar, etc.
}

const ChatMessage: React.FC<ChatMessageProps> = ({ persona, message }) => {
  const chatClass = persona === 'User' ? 'chat chat-start' : 'chat chat-end';
  const headerText = persona === 'Bot' ? 'FFBot' : 'Adventurer';

  // Replace literal escaped sequences with actual characters so the
  // chat bubble shows newlines and tabs as intended.
  const formattedMessage = message
    .replace(/\\r\\n/g, '\r\n')
    .replace(/\\n/g, '\n')
    .replace(/\\t/g, '\t');
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
      <div className="chat-bubble whitespace-pre-wrap">{formattedMessage}</div>
    </div>
  );
};

export default ChatMessage;