import { useState } from 'react'
import axios from 'axios'

function Search() {
  const [url, setUrl] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    if (!url) return
    setLoading(true)
    setError(null)
    setResults([])
    try {
      const response = await axios.post('http://127.0.0.1:8000/search', {
        image_url: url
      })
      setResults(response.data.results)
    } catch (err) {
      setError('Something went wrong. Make sure the URL is a direct image link.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px 24px' }}>
      <h1 style={{ fontSize: '28px', marginBottom: '8px' }}>Find it secondhand</h1>
      <p style={{ color: '#666', marginBottom: '32px' }}>
        Paste a Pinterest image URL to find similar items on secondhand platforms
      </p>
      <div style={{ display: 'flex', gap: '12px', marginBottom: '40px' }}>
        <input
          type="text"
          placeholder="Paste a Pinterest image URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ flex: 1, padding: '12px 16px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px' }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{ padding: '12px 24px', background: '#000', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      {error && (
        <p style={{ color: 'red', marginBottom: '24px' }}>{error}</p>
      )}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '24px' }}>
        {results.map((item) => (
          <div key={item.id} style={{ border: '1px solid #eee', borderRadius: '12px', overflow: 'hidden' }}>
            <img
              src={item.image_url}
              alt={item.title}
              style={{ width: '100%', height: '250px', objectFit: 'cover' }}
            />
            <div style={{ padding: '16px' }}>
              <p style={{ fontSize: '13px', color: '#666', marginBottom: '4px' }}>{item.platform}</p>
              <p style={{ fontSize: '15px', fontWeight: '500', marginBottom: '8px' }}>{item.title}</p>
              <p style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '12px' }}>${item.price}</p>
              <a
                href={item.link}
                target="_blank"
                rel="noreferrer"
                style={{ display: 'block', textAlign: 'center', padding: '10px', background: '#000', color: '#fff', borderRadius: '8px', textDecoration: 'none', fontSize: '14px' }}
              >
                View Listing
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Search