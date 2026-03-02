import React from 'react'
import { Link } from 'react-router-dom'

export default function Header({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">✨ Freelance Beauty</Link>
        <ul className="nav-links">
          <li><a href="/">Browse Experts</a></li>
          <li><a href="#book">Book Now</a></li>
          <li><a href="#contact">Contact</a></li>
          {user ? (
            <>
              <li><span style={{ color: 'var(--gold)' }}>{user.email}</span></li>
              <li><a href="#" onClick={(e) => { e.preventDefault(); onLogout(); }}>Logout</a></li>
            </>
          ) : (
            <li><a href="/login">Login</a></li>
          )}
        </ul>
      </div>
    </nav>
  )
}
