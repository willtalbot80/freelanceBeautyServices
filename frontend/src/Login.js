import React, { useState } from 'react'
import { firebaseAuth } from './firebase'
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isRegister, setIsRegister] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      if (isRegister) {
        await createUserWithEmailAndPassword(firebaseAuth, email, password)
      } else {
        await signInWithEmailAndPassword(firebaseAuth, email, password)
      }
      // Redirect to home page after successful login
      navigate('/')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>{isRegister ? 'Register' : 'Login'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button className="btn btn-primary" type="submit">
          {isRegister ? 'Sign up' : 'Sign in'}
        </button>
      </form>
      <p style={{ marginTop: '1rem' }}>
        {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
        <a href="#" onClick={(e) => { e.preventDefault(); setIsRegister(!isRegister); }}>
          {isRegister ? 'Log in' : 'Register'}
        </a>
      </p>
    </div>
  )
}

