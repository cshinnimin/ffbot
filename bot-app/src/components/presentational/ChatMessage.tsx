import React from 'react';

interface ChatMessageProps {
  persona: 'User' | 'Bot';
  message: string;
  // Add other props as needed, e.g. avatar, etc.
}

const ChatMessage: React.FC<ChatMessageProps> = ({ persona, message }) => {
  const chatClass = persona === 'User' ? 'chat chat-start' : 'chat chat-end';
  const headerText = persona === 'Bot' ? 'FFBot' : 'Adventurer';

  // Replace literal "\\n" sequences in the message with actual newlines and render
  // with `white-space: pre-wrap` so newlines are preserved in the UI.
  const formattedMessage = message.replace(/\\n/g, '\n');
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