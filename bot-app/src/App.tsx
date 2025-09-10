import { useState } from 'react'
import './App.css'
import MainContainer from './components/containers/MainContainer.tsx';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <MainContainer />
      </div>
    </>
  )
}

export default App
