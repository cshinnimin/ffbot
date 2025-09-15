/**
 * LlmMessagesRef.tsx
 * 
 * This is a React `Reference` to track the history of messages that have 
 * been exchanged with the LLM. Because it is a Reference, updates to it occur
 * within a render context, but updates to it do not trigger re-renders. This is
 * important because we want to keep an accurate history of messages, but we
 * don't want to trigger re-renders every time a message is added since some
 * messages to and from the LLM are intended to happen behind the scenes.
 */

import React, { createContext, useRef, useContext } from 'react';
import type { ReactNode } from 'react';
import type { LlmMessage, LlmRole } from '../types/LlmMessage';

interface LlmMessagesRefContextType {
  llmMessagesRef: React.RefObject<LlmMessage[]>;
  addLlmMessage: (role: LlmRole, llmMessage: string) => void;
  clearLlmMessages: () => void;
}

const LlmMessagesRefContext = createContext<LlmMessagesRefContextType | undefined>(undefined);

export const useLlmMessages = () => {
  const context = useContext(LlmMessagesRefContext);
  if (!context) {
    throw new Error('useLlmMessages must be used within an LlmMessagesProvider');
  }
  return context;
};

export const LlmMessagesProvider = ({ children }: { children: ReactNode }) => {
  const llmMessagesRef = useRef<LlmMessage[]>([]);

  const addLlmMessage = (role: LlmRole, llmMessage: string) => {
    llmMessagesRef.current.push({ role, content: llmMessage });
  };

  const clearLlmMessages = () => {
    llmMessagesRef.current = [];
  };

  return (
    <LlmMessagesRefContext.Provider value={{ llmMessagesRef, addLlmMessage, clearLlmMessages }}>
      {children}
    </LlmMessagesRefContext.Provider>
  );
};
