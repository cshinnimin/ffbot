import { Component } from 'react'
import ChatContainer from './ChatContainer';
import ViewPort from '../presentational/ViewPort';

interface MainContainerState {
  conversations: string[];
}

class MainContainer extends Component<{}, MainContainerState> {
  state: MainContainerState = {
    conversations: []
  }

  addConversation = () => {
    this.setState(prevState => ({
      conversations: prevState.conversations.concat('Foo')
    }))
  }

  render() {
    return (
       <>
          <ViewPort>
            <ChatContainer />
          </ViewPort>
       </>
    )
  }
}

export default MainContainer;