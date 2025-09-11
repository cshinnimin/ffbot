import React, { Component } from 'react'
import ViewPort from '../presentational/ViewPort';
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';

interface ChatContainerState {
  conversations: string[];
}

class ChatContainer extends Component<{}, ChatContainerState> {
  state: ChatContainerState = {
    conversations: []
  }

  addConversation = () => {
    this.setState(prevState => ({
      conversations: prevState.conversations.concat('Foo')
    }))
  }

  render() {
    return (
      <ChatLayout>
        <ChatWindow />
        <ChatInput onSend={this.addConversation} />
      </ChatLayout>
    )
  }
}

export default ChatContainer;