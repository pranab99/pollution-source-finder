# Development Requirements

## System Requirements
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Python Dependencies (Backend)
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0

## Node Dependencies (Frontend)
react@^18.2.0
react-dom@^18.2.0
react-scripts@5.0.1
axios@^1.5.0
recharts@^2.10.0

## External APIs
1. WeatherAPI.com - For real-time AQI data
2. OpenWeatherMap - Backup AQI data source
3. OpenStreetMap (Nominatim) - For geocoding

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Installation Time
- Backend: ~2-3 minutes
- Frontend: ~3-5 minutes
- Total: ~5-8 minutes

## Disk Space
- Backend: ~200MB (with venv)
- Frontend: ~500MB (with node_modules)
- Total: ~700MB

## RAM Requirements
- Development: ~500MB
- Production (Docker): ~1GB
