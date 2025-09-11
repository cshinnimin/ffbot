
import { Component } from 'react'
import ChatInput from '../presentational/ChatInput';
import ChatWindow from '../presentational/ChatWindow';
import ChatLayout from '../presentational/ChatLayout';
import type { Message } from '../../types/Message';

interface ChatContainerState {
  messages: Message[];
}

class ChatContainer extends Component<{}, ChatContainerState> {
  state: ChatContainerState = {
    messages: [
      {persona: 'User',
        message: 'Hello, this is a hardcoded message!'
      }
    ]
  }

  addMessage = () => {
    this.setState(prevState => ({
      messages: prevState.messages.concat({
        persona: 'User',
        message: 'Foo'
      })
    }))
  }

  render() {
    return (
      <ChatLayout>
        <ChatWindow messages={this.state.messages} />
        <ChatInput onSend={this.addMessage} />
      </ChatLayout>
    )
  }
}

export default ChatContainer;