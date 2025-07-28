import React, { useState } from 'react';

function EssayForm() {
    const [essay, setEssay] = useState('');
    const [feedback, setFeedback] = useState('');
    const [loading, setLoading] = useState(false);
    const token = localStorage.getItem('jwt_token');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
          const response = await fetch('http://localhost:8000/api/analyze-essay', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
              content: essay,
              author: 'Anonymous'
            })
          });
          
          const data = await response.json();
          setFeedback(data.feedback);
        } catch (error) {
          setFeedback('Error: Could not connect to server');
        } finally {
          setLoading(false);
        }
      };

      return (
        <form onSubmit={handleSubmit}>
          <textarea
            value={essay}
            onChange={(e) => setEssay(e.target.value)}
            placeholder="Paste your essay here..."
            rows="10"
            cols="50"
          />
          <br />
          <button type="submit" disabled={loading}>
            {loading ? 'Processing...' : 'Get Feedback'}
          </button>
          {feedback && (
          <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
            <h3>Feedback:</h3>
            <p>{feedback}</p>
          </div>
        )}
        </form>
      ); 
}

export default EssayForm;
