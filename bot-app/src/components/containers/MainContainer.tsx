import { useState } from 'react';
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';

const MainContainer: React.FC = () => {
  // Define state at the top of the function component
  // State to hold the list of chat messages
  const [messages, setMessages] = useState<Message[]>([
    {
      persona: 'User',
      message: 'Hello, this is a hardcoded message!'
    }
  ]);

  // Next come the handlers which represent actions that can be taken
  // Handler to add a new message to the chat
  const addMessage = (userMessage: string) => {
    setMessages(prevMessages => prevMessages.concat(
      {
        persona: 'User',
        message: userMessage
      }
    ));
  };

  return (
    <>
      <ViewPort>
        <ChatContainer />
      </ViewPort>
    </>
  );
};

export default MainContainer;