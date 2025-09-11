import React from 'react';

interface ChatMessageProps {
  persona: 'User' | 'Bot';
  message: string;
  // Add other props as needed, e.g. avatar, etc.
}

const ChatMessage: React.FC<ChatMessageProps> = ({ persona, message }) => {
  const chatClass = persona === 'User' ? 'chat chat-start' : 'chat chat-end';
  const headerText = persona === 'Bot' ? 'FFBot' : 'Adventurer';

  return (
    <div className={chatClass}>
        <div className="chat-image avatar">
            <div className="w-10 rounded-full">
                <img
                    alt="Final Fantasy Bot Avatar"
                    src="/images/ffbot-avatar.png"
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