import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import QueryInput from './components/QueryInput';
import ResultTabs from './components/ResultTabs';
import EmergencyAlert from './components/EmergencyAlert';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (query, location) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/query', {
        query,
        location
      }, {
        timeout: 120000 // 2 minutes timeout
      });

      setResult(response.data);
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timed out. The backend is still processing. Please try again.');
      } else if (err.response) {
        setError(`Server error: ${err.response.data.detail || err.message}`);
      } else if (err.request) {
        setError('Cannot connect to backend. Make sure the FastAPI server is running on port 8000.');
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>⚖️ OBJECTION.ai</h1>
        <p className="subtitle">Your Constitutional Copilot for Legal Rights</p>
      </header>

      <div className="container">
        <QueryInput onSubmit={handleSubmit} loading={loading} />

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>⚖️ Analyzing your situation... This may take 30-60 seconds...</p>
          </div>
        )}

        {error && (
          <div className="error-alert">
            <strong>❌ Error:</strong> {error}
            <br />
            <small>💡 Make sure the backend server is running: <code>python backend/main.py</code></small>
          </div>
        )}

        {result && !loading && (
          <>
            <EmergencyAlert triage={result.triage} query={result.query} />
            <ResultTabs result={result} />
            <div className="success-message">
              ✅ Analysis complete! Review all tabs for comprehensive guidance.
            </div>
          </>
        )}
      </div>

      <footer className="app-footer">
        ⚠️ <strong>Disclaimer:</strong> This is legal information, not legal advice. 
        For serious legal matters, consult a licensed attorney.
      </footer>
    </div>
  );
}

export default App;