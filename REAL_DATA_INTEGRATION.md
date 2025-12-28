# 🌍 Real-Time Pollution Data Integration Guide

This document explains how to integrate real, location-specific pollution data based on actual industries, traffic patterns, and news events.

## 📊 Current Implementation Status

### ✅ Completed Features:
1. **City-Specific Pollution Sources** - 12+ cities with real government data
2. **News API Integration** - Structure ready for pollution news
3. **Multi-Source AQI Aggregation** - WeatherAPI + OpenWeatherMap fallback
4. **IQAir API Integration** - World Air Quality Index data

### 🔄 Next Steps (This Document):
1. Get News API key and enable real-time pollution news
2. Integrate industrial facility data
3. Add traffic-based emission calculations
4. Implement seasonal adjustments (Parali burning, Diwali, etc.)

---

## 🔑 **Step 1: Get News API Key** (Free, 5 minutes)

### Get Free NewsAPI.org Key:

1. Visit: https://newsapi.org/register
2. Create account (free tier available)
3. Copy your API key from dashboard
4. Add to `.env` file:

```bash
NEWS_API_KEY=your_actual_newsapi_key_here
```

5. Restart backend:
```bash
docker-compose restart backend
```

### What You Get:
- ✅ Real-time pollution news for searched cities
- ✅ 100 requests/day on free tier (plenty for testing)
- ✅ Automatically filters news by city name + "air quality", "pollution", "emissions"

### Test It:
```bash
curl "http://localhost:5001/api/pollution-data?location=Delhi" | python3 -m json.tool | grep -A 30 "pollution_news"
```

---

## 🏭 **Step 2: Industrial Facility Data**

### Data Sources:

#### India - CPCB (Central Pollution Control Board)
- **Website:** https://cpcb.nic.in/
- **Database:** CPCB Consent/Authorization Database
- **Access:** Public - can be scraped or downloaded as CSV
- **Data Points:** Factory location, type, emissions, pollution control equipment

#### USA - EPA Facility Registry System (FRS)
- **Website:** https://www.epa.gov/frs
- **API:** Available for querying
- **Data Points:** Industrial facilities, chemical releases, emissions by facility

#### Global - OpenStreetMap
- **Use:** Overpass API to query industrial areas
- **Free:** Yes
- **Query Example:**
```python
# Query all industrial facilities within 10km of a location
node["industrial"="yes"]({{lat}}-0.089,{{lon}}-0.089,{{lat}}+0.089,{{lon}}+0.089);
```

### Implementation Approach:

```python
def get_nearby_industries(lat, lon, radius_km=15):
    """Get industrial facilities near coordinates"""
    # Query Overpass API for factories, power plants, refineries
    # Returns count and types of industries
    # Calculate their contribution to pollution
    pass
```

---

## 🚗 **Step 3: Traffic-Based Emission Calculation**

### Real Traffic Data Sources:

#### 1. **Google Maps API** (Paid, ~$7/month for testing)
- Real-time traffic density
- Historical traffic patterns
- Vehicle count estimates

#### 2. **TomTom Traffic API** (Paid)
- Road network density
- Vehicle flow rates

#### 3. **Free Alternative: OpenStreetMap + OSMNX**
```python
import osmnx as ox

# Get road network density for a city
G = ox.graph_from_place('Delhi', network_type='drive')
road_density = ox.stats.describe_graph(G)

# Roads with higher density = more vehicles = more emissions
```

### Vehicle Count Calculation:

```python
def estimate_traffic_pollution(city_name, lat, lon):
    """
    Estimate vehicle count and emissions based on:
    1. City population
    2. Road density from OSM
    3. Vehicle ownership rates (country-specific)
    4. Peak hours
    """
    
    # Example: Delhi with ~30M people
    # ~10M vehicles estimated
    # Average 30% are on road = 3M vehicles
    # Each vehicle emits ~2kg CO2/hour = 6M kg/hour
    
    pass
```

---

## 🔥 **Step 4: Seasonal Events & Special Factors**

### Important Events by Location:

#### India - Punjab (Oct-Nov):
- **Parali (Stubble) Burning**
- Impact: +200-300 AQI points in Delhi/NCR
- Data: Monitor agricultural calendar
- APIs: Government agriculture ministries

#### India - Diwali (Oct-Nov):
- **Fireworks & Firecrackers**
- Impact: +100-200 AQI points peak night
- Fixed date: Can predict

#### China - Winter Heating:
- **Coal-burning season**
- Impact: +150-250 AQI points (Nov-Feb)
- Heating starts after Oct 15

#### USA - Wildfire Season (July-Oct):
- **Forest fires in California, Oregon**
- Impact: +100-300 AQI points depending on proximity
- Real-time smoke tracking available

### Implementation:

```python
def get_seasonal_adjustment(city, country, date):
    """Return pollution multiplier based on seasonal events"""
    
    adjustments = {
        ('Delhi', 'India'): {
            'Oct-Nov': 1.5,  # Parali burning season
            'Nov': 1.8,      # Parali + Diwali
        },
        ('Beijing', 'China'): {
            'Nov-Feb': 1.4,  # Heating season
        },
        ('Los Angeles', 'United States'): {
            'Jul-Oct': 1.3,  # Wildfire season
        },
    }
    
    return adjustments.get((city, country), {}).get(month, 1.0)
```

---

## 📰 **Step 5: News-Based Pollution Attribution**

### How News Helps:

1. **Identify current pollution events:**
   - "Parali burning reported in Punjab" → Adjust AQI upward for North India
   - "Traffic congestion on highway" → Local traffic pollution high
   - "Industrial accident at refinery" → Spike in industrial source contribution

2. **Track pollution sources in real-time:**
   - News article about "Stubble burning" → Biomass burning % increases
   - Article about "Manufacturing shutdown" → Industrial emissions % decreases

3. **Provide context to users:**
   - Show users why AQI is high
   - Display relevant news in dashboard table

### Example News Headlines to Watch:
```
✓ "Delhi AQI spikes to 450 due to stubble burning" → +Biomass burning
✓ "Traffic jams on Delhi-Noida expressway" → +Vehicle emissions
✓ "Thermal power plant shut for maintenance" → -Power plant emissions
✓ "Diwali fireworks cause air pollution spike" → +Fireworks/special event
✓ "Industrial pollution audit finds 50 factories violating norms" → +Industrial
```

---

## 🛠️ **Full Implementation Example**

Here's how all pieces work together:

```python
def get_dynamic_pollution_sources(city, country, lat, lon):
    """
    Calculate pollution sources based on:
    1. Base city-specific data (government reports)
    2. Nearby industries (OSM data)
    3. Current traffic (road density + time of day)
    4. Seasonal factors (Parali, Diwali, heating, wildfires)
    5. News-based adjustments (current events)
    """
    
    # Start with base city data
    sources = CITY_POLLUTION_DATA.get(city, COUNTRY_POLLUTION_DATA.get(country))
    
    # 1. Get nearby industries
    industries = get_nearby_industries(lat, lon)
    sources['Industrial Emissions']['percentage'] += industries['count'] * 0.5
    
    # 2. Calculate traffic contribution
    traffic_factor = estimate_traffic_pollution(city, lat, lon)
    sources['Vehicle Emissions']['percentage'] *= (1 + traffic_factor)
    
    # 3. Apply seasonal adjustments
    seasonal_mult = get_seasonal_adjustment(city, country, date.today())
    sources = apply_seasonal_multiplier(sources, seasonal_mult)
    
    # 4. Check for news events
    news_items = get_pollution_news(city, country, limit=10)
    news_adjustments = parse_news_for_pollution_factors(news_items)
    sources = apply_news_adjustments(sources, news_adjustments)
    
    # Normalize to 100%
    total = sum(s['percentage'] for s in sources)
    for source in sources:
        source['percentage'] = (source['percentage'] / total) * 100
    
    return sources
```

---

## 📊 **Dashboard Changes Needed**

### Frontend Components to Update:

1. **PollutionSourcesNews Component** (New):
   - Display recent pollution news in a table
   - Show publication date, source, title
   - Link to full article
   - Color-code by relevance (red = highly relevant, yellow = somewhat relevant)

2. **Enhanced PollutionSources.js**:
   - Show "Adjusted due to: Parali burning (Punjab)" badge
   - Show "Influenced by: 5 recent news articles" indicator
   - Tooltip showing which news articles affected the calculation

3. **AQIDisplay.js Enhancement**:
   - Add "Primary factors today" breakdown
   - Show main contributor to high AQI
   - Link to relevant news

### Example UI Changes:

```
┌─────────────────────────────────────┐
│ AQI: 320 (Very Unhealthy)          │
│ Primary Factor: Parali Burning      │
│ (Also: Industrial, Traffic high)    │
└─────────────────────────────────────┘

Pollution Sources (Dynamic):
├─ Biomass Burning: 35% ↑↑ (Parali season)
├─ Vehicle Emissions: 28% ↑ (Peak traffic)
├─ Industrial: 20%
├─ Power Plants: 12%
└─ Construction: 5%

Recent News (Relevant):
┌────────────────────────────────────┐
│ "Stubble burning peaks in Punjab"  │
│ Source: The Hindu • 2 hours ago    │
│                                     │
│ "Delhi traffic congestion...       │
│ Source: Hindustan Times • 1h ago   │
│                                     │
│ "Air quality alert issued..."      │
│ Source: Times of India • 30m ago   │
└────────────────────────────────────┘
```

---

## 🚀 **Quick Start Checklist**

- [ ] Get NewsAPI key from https://newsapi.org/register
- [ ] Add `NEWS_API_KEY=...` to `.env`
- [ ] Restart backend: `docker-compose restart backend`
- [ ] Test news endpoint:
  ```bash
  curl "http://localhost:5001/api/pollution-data?location=Delhi" | grep pollution_news
  ```
- [ ] Create PollutionNews component in React frontend
- [ ] Add news table to dashboard

---

## 📚 **Additional Resources**

### Government Data Sources:
- **India CPCB:** https://cpcb.nic.in/
- **USA EPA:** https://www.epa.gov/
- **China MEE:** http://www.mee.gov.cn/
- **UK Environment Agency:** https://www.gov.uk/government/organisations/environment-agency

### APIs Used:
- **NewsAPI:** https://newsapi.org/
- **OpenStreetMap Overpass:** https://overpass-api.de/
- **Google Maps:** https://developers.google.com/maps
- **WeatherAPI:** https://www.weatherapi.com/

### Research Papers:
- "Source Apportionment of Fine Particulate Matter in Urban Areas"
- "Traffic-related Emissions and Health Effects"
- "Industrial Emissions Inventory & Modeling"

---

## 📞 **Next Steps**

1. **Get free API keys** (NewsAPI, Google Maps if needed)
2. **Create new React component** for news display
3. **Implement industrial data** integration
4. **Add seasonal adjustments** for Parali, Diwali, etc.
5. **Test with real cities** and validate against government data

Good luck! 🌱
