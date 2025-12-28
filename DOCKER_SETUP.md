# 🐳 Docker Compose Setup Guide

> Use this guide when you want to run the Pollution Tracker using Docker Compose instead of manual setup.

## When to Use Docker

Use Docker when you want to:
- Deploy to production
- Run in a containerized environment
- Avoid installing Python/Node locally
- Ensure consistent environments
- Scale the application
- Ship to other machines easily

## Prerequisites

### Install Docker
- **macOS:** [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Windows:** [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- **Linux:** [Docker Engine](https://docs.docker.com/engine/install/)

### Verify Installation
```bash
docker --version
docker-compose --version
```

Both should show version numbers.

## Step 1: Prepare Environment Variables

The `.env` file in the project root is already created. Update it with your API keys:

```bash
cd /Users/pranabdas/Desktop/PollutionMain

# Edit the .env file
nano .env
```

Update the file with your API keys:
```env
WEATHER_API_KEY=your_actual_weatherapi_key_here
OPEN_WEATHER_API_KEY=your_actual_openweather_key_here
```

Save and exit (Ctrl+X, then Y, then Enter)

## Step 2: Build Docker Images

```bash
cd /Users/pranabdas/Desktop/PollutionMain

# Build both images (backend and frontend)
docker-compose build --no-cache
```

**Expected output:**
```
 pollutionmain-backend  Built
 pollutionmain-frontend Built
```

This may take 5-10 minutes on first build.

## Step 3: Start the Application

```bash
# Start both containers
docker-compose up
```

**Expected output:**
```
[+] Running 2/2
 ✔ Container pollutionmain-backend-1  Running
 ✔ Container pollutionmain-frontend-1 Running
```

## Step 4: Access the Application

Open your browser:
```
http://localhost:3001
```

The application should load automatically.

## Step 5: Test the Application

1. Search for a city: "Delhi", "New York", "London"
2. View the pollution data
3. Check the health recommendations

## Useful Docker Commands

### View Running Containers
```bash
docker ps
```

### View Logs
```bash
# Both containers
docker-compose logs -f

# Specific container
docker-compose logs -f backend
docker-compose logs -f frontend

# Recent logs
docker-compose logs --tail=50
```

### Stop Containers
```bash
# Stop but keep containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (volumes too)
docker-compose down -v
```

### Restart Containers
```bash
docker-compose restart
```

### Rebuild and Restart
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### View Container Details
```bash
docker-compose ps
docker ps
```

### Execute Command in Container
```bash
# Backend Python shell
docker-compose exec backend python

# Frontend Node shell
docker-compose exec frontend sh

# Run command
docker-compose exec backend pip list
```

### Check Container Logs
```bash
docker-compose logs backend | tail -50
docker-compose logs frontend | tail -50
```

## Docker Compose File Structure

```yaml
services:
  backend:
    build: ./backend              # Build from backend/Dockerfile
    ports: - "5001:5000"          # Expose port 5001 (external) → 5000 (internal)
    environment:                  # Environment variables from .env
      - WEATHER_API_KEY=...
      - OPEN_WEATHER_API_KEY=...
    volumes: - ./backend:/app     # Mount backend directory
    networks: - pollution-tracker

  frontend:
    build: ./frontend             # Build from frontend/Dockerfile
    ports: - "3001:3000"          # Expose port 3001 (external) → 3000 (internal)
    environment:                  # Environment variables
      - REACT_APP_API_BASE_URL=http://localhost:5001
    depends_on: - backend         # Wait for backend to start
    networks: - pollution-tracker

networks:
  pollution-tracker:
    driver: bridge
```

## Dockerfile Explanations

### Backend Dockerfile (`backend/Dockerfile`)

```dockerfile
FROM python:3.9-slim          # Use Python 3.9 slim image

WORKDIR /app                  # Set working directory

COPY requirements.txt .       # Copy dependencies
RUN pip install ...           # Install Python packages

COPY . .                      # Copy application code

CMD ["gunicorn", ...]         # Run production server
```

### Frontend Dockerfile (`frontend/Dockerfile`)

```dockerfile
FROM node:18-alpine           # Use Node 18 Alpine image

WORKDIR /app                  # Set working directory

COPY package.json ./          # Copy dependencies
RUN npm install               # Install Node packages

COPY . .                      # Copy application code

EXPOSE 3000                   # Expose port 3000

CMD ["npm", "start"]          # Run React development server
```

## Common Docker Issues & Solutions

### Issue: Port Already in Use

```
Error response from daemon: ports are not available: 
exposing port TCP 0.0.0.0:5001
```

**Solution:**

```bash
# Find what's using port 5001
lsof -i :5001

# Kill the process (replace XXX with PID)
kill -9 XXX

# Try again
docker-compose up
```

### Issue: Docker Daemon Not Running

```
Cannot connect to Docker daemon
```

**Solution:**
- macOS: Start Docker Desktop
- Linux: `sudo systemctl start docker`
- Windows: Start Docker Desktop

### Issue: Image Build Failed

```
failed to solve: context deadline exceeded
```

**Solution:**

```bash
# Clean up and try again
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

### Issue: Container Won't Start

```
docker: Error response from daemon
```

**Solution:**

```bash
# Check logs
docker-compose logs

# Clean and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Issue: Can't Connect to Backend

```
Error: connect ECONNREFUSED 127.0.0.1:5000
```

**Solution:**

```bash
# Check if backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Restart
docker-compose restart backend
```

## Environment Variables in Docker

The `.env` file in the project root is automatically loaded by Docker Compose.

Variables used:
```env
# Backend environment variables
WEATHER_API_KEY=your_key          # WeatherAPI key
OPEN_WEATHER_API_KEY=your_key     # OpenWeatherMap key

# Frontend environment variables
# (configured in docker-compose.yml)
REACT_APP_API_BASE_URL=http://localhost:5000
```

## Volumes in Docker

The backend has a volume mount:

```yaml
volumes:
  - ./backend:/app
```

This means:
- Changes to `backend/` on your machine
- Automatically reflected in the container
- Useful for development (auto-reload)
- Can be removed for production

## Networks in Docker

Both services are on the same network: `pollution-tracker`

This allows:
- `backend` container to communicate with `frontend`
- Services use container names as hostnames
- Container-to-container communication

## Production Deployment

For production, modify `docker-compose.yml`:

```yaml
backend:
  build: ./backend
  ports:
    - "0.0.0.0:5000:5000"  # Expose to all interfaces
  environment:
    - FLASK_ENV=production
  # Remove volumes for production

frontend:
  build: ./frontend
  ports:
    - "0.0.0.0:3000:3000"  # Expose to all interfaces
  # Can disable CORS for specific domains
```

Then deploy using:
- Docker Hub + Kubernetes
- AWS ECS
- Google Cloud Run
- Heroku Container Registry
- Digital Ocean App Platform

## Docker Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `docker-compose up` | Start containers |
| `docker-compose down` | Stop & remove containers |
| `docker-compose build` | Build images |
| `docker-compose logs -f` | View live logs |
| `docker-compose ps` | List running containers |
| `docker-compose exec <service> <cmd>` | Execute command in container |
| `docker-compose restart` | Restart containers |
| `docker ps` | List all containers |
| `docker images` | List all images |
| `docker system prune` | Clean up unused data |

## Monitoring Docker Usage

```bash
# CPU, memory, network stats
docker stats

# Disk usage
docker system df

# View image sizes
docker images
```

## Next Steps

1. **If using Docker now:** Follow "Step 1-5" above
2. **If using manual setup:** Come back to this guide when ready
3. **For production:** Modify docker-compose.yml as needed
4. **For deployment:** Use Docker Hub or cloud provider

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Support

- **Setup Issues:** See "Common Docker Issues" section above
- **Docker General:** Check [Docker Docs](https://docs.docker.com/)
- **Project Issues:** See TROUBLESHOOTING.md

---

**Ready to use Docker?** Follow Steps 1-5 above!

Or go back to [MANUAL_SETUP.md](MANUAL_SETUP.md) for manual setup.

---

*Last Updated: December 29, 2025*
*Status: ✅ Docker ready and tested*
