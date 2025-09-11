import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { Message } from '../types/Message';

interface MessagesContextType {
  messages: Message[];
  addMessage: (userMessage: string) => void;
}

const MessagesContext = createContext<MessagesContextType | undefined>(undefined);

export const useMessages = () => {
  const context = useContext(MessagesContext);
  if (!context) {
    throw new Error('useMessages must be used within a MessagesProvider');
  }
  return context;
};

export const MessagesProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      persona: 'User',
      message: 'Hello, this is a hardcoded message!'
    }
  ]);

  const addMessage = (userMessage: string) => {
    setMessages(prevMessages => prevMessages.concat({
      persona: 'User',
      message: userMessage
    }));
  };

  return (
    <MessagesContext.Provider value={{ messages, addMessage }}>
      {children}
    </MessagesContext.Provider>
  );
};
