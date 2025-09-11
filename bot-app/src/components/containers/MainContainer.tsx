
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';
import { AppMessagesProvider } from '../../context/MessagesContext';

const MainContainer: React.FC = () => {
  return (
    <ViewPort>
      <AppMessagesProvider>
        <ChatContainer />
      </AppMessagesProvider>
    </ViewPort>
  );
};

export default MainContainer;