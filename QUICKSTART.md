# Quick Start Guide 🚀

## Option 1: Using Docker (Easiest)

### Prerequisites
- Docker
- Docker Compose

### Steps
1. Navigate to the project root:
   ```bash
   cd /Users/pranabdas/Desktop/PollutionMain
   ```

2. Update the `.env` file with your API keys:
   ```bash
   # Open .env and replace:
   WEATHER_API_KEY=your_actual_weatherapi_key_here
   OPEN_WEATHER_API_KEY=your_actual_openweather_key_here
   ```

3. Run:
   ```bash
   docker-compose up
   ```

4. Open http://localhost:3000 in your browser

**Note:** Docker will build and start both backend and frontend automatically.

---

## Option 2: Manual Setup (Recommended for Development)

### Backend Setup (Terminal 1)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your API keys
# WEATHER_API_KEY=your_key
# OPEN_WEATHER_API_KEY=your_key

# Run server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

---

## Getting API Keys

### WeatherAPI.com (Primary)
1. Go to https://www.weatherapi.com/
2. Sign up for a free account
3. Copy your API key
4. Add to backend `.env`

### OpenWeatherMap (Backup)
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Get API key from account settings
4. Add to backend `.env`

---

## Testing the Application

1. **Open Frontend**: http://localhost:3000
2. **Try a Search**: 
   - Enter "Delhi" or "New York" or "Beijing"
   - Click Search
3. **View Results**:
   - AQI and pollution level
   - Main pollution sources
   - Health recommendations
   - Detailed pollutant levels

---

## Troubleshooting

### CORS Error
- Make sure backend is running on port 5000
- Check `.env` in frontend has correct `REACT_APP_API_BASE_URL`

### API Key Error
- Verify API keys are correct in backend `.env`
- Check API key has not exceeded rate limits

### Port Already in Use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## Environment Variables

### Backend (.env)
```
WEATHER_API_KEY=your_weatherapi_key
OPEN_WEATHER_API_KEY=your_openweather_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:5000
```

For production, change to your deployed backend URL.

---

## Project Structure

```
PollutionMain/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Example env file
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js           # Main component
│   │   └── index.js         # Entry point
│   ├── package.json         # NPM dependencies
│   └── .env                 # Environment config
├── docker-compose.yml       # Docker setup
└── README.md               # Full documentation
```

---

## Supported Regions

The application works with any location in the world. Current pre-configured pollution sources are for:
- India
- United States
- China

Other regions will use default pollution source data.

---

## Features

✅ Real-time AQI data
✅ Pollution source breakdown
✅ Health recommendations
✅ Detailed pollutant levels
✅ Responsive design
✅ No authentication required
✅ Free to use

---

## Need Help?

1. Check the full README.md
2. Verify API keys are correct
3. Ensure backend and frontend are both running
4. Check browser console for errors (F12)
5. Check backend logs in terminal

Happy tracking! 🌍
