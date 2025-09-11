import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { AppMessage, AppPersona } from '../types/AppMessage';

interface MessagesContextType {
  appMessages: AppMessage[];
  addAppMessage: (persona: AppPersona, message: string) => void;
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
  const [appMessages, setAppMessages] = useState<AppMessage[]>([
    {
      persona: 'User',
      message: 'Hello, this is a hardcoded message!'
    }
  ]);

  const addAppMessage = (persona: AppPersona, message: string) => {
    setAppMessages(prevAppMessages => prevAppMessages.concat({
      persona,
      message
    }));
  };

  return (
    <AppMessageContext.Provider value={{ appMessages, addAppMessage }}>
      {children}
    </AppMessageContext.Provider>
  );
};
