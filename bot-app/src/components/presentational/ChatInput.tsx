import React from 'react';

interface ChatInputProps {
  onSend: () => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  return (
    <div className="flex flex-col h-full justify-end">
      <textarea
        className="textarea textarea-bordered rounded-lg mb-2 w-full resize-none"
        placeholder="Type your message..."
        rows={3}
      />
      <div className="flex justify-end">
        <button
          className="btn btn-primary rounded-lg"
          onClick={onSend}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInput;