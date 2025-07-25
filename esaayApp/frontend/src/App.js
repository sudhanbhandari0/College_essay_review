import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import EssayForm from './components/EssayForm';
import FileUpload from './components/FileUpload';
import Navbar from './components/Navbar';
import { GoogleOAuthProvider } from '@react-oauth/google';
import LoginModal from './components/LoginModal';
import Profile from './components/Profile';

function App() {
  const [loggedIn, setLoggedIn] = React.useState(false);
  const [user, setUser] = useState(null);
  const handleLoginSuccess = (data) => {
    setLoggedIn(true);
    setUser(data);
    localStorage.setItem('user', JSON.stringify(data));
    localStorage.setItem('loggedIn', 'true');
  };
  const handleLogout = () => {
    setLoggedIn(false);
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('loggedIn');
  };
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const savedLoggedIn = localStorage.getItem('loggedIn');
    if (savedUser && savedLoggedIn === 'true') {
      setUser(JSON.parse(savedUser));
      setLoggedIn(true);
    }
  }, []);
  return (
    <GoogleOAuthProvider clientId="6719042499-jglnu24jorj4qlpgc11dlb1uv6utqvkl.apps.googleusercontent.com">
      <Router>
        <LoginModal open={!loggedIn} onSuccess={handleLoginSuccess} />
        {loggedIn && (
          <div className="App">
            <Navbar onLogout={handleLogout}/>
            <Routes>
              <Route path="/" element={
                <>
                  {user && (
                    <div style={{ margin: '20px', textAlign: 'right' }}>
                      <img src={user.picture} alt="Profile" style={{ width: 40, borderRadius: '50%', marginRight: 8 }} />
                      <span>Welcome, {user.name || user.email}!</span>
                    </div>
                  )}
                  <header className="App-header" style={{ marginTop: '60px', color: '#000' }} >
                    <h1 style={{color: '#4fc3f7' }}>AI Essay Feedback</h1>
                    <EssayForm />
                    <FileUpload />
                  </header>
                </>
              } />
              <Route path="/profile" element={<Profile user={user} />} />
            </Routes>
          </div>
        )}
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;