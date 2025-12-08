import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [healthStatus, setHealthStatus] = useState<string>('checking...')

  useEffect(() => {
    // Test health endpoint on mount
    fetch('/api/health')
      .then(res => res.json())
      .then(data => {
        setHealthStatus(data.status === 'healthy' ? '✅ Connected' : '❌ Error')
      })
      .catch(() => {
        setHealthStatus('❌ Backend not reachable')
      })
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🍳 Kitchen Simulator</h1>
        <p className="subtitle">willdinnergowell.com</p>
        <p className="status">Backend Status: {healthStatus}</p>
      </header>
      <main className="app-main">
        <p>Phase 1 - Project Foundation ✅</p>
        <p>Ready to build the kitchen simulator!</p>
      </main>
    </div>
  )
}

export default App

