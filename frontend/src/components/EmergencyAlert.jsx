import React from 'react';

function EmergencyAlert({ triage, query }) {
  if (!triage) return null;

  const urgency = triage.urgency?.toLowerCase() || 'medium';
  const situationType = triage.situation_type || 'legal_dispute';

  // Active violence - 911 alert
  if (situationType === 'active_violence') {
    return (
      <div className="emergency-alert active-violence">
        <div className="emergency-icon">🚨</div>
        <div className="emergency-title">EMERGENCY - CALL 911 IMMEDIATELY</div>
        <div className="emergency-text">
          If you are in immediate physical danger, call 911 now.<br />
          Get to a safe location if possible.
        </div>
        <div className="emergency-contacts">
          <strong>🚨 Police/Fire/Medical: 911</strong>
        </div>
      </div>
    );
  }

  // Mental health crisis - 988 alert
  if (situationType === 'mental_health_crisis') {
    return (
      <div className="emergency-alert mental-health">
        <div className="emergency-icon">💜</div>
        <div className="emergency-title">YOU ARE NOT ALONE - HELP IS AVAILABLE</div>
        <div className="emergency-text">
          If you're thinking about suicide or need someone to talk to right now
        </div>
        <div className="crisis-contacts">
          <div className="crisis-contact">
            <strong>📞 988 Suicide & Crisis Lifeline</strong>
            <p>Call or text <strong>988</strong> anytime, 24/7</p>
            <p>Free, confidential support</p>
          </div>
          <div className="crisis-contact">
            <strong>💬 Crisis Text Line</strong>
            <p>Text <strong>HOME</strong> to <strong>741741</strong></p>
            <p>Trained crisis counselors available</p>
          </div>
        </div>
      </div>
    );
  }

  // Past violence/high priority
  if (situationType === 'past_violence' || urgency === 'high') {
    return (
      <div className="warning-alert">
        <strong>⚠️ HIGH PRIORITY SITUATION</strong>
        <p>This situation requires prompt attention. Consider:</p>
        <ul>
          <li>Filing a police report (non-emergency: 311 or local police non-emergency number)</li>
          <li>Consulting with a lawyer about protective orders</li>
          <li>Contacting a domestic violence hotline for guidance: <strong>1-800-799-7233</strong></li>
        </ul>
      </div>
    );
  }

  return null;
}

export default EmergencyAlert;