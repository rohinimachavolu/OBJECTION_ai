import React from 'react';
import { Download } from 'lucide-react';

function DocumentTab({ result }) {
  const document = result.document || 'No document generated';

  const handleDownload = () => {
    const blob = new Blob([document], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = window.document.createElement('a');
    a.href = url;
    a.download = 'legal_document.txt';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="document-tab">
      <h2>Generated Legal Document</h2>
      
      <textarea
        readOnly
        value={document}
        className="document-textarea"
        rows={20}
      />

      <button onClick={handleDownload} className="download-button">
        <Download size={16} />
        Download Document
      </button>
    </div>
  );
}

export default DocumentTab;