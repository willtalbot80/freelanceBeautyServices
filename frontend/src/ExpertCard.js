import React from 'react'

export default function ExpertCard({ expert }) {
  const { user, location, services, portfolio_images } = expert
  const firstName = user.first_name || user.username
  const image = portfolio_images?.length > 0 ? portfolio_images[0].image : null

  return (
    <div className="card">
      {image && (
        <img
          src={image}
          alt={firstName}
          className="card-image"
        />
      )}
      <div className="card-title">{firstName}</div>
      <div className="card-meta">📍 {location || 'Location not specified'}</div>
      <p className="card-text">{services.substring(0, 80)}...</p>
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button className="btn btn-primary btn-small">View Profile</button>
        <button className="btn btn-outline btn-small">Book</button>
      </div>
    </div>
  )
}
