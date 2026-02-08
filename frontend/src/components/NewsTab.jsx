import React from 'react';

function NewsTab({ result }) {
  const newsData = result.news || {};
  const articles = newsData.articles || [];
  const queryUsed = newsData.query_used || '';

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    } catch {
      return '';
    }
  };

  return (
    <div className="news-tab">
      <h2>📰 Recent News & Developments</h2>

      {queryUsed && (
        <p className="news-query">🔍 Search: {queryUsed}</p>
      )}

      {articles.length > 0 ? (
        <>
          <p className="news-count">
            Found {articles.length} recent articles related to your issue
          </p>

          <div className="articles-list">
            {articles.map((article, idx) => (
              <div key={idx} className="article-card">
                <div className="article-content">
                  <h3>
                    {article.url ? (
                      <a href={article.url} target="_blank" rel="noopener noreferrer">
                        {article.title || 'No title'}
                      </a>
                    ) : (
                      article.title || 'No title'
                    )}
                  </h3>

                  {article.description && (
                    <p className="article-description">{article.description}</p>
                  )}

                  <div className="article-meta">
                    {article.source && <span><strong>Source:</strong> {article.source}</span>}
                    {article.published_at && (
                      <span><strong>Date:</strong> {formatDate(article.published_at)}</span>
                    )}
                  </div>
                </div>

                {article.image_url && (
                  <div className="article-image">
                    <img src={article.image_url} alt={article.title} />
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="news-disclaimer">
            💡 <strong>Note:</strong> These articles are related to your issue but may not directly 
            apply to your specific situation. Use them for general awareness.
          </div>
        </>
      ) : (
        <div className="no-news">
          <p>⚠️ No recent news articles found for this topic.</p>
          <p>
            💡 Try searching Google News for:{' '}
            <strong>{result.triage?.category || 'legal'} news {result.location}</strong>
          </p>
        </div>
      )}
    </div>
  );
}

export default NewsTab;