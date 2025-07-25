import React, { useState } from 'react';
import logo from '../assets/logo.png';
import { useNavigate } from 'react-router-dom';

function Navbar({onLogout}) {
  const [menuOpen, setMenuOpen] = useState(false);

  // Toggle menu visibility
  const handleMenuClick = () => setMenuOpen(!menuOpen);

  // Close menu when clicking an option
  const handleMenuOptionClick = () => setMenuOpen(false);

  const navigate = useNavigate();

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      width: '100%',
      background: '#000',
      color: '#fff',
      borderBottom: '1px solid #222',
      padding: '10px 0',
      zIndex: 1000,
      overflow: 'visible'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        maxWidth: '1200px', // Keeps content centered and away from edges
        margin: '0 auto',
        paddingLeft: '32px',
        paddingRight: '32px'
      }}>
        {/* Left: Logo and Title */}
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <img
            src={logo}
            alt="App Logo"
            style={{ height: '40px', marginRight: '16px' ,  cursor: 'pointer'}}
            onClick={() => navigate('/')}
          />
          <h2
            style={{ margin: 0, fontWeight: 'normal', letterSpacing: '2px',  cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            AI Essay App
          </h2>
        </div>
  
        {/* Right: Menu Icon */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={handleMenuClick}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '28px',
              cursor: 'pointer',
              outline: 'none',
              color: '#fff'
            }}
            aria-label="Menu"
          >
            &#9776; {/* Unicode for ☰ */}
          </button>
          {menuOpen && (
            <div style={{
              position: 'absolute',
              right: 0,
              top: '40px',
              background: '#222',
              color: '#fff',
              border: '1px solid #ddd',
              borderRadius: '6px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              minWidth: '120px',
              zIndex: 2000
            }}>
              <div
                onClick={() => { handleMenuOptionClick(); navigate('/profile'); }}
                style={{ padding: '10px 20px', cursor: 'pointer', borderBottom: '1px solid #eee' }}
              >
                Profile
              </div>
              <div
                onClick={handleMenuOptionClick}
                style={{ padding: '10px 20px', cursor: 'pointer', borderBottom: '1px solid #eee' }}
              >
                Settings
              </div>
              <div
                onClick={() => { handleMenuOptionClick(); onLogout(); }}
                style={{ padding: '10px 20px', cursor: 'pointer' }}
              >
                Log out
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
export default Navbar;