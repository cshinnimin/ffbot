
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';
import { AppMessagesProvider } from '../../context/AppMessagesContext';
import { LlmMessagesProvider } from '../../references/LlmMessagesRef';

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