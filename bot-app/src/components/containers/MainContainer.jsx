import React, { Component } from 'react'

class MainContainer extends Component {
  state = {
    conversations: []
  }

  addConversation = () => {
    this.setState(prevState => ({
      conversations: prevState.conversations.concat('Foo')
    }))
  }

  render() {
    return (
      <div className="w-screen h-screen bg-base-900 flex items-center justify-center">
        <div className="rounded-lg bg-base-200 w-[90vw] h-[90vh] p-[5%] overflow-auto flex flex-col">
          <h1>FFBot</h1>
        </div>
      </div>
    )
  }
}

export default MainContainer;