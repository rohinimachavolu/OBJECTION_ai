import React, { useState } from 'react';
import RightsTab from './RightsTab';
import ActionsTab from './ActionsTab';
import DocumentTab from './DocumentTab';
import ResourcesTab from './ResourcesTab';
import NewsTab from './NewsTab';

function ResultTabs({ result }) {
  const [activeTab, setActiveTab] = useState('rights');

  const tabs = [
    { id: 'rights', label: '📜 Your Rights', component: RightsTab },
    { id: 'actions', label: '🎯 Action Plan', component: ActionsTab },
    { id: 'document', label: '📄 Document', component: DocumentTab },
    { id: 'resources', label: '🤝 Resources', component: ResourcesTab },
    { id: 'news', label: '📰 Recent News', component: NewsTab }
  ];

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component;

  return (
    <div className="result-tabs">
      <div className="tab-headers">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-header ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {ActiveComponent && <ActiveComponent result={result} />}
      </div>
    </div>
  );
}

export default ResultTabs;