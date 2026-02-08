import React, { useState } from 'react';

const SCENARIOS = {
  "Custom Query": "",
  "Unpaid overtime wages": "My boss hasn't paid me overtime for the last 3 months. I work 50 hours per week as a server at a restaurant in Boston. They only pay me regular hourly rate.",
  "Landlord won't fix mold": "There's black mold growing in my bathroom and bedroom. I told my landlord 3 weeks ago in writing but they haven't fixed it. The lease says they're responsible for repairs.",
  "ICE encounter as immigrant": "I'm an international student on F-1 visa. I'm worried about ICE enforcement in my area. What are my rights if approached by immigration officers?",
  "Domestic violence emergency": "My partner physically attacked me and is threatening me. I'm scared and don't know what to do. I need help immediately."
};

function QueryInput({ onSubmit, loading }) {
  const [location, setLocation] = useState('Boston, MA');
  const [scenario, setScenario] = useState('Custom Query');
  const [customQuery, setCustomQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const query = scenario === 'Custom Query' ? customQuery : SCENARIOS[scenario];
    
    if (!query.trim()) {
      alert('Please enter a query or select a demo scenario!');
      return;
    }

    onSubmit(query, location);
  };

  return (
    <div className="query-input-section">
      <div className="sidebar">
        <div className="sidebar-section">
          <h3>📍 Your Location</h3>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="City, State"
            className="location-input"
          />
        </div>

        <div className="sidebar-section">
          <h3>🎯 Quick Scenarios</h3>
          <select
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            className="scenario-select"
          >
            {Object.keys(SCENARIOS).map(key => (
              <option key={key} value={key}>{key}</option>
            ))}
          </select>
        </div>

        <div className="sidebar-tip">
          💡 <strong>Tip:</strong> Be specific about dates, amounts, and what happened.
        </div>
      </div>

      <div className="main-input">
        <form onSubmit={handleSubmit}>
          {scenario !== 'Custom Query' && (
            <div className="scenario-preview">
              <strong>Demo Scenario:</strong> {SCENARIOS[scenario]}
            </div>
          )}

          {scenario === 'Custom Query' && (
            <textarea
              value={customQuery}
              onChange={(e) => setCustomQuery(e.target.value)}
              placeholder="Describe your legal situation... Example: My landlord is trying to evict me without proper notice..."
              className="query-textarea"
              rows={6}
            />
          )}

          <button
            type="submit"
            disabled={loading}
            className="submit-button"
          >
            {loading ? 'Analyzing...' : '🔍 Get Legal Guidance'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default QueryInput;