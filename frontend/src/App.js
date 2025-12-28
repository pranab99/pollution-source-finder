import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import SearchBar from './components/SearchBar';
import AQIDisplay from './components/AQIDisplay';
import PollutionSources from './components/PollutionSources';
import HealthTips from './components/HealthTips';
import PollutionNews from './components/PollutionNews';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [pollutionData, setPollutionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5001';

  const handleSearch = async (location) => {
    if (!location.trim()) {
      setError('Please enter a location');
      return;
    }

    setLoading(true);
    setError(null);
    setPollutionData(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/api/pollution-data`, {
        params: { location }
      });
      setPollutionData(response.data);
      setError(null);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        'Failed to fetch pollution data. Please try again.'
      );
      setPollutionData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Pollution Tracker</h1>
        <p>Check air quality and pollution sources in your area</p>
      </header>

      <main className="app-main">
        <SearchBar onSearch={handleSearch} />

        {error && <ErrorMessage message={error} />}
        {loading && <LoadingSpinner />}

        {pollutionData && (
          <div className="results-container">
            <div className="results-header">
              <h2>Pollution Data for {pollutionData.location}</h2>
              {pollutionData.country && (
                <p className="country-info">{pollutionData.country}</p>
              )}
            </div>

            <div className="data-grid">
              <AQIDisplay data={pollutionData} />
              <PollutionSources sources={pollutionData.pollution_sources} />
              {pollutionData.aqi_level && (
                <HealthTips aqiLevel={pollutionData.aqi_level} />
              )}
            </div>

            <div className="pollutants-detail">
              <h3>Detailed Pollutant Levels</h3>
              <div className="pollutants-grid">
                <PollutantCard
                  name="PM2.5"
                  value={pollutionData.aqi_data.pm25?.toFixed(2)}
                  unit="µg/m³"
                />
                <PollutantCard
                  name="PM10"
                  value={pollutionData.aqi_data.pm10?.toFixed(2)}
                  unit="µg/m³"
                />
                <PollutantCard
                  name="NO₂"
                  value={pollutionData.aqi_data.no2?.toFixed(2)}
                  unit="µg/m³"
                />
                <PollutantCard
                  name="O₃"
                  value={pollutionData.aqi_data.o3?.toFixed(2)}
                  unit="µg/m³"
                />
                <PollutantCard
                  name="SO₂"
                  value={pollutionData.aqi_data.so2?.toFixed(2)}
                  unit="µg/m³"
                />
                <PollutantCard
                  name="CO"
                  value={pollutionData.aqi_data.co?.toFixed(2)}
                  unit="µg/m³"
                />
              </div>
            </div>

            {pollutionData.pollution_news && pollutionData.pollution_news.length > 0 && (
              <PollutionNews newsItems={pollutionData.pollution_news} />
            )}
          </div>
        )}

        {!pollutionData && !loading && !error && (
          <div className="empty-state">
            <p>👆 Search for a location to see pollution data</p>
          </div>
        )}
        <footer className="app-footer">
        <div className="footer-content">
          <p className="footer-main">Made with ❤️ by Pranab</p>
          <div className="footer-deployment">
            <p className="footer-title">Want to deploy for your friends?</p>
            <ul className="deployment-options">
              <li><strong>Option 1: Docker (Recommended)</strong> - Run <code>docker-compose up</code></li>
              <li><strong>Option 2: Heroku</strong> - Push code to Heroku with Procfile</li>
              <li><strong>Option 3: AWS/GCP</strong> - Deploy backend to Cloud Run, frontend to Firebase Hosting</li>
              <li><strong>Option 4: DigitalOcean</strong> - Simple Docker deployment on a VPS</li>
            </ul>
            <p className="footer-docs">See README.md for detailed deployment instructions</p>
          </div>
        </div>
        <p className="footer-attribution">Data sources: WeatherAPI.com, OpenStreetMap, NewsAPI.org, Government Environmental Agencies</p>
        <p className="footer-main">Made with ❤️ by Pranab</p>
      </footer>
      </main>

      
    </div>
  );
}

function PollutantCard({ name, value, unit }) {
  return (
    <div className="pollutant-card">
      <h4>{name}</h4>
      <p className="pollutant-value">{value || 'N/A'}</p>
      <p className="pollutant-unit">{unit}</p>
    </div>
  );
}

export default App;
