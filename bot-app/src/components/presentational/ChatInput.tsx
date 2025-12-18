import React from 'react';
import { useLlmMessages } from '../../references/LlmMessagesRef';

interface ChatInputProps {
  onSend: (message: string) => void;
  onRestartLlm: () => void;
  inputSpinnerOn?: boolean;
  fullSpinnerOn?: boolean;
}


const ChatInput: React.FC<ChatInputProps> = ({ onSend, onRestartLlm, inputSpinnerOn, fullSpinnerOn }) => {
  // Local state for this presentational component to manage the input field
  const [input, setInput] = React.useState("");
  const { llmMessagesRef } = useLlmMessages();

  // disable the input if we are using a Chat Completion provider and we haven't
  // sent the training message yet (not relevant for Langchain provider since
  // training is done on every message by pulling ony relevant instructions
  // from the vector database in that case)
  const llmProvider = import.meta.env.LLM_PROVIDER;
  const disableInput = !llmProvider.includes('langchain') && llmMessagesRef.current.length == 0;

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
        disabled={inputSpinnerOn || disableInput}
        aria-disabled={inputSpinnerOn || disableInput}
        style={inputSpinnerOn || disableInput ? { cursor: 'default' } : undefined}
      />
      <div className="flex justify-end gap-2 items-center">
        {disableInput && !inputSpinnerOn && !fullSpinnerOn && (
          <span className="start-conversation-arrow" aria-hidden="true">➡️</span>
        )}
        <button
          className={`btn rounded-lg bg-gray-200 text-gray-800 border border-gray-300 hover:bg-gray-300
            ${inputSpinnerOn ? 'opacity-50 cursor-not-allowed' : ''}`}
          type="button"
          onClick={onRestartLlm}
          disabled={inputSpinnerOn}
          aria-disabled={inputSpinnerOn}
        >
          New Conversation
        </button>
        <button
          className="btn rounded-lg bg-[#0000FF] text-white hover:bg-blue-800 flex items-center justify-center min-w-[80px]"
          onClick={handleSend}
          disabled={inputSpinnerOn || disableInput}
          aria-disabled={inputSpinnerOn || disableInput}
        >
          {inputSpinnerOn ? (
            <span className="loading loading-spinner loading-sm"></span>
          ) : (
            <span>Send</span>
          )}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;