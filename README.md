# 🌍 Pollution Tracker

A comprehensive web application that helps users track air pollution levels and identify major pollution sources in their region. The application uses real-time AQI data from public APIs and provides health recommendations based on air quality levels.

## Features

- **Real-time AQI Data**: Fetches current Air Quality Index from WeatherAPI
- **Pollution Sources**: Shows breakdown of pollution sources by percentage in different regions
- **Health Recommendations**: Provides health tips based on AQI levels
- **Detailed Pollutant Levels**: Displays individual pollutant concentrations (PM2.5, PM10, NO₂, O₃, SO₂, CO)
- **User-friendly Interface**: Clean, responsive design built with React
- **No Authentication Required**: Simple location search interface

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **API Integration**: WeatherAPI.com, OpenWeatherMap, OpenStreetMap
- **CORS Support**: Flask-CORS for cross-origin requests
- **Environment Management**: python-dotenv

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Visualization**: Recharts
- **Styling**: CSS3 with gradients and animations

## Project Structure

```
PollutionMain/
├── backend/
│   ├── app.py                 # Flask application with all API endpoints
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Example environment variables
│
└── frontend/
    ├── public/
    │   └── index.html         # HTML template
    ├── src/
    │   ├── components/        # React components
    │   │   ├── SearchBar.js
    │   │   ├── AQIDisplay.js
    │   │   ├── PollutionSources.js
    │   │   ├── HealthTips.js
    │   │   ├── LoadingSpinner.js
    │   │   └── ErrorMessage.js
    │   ├── App.js             # Main app component
    │   ├── App.css
    │   ├── index.js
    │   └── index.css
    ├── .env                   # Environment configuration
    └── package.json
```

## API Endpoints

### Backend API (Flask)

#### 1. Get Pollution Data
```
GET /api/pollution-data?location={location}
```
Returns AQI data, pollution sources, and health information for a location.

**Response:**
```json
{
  "location": "Delhi",
  "country": "India",
  "coordinates": {
    "latitude": 28.7041,
    "longitude": 77.1025
  },
  "aqi_data": {
    "aqi": 125,
    "pm25": 85.5,
    "pm10": 150.2,
    "o3": 45.3,
    "no2": 65.2,
    "so2": 30.1,
    "co": 1200.5
  },
  "aqi_level": "Unhealthy for Sensitive Groups",
  "pollution_sources": [
    {
      "source": "Vehicle Emissions",
      "percentage": 35,
      "impact": "high"
    },
    ...
  ],
  "timestamp": "2024-12-29T10:30:00"
}
```

#### 2. Get Health Tips
```
GET /api/health-tips?aqi_level={aqi_level}
```
Returns health recommendations based on AQI level.

#### 3. Get Pollution Sources
```
GET /api/pollution-sources
```
Returns pollution sources data for all countries.

#### 4. Health Check
```
GET /health
```
Checks if backend is running.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Get API Keys:**
   - WeatherAPI: Register at https://www.weatherapi.com/ and get your free API key
   - OpenWeatherMap: Register at https://openweathermap.org/api and get your free API key
   - Update the `.env` file with your API keys

6. **Run the Flask server:**
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API endpoint (optional):**
   - The `.env` file already has `REACT_APP_API_BASE_URL=http://localhost:5000`
   - Change if your backend is running on a different URL

4. **Start the development server:**
   ```bash
   npm start
   ```
   The frontend will open at `http://localhost:3000`

## Usage

1. **Search for a Location:**
   - Enter a city name in the search bar
   - Click "Search" or press Enter

2. **View Results:**
   - **AQI Display**: Shows the current Air Quality Index and level
   - **Pollution Sources**: Displays breakdown of pollution sources
   - **Health Recommendations**: Shows tips based on current AQI
   - **Detailed Pollutants**: View individual pollutant concentrations

3. **Health Tips:**
   - Different recommendations based on AQI level
   - Guidelines from Good to Hazardous air quality

## API Data Sources

1. **AQI Data**: 
   - Primary: WeatherAPI.com (Free tier available)
   - Fallback: OpenWeatherMap Air Pollution API

2. **Location Data**: 
   - OpenStreetMap (Nominatim) for geocoding

3. **Pollution Sources**: 
   - Simulated government data with region-specific breakdowns
   - Can be replaced with actual government APIs (e.g., CPCB for India, EPA for USA)

## Future Enhancements

1. **Real Government Data Integration:**
   - Indian government (CPCB - Central Pollution Control Board)
   - US EPA data
   - EU air quality databases

2. **Historical Trends:**
   - AQI trends over time
   - Seasonal patterns

3. **Advanced Visualization:**
   - Interactive maps with pollution heatmaps
   - Time-series charts
   - Comparative analysis between cities

4. **Additional Features:**
   - Favorite locations
   - Push notifications for high pollution alerts
   - Pollen count data
   - Weather-based pollution forecasts

5. **Mobile App:**
   - React Native version
   - Native iOS/Android apps

## Environment Variables

### Backend (.env)
```
WEATHER_API_KEY=your_weatherapi_key_here
OPEN_WEATHER_API_KEY=your_openweather_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:5000
```

## Deployment

### Backend Deployment (Heroku/Railway/Render)
```bash
cd backend
pip freeze > requirements.txt
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)
```bash
cd frontend
npm run build
# Deploy the build folder to Vercel/Netlify
```

## CORS Configuration

The backend is configured to accept requests from the frontend. Update CORS settings in `app.py` if deploying to production:

```python
CORS(app, origins=['https://yourdomain.com'])
```

## License

MIT License

## Contributing

Feel free to submit issues and pull requests for improvements.

## Support

For issues or questions, please create an issue in the repository.

## Disclaimer

The pollution data provided is for informational purposes. Always refer to official government agencies for health and safety decisions.
