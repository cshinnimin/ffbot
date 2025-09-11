import React from 'react';

interface ChatLayoutProps {
  children: React.ReactNode;
}

const ChatLayout: React.FC<ChatLayoutProps> = ({ children }) => {
  // Expecting children: [ChatWindow, ChatInput]
  const [chatWindow, chatInput] = React.Children.toArray(children);
  return (
    <div className="flex flex-col h-full min-h-0 w-full">
        <div className="flex-1 min-h-0 mb-2 rounded-lg border border-gray-300 bg-base-100 w-full flex flex-col p-4">
            <div className="flex-1 min-h-0 overflow-y-auto">
            {chatWindow}
            </div>
        </div>
        <div className="shrink-0 mt-4">
            {chatInput}
        </div>
    </div>
  );
};

export default ChatLayout;
