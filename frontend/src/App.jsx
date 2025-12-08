import React from 'react'
import CustomerList from './components/CustomerList'
import RiskScore from './components/RiskScore'
import Analytics from './components/Analytics'

export default function App() {
  return (
    <div style={{ padding: 16, fontFamily: 'sans-serif' }}>
      <h1>Jumia Price Trend Dashboard</h1>
      <RiskScore />
      <Analytics />
      <CustomerList />
    </div>
  )
}
