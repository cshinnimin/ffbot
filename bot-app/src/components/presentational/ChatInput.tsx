import React from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  onRestartLlm: () => void;
  inputSpinnerOn?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend, onRestartLlm, inputSpinnerOn }) => {
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
        disabled={inputSpinnerOn}
        aria-disabled={inputSpinnerOn}
        style={inputSpinnerOn ? { cursor: 'default' } : undefined}
      />
      <div className="flex justify-end gap-2">
        <button
          className="btn rounded-lg bg-gray-200 text-gray-800 border border-gray-300 hover:bg-gray-300"
          type="button"
          onClick={onRestartLlm}
          disabled={inputSpinnerOn}
          aria-disabled={inputSpinnerOn}
        >
          Restart LLM
        </button>
        <button
          className="btn rounded-lg bg-[#0000FF] text-white hover:bg-blue-800 flex items-center justify-center min-w-[64px]"
          onClick={handleSend}
          disabled={inputSpinnerOn}
          aria-disabled={inputSpinnerOn}
        >
          {inputSpinnerOn ? <span className="loading loading-spinner loading-sm"></span> : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;