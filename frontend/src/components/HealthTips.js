import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HealthTips.css';

function HealthTips({ aqiLevel }) {
  const [tips, setTips] = useState([]);
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

  useEffect(() => {
    const fetchTips = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/health-tips`, {
          params: { aqi_level: aqiLevel }
        });
        setTips(response.data.health_tips);
      } catch (error) {
        console.error('Error fetching health tips:', error);
        setTips([]);
      }
    };

    fetchTips();
  }, [aqiLevel, API_BASE_URL]);

  return (
    <div className="health-tips">
      <h3>💡 Health Recommendations</h3>
      <div className="tips-list">
        {tips && tips.map((tip, index) => (
          <div key={index} className="tip-item">
            <span className="tip-icon">✓</span>
            <p>{tip}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HealthTips;
