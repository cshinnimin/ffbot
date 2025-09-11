import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { LlmMessage, LlmRole } from '../types/LlmMessage';

interface LlmMessagesContextType {
  llmMessages: LlmMessage[];
  addLlmMessage: (role: LlmRole, llmMessage: string) => void;
}

const LlmMessageContext = createContext<LlmMessagesContextType | undefined>(undefined);

export const useLlmMessages = () => {
  const context = useContext(LlmMessageContext);
  if (!context) {
    throw new Error('useLlmMessages must be used within an LlmMessagesProvider');
  }
  return context;
};

export const LlmMessagesProvider = ({ children }: { children: ReactNode }) => {

  const [llmMessages, setLlmMessages] = useState<LlmMessage[]>([]);

  const addLlmMessage = (role: LlmRole, llmMessage: string) => {
    setLlmMessages(prevLlmMessages => prevLlmMessages.concat({
      role,
      content: llmMessage
    }));
  };

  return (
    <LlmMessageContext.Provider value={{ llmMessages, addLlmMessage }}>
      {children}
    </LlmMessageContext.Provider>
  );
};
