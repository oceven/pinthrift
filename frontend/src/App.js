import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Search from './pages/Search'
import Sell from './pages/Sell'

function App() {
  return (
    <Router>
      <nav style={{ padding: '16px 32px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ fontWeight: 'bold', fontSize: '20px', textDecoration: 'none', color: '#000' }}>
          PinThrift
        </Link>
        <Link to="/sell" style={{ textDecoration: 'none', color: '#000', fontSize: '14px' }}>
          Sell an item
        </Link>
      </nav>
      <Routes>
        <Route path="/" element={<Search />} />
        <Route path="/sell" element={<Sell />} />
      </Routes>
    </Router>
  )
}

export default App