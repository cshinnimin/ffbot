import React, { Component } from 'react'
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
            
          </ViewPort>
       </>
    )
  }
}

export default MainContainer;