import React from 'react';

function ActionsTab({ result }) {
  const actions = result.actions || {};

  return (
    <div className="actions-tab">
      <h2>What You Should Do Next</h2>
      <div className="action-content">
        {actions.action_plan || 'No action plan available'}
      </div>
    </div>
  );
}

export default ActionsTab;