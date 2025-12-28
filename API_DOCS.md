# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Get Pollution Data
**Endpoint:** `GET /api/pollution-data`

**Query Parameters:**
- `location` (required): City name or location string

**Example Request:**
```
GET http://localhost:5000/api/pollution-data?location=Delhi
```

**Example Response (200 OK):**
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
    {
      "source": "Industrial Emissions",
      "percentage": 25,
      "impact": "high"
    },
    {
      "source": "Power Plants",
      "percentage": 15,
      "impact": "high"
    },
    {
      "source": "Construction & Dust",
      "percentage": 15,
      "impact": "medium"
    },
    {
      "source": "Biomass Burning",
      "percentage": 10,
      "impact": "medium"
    }
  ],
  "timestamp": "2024-12-29T10:30:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Unable to fetch pollution data for this location",
  "location": "InvalidCity123"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Location parameter is required"
}
```

---

### 2. Get Health Tips
**Endpoint:** `GET /api/health-tips`

**Query Parameters:**
- `aqi_level` (required): One of the AQI levels

**Example Request:**
```
GET http://localhost:5000/api/health-tips?aqi_level=Unhealthy
```

**Example Response (200 OK):**
```json
{
  "aqi_level": "Unhealthy",
  "health_tips": [
    "Everyone may begin to experience health effects",
    "Wear an N95 or P100 mask if venturing outdoors",
    "Limit outdoor activities"
  ]
}
```

**Available AQI Levels:**
- `Good`
- `Moderate`
- `Unhealthy for Sensitive Groups`
- `Unhealthy`
- `Very Unhealthy`
- `Hazardous`

---

### 3. Get Pollution Sources
**Endpoint:** `GET /api/pollution-sources`

**Example Request:**
```
GET http://localhost:5000/api/pollution-sources
```

**Example Response (200 OK):**
```json
{
  "pollution_sources": {
    "India": {
      "sources": [
        {
          "source": "Vehicle Emissions",
          "percentage": 35,
          "impact": "high"
        },
        {
          "source": "Industrial Emissions",
          "percentage": 25,
          "impact": "high"
        },
        {
          "source": "Power Plants",
          "percentage": 15,
          "impact": "high"
        },
        {
          "source": "Construction & Dust",
          "percentage": 15,
          "impact": "medium"
        },
        {
          "source": "Biomass Burning",
          "percentage": 10,
          "impact": "medium"
        }
      ]
    },
    "United States": {
      "sources": [
        {
          "source": "Vehicle Emissions",
          "percentage": 40,
          "impact": "high"
        },
        {
          "source": "Power Plants",
          "percentage": 20,
          "impact": "high"
        },
        {
          "source": "Industrial Emissions",
          "percentage": 20,
          "impact": "high"
        },
        {
          "source": "Oil & Gas Production",
          "percentage": 12,
          "impact": "high"
        },
        {
          "source": "Other Sources",
          "percentage": 8,
          "impact": "medium"
        }
      ]
    },
    "China": {
      "sources": [
        {
          "source": "Industrial Emissions",
          "percentage": 40,
          "impact": "high"
        },
        {
          "source": "Power Plants",
          "percentage": 25,
          "impact": "high"
        },
        {
          "source": "Vehicle Emissions",
          "percentage": 20,
          "impact": "high"
        },
        {
          "source": "Construction & Dust",
          "percentage": 10,
          "impact": "medium"
        },
        {
          "source": "Other Sources",
          "percentage": 5,
          "impact": "medium"
        }
      ]
    }
  }
}
```

---

### 4. Health Check
**Endpoint:** `GET /health`

**Example Request:**
```
GET http://localhost:5000/health
```

**Example Response (200 OK):**
```json
{
  "status": "Backend is running"
}
```

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (missing parameters) |
| 404 | Not Found (location not found) |
| 500 | Internal Server Error |

---

## Data Field Descriptions

### AQI (Air Quality Index)
- **Good**: 0-50
- **Moderate**: 51-100
- **Unhealthy for Sensitive Groups**: 101-150
- **Unhealthy**: 151-200
- **Very Unhealthy**: 201-300
- **Hazardous**: 301+

### Pollutant Units
- **PM2.5/PM10**: Particulate Matter (µg/m³)
- **NO₂**: Nitrogen Dioxide (µg/m³)
- **O₃**: Ozone (µg/m³)
- **SO₂**: Sulfur Dioxide (µg/m³)
- **CO**: Carbon Monoxide (µg/m³)

### Impact Levels
- **high**: Significant health impact
- **medium**: Moderate health impact
- **low**: Minimal health impact

---

## Example cURL Commands

### Get Pollution Data
```bash
curl "http://localhost:5000/api/pollution-data?location=London"
```

### Get Health Tips
```bash
curl "http://localhost:5000/api/health-tips?aqi_level=Moderate"
```

### Get Pollution Sources
```bash
curl "http://localhost:5000/api/pollution-sources"
```

### Health Check
```bash
curl "http://localhost:5000/health"
```

---

## Rate Limiting
Currently, there is no rate limiting implemented. For production deployment, consider implementing rate limiting using Flask-Limiter.

---

## CORS Configuration
The API is configured to accept requests from any origin. For production, restrict CORS to your domain:

```python
CORS(app, origins=['https://yourdomain.com'])
```

---

## Authentication
Currently, no authentication is required. All endpoints are public.

---

## Caching
Consider implementing caching for frequently requested locations:
- Frontend: Cache results for 1 hour
- Backend: Redis cache for API responses (5-15 minutes)
