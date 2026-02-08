import React from 'react';

function RightsTab({ result }) {
  const triage = result.triage || {};
  const rights = result.rights || {};
  
  const urgency = triage.urgency?.toLowerCase() || 'medium';
  const urgencyColors = {
    low: '🟢',
    medium: '🟡',
    high: '🟠',
    critical: '🔴'
  };

  return (
    <div className="rights-tab">
      <h2>Your Legal Rights</h2>

      <div className="triage-metrics">
        <div className="metric">
          <span className="metric-label">Category</span>
          <span className="metric-value">{triage.category?.toUpperCase() || 'N/A'}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Urgency</span>
          <span className="metric-value">
            {urgencyColors[urgency]} {urgency?.toUpperCase() || 'MEDIUM'}
          </span>
        </div>
        <div className="metric">
          <span className="metric-label">Need Lawyer?</span>
          <span className="metric-value">
            {triage.requires_lawyer ? 'Yes ⚠️' : 'Not Required'}
          </span>
        </div>
      </div>

      <div className="rights-explanation">
        {rights.explanation || 'No rights information available'}
      </div>

      {rights.sources && rights.sources.length > 0 && (
        <details className="sources-section">
          <summary>📚 Legal Sources</summary>
          <div className="sources-list">
            {rights.sources.map((source, idx) => (
              <code key={idx} className="source-item">
                {source.source || 'Unknown'}
              </code>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}

export default RightsTab;