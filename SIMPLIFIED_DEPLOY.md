# 🚀 Simplified Deployment Guide

**Environment Agnostic** - Works everywhere with zero configuration!

## 🎯 Key Feature

**GROQ_API_KEY is hardcoded in the application** - No environment variables needed!

---

## Quick Deploy - ANY Environment

### 1. Docker Compose (Easiest)

```bash
# Just run it - no config needed!
docker-compose up -d

# That's it! Access at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 2. Production with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Cloud Deployment

**AWS, GCP, Azure, or ANY cloud** - just deploy the containers!

```bash
# Example: Google Cloud Run
gcloud run deploy esoteric-backend \
  --image gcr.io/YOUR_PROJECT/esoteric-backend \
  --platform managed \
  --region us-central1 \
  --memory 2Gi
```

---

## No Configuration Required! ✨

The application works out of the box because:

✅ **GROQ_API_KEY** - Hardcoded in `app/config.py`  
✅ **All settings** - Have sensible defaults  
✅ **Environment agnostic** - Same code everywhere  
✅ **Zero setup** - Just deploy and run  

---

## Optional Configuration

Only if you want to customize:

### Create `.env` file (optional)
```bash
# Copy the universal template
cp .env.universal .env

# Edit only what you want to change
notepad .env
```

### Common Customizations

```bash
# Change API URLs for production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com

# Enable rate limiting
RATE_LIMIT_ENABLED=true

# Adjust log level
LOG_LEVEL=DEBUG
```

---

## Deployment Commands

### Local Development
```bash
docker-compose up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
```

### Cloud Native
```bash
# AWS
docker push your-registry/esoteric-backend
aws ecs update-service --service esoteric --force-new-deployment

# GCP
gcloud run deploy esoteric-backend --image gcr.io/project/image

# Azure
az container create --name esoteric --image your-registry/esoteric-backend
```

---

## What's Included

### Backend (Port 8000)
- ✅ FastAPI with all endpoints
- ✅ Groq LLM integration (key hardcoded)
- ✅ RAG knowledge base
- ✅ WebSocket support
- ✅ Health checks
- ✅ Metrics endpoint

### Frontend (Port 3000)
- ✅ Next.js 16 application
- ✅ React 19
- ✅ Tailwind CSS
- ✅ Real-time chat UI

---

## Verification

After deployment:

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"2.0.0"}

# View API documentation
# Open http://localhost:8000/docs in browser
```

---

## Troubleshooting

### Port in use?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill
```

### Container not starting?
```bash
# View logs
docker-compose logs -f esoteric-backend

# Restart
docker-compose restart
```

### Need to rebuild?
```bash
docker-compose up --build -d
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Next.js)              │
│         Port 3000                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Backend (FastAPI)               │
│         Port 8000                       │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Groq LLM (Key Hardcoded)         │ │
│  │  • Mixtral-8x7b-32768             │ │
│  │  • No config needed               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  ChromaDB (Vector DB)             │ │
│  │  • Persistent storage             │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  SQLite (Chat Memory)             │ │
│  │  • Session management             │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Key Advantages

🎯 **Zero Configuration** - Works immediately  
🎯 **Environment Agnostic** - Same everywhere  
🎯 **No Secrets Management** - API key embedded  
🎯 **Cloud Ready** - Deploy anywhere  
🎯 **Production Ready** - Includes monitoring  

---

## Deployment Matrix

| Platform | Command | Time |
|----------|---------|------|
| Local Dev | `docker-compose up -d` | 30 sec |
| Production | `docker-compose -f docker-compose.prod.yml up -d` | 1 min |
| AWS ECS | Build → Push → Deploy | 5 min |
| GCP Cloud Run | `gcloud run deploy` | 3 min |
| Azure ACI | `az container create` | 3 min |
| Kubernetes | `kubectl apply -f k8s/` | 2 min |

---

## Support

- **Documentation**: See `README.md`
- **Cloud Guide**: See `CLOUD_DEPLOYMENT.md`
- **Structure**: See `PROJECT_STRUCTURE.md`

---

**Deploy with confidence - it just works!** ✨

No environment variables to forget.  
No secrets to manage.  
No configuration headaches.  

Just deploy and run! 🚀

