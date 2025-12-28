import React from 'react';
import './PollutionSources.css';

function PollutionSources({ sources }) {
  const getImpactColor = (impact) => {
    const colors = {
      'high': '#e74c3c',
      'medium': '#f39c12',
      'low': '#2ecc71'
    };
    return colors[impact] || '#95a5a6';
  };

  return (
    <div className="pollution-sources">
      <h3>Pollution Sources</h3>
      <div className="sources-list">
        {sources && sources.map((source, index) => (
          <div key={index} className="source-item">
            <div className="source-info">
              <h4>{source.source}</h4>
              <div className="source-bar">
                <div
                  className="source-bar-fill"
                  style={{
                    width: `${source.percentage}%`,
                    backgroundColor: getImpactColor(source.impact)
                  }}
                />
              </div>
              <p className="source-percentage">{source.percentage}%</p>
            </div>
            <span
              className="impact-badge"
              style={{ backgroundColor: getImpactColor(source.impact) }}
            >
              {source.impact}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PollutionSources;
