import React from 'react';
import './AQIDisplay.css';

function AQIDisplay({ data }) {
  const getAQIColor = (aqiLevel) => {
    const colors = {
      'Good': '#2ecc71',
      'Moderate': '#f39c12',
      'Unhealthy for Sensitive Groups': '#e74c3c',
      'Unhealthy': '#c0392b',
      'Very Unhealthy': '#8b0000',
      'Hazardous': '#4b0000'
    };
    return colors[aqiLevel] || '#95a5a6';
  };

  // Get country flag emoji
  const getCountryFlag = (country) => {
    const flagMap = {
      'India': '🇮🇳',
      'United States': '🇺🇸',
      'China': '🇨🇳',
      'United Kingdom': '🇬🇧',
      'France': '🇫🇷',
      'Japan': '🇯🇵',
      'South Korea': '🇰🇷',
      'Germany': '🇩🇪',
      'Italy': '🇮🇹',
      'Spain': '🇪🇸',
      'Australia': '🇦🇺',
      'Canada': '🇨🇦',
      'Brazil': '🇧🇷',
      'Mexico': '🇲🇽',
      'Russia': '🇷🇺',
    };
    return flagMap[country] || '🌍';
  };

  const aqiValue = data.aqi_data.aqi || 0;
  const aqiLevel = data.aqi_level;
  const color = getAQIColor(aqiLevel);
  const locationName = data.location || 'Unknown Location';
  const address = data.address || '';
  const country = data.country || '';
  const countryFlag = getCountryFlag(country);

  return (
    <div className="aqi-display" style={{ borderColor: color }}>
      <div className="location-header">
        <div className="location-info">
          <h2>{locationName}</h2>
          {country && (
            <p className="country-info">{countryFlag} {country}</p>
          )}
          {data.state && (
            <p className="state-info">{data.state}</p>
          )}
          {address && (
            <p className="address-info">{address}</p>
          )}
        </div>
      </div>
      <h3>Air Quality Index (AQI)</h3>
      <div className="aqi-circle" style={{ backgroundColor: color }}>
        <div className="aqi-value">{aqiValue}</div>
      </div>
      <p className="aqi-level" style={{ color }}>
        {aqiLevel}
      </p>
      <p className="aqi-description">
        {getAQIDescription(aqiLevel)}
      </p>
    </div>
  );
}

function getAQIDescription(level) {
  const descriptions = {
    'Good': 'Air quality is satisfactory',
    'Moderate': 'Air quality is acceptable',
    'Unhealthy for Sensitive Groups': 'Sensitive groups should take precautions',
    'Unhealthy': 'Air quality is harmful',
    'Very Unhealthy': 'Air quality is very harmful',
    'Hazardous': 'Air quality is hazardous'
  };
  return descriptions[level] || 'Check air quality';
}

export default AQIDisplay;
