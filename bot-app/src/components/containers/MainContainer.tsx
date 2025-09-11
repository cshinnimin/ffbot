
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';
import { MessagesProvider } from '../../context/MessagesContext';

const MainContainer: React.FC = () => {
  return (
    <ViewPort>
      <MessagesProvider>
        <ChatContainer />
      </MessagesProvider>
    </ViewPort>
  );
};

export default MainContainer;