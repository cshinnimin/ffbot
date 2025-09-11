
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';
import { AppMessagesProvider } from '../../context/AppMessagesContext';
import { LlmMessagesProvider } from '../../context/LlmMessagesContext';

const MainContainer: React.FC = () => {
  return (
    <ViewPort>
      <AppMessagesProvider>
        <LlmMessagesProvider>
          <ChatContainer />
        </LlmMessagesProvider>
      </AppMessagesProvider>
    </ViewPort>
  );
};

export default MainContainer;