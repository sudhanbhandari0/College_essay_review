import React from 'react';

import GoogleLoginHandler from './GoogleLoginHandler';


function LoginModal({ open, onSuccess }) {
    if (!open) return null;

    return (
        <div style={{
            position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
            background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999
        }}>
            <div style={{
                background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, textAlign: 'center'
             }}>
                <h2>Welcome!</h2>
                <p>Please log in to continue</p>
                <GoogleLoginHandler onLoginSuccess={onSuccess} />
            </div>
        </div>
    );
}

export default LoginModal;