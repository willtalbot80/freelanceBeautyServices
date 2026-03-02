import React, { useEffect, useState } from 'react'
import Header from './Header'
import Hero from './Hero'
import ExpertCard from './ExpertCard'
import Login from './Login'
import { firebaseAuth } from './firebase'
import { onAuthStateChanged, signOut } from 'firebase/auth'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

export default function App() {
  const [experts, setExperts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [user, setUser] = useState(null)
  const [drfToken, setDrfToken] = useState(null)

  // Subscribe to Firebase auth changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(firebaseAuth, async (usr) => {
      setUser(usr)
      if (usr) {
        // User just signed in; exchange ID token for DRF token
        try {
          const idToken = await usr.getIdToken()
          const resp = await fetch('/api/exchange-firebase-token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_token: idToken })
          })
          if (resp.ok) {
            const data = await resp.json()
            setDrfToken(data.token)
            localStorage.setItem('drfToken', data.token)
          }
        } catch (err) {
          console.error('Failed to exchange token:', err)
        }
      } else {
        // User signed out
        setDrfToken(null)
        localStorage.removeItem('drfToken')
      }
    })
    return () => unsubscribe()
  }, [])

  // Load DRF token from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('drfToken')
    if (stored) setDrfToken(stored)
  }, [])

  // Fetch experts list
  useEffect(() => {
    const headers = drfToken ? { 'Authorization': `Token ${drfToken}` } : {}
    fetch('/api/experts/', { headers })
      .then(r => {
        if (!r.ok) throw new Error('Failed to fetch')
        return r.json()
      })
      .then(d => {
        setExperts(d.results || d)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [drfToken])

  const handleLogout = async () => {
    try {
      if (drfToken && user) {
        // Optionally revoke Firebase tokens on backend
        await fetch('/api/revoke-firebase-tokens/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${drfToken}`
          },
          body: JSON.stringify({ uid: user.uid })
        })
      }
    } catch (err) {
      console.error('Failed to revoke tokens:', err)
    }
    // Sign out from Firebase
    await signOut(firebaseAuth)
  }

  return (
    <Router>
      <Header user={user} onLogout={handleLogout} />
      <main className="container">
        <Hero />

        <div className="mt-2xl mb-lg">
          <h2 className="text-center mb-lg">Featured Beauty Experts</h2>

          {loading && (
            <div className="text-center mt-lg">
              <div className="loading"></div>
              <p className="text-muted mt-md">Loading experts...</p>
            </div>
          )}

          {error && (
            <div style={{
              background: '#FEE',
              border: '1px solid #F88',
              color: '#C33',
              padding: '1rem',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              Error loading experts: {error}
            </div>
          )}

          {experts.length === 0 && !loading && !error && (
            <p className="text-center text-muted">No experts available yet.</p>
          )}

          {experts.length > 0 && (
            <div className="grid grid-3">
              {experts.map(expert => (
                <ExpertCard key={expert.id} expert={expert} />
              ))}
            </div>
          )}
        </div>

        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
        </Routes>

        <div style={{
          textAlign: 'center',
          padding: '3rem 0',
          borderTop: '1px solid var(--border)',
          marginTop: '3rem'
        }}>
          <p className="text-muted">
            👩‍💄 Connecting clients with talented beauty professionals
          </p>
        </div>
      </main>
    </Router>
  )
}

