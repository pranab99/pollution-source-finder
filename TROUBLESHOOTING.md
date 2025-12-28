# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Port Already in Use

#### Problem
```
Error: Port 5000/3000 already in use
```

#### Solution

**For Port 5000 (Backend):**
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace XXX with PID)
kill -9 <PID>

# Verify it's gone
lsof -i :5000
```

**For Port 3000 (Frontend):**
```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Verify it's gone
lsof -i :3000
```

**Alternative: Use Different Ports**

Edit `docker-compose.yml` or change your startup commands to use different ports.

---

### 2. Python Virtual Environment Issues

#### Problem
```
ModuleNotFoundError: No module named 'flask'
```

#### Solution

```bash
# Ensure you're in the correct directory
cd /Users/pranabdas/Desktop/PollutionMain/backend

# Check if venv is activated (should show "venv" in prompt)
# If not, activate it:
source venv/bin/activate

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt

# Verify Flask is installed
python -c "import flask; print(flask.__version__)"
```

#### Problem
```
python: command not found
```

#### Solution

```bash
# Check Python is installed
python3 --version

# Use python3 instead:
python3 -m venv venv
source venv/bin/activate
python3 app.py
```

---

### 3. NPM Issues

#### Problem
```
npm ERR! code ENOENT
npm ERR! syscall open
```

#### Solution

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Try again
npm start
```

#### Problem
```
Node version mismatch
```

#### Solution

```bash
# Check Node version
node --version

# Should be 14+ (prefer 16+)
# If too old, upgrade Node from nodejs.org

# Then reinstall:
rm -rf node_modules
npm install
npm start
```

---

### 4. API Key Issues

#### Problem
```
WARN[0000] The "WEATHER_API_KEY" variable is not set
```

#### Solution

**For Docker:**
```bash
# Update .env file in project root
WEATHER_API_KEY=your_actual_key_here
OPEN_WEATHER_API_KEY=your_actual_key_here
```

**For Manual Setup:**
```bash
# Backend .env
cd backend
cat .env

# Should show:
# WEATHER_API_KEY=your_key_here
# OPEN_WEATHER_API_KEY=your_key_here

# Edit if needed:
nano .env  # or use your editor
```

#### Problem
```
API Error: Invalid API Key
```

#### Solution

1. **Verify your API keys are correct**
   - Copy them exactly (no spaces)
   - Check for expired keys

2. **Get new API keys**
   - WeatherAPI.com: https://www.weatherapi.com/
   - OpenWeatherMap: https://openweathermap.org/api

3. **Update .env file**
   ```bash
   WEATHER_API_KEY=new_key_here
   OPEN_WEATHER_API_KEY=new_key_here
   ```

4. **Restart servers**
   - Kill and restart both backend and frontend

---

### 5. CORS Errors

#### Problem
```
Access to XMLHttpRequest at 'http://localhost:5000/...' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

#### Solution

1. **Ensure backend is running**
   ```bash
   # Check if backend is running
   lsof -i :5000
   
   # If not, start it:
   cd backend && source venv/bin/activate && python app.py
   ```

2. **Check frontend .env**
   ```bash
   cd frontend
   cat .env
   
   # Should show:
   # REACT_APP_API_BASE_URL=http://localhost:5000
   ```

3. **Backend has CORS enabled**
   - Check `backend/app.py` has: `CORS(app)`

4. **Restart frontend**
   ```bash
   # Stop frontend (Ctrl+C)
   # Then restart:
   npm start
   ```

---

### 6. Database/Connection Issues

#### Problem
```
Error: Connection refused
```

#### Solution

1. **Check if backend is running**
   ```bash
   curl http://localhost:5000/health
   
   # Should return: {"status": "Backend is running"}
   ```

2. **If not running, start it**
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

3. **Check firewall/network**
   - Ensure ports 5000 & 3000 are not blocked

---

### 7. API Search Returning Errors

#### Problem
```
Error: Unable to fetch pollution data for this location
```

#### Solution

1. **Verify location name is correct**
   - Try: "Delhi", "New York", "London"
   - Avoid special characters

2. **Check backend logs**
   - Look at backend terminal for error messages

3. **Verify API keys are working**
   ```bash
   # Test WeatherAPI directly (replace YOUR_KEY)
   curl "https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=London&aqi=yes"
   ```

4. **Check rate limits**
   - Free tier has request limits
   - Wait a minute and try again

---

### 8. Docker Issues

#### Problem
```
Docker daemon is not running
```

#### Solution

```bash
# Start Docker Desktop (macOS)
# Or restart Docker service

# Verify Docker is running:
docker --version
docker ps
```

#### Problem
```
Cannot connect to Docker daemon
```

#### Solution

```bash
# Restart Docker
# macOS: Docker > Restart

# Then try again:
docker-compose up
```

#### Problem
```
Image build failed
```

#### Solution

```bash
# Clean up
docker-compose down
docker system prune -a

# Rebuild
docker-compose build --no-cache

# Start
docker-compose up
```

---

### 9. Browser Issues

#### Problem
```
Page not loading / Blank screen
```

#### Solution

1. **Hard refresh browser**
   ```
   macOS: Cmd + Shift + R
   Windows: Ctrl + Shift + R
   ```

2. **Check browser console**
   ```
   F12 → Console tab
   Look for red error messages
   ```

3. **Check if server is running**
   ```bash
   # Frontend
   curl http://localhost:3000
   
   # Backend
   curl http://localhost:5000/health
   ```

#### Problem
```
Infinite loading spinner
```

#### Solution

1. **Check backend is running**
   - Open new terminal: `curl http://localhost:5000/health`
   - If error, backend is not running

2. **Check API keys**
   - Verify they're in backend `.env`

3. **Check browser console for errors**
   - F12 → Console
   - Look for CORS or network errors

---

### 10. Memory/Performance Issues

#### Problem
```
Application running slowly / High memory usage
```

#### Solution

```bash
# Frontend memory issues
# Close other tabs/applications
# Try in private/incognito mode

# Backend memory issues
# Restart backend:
# (In backend terminal) Ctrl+C
# python app.py

# Docker memory issues
docker stats  # Check memory usage
docker-compose down  # Stop containers
docker system prune  # Clean up
```

---

## Quick Diagnostic Commands

```bash
# Check Python installation
python3 --version

# Check Node/npm installation
node --version
npm --version

# Check if ports are in use
lsof -i :5000
lsof -i :3000

# Test backend health
curl http://localhost:5000/health

# Test frontend
curl http://localhost:3000

# Check Docker
docker --version
docker ps

# View backend logs
# (In backend terminal, you'll see logs)

# View frontend logs
# (In frontend terminal, you'll see logs)
```

---

## Getting Help

### 1. Check the Logs
- **Backend logs:** Terminal where you ran `python app.py`
- **Frontend logs:** Terminal where you ran `npm start`
- **Docker logs:** Run `docker-compose logs -f`

### 2. Check Error Messages
- Read the full error message (don't just see red text!)
- Google the specific error message
- Check the documentation

### 3. Verify Setup
- Check API keys are correct
- Check ports are free (5000, 3000)
- Check servers are running
- Check .env files are updated

### 4. Try a Fresh Start
```bash
# Stop everything
# (Ctrl+C in all terminals)

# Clean up
docker-compose down 2>/dev/null
rm -rf frontend/node_modules
rm -rf backend/venv

# Restart
# Follow MANUAL_SETUP.md
```

---

## Common Success Indicators

✅ Backend terminal shows:
```
 * Running on http://127.0.0.1:5000
```

✅ Frontend terminal shows:
```
You can now view pollution-tracker-frontend in the browser.
  Local:            http://localhost:3000
```

✅ Browser shows the Pollution Tracker UI

✅ Searching for "Delhi" returns pollution data

✅ No errors in browser console (F12)

---

## Need More Help?

- **API Documentation:** [API_DOCS.md](API_DOCS.md)
- **Setup Guide:** [MANUAL_SETUP.md](MANUAL_SETUP.md)
- **Full Guide:** [README.md](README.md)
- **Development:** [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)

---

**Remember:** Most issues are solved by:
1. Restarting the servers
2. Checking the logs
3. Verifying API keys
4. Clearing cache/node_modules

Good luck! 🚀
