import React from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  // Local state for this presentational component to manage the input field
  const [input, setInput] = React.useState("");

  const handleSend = () => {
    if (input.trim() !== "") {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="flex flex-col h-full justify-end">
      <textarea
        className="textarea textarea-bordered rounded-lg mb-2 w-full resize-none"
        placeholder="Type your message..."
        rows={3}
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
          }
        }}
      />
      <div className="flex justify-end">
        <button
          className="btn btn-primary rounded-lg"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInput;