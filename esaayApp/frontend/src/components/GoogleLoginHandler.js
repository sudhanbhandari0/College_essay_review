import React from 'react';
import { GoogleLogin } from '@react-oauth/google';

function GoogleLoginHandler({ onLoginSuccess }) {
  const handleGoogleLogin = async (credentialResponse) => {
    const token = credentialResponse.credential;

    // Send the token to your backend
    try {
      const response = await fetch('http://localhost:8000/api/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      const data = await response.json();
      if (response.ok) {
        //console.log('JWT token from backend:', data.jwt_token);
        // Store JWT token for future API calls
        localStorage.setItem('jwt_token', data.jwt_token);
        onLoginSuccess(data); // Pass user/session info up to parent
      } else {
        alert('Login failed: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      alert('Could not connect to server');
    }
  };

  return (
    <GoogleLogin
      onSuccess={handleGoogleLogin}
      onError={() => alert('Login Failed')}
    />
  );
}

export default GoogleLoginHandler;