# 🚀 Manual Setup Guide (Recommended)

If Docker is giving you issues, here's the **manual setup guide** to run everything directly on your machine.

## Prerequisites

✅ Python 3.8+ installed
✅ Node.js 14+ installed
✅ npm installed
✅ Internet connection (for API calls)

## Step-by-Step Setup

### Step 1: Get API Keys (5 minutes)

1. **WeatherAPI.com**
   - Go to: https://www.weatherapi.com/
   - Click "Sign Up"
   - Create a free account
   - Copy your API key
   - Keep it handy

2. **OpenWeatherMap**
   - Go to: https://openweathermap.org/api
   - Click "Sign Up"
   - Create a free account
   - Go to API keys section
   - Copy your API key
   - Keep it handy

### Step 2: Setup Backend (Python Flask)

```bash
# Navigate to backend directory
cd /Users/pranabdas/Desktop/PollutionMain/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
# Open .env and replace:
# WEATHER_API_KEY=your_actual_key_here
# OPEN_WEATHER_API_KEY=your_actual_key_here

# Start Flask server
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!** ← Important

### Step 3: Setup Frontend (React)

**Open a NEW terminal window:**

```bash
# Navigate to frontend directory
cd /Users/pranabdas/Desktop/PollutionMain/frontend

# Install Node packages
npm install

# Start React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view pollution-tracker-frontend in the browser.
  Local:            http://localhost:3000
```

Your browser should automatically open to http://localhost:3000

### Step 4: Test the Application

1. You should see the Pollution Tracker homepage
2. Try searching for:
   - "Delhi"
   - "New York"
   - "London"
   - "Tokyo"
   - Your own city

3. You should see:
   - Air Quality Index (AQI)
   - Pollution sources breakdown
   - Health recommendations
   - Detailed pollutant levels

## Troubleshooting

### Problem: "Port 5000 already in use"

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Problem: "Port 3000 already in use"

```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Problem: "ModuleNotFoundError" in backend

```bash
# Make sure you're in the venv
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Problem: "npm ERR!" in frontend

```bash
# Try clearing npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules

# Reinstall
npm install
```

### Problem: API calls returning errors

1. Check your .env file has correct API keys
2. Verify API keys are active (not revoked)
3. Check you're not rate limited
4. Try searching again

### Problem: "CORS error" in browser console

1. Make sure backend is running on http://localhost:5000
2. Check frontend .env has:
   ```
   REACT_APP_API_BASE_URL=http://localhost:5000
   ```

## Keeping Terminals Organized

### Terminal 1 (Backend)
```bash
cd /Users/pranabdas/Desktop/PollutionMain/backend
source venv/bin/activate
python app.py
```

### Terminal 2 (Frontend)
```bash
cd /Users/pranabdas/Desktop/PollutionMain/frontend
npm start
```

### Terminal 3 (Optional - for other commands)
```bash
cd /Users/pranabdas/Desktop/PollutionMain
# Use this for git, file management, etc.
```

## Stopping the Application

1. **Backend terminal:** Press `Ctrl+C`
2. **Frontend terminal:** Press `Ctrl+C`

## Next Steps

1. ✅ Setup complete!
2. ✅ Both servers running
3. ✅ Application accessible at http://localhost:3000
4. 📝 Test with different cities
5. 🚀 Deploy when ready (optional)

## Deactivating Virtual Environment (when done)

```bash
# In backend terminal
deactivate
```

## Restarting Next Time

```bash
# Backend
cd backend
source venv/bin/activate
python app.py

# Frontend (in new terminal)
cd frontend
npm start
```

## Need Help?

- **Setup Issues:** Check "Troubleshooting" section above
- **API Issues:** Check your API keys are correct
- **Port Issues:** Make sure ports 3000 and 5000 are free
- **Module Issues:** Reinstall dependencies
- **CORS Issues:** Verify backend is running

## Quick Reference

| Command | Purpose |
|---------|---------|
| `source venv/bin/activate` | Activate Python venv |
| `deactivate` | Deactivate Python venv |
| `pip install -r requirements.txt` | Install Python packages |
| `npm install` | Install Node packages |
| `python app.py` | Start Flask backend |
| `npm start` | Start React frontend |
| `Ctrl+C` | Stop a running process |
| `lsof -i :5000` | Check what's using port 5000 |
| `lsof -i :3000` | Check what's using port 3000 |

---

**You're all set!** 🎉

The application is now running at **http://localhost:3000**

Try searching for your city to see pollution data!
