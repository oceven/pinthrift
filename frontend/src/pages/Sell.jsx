import { useState } from 'react'
import axios from 'axios'

function Sell() {
  const [url, setUrl] = useState('')
  const [platform, setPlatform] = useState('Poshmark')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    if (!url) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/listings`, {
        listing_url: url,
        platform: platform
      })
      if (response.data.error) {
        setError(response.data.error)
      } else {
        setResult(response.data.listing)
        setUrl('')
      }
    } catch (err) {
      setError('Something went wrong. Make sure the URL is a valid listing.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '40px 24px' }}>
      <h1 style={{ fontSize: '28px', marginBottom: '8px' }}>Sell an item</h1>
      <p style={{ color: '#666', marginBottom: '32px' }}>
        Submit your listing and make it discoverable to Pinterest shoppers
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div>
          <label style={{ fontSize: '14px', fontWeight: '500', display: 'block', marginBottom: '8px' }}>
            Listing URL
          </label>
          <input
            type="text"
            placeholder="https://poshmark.ca/listing/..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ width: '100%', padding: '12px 16px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px', boxSizing: 'border-box' }}
          />
        </div>

        <div>
          <label style={{ fontSize: '14px', fontWeight: '500', display: 'block', marginBottom: '8px' }}>
            Platform
          </label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            style={{ width: '100%', padding: '12px 16px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px', background: '#fff' }}
          >
            <option>Poshmark</option>
            <option>Vinted</option>
          </select>
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{ padding: '14px', background: '#000', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '15px', fontWeight: '500' }}
        >
          {loading ? 'Submitting...' : 'Submit listing'}
        </button>
      </div>

      {error && (
        <p style={{ color: 'red', marginTop: '24px' }}>{error}</p>
      )}

      {result && (
        <div style={{ marginTop: '32px', padding: '20px', border: '1px solid #eee', borderRadius: '12px' }}>
          <p style={{ color: 'green', fontWeight: '500', marginBottom: '16px' }}>✓ Listing added successfully!</p>
          <img
            src={result.image_url}
            alt={result.title}
            style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '8px', marginBottom: '12px' }}
          />
          <p style={{ fontWeight: '500' }}>{result.title}</p>
          <p style={{ color: '#666', fontSize: '14px' }}>${result.price} · {result.platform}</p>
        </div>
      )}
    </div>
  )
}

export default Sell