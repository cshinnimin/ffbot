/**
 * AppMessagesContext.tsx
 * 
 * This is a React `Context` to track the history of messages that have been exchanged
 * between the user and the app. Because it is a Context, updates to it only occur
 * after a re-render, therefore data read from it could be stale if other functions
 * have made updates within the same render context. This is acceptable because
 * the messages in this context are used for display purposes in the chat window,
 * and we must have a re-render to show new messages when updated.
 */

import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { AppMessage, AppPersona } from '../types/AppMessage';

interface MessagesContextType {
  appMessages: AppMessage[];
  addAppMessage: (persona: AppPersona, message: string) => void;
  clearAppMessages: () => void;
}

const AppMessageContext = createContext<MessagesContextType | undefined>(undefined);

export const useAppMessages = () => {
  const context = useContext(AppMessageContext);
  if (!context) {
    throw new Error('useAppMessages must be used within an AppMessagesProvider');
  }
  return context;
};

export const AppMessagesProvider = ({ children }: { children: ReactNode }) => {
  const [appMessages, setAppMessages] = useState<AppMessage[]>([]);

  const addAppMessage = (persona: AppPersona, message: string) => {
    setAppMessages(prevAppMessages => prevAppMessages.concat({
      persona,
      message
    }));
  };

  const clearAppMessages = () => {
    setAppMessages([]);
  };

  return (
    <AppMessageContext.Provider value={{ appMessages, addAppMessage, clearAppMessages }}>
      {children}
    </AppMessageContext.Provider>
  );
};
