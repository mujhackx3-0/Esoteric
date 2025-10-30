# 🚀 Quick Start - Deploy in 5 Minutes

Fast deployment guide for Esoteric AI Loan Sales Assistant.

## Prerequisites

```powershell
# Check you have these installed
docker --version
docker-compose --version
```

---

## Option 1: Local Development (Fastest)

### Step 1: Start the application
```powershell
# Start both backend and frontend
docker-compose up -d
```

### Step 2: Access the application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 3: Test it
```powershell
# Check health
curl http://localhost:8000/health
```

**Done!** 🎉

---

## Option 2: Production Deployment

### Step 1: Configure environment
```powershell
# Copy and edit production config
Copy-Item .env.production .env.prod
notepad .env.prod
```

**Update these values:**
```bash
GROQ_API_KEY=your_actual_groq_api_key_here
SECRET_KEY=generate_a_strong_random_key
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Step 2: Deploy with production config
```powershell
docker-compose -f docker-compose.prod.yml up -d
```

### Step 3: Verify deployment
```powershell
# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Test health
curl http://localhost:8000/health
```

**Production ready!** ✅

---

## Option 3: Cloud Deployment

### AWS (Cloud Run / ECS)
```bash
# See CLOUD_DEPLOYMENT.md for detailed steps
gcloud run deploy esoteric-backend --image gcr.io/YOUR_PROJECT/esoteric-backend
```

### Google Cloud (Cloud Run)
```bash
gcloud run deploy esoteric-backend \
  --image gcr.io/YOUR_PROJECT/esoteric-backend \
  --platform managed \
  --region us-central1 \
  --memory 2Gi
```

### Azure (Container Instances)
```bash
az container create \
  --resource-group esoteric-rg \
  --name esoteric-app \
  --image esotericacr.azurecr.io/esoteric-backend:latest
```

**Full cloud guide**: [CLOUD_DEPLOYMENT.md](./CLOUD_DEPLOYMENT.md)

---

## Common Commands

### Development
```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build -d
```

### Production
```powershell
# Start
docker-compose -f docker-compose.prod.yml up -d

# Stop
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Update
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Port already in use?
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (replace PID)
taskkill /PID <PID> /F
```

### Can't connect to backend?
```powershell
# Check if running
docker-compose ps

# Check logs for errors
docker-compose logs esoteric-backend
```

### Need to rebuild?
```powershell
docker-compose down
docker-compose up --build -d
```

---

## Environment Variables

### Development (in `.env.development`)
```bash
GROQ_API_KEY=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
DEBUG=true
ALLOWED_ORIGINS=["*"]
```

### Production (in `.env.production`)
```bash
GROQ_API_KEY=your_production_key_here
SECRET_KEY=strong_random_key_here
DEBUG=false
ALLOWED_ORIGINS=["https://yourdomain.com"]
RATE_LIMIT_ENABLED=true
```

---

## What's Running?

### Backend (Port 8000)
- FastAPI application
- WebSocket support
- AI agent with Groq LLM
- RAG knowledge base
- Health checks at `/health`

### Frontend (Port 3000)
- Next.js 16 application
- React 19
- Tailwind CSS
- Real-time chat interface

### Nginx (Port 80/443) - Production only
- Reverse proxy
- SSL termination
- Rate limiting
- Load balancing

---

## Next Steps

1. ✅ **Deployed?** Check http://localhost:8000/docs
2. ✅ **Customize?** Edit `app/core/agent.py` for AI behavior
3. ✅ **Scale?** See [CLOUD_DEPLOYMENT.md](./CLOUD_DEPLOYMENT.md)
4. ✅ **Monitor?** Check `/metrics` endpoint
5. ✅ **Secure?** Review security in `.env.production`

---

## Need Help?

- **Full Documentation**: [README.md](./README.md)
- **Cloud Deployment**: [CLOUD_DEPLOYMENT.md](./CLOUD_DEPLOYMENT.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)
- **API Guide**: [API_GUIDE.md](./API_GUIDE.md)

---

**That's it! Your AI Loan Assistant is running.** 🎉

Access it at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

