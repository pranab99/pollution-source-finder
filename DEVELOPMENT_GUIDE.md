# 📖 Development Guide

## Architecture Overview

### Frontend Architecture
```
React App (Port 3000)
    ↓
React Router (no routing currently, ready to add)
    ↓
Component Tree:
  - App (main container)
    - SearchBar (input)
    - LoadingSpinner (conditional)
    - ErrorMessage (conditional)
    - Results Container
      - AQIDisplay (visual circle)
      - PollutionSources (bar chart style)
      - HealthTips (list)
      - Pollutants Grid (cards)
```

### Backend Architecture
```
Flask App (Port 5000)
    ↓
Request Handler
    ↓
Data Processor
    ├── Geocoding (OpenStreetMap)
    ├── AQI Fetch (WeatherAPI)
    ├── Fallback (OpenWeatherMap)
    └── Country Data (Local)
    ↓
JSON Response
```

## Code Structure

### Frontend Components

#### 1. SearchBar.js
- Controlled input component
- Handles form submission
- Props: `onSearch` callback function

#### 2. AQIDisplay.js
- Shows AQI value in circular visualization
- Color-coded based on AQI level
- Props: `data` object with aqi_data

#### 3. PollutionSources.js
- Displays pollution sources with progress bars
- Impact level badges
- Props: `sources` array

#### 4. HealthTips.js
- Fetches health tips from backend
- Displays tips based on AQI level
- Props: `aqiLevel` string

#### 5. LoadingSpinner.js
- Simple spinner animation
- No props needed

#### 6. ErrorMessage.js
- Displays error alerts
- Props: `message` string

### Backend Endpoints

#### app.py Structure
```python
# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

# Data
POLLUTION_SOURCES = {...}
COUNTRY_POLLUTION_DATA = {...}

# Functions
def get_aqi_from_weather_api(location)
def get_aqi_from_openweather(lat, lon)
def get_aqi_level(aqi_value)
def get_country_from_location(location)

# Routes
@app.route('/api/pollution-data', methods=['GET'])
@app.route('/api/health-tips', methods=['GET'])
@app.route('/api/pollution-sources', methods=['GET'])
@app.route('/health', methods=['GET'])
```

## Development Workflow

### Adding a New Component

1. Create file in `frontend/src/components/MyComponent.js`
2. Create CSS file `MyComponent.css`
3. Import in `App.js`
4. Add to JSX in appropriate location
5. Style as needed

Example:
```javascript
// MyComponent.js
import React from 'react';
import './MyComponent.css';

function MyComponent({ prop1, prop2 }) {
  return (
    <div className="my-component">
      {/* Component content */}
    </div>
  );
}

export default MyComponent;
```

### Adding a New API Endpoint

1. Create function in `backend/app.py`
2. Add @app.route decorator
3. Handle query parameters with `request.args.get()`
4. Return JSON with `jsonify()`
5. Document in API_DOCS.md

Example:
```python
@app.route('/api/new-endpoint', methods=['GET'])
def new_endpoint():
    param = request.args.get('param')
    # Process param
    return jsonify({'result': data}), 200
```

### Styling Guidelines

- Use CSS classes for component styling
- Follow BEM naming convention: `.component__element--modifier`
- Use gradient backgrounds for consistency
- Add hover effects for interactive elements
- Ensure mobile responsiveness with media queries

## State Management

### Current Approach (Simple)
- App.js maintains `pollutionData` state
- SearchBar passes location to parent via callback
- Components receive data as props

### If You Need More Complexity
Consider adding:
- Redux for global state
- Context API for theme switching
- Local storage for favorites

## API Integration

### Current Approach
```javascript
// In frontend
const response = await axios.get(
  `${API_BASE_URL}/api/pollution-data`,
  { params: { location } }
);

// In backend
location = request.args.get('location')
response = requests.get(API_URL, params=params)
```

### Error Handling
```javascript
try {
  // API call
} catch (err) {
  setError(err.response?.data?.error || 'Default error');
}
```

## Testing

### Frontend Testing
```bash
# Run in frontend directory
npm test
```

Add test files: `ComponentName.test.js`

Example:
```javascript
import { render, screen } from '@testing-library/react';
import SearchBar from '../components/SearchBar';

test('renders search input', () => {
  render(<SearchBar onSearch={jest.fn()} />);
  expect(screen.getByPlaceholderText(/Enter city/i)).toBeInTheDocument();
});
```

### Backend Testing
```bash
# Create backend/test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run with: `python -m unittest test_app.py`

## Performance Optimization

### Frontend
1. **Code Splitting**: Use React.lazy() for components
```javascript
const PollutionSources = React.lazy(() => import('./PollutionSources'));
```

2. **Memoization**: Use React.memo() for expensive components
```javascript
const MyComponent = React.memo(({ data }) => {
  return <div>{data}</div>;
});
```

3. **Debouncing**: Debounce search input
```javascript
import { debounce } from 'lodash';
const debouncedSearch = debounce(handleSearch, 300);
```

### Backend
1. **Caching**: Add Redis caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/pollution-data')
@cache.cached(timeout=300)
def get_pollution_data():
    ...
```

2. **Request Timeout**: Already implemented (10 seconds)
3. **Connection Pooling**: Use connection pools for APIs

## Logging

### Frontend Logging
```javascript
console.log('Development log:', data);
console.error('Error occurred:', error);
```

### Backend Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('Location searched: %s', location)
logger.error('API Error: %s', str(e))
```

## Environment Variables

### Add New Variable
1. Add to `.env.example`
2. Update `.env` locally
3. Access in code:
   - Frontend: `process.env.REACT_APP_VAR_NAME`
   - Backend: `os.getenv('VAR_NAME')`

## Git Workflow

```bash
# Clone
git clone <repo>
cd PollutionMain

# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature

# Create Pull Request
```

## Deployment Checklist

### Backend
- [ ] Update .env with production API keys
- [ ] Set FLASK_ENV=production
- [ ] Set FLASK_DEBUG=False
- [ ] Restrict CORS origins
- [ ] Add rate limiting
- [ ] Add request logging
- [ ] Test all endpoints
- [ ] Set up SSL/TLS

### Frontend
- [ ] Run `npm run build`
- [ ] Update REACT_APP_API_BASE_URL to production backend
- [ ] Test all features in production build
- [ ] Check console for errors
- [ ] Optimize images
- [ ] Set up analytics (optional)

## Common Tasks

### Update AQI Thresholds
Edit in `backend/app.py` function `get_aqi_level()`:
```python
def get_aqi_level(aqi_value):
    if aqi_value <= 50:
        return 'Good'
    # ... update thresholds
```

### Add New Country Data
Add to `COUNTRY_POLLUTION_DATA` in `backend/app.py`:
```python
'Country Name': {
    'sources': [
        {'source': 'Source1', 'percentage': 50, 'impact': 'high'},
        # ...
    ]
}
```

### Change Color Scheme
Update in `frontend/src/App.css` and component CSS files:
```css
background: linear-gradient(135deg, #newColor1 0%, #newColor2 100%);
```

### Add New Pollutant
1. Backend: Update API response in `app.py`
2. Frontend: Update `PollutantCard` in `App.js`
3. Update API_DOCS.md

## Debugging Tips

### Frontend
1. Use React Developer Tools (browser extension)
2. Check Network tab for API calls
3. Use `console.log()` for debugging
4. Check error boundaries

### Backend
1. Enable `FLASK_DEBUG=True`
2. Check logs in terminal
3. Use print statements
4. Test endpoints with curl or Postman

### CORS Issues
```python
# Update CORS in app.py
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
```

### Port Conflicts
```bash
# macOS/Linux
lsof -i :5000  # Check port
lsof -ti:5000 | xargs kill -9  # Kill process

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Documentation Standards

### Code Comments
```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
```

### Component Documentation
```javascript
/**
 * ComponentName - Brief description
 * @param {Object} props - Component props
 * @param {string} props.prop1 - Description
 * @returns {JSX.Element} The rendered component
 */
```

## Tools & Extensions

### Recommended VS Code Extensions
- ES7+ React/Redux/React-Native snippets
- Python
- Flask-specific extensions
- Prettier - Code formatter
- ESLint
- Thunder Client (API testing)

### Development Tools
- Postman - API testing
- React DevTools - Browser extension
- Redux DevTools - If using Redux
- Chrome DevTools - Network & debugging

## Resources

- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [WeatherAPI Docs](https://www.weatherapi.com/docs/)
- [OpenWeatherMap API](https://openweathermap.org/api)

## Support & Contribution

1. Check existing issues
2. Create detailed bug reports
3. Follow code style guidelines
4. Write tests for new features
5. Update documentation
6. Submit pull requests with clear descriptions

---

Happy developing! 🚀
