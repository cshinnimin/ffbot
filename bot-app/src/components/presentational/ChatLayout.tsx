import React from 'react';


interface ChatLayoutProps {
  children: React.ReactNode;
  spinnerOn?: boolean;
}

const ChatLayout: React.FC<ChatLayoutProps> = ({ children, spinnerOn }) => {
  // Expecting children: [ChatWindow, ChatInput]
  const [chatWindow, chatInput] = React.Children.toArray(children);
  return (
    <div className="flex flex-col h-full min-h-0 w-full relative">
      <div className="flex-1 min-h-0 mb-2 rounded-lg border border-gray-300 bg-base-100 w-full flex flex-col p-4 relative">
        {spinnerOn && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-base-100 bg-opacity-60 pointer-events-none">
            <span className="loading loading-spinner loading-xl"></span>
          </div>
        )}
        <div className={`flex-1 min-h-0 overflow-y-auto transition duration-200 ${spinnerOn ? 'opacity-50 grayscale pointer-events-none' : ''}`}>
          {chatWindow}
        </div>
      </div>
      <div className="shrink-0 mt-4 relative">
        <div className={`transition duration-200 ${spinnerOn ? 'opacity-50 grayscale pointer-events-none' : ''}`}>{chatInput}</div>
      </div>
    </div>
  );
};

export default ChatLayout;
