# Pollution Tracker - Deployment Guide

**Made with ❤️ by Pranab**

This guide shows you how to deploy the Pollution Tracker application for your friends and the public to use.

## Table of Contents
1. [Docker (Local/VPS)](#docker-local--vps) - Easiest option
2. [Heroku](#heroku) - Cloud deployment, free tier available
3. [AWS/GCP](#awsgcp) - Professional cloud solutions
4. [DigitalOcean](#digitalocean) - Simple VPS deployment

---

## Docker (Local / VPS)

### Prerequisites
- Docker installed (https://www.docker.com/products/docker-desktop)
- API Keys configured in `.env` file

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd PollutionMain
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# WEATHER_API_KEY=your_key_here
# OPEN_WEATHER_API_KEY=your_key_here
# NEWS_API_KEY=your_key_here
# IQAIR_API_KEY=your_key_here
```

3. **Run with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3001
- Backend API: http://localhost:5001

### For Your Friends (LAN Access)

If you want to share on your local network:

```bash
# Get your machine IP
ipconfig getifaddr en0  # macOS
# or
hostname -I  # Linux

# Friends access via: http://YOUR_IP:3001
```

### Stop the application
```bash
docker-compose down
```

---

## Heroku

### Prerequisites
- Heroku account (https://www.heroku.com)
- Heroku CLI installed

### Deployment Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku app**
```bash
heroku create your-pollution-tracker
```

3. **Set environment variables**
```bash
heroku config:set WEATHER_API_KEY=your_key_here
heroku config:set OPEN_WEATHER_API_KEY=your_key_here
heroku config:set NEWS_API_KEY=your_key_here
heroku config:set IQAIR_API_KEY=your_key_here
```

4. **Deploy**
```bash
git push heroku main
```

5. **Access**
```bash
heroku open
```

**Note:** Heroku free tier is being phased out. Use paid dynos (~$7/month) for reliable hosting.

---

## AWS/GCP

### AWS Option: Lambda + CloudFront

**Backend (Flask) on AWS Lambda:**
1. Install AWS SAM CLI
2. Create Lambda function from docker image
3. Deploy with: `sam deploy`

**Frontend on S3 + CloudFront:**
1. Build React: `npm run build`
2. Upload to S3 bucket
3. Create CloudFront distribution
4. Enable CORS for API calls

**Estimated Cost:** ~$1-10/month

### GCP Option: Cloud Run + Firebase Hosting

**Backend on Cloud Run:**
```bash
gcloud run deploy pollution-tracker \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Frontend on Firebase:**
```bash
firebase init hosting
npm run build
firebase deploy
```

**Estimated Cost:** ~$0-5/month (within free tier)

---

## DigitalOcean

### Easiest Cloud VPS Option

1. **Create Droplet**
   - Choose: Docker enabled droplet
   - Size: Basic plan (~$6/month)
   - Region: Nearest to you

2. **Connect via SSH**
```bash
ssh root@your_droplet_ip
```

3. **Clone repository**
```bash
git clone <your-repo-url>
cd PollutionMain
```

4. **Set environment variables**
```bash
nano .env  # Create and edit the file
```

5. **Run with Docker**
```bash
docker-compose up -d
```

6. **Setup Firewall**
```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
```

7. **Access**
- Frontend: http://your_droplet_ip:3001
- Backend: http://your_droplet_ip:5001

### Add SSL Certificate (Let's Encrypt)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot certonly --standalone -d your_domain.com

# Add to nginx/reverse proxy
```

---

## Quick Comparison Table

| Platform | Cost | Setup Time | Best For |
|----------|------|-----------|----------|
| **Docker Local** | $0 | 5 mins | Friends on same network |
| **Heroku** | $7-50/mo | 10 mins | Quick cloud deployment |
| **DigitalOcean** | $6+/mo | 20 mins | Reliable, scalable |
| **AWS Lambda** | $0.20/M reqs | 30 mins | High traffic, scalable |
| **GCP Cloud Run** | Free tier | 20 mins | Modern, fast |

---

## Recommended Setup for Friends

### Option 1: Docker on Your Computer (Simplest)
- Run `docker-compose up -d`
- Share your IP: `http://YOUR_IP:3001`
- Friends access via your LAN

### Option 2: DigitalOcean Droplet (Best Value)
- Cost: $6/month
- Always online for friends
- Easy to manage
- Professional URL support

### Option 3: Combination
- **Development:** Docker locally
- **Production:** DigitalOcean or AWS
- Keep both running simultaneously

---

## Security Tips

1. **Change default API keys** - Use your own keys from:
   - https://www.weatherapi.com (free tier available)
   - https://openweathermap.org (free tier available)
   - https://newsapi.org (100 free requests/day)

2. **Enable HTTPS** - Use Let's Encrypt (free certificates)

3. **Rate Limiting** - Add rate limiter to Flask backend:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/pollution-data')
@limiter.limit("100/hour")
def get_pollution_data():
    # ...
```

4. **CORS Configuration** - Update in `app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "OPTIONS"],
    }
})
```

---

## Environment Variables Required

Create `.env` file with:

```env
# API Keys
WEATHER_API_KEY=your_weatherapi_key
OPEN_WEATHER_API_KEY=your_openweather_key
NEWS_API_KEY=your_newsapi_key
IQAIR_API_KEY=your_iqair_key

# Optional
FLASK_ENV=production
PORT=5000
REACT_APP_API_BASE_URL=http://localhost:5001
```

---

## Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "5002:5000"  # Use 5002 instead of 5001
  - "3002:3001"  # Use 3002 instead of 3001
```

**API Keys not working:**
- Verify keys in `.env` file
- Restart containers: `docker-compose restart`
- Check logs: `docker-compose logs backend`

**Slow performance:**
- Check News API rate limit (100 requests/day free tier)
- Consider caching responses
- Use CDN for frontend (CloudFlare is free)

---

## Next Steps

1. **Test locally** - `docker-compose up`
2. **Get API keys** - Sign up at services above
3. **Choose platform** - DigitalOcean recommended
4. **Deploy** - Follow platform-specific steps
5. **Share with friends** - Give them the URL

---

## Support & Feedback

For issues or improvements:
1. Check backend logs: `docker-compose logs backend`
2. Check frontend console: Open DevTools (F12) in browser
3. Review code in `/backend/app.py` and `/frontend/src/`

---

**Happy deploying! 🚀**

Made with ❤️ by Pranab
