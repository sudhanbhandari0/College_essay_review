import React from 'react';

function Profile({ user }) {
  if (!user) {
    return <div style={{ padding: 32 }}>No user info available.</div>;
  }

  return (
    <div style={{ padding: 32 }}>
      <h2>Profile</h2>
      <img src={user.picture} alt="Profile" style={{ width: 80, borderRadius: '50%' }} />
      <p><strong>Name:</strong> {user.name || 'N/A'}</p>
      <p><strong>Email:</strong> {user.email}</p>
    </div>
  );
}

export default Profile;