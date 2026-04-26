
import axios from 'axios'
import { useState, useEffect, useCallback } from 'react'

function Search() {
    const [url, setUrl] = useState('')
    const [results, setResults] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [searched, setSearched] = useState(false)

    const handleSearch = useCallback(async (searchUrl = url) => {
        if (!searchUrl){
            console.log('handleSearch called with:', searchUrl)
            return} 
        setLoading(true)
        setError(null)
        setResults([])
        setSearched(false)
        console.log('about to make API call')
        try {
            console.log('making request to:', `${process.env.REACT_APP_API_URL}/search`)
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/search`, {
                image_url: searchUrl
            })
            console.log('response:', response.data)
            setResults(response.data.results)
            setSearched(true)
        } catch (err) {
            console.log('error:', err)
            setError('Something went wrong. Make sure the URL is a valid Pinterest pin or image URL.')
        } finally {
            setLoading(false)
        }
    }, [url])

    useEffect(() => {
        const params = new URLSearchParams(window.location.search)
        const sharedUrl = params.get('url') || params.get('text')
        if (sharedUrl) {
            setUrl(sharedUrl)
            handleSearch(sharedUrl)
        }
    }, [handleSearch])

    return (
        <div style={{ maxWidth: '960px', margin: '0 auto', padding: '40px 24px' }}>
            <h1 style={{ fontSize: '28px', marginBottom: '8px' }}>Find it secondhand</h1>
            <p style={{ color: '#666', marginBottom: '32px' }}>
                Paste a Pinterest pin URL to find similar items on secondhand platforms
            </p>

            <div style={{ display: 'flex', gap: '12px', marginBottom: '40px' }}>
                <input
                    type="text"
                    placeholder="Paste a Pinterest pin URL..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    style={{ flex: 1, padding: '12px 16px', border: '1px solid #ddd', borderRadius: '8px', fontSize: '14px' }}
                />
                <button
                    onClick={() => handleSearch()}
                    disabled={loading}
                    style={{ padding: '12px 24px', background: '#000', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' }}
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </div>

            {error && <p style={{ color: 'red', marginBottom: '24px' }}>{error}</p>}

            {searched && results.length === 0 && (
                <p style={{ color: '#666' }}>No similar items found. Try a different pin!</p>
            )}

            {results.length > 0 && (
                <>
                    <p style={{ color: '#666', marginBottom: '24px', fontSize: '14px' }}>
                        {results.length} similar {results.length === 1 ? 'item' : 'items'} found
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '24px' }}>
                        {results.map((item) => (
                            <div
                                key={item.id}
                                style={{
                                    border: '1px solid #eee',
                                    borderRadius: '12px',
                                    overflow: 'hidden',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    height: '100%',
                                }}
                            >
                                <img
                                    src={item.image_url}
                                    alt={item.title}
                                    style={{ width: '100%', height: '250px', objectFit: 'cover', flexShrink: 0 }}
                                />
                                <div
                                    style={{
                                        padding: '16px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        flex: 1,
                                        minHeight: 0,
                                    }}
                                >
                                    <p style={{ fontSize: '13px', color: '#666', marginBottom: '4px' }}>{item.platform}</p>
                                    <div
                                        style={{
                                            flex: 1,
                                            minHeight: 0,
                                            display: 'flex',
                                            flexDirection: 'column',
                                            marginBottom: '8px',
                                        }}
                                    >
                                        <p style={{ fontSize: '15px', fontWeight: '500', margin: 0 }}>{item.title}</p>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                        <p style={{ fontSize: '16px', fontWeight: 'bold', margin: 0 }}>${item.price}</p>
                                        <p style={{ fontSize: '12px', color: '#999', margin: 0 }}>{Math.round(item.similarity * 100)}% match</p>
                                    </div>
                                    <a
                                        href={item.link}
                                        target="_blank"
                                        rel="noreferrer"
                                        style={{
                                            display: 'block',
                                            textAlign: 'center',
                                            padding: '10px',
                                            background: '#000',
                                            color: '#fff',
                                            borderRadius: '8px',
                                            textDecoration: 'none',
                                            fontSize: '14px',
                                        }}
                                    >
                                        View Listing
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    )
}

export default Search