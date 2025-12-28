import React from 'react';
import './PollutionNews.css';

export default function PollutionNews({ newsItems = [] }) {
  // Format date to readable format
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Truncate text to specific length
  const truncateText = (text, maxLength = 100) => {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  return (
    <div className="pollution-news-container">
      <div className="news-header">
        <h3>📰 Recent Pollution News</h3>
        <span className="news-count">{newsItems.length} articles</span>
      </div>

      {newsItems && newsItems.length > 0 ? (
        <div className="news-table-wrapper">
          <table className="news-table">
            <thead>
              <tr>
                <th className="col-title">Title</th>
                <th className="col-source">Source</th>
                <th className="col-date">Published</th>
                <th className="col-action">Link</th>
              </tr>
            </thead>
            <tbody>
              {newsItems.map((item, idx) => (
                <tr key={idx} className="news-row">
                  <td className="col-title">
                    <div className="title-text" title={item.title}>
                      {truncateText(item.title, 60)}
                    </div>
                    {item.description && (
                      <div className="description-text">
                        {truncateText(item.description, 80)}
                      </div>
                    )}
                  </td>
                  <td className="col-source">
                    <span className="source-badge">{item.source}</span>
                  </td>
                  <td className="col-date">
                    <span className="date-text">
                      {formatDate(item.published_at)}
                    </span>
                  </td>
                  <td className="col-action">
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="read-link"
                      title="Read full article"
                    >
                      Read →
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="no-news">
          <p>📭 No recent pollution news found for this location</p>
        </div>
      )}
    </div>
  );
}
