import React from 'react';

function ResourcesTab({ result }) {
  const resources = result.resources?.resources || [];

  return (
    <div className="resources-tab">
      <h2>Free Legal Resources</h2>

      {resources.length > 0 ? (
        <div className="resources-list">
          {resources.map((resource, idx) => (
            <div key={idx} className="resource-card">
              <h3>{resource.name || 'Unknown'}</h3>
              
              {resource.phone && (
                <p><strong>📞 Phone:</strong> {resource.phone}</p>
              )}
              
              {resource.website && (
                <p>
                  <strong>🌐 Website:</strong>{' '}
                  <a href={resource.website} target="_blank" rel="noopener noreferrer">
                    {resource.website}
                  </a>
                </p>
              )}
              
              {resource.services && (
                <p><strong>Services:</strong> {resource.services.join(', ')}</p>
              )}
              
              {resource.eligibility && (
                <div className="eligibility-info">
                  ℹ️ {resource.eligibility}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="no-resources">
          <p>⚠️ No specific resources found for your location/category.</p>
          <p>💡 Try contacting your state's Attorney General office or local legal aid society.</p>
        </div>
      )}
    </div>
  );
}

export default ResourcesTab;