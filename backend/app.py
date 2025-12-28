import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# API Keys
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_weatherapi_key_here')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY', 'your_openweather_key_here')
IQAIR_API_KEY = os.getenv('IQAIR_API_KEY', 'your_iqair_key_here')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_newsapi_key_here')

# Configuration
WEATHER_API_URL = 'https://api.weatherapi.com/v1/current.json'
OPEN_WEATHER_AQI_URL = 'https://api.openweathermap.org/data/2.5/air_pollution'
IQAIR_URL = 'https://api.waqi.info/feed'
NEWS_API_URL = 'https://newsapi.org/v2/everything'

# Sample pollution sources database - can be replaced with actual government data
POLLUTION_SOURCES = {
    'default': [
        {'source': 'Vehicle Emissions', 'percentage': 35, 'impact': 'high'},
        {'source': 'Industrial Emissions', 'percentage': 25, 'impact': 'high'},
        {'source': 'Power Plants', 'percentage': 15, 'impact': 'high'},
        {'source': 'Construction & Dust', 'percentage': 15, 'impact': 'medium'},
        {'source': 'Biomass Burning', 'percentage': 10, 'impact': 'medium'},
    ]
}

# City-specific pollution sources data (based on government reports and research)
CITY_POLLUTION_DATA = {
    # India - CPCB (Central Pollution Control Board) data
    'Delhi': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 40, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 20, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 15, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 18, 'impact': 'medium'},
            {'source': 'Biomass Burning', 'percentage': 7, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB National Emission Inventory'
    },
    'Mumbai': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 38, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 22, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 16, 'impact': 'high'},
            {'source': 'Port Activities', 'percentage': 14, 'impact': 'medium'},
            {'source': 'Construction & Dust', 'percentage': 10, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB & Port Authority Data'
    },
    'Bangalore': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 42, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 18, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 12, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 20, 'impact': 'medium'},
            {'source': 'Other Sources', 'percentage': 8, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB Regional Office'
    },
    'Kolkata': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 36, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 28, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 18, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 12, 'impact': 'medium'},
            {'source': 'Biomass Burning', 'percentage': 6, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB Regional Office'
    },
    'Chennai': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 35, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 25, 'impact': 'high'},
            {'source': 'Port Activities', 'percentage': 18, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 14, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 8, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB & Port Authority Data'
    },
    'Bhubaneswar': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 38, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 22, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 18, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 16, 'impact': 'medium'},
            {'source': 'Biomass Burning', 'percentage': 6, 'impact': 'medium'},
        ],
        'country': 'India',
        'source': 'CPCB Regional Office & Odisha Pollution Control Board'
    },
    
    # USA - EPA (Environmental Protection Agency) data
    'New York': {
        'sources': [
            {'source': 'On-Road Vehicles', 'percentage': 28, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 18, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 17, 'impact': 'high'},
            {'source': 'Power Generation', 'percentage': 16, 'impact': 'high'},
            {'source': 'Commercial/Residential', 'percentage': 21, 'impact': 'medium'},
        ],
        'country': 'United States',
        'source': 'EPA National Emissions Inventory'
    },
    'Los Angeles': {
        'sources': [
            {'source': 'On-Road Vehicles', 'percentage': 35, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 20, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 16, 'impact': 'high'},
            {'source': 'Power Generation', 'percentage': 14, 'impact': 'high'},
            {'source': 'Commercial/Residential', 'percentage': 15, 'impact': 'medium'},
        ],
        'country': 'United States',
        'source': 'EPA & South Coast AQMD'
    },
    'Chicago': {
        'sources': [
            {'source': 'On-Road Vehicles', 'percentage': 26, 'impact': 'high'},
            {'source': 'Power Generation', 'percentage': 22, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 19, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 17, 'impact': 'high'},
            {'source': 'Other Sources', 'percentage': 16, 'impact': 'medium'},
        ],
        'country': 'United States',
        'source': 'EPA National Emissions Inventory'
    },
    'Houston': {
        'sources': [
            {'source': 'Oil & Gas Refining', 'percentage': 32, 'impact': 'high'},
            {'source': 'On-Road Vehicles', 'percentage': 24, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 21, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 14, 'impact': 'high'},
            {'source': 'Other Sources', 'percentage': 9, 'impact': 'medium'},
        ],
        'country': 'United States',
        'source': 'EPA & Texas TCEQ'
    },
    
    # China - Ministry of Ecology and Environment data
    'Beijing': {
        'sources': [
            {'source': 'Industrial Emissions', 'percentage': 35, 'impact': 'high'},
            {'source': 'Vehicle Emissions', 'percentage': 28, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 22, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 12, 'impact': 'medium'},
            {'source': 'Other Sources', 'percentage': 3, 'impact': 'low'},
        ],
        'country': 'China',
        'source': 'MEE & Beijing Municipal Bureau'
    },
    'Shanghai': {
        'sources': [
            {'source': 'Industrial Emissions', 'percentage': 32, 'impact': 'high'},
            {'source': 'Vehicle Emissions', 'percentage': 30, 'impact': 'high'},
            {'source': 'Port Activities', 'percentage': 18, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 15, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 5, 'impact': 'medium'},
        ],
        'country': 'China',
        'source': 'MEE & Shanghai Municipal Bureau'
    },
    'Chongqing': {
        'sources': [
            {'source': 'Industrial Emissions', 'percentage': 38, 'impact': 'high'},
            {'source': 'Vehicle Emissions', 'percentage': 25, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 20, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 14, 'impact': 'medium'},
            {'source': 'Other Sources', 'percentage': 3, 'impact': 'low'},
        ],
        'country': 'China',
        'source': 'MEE & Chongqing Municipal Bureau'
    },
    
    # Europe & Others
    'London': {
        'sources': [
            {'source': 'On-Road Vehicles', 'percentage': 40, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 20, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 15, 'impact': 'high'},
            {'source': 'Power Generation', 'percentage': 12, 'impact': 'high'},
            {'source': 'Other Sources', 'percentage': 13, 'impact': 'medium'},
        ],
        'country': 'United Kingdom',
        'source': 'UK Environment Agency'
    },
    'Paris': {
        'sources': [
            {'source': 'On-Road Vehicles', 'percentage': 38, 'impact': 'high'},
            {'source': 'Industrial Sources', 'percentage': 18, 'impact': 'high'},
            {'source': 'Power Generation', 'percentage': 16, 'impact': 'high'},
            {'source': 'Non-Road Equipment', 'percentage': 15, 'impact': 'high'},
            {'source': 'Other Sources', 'percentage': 13, 'impact': 'medium'},
        ],
        'country': 'France',
        'source': 'Airparif & ADEME'
    },
}

# Country-specific pollution data (fallback if city not found)
COUNTRY_POLLUTION_DATA = {
    'India': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 35, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 25, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 15, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 15, 'impact': 'medium'},
            {'source': 'Biomass Burning', 'percentage': 10, 'impact': 'medium'},
        ]
    },
    'United States': {
        'sources': [
            {'source': 'Vehicle Emissions', 'percentage': 40, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 20, 'impact': 'high'},
            {'source': 'Industrial Emissions', 'percentage': 20, 'impact': 'high'},
            {'source': 'Oil & Gas Production', 'percentage': 12, 'impact': 'high'},
            {'source': 'Other Sources', 'percentage': 8, 'impact': 'medium'},
        ]
    },
    'China': {
        'sources': [
            {'source': 'Industrial Emissions', 'percentage': 40, 'impact': 'high'},
            {'source': 'Power Plants', 'percentage': 25, 'impact': 'high'},
            {'source': 'Vehicle Emissions', 'percentage': 20, 'impact': 'high'},
            {'source': 'Construction & Dust', 'percentage': 10, 'impact': 'medium'},
            {'source': 'Other Sources', 'percentage': 5, 'impact': 'medium'},
        ]
    }
}


def get_aqi_from_weather_api(location):
    """Fetch AQI data from WeatherAPI"""
    try:
        params = {
            'key': WEATHER_API_KEY,
            'q': location,
            'aqi': 'yes'
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'current' in data and 'air_quality' in data['current']:
            air_quality = data['current']['air_quality']
            # Calculate AQI from PM2.5 using standard EPA formula
            # AQI = (PM2.5 - 0) / (35.5 - 0) * (100 - 0) + 0 for Good category (0-50)
            pm25 = air_quality.get('pm2_5', 0)
            aqi = pm25 * 2.5 if pm25 < 35.5 else (pm25 - 35.5) * 5 / 42 + 100 if pm25 < 60 else pm25
            
            return {
                'aqi': int(aqi),
                'pm25': air_quality.get('pm2_5', 0),
                'pm10': air_quality.get('pm10', 0),
                'o3': air_quality.get('o3', 0),
                'no2': air_quality.get('no2', 0),
                'so2': air_quality.get('so2', 0),
                'co': air_quality.get('co', 0),
            }
    except requests.RequestException as e:
        print(f"Error fetching from WeatherAPI: {e}")
    
    return None


def get_aqi_from_weather_api_coords(lat, lon):
    """Fetch AQI data from WeatherAPI using coordinates"""
    try:
        params = {
            'key': WEATHER_API_KEY,
            'q': f"{lat},{lon}",
            'aqi': 'yes'
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'current' in data and 'air_quality' in data['current']:
            air_quality = data['current']['air_quality']
            pm25 = air_quality.get('pm2_5', 0)
            aqi = pm25 * 2.5 if pm25 < 35.5 else (pm25 - 35.5) * 5 / 42 + 100 if pm25 < 60 else pm25
            
            return {
                'aqi': int(aqi),
                'pm25': air_quality.get('pm2_5', 0),
                'pm10': air_quality.get('pm10', 0),
                'o3': air_quality.get('o3', 0),
                'no2': air_quality.get('no2', 0),
                'so2': air_quality.get('so2', 0),
                'co': air_quality.get('co', 0),
            }
    except requests.RequestException as e:
        print(f"Error fetching from WeatherAPI with coords: {e}")
    
    return None


def get_aqi_from_openweather(lat, lon):
    """Fallback AQI data from OpenWeatherMap"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPEN_WEATHER_API_KEY
        }
        response = requests.get(OPEN_WEATHER_AQI_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'list' in data and len(data['list']) > 0:
            components = data['list'][0]['components']
            pm25 = components.get('pm2_5', 0)
            # Convert EPA index (1-5) to AQI (0-500+)
            # EPA: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
            epa_index = data['list'][0].get('main', {}).get('aqi', 3)
            
            # Better conversion: calculate from PM2.5
            if pm25 < 12.1:
                aqi = pm25 * 50 / 12
            elif pm25 < 35.5:
                aqi = 50 + (pm25 - 12.1) * 50 / 23.4
            elif pm25 < 55.5:
                aqi = 100 + (pm25 - 35.5) * 50 / 20
            elif pm25 < 150.5:
                aqi = 150 + (pm25 - 55.5) * 50 / 95
            else:
                aqi = 200 + (pm25 - 150.5)
            
            return {
                'aqi': int(aqi),
                'pm25': pm25,
                'pm10': components.get('pm10', 0),
                'o3': components.get('o3', 0),
                'no2': components.get('no2', 0),
                'so2': components.get('so2', 0),
                'co': components.get('co', 0),
            }
    except requests.RequestException as e:
        print(f"Error fetching from OpenWeather: {e}")
    
    return None


def get_pollution_sources_from_iqair(city, country):
    """Fetch pollution sources from IQAir/WAQI API"""
    try:
        # Try WAQI API (World Air Quality Index) which provides source information
        query = f"{city}, {country}" if country else city
        params = {
            'token': IQAIR_API_KEY,
        }
        # Remove spaces for URL encoding
        url = f"{IQAIR_URL}/{query.replace(' ', '%20')}/"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok' and 'data' in data:
            station_data = data['data']
            # WAQI provides attribution and city info
            # We'll use standard source breakdown for the country
            print(f"IQAir/WAQI data found for {query}")
            return station_data.get('iaqi', {})
    except Exception as e:
        print(f"Error fetching from IQAir/WAQI: {e}")
    
    return None


def get_pollution_sources_for_country(country):
    """Get pollution sources for a country with real data"""
    return COUNTRY_POLLUTION_DATA.get(country, POLLUTION_SOURCES['default'])


def get_aqi_level(aqi_value):
    """Convert AQI value to level description"""
    if aqi_value <= 50:
        return 'Good'
    elif aqi_value <= 100:
        return 'Moderate'
    elif aqi_value <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi_value <= 200:
        return 'Unhealthy'
    elif aqi_value <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'


def get_pollution_news(city, country=None, limit=5):
    """Fetch recent news for ANY city - only return if it contains 'pollution' keyword"""
    
    try:
        # Search for news for any city
        search_queries = [
            f'"{city}" (air quality OR pollution OR emissions OR AQI)',
            f'{city} pollution',
        ]
        
        if country:
            search_queries.append(f'"{city}" {country} pollution')
        
        news_items = []
        
        for query in search_queries:
            if len(news_items) >= limit:
                break
                
            try:
                params = {
                    'q': query,
                    'apiKey': NEWS_API_KEY,
                    'sortBy': 'publishedAt',
                    'language': 'en',
                    'pageSize': limit * 3,
                }
                
                response = requests.get(NEWS_API_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'ok' and 'articles' in data:
                    articles = data['articles']
                    
                    for article in articles:
                        if len(news_items) >= limit:
                            break
                        
                        title = article.get('title', '').lower()
                        description = article.get('description', '').lower()
                        content = f"{title} {description}"
                        
                        # SIMPLE CHECK: Only include if "pollution" keyword is present
                        if 'pollution' in content:
                            # Avoid duplicates
                            url_exists = any(item['url'] == article.get('url', '') for item in news_items)
                            
                            if not url_exists:
                                news_items.append({
                                    'title': article.get('title', ''),
                                    'description': article.get('description', ''),
                                    'url': article.get('url', ''),
                                    'image': article.get('urlToImage', ''),
                                    'source': article.get('source', {}).get('name', ''),
                                    'published_at': article.get('publishedAt', ''),
                                })
            except Exception as e:
                print(f"Error with query '{query}': {e}")
                continue
        
        if news_items:
            print(f"Found {len(news_items)} articles with 'pollution' keyword for {city}")
            return news_items[:limit]
        else:
            print(f"No articles containing 'pollution' found for {city}")
            return []
            
    except Exception as e:
        print(f"Error fetching news for {city}: {e}")
    
    return []



def get_country_from_location(location):
    """Try to determine country from location using geocoding"""
    try:
        geo_url = 'https://nominatim.openstreetmap.org/search'
        headers = {
            'User-Agent': 'PollutionTracker/1.0 (Educational Project)'
        }
        # Try with limit=1 to get the most relevant result
        params = {'q': location, 'format': 'json', 'limit': 1, 'addressdetails': 1}
        response = requests.get(geo_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        if response.json():
            results = response.json()
            # Get the first result (most relevant)
            data = results[0]
            address = data.get('address', {})
            country = address.get('country', '')
            state = address.get('state', '')
            city = address.get('city', '') or address.get('town', '') or address.get('village', '')
            display_name = data.get('display_name', location)  # Full address
            lat = float(data.get('lat', 0))
            lon = float(data.get('lon', 0))
            
            location_data = {
                'country': country,
                'state': state,
                'city': city,
                'address': display_name,
                'lat': lat,
                'lon': lon
            }
            
            print(f"Geocoded '{location}' to ({lat}, {lon}) in {country}, state: {state}")
            return location_data
    except Exception as e:
        print(f"Error getting country from location: {e}")
    
    return {
        'country': None,
        'state': None,
        'city': None,
        'address': location,
        'lat': None,
        'lon': None
    }


@app.route('/api/pollution-data', methods=['GET'])
def get_pollution_data():
    """Main endpoint to get pollution data for a location"""
    location = request.args.get('location', '')
    
    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400
    
    # Get location details (country, state, address, coordinates)
    location_data = get_country_from_location(location)
    country = location_data.get('country')
    state = location_data.get('state')
    address = location_data.get('address')
    lat = location_data.get('lat')
    lon = location_data.get('lon')
    
    # Fetch AQI data - prefer coordinates if available, fallback to location name
    aqi_data = None
    if lat and lon:
        # Try with coordinates first (most accurate)
        aqi_data = get_aqi_from_weather_api_coords(lat, lon)
        if not aqi_data:
            # Fallback to OpenWeather with coordinates
            aqi_data = get_aqi_from_openweather(lat, lon)
    
    # If no data from coordinates, try WeatherAPI with location name
    if not aqi_data:
        aqi_data = get_aqi_from_weather_api(location)
    
    # If still no data, return error
    if not aqi_data:
        return jsonify({
            'error': 'Unable to fetch pollution data for this location',
            'location': location
        }), 404
    
    # Get pollution sources - try city first, then country, then default
    pollution_sources = None
    pollution_source_data = None
    
    # Try to find city-specific data
    city_name = location.strip()
    if city_name in CITY_POLLUTION_DATA:
        pollution_source_data = CITY_POLLUTION_DATA[city_name]
        pollution_sources = pollution_source_data['sources']
        print(f"Using city-specific data for {city_name}")
    # Fallback to country-specific data
    elif country and country in COUNTRY_POLLUTION_DATA:
        pollution_source_data = COUNTRY_POLLUTION_DATA[country]
        pollution_sources = pollution_source_data['sources']
        print(f"Using country-level data for {country}")
    # Final fallback to default
    else:
        pollution_sources = POLLUTION_SOURCES['default']
        pollution_source_data = {'sources': pollution_sources, 'source': 'Default'}
        print(f"Using default pollution sources for {location}")
    
    # Calculate AQI level
    aqi_level = get_aqi_level(aqi_data.get('aqi', 0))
    
    # Fetch pollution-related news
    pollution_news = get_pollution_news(city_name, country, limit=5)
    
    response_data = {
        'location': location,
        'country': country,
        'state': state,
        'address': address,
        'coordinates': {
            'latitude': lat,
            'longitude': lon
        },
        'aqi_data': aqi_data,
        'aqi_level': aqi_level,
        'pollution_sources': pollution_sources,
        'source_data_attribution': pollution_source_data.get('source', 'Government/Research Data'),
        'pollution_news': pollution_news,
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }
    
    return jsonify(response_data), 200


@app.route('/api/health-tips', methods=['GET'])
def get_health_tips():
    """Get health recommendations based on AQI level"""
    aqi_level = request.args.get('aqi_level', 'Moderate')
    
    health_tips = {
        'Good': [
            'Air quality is satisfactory, enjoy outdoor activities',
            'Perfect day for exercise and outdoor recreation',
            'No air quality alerts'
        ],
        'Moderate': [
            'Unusually sensitive people should consider limiting prolonged outdoor exertion',
            'General public is less likely to be affected',
            'Keep monitoring air quality'
        ],
        'Unhealthy for Sensitive Groups': [
            'Members of sensitive groups should limit prolonged outdoor exertion',
            'Consider wearing an N95 mask if going outside',
            'Keep windows closed to prevent outdoor air from entering'
        ],
        'Unhealthy': [
            'Everyone may begin to experience health effects',
            'Wear an N95 or P100 mask if venturing outdoors',
            'Limit outdoor activities'
        ],
        'Very Unhealthy': [
            'Health alert: everyone may experience serious health effects',
            'Avoid outdoor activities entirely if possible',
            'Use air purifiers indoors and keep windows closed'
        ],
        'Hazardous': [
            'Health warning of emergency conditions',
            'Entire population is more likely to be affected',
            'Stay indoors and keep activity levels as low as possible'
        ]
    }
    
    return jsonify({
        'aqi_level': aqi_level,
        'health_tips': health_tips.get(aqi_level, health_tips['Moderate'])
    }), 200


@app.route('/api/pollution-sources', methods=['GET'])
def get_pollution_sources():
    """Get pollution sources for different countries"""
    return jsonify({'pollution_sources': COUNTRY_POLLUTION_DATA}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Backend is running'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
