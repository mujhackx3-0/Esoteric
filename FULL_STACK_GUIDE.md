# 🚀 Debenture - Full Stack Setup Guide

## Overview

**Debenture** is an intelligent loan sales assistant for NBFCs, featuring:
- 🎨 **Next.js Frontend** - Modern React interface with animations and WebSocket chat
- ⚡ **FastAPI Backend** - AI-powered loan assistant with Groq LLM
- 🐳 **Docker** - Fully containerized deployment with docker-compose

---

## 📁 Project Structure

```
Esoteric-ui-fix/
├── frontend/                    # Next.js 16 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── lu/page.tsx     # Chat interface (connects to backend)
│   │   │   ├── about/page.tsx  # About page
│   │   │   └── contact/page.tsx # Contact page
│   │   ├── components/         # Reusable React components
│   │   └── utils/              # Utility functions
│   ├── Dockerfile              # Frontend Docker configuration
│   ├── package.json
│   └── .env.local              # Frontend environment variables
│
├── app/                        # FastAPI backend
├── data/                       # Backend data files
├── Dockerfile.fastapi          # Backend Docker configuration
├── docker-compose.yml          # Orchestrates frontend + backend
├── requirements.txt            # Python dependencies
└── .env                        # Backend environment variables
```

---

## 🏃 Quick Start (Docker - Recommended)

### Prerequisites

- Docker Desktop (for Windows)
- Git

### Step 1: Clone the Repository

```powershell
cd C:\Users\chakr\OneDrive\Desktop
git clone <your-repo-url>
cd Esoteric-ui-fix
```

### Step 2: Configure Environment Variables

The backend `.env` file is already configured with a Groq API key. You can verify it:

```powershell
cat .env
```

Should contain:
```env
GROQ_API_KEY=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
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

### Step 3: Build and Run Everything

```powershell
docker-compose up --build
```

This single command will:
1. ✅ Build the FastAPI backend
2. ✅ Build the Next.js frontend
3. ✅ Start both services
4. ✅ Connect them on a shared network

**Wait 2-3 minutes for the build to complete.**

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎯 Using the Application

### Landing Page (http://localhost:3000)

The home page features:
- Animated blur text
- Interactive bubble menu
- 3D color bend background

Click **"Open Lu"** to access the chat interface.

### Chat Interface (http://localhost:3000/lu)

The Lu chat page connects to the backend via WebSocket:
1. Automatically creates a session on load
2. Sends messages to the FastAPI backend
3. Displays AI responses in real-time

**Example conversation:**
```
You: I need a loan of 5 lakh rupees
Lu: Great! I can help you with that. May I have your name?
You: My name is Rahul
Lu: Thank you, Rahul. What is the purpose of this loan?
```

---

## 🔧 Development Setup (Without Docker)

### Backend Setup

```powershell
# Navigate to project root
cd C:\Users\chakr\OneDrive\Desktop\Esoteric-ui-fix

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python -m uvicorn app.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: http://localhost:3000

---

## 🐳 Docker Configuration Explained

### docker-compose.yml

Orchestrates both services:

```yaml
services:
  esoteric-backend:
    # FastAPI backend on port 8000
    # Includes health checks
    
  esoteric-frontend:
    # Next.js frontend on port 3000
    # Waits for backend to be healthy
    # Connected via esoteric-network
```

### Frontend Dockerfile

Multi-stage build for optimization:
1. **deps stage**: Install Node.js dependencies
2. **builder stage**: Build Next.js app with environment variables
3. **runner stage**: Production-ready minimal image

### Backend Dockerfile (Dockerfile.fastapi)

Python-based FastAPI setup with Groq LLM integration.

---

## 🌐 Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

- Used in development
- **Note**: In Docker, these are set to `http://esoteric-backend:8000` for internal networking

### Backend (.env)

```env
GROQ_API_KEY=<your-groq-api-key>
GROQ_MODEL_NAME=mixtral-8x7b-32768
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

---

## 📡 API Endpoints

### Session Management

**Create Session**
```bash
POST /api/v1/sessions
# Returns: { "session_id": "...", "greeting_message": "..." }
```

**Get Session**
```bash
GET /api/v1/sessions/{session_id}
# Returns session details and loan application state
```

### Chat

**REST Chat**
```bash
POST /api/v1/chat
Body: { "message": "I need a loan", "session_id": "..." }
# Returns AI response
```

**WebSocket Chat**
```
ws://localhost:8000/api/v1/ws/{session_id}
# Real-time bidirectional chat
```

### Health Checks

```bash
GET /health        # Basic health check
GET /ready         # Readiness check
GET /metrics       # Application metrics
```

For full API documentation: http://localhost:8000/docs

---

## 🛠️ Build Commands

### Frontend

```powershell
cd frontend

# Install dependencies
npm install

# Lint code
npm run lint

# Build for production
npm run build

# Run production build locally
npm start
```

### Backend

```powershell
# Install dependencies
pip install -r requirements.txt

# Run with Uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker

```powershell
# Build all services
docker-compose build

# Build without cache
docker-compose build --no-cache

# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 🔍 Troubleshooting

### Issue: Frontend can't connect to backend

**Solution 1**: Check if backend is running
```powershell
curl http://localhost:8000/health
```

**Solution 2**: Verify environment variables in `frontend/.env.local`

**Solution 3**: Check Docker network
```powershell
docker network inspect esoteric-ui-fix_esoteric-network
```

### Issue: Docker build fails

**Solution 1**: Clear Docker cache
```powershell
docker system prune -a
docker-compose build --no-cache
```

**Solution 2**: Check Docker Desktop is running

### Issue: Port already in use

**Solution**: Stop conflicting services
```powershell
# Check what's using port 3000
netstat -ano | findstr :3000

# Check what's using port 8000
netstat -ano | findstr :8000

# Stop the process or change port in docker-compose.yml
```

### Issue: WebSocket connection fails

**Solution 1**: Ensure backend is healthy
```powershell
docker-compose logs esoteric-backend
```

**Solution 2**: Check CORS settings in backend

### Issue: Frontend build fails with TypeScript errors

**Solution**: Rebuild with latest changes
```powershell
cd frontend
npm run build
```

---

## 🎨 Frontend Features

### Pages

1. **Landing Page** (`/`)
   - Animated blur text
   - Color bend background
   - Bubble menu navigation

2. **Chat Page** (`/lu`)
   - Real-time WebSocket chat
   - GitHub-inspired dark theme
   - Auto-scrolling messages

3. **About Page** (`/about`)
   - Information about the platform

4. **Contact Page** (`/contact`)
   - Team member GitHub profiles
   - Conway's Game of Life grid background

### Components

- **ColorBends**: 3D animated background with customizable colors
- **BlurText**: Text animation with blur effect
- **BubbleMenu**: Interactive floating menu
- **ClickSpark**: Click effect particles

---

## 🔐 Security Considerations

### Development
- `.env` files are gitignored
- Use `.env.example` as template
- Never commit API keys

### Production
- Rotate Groq API keys regularly
- Use Docker secrets for sensitive data
- Enable HTTPS with reverse proxy (nginx)
- Implement rate limiting
- Add authentication to API endpoints

---

## 📈 Performance Optimization

### Frontend
- Next.js standalone output for smaller Docker image
- Multi-stage Docker build
- Static page generation where possible

### Backend
- FastAPI async endpoints
- Connection pooling for database
- Persistent ChromaDB and SQLite volumes

---

## 🚀 Deployment

### Docker Deployment (Production)

```powershell
# Build for production
docker-compose -f docker-compose.yml build

# Run in production mode
docker-compose up -d

# Monitor logs
docker-compose logs -f
```

### Cloud Deployment

**Recommended platforms:**
- AWS (ECS/EKS)
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

**Steps:**
1. Push images to container registry (Docker Hub, ECR, GCR)
2. Configure environment variables in cloud platform
3. Set up load balancer for frontend
4. Configure DNS
5. Enable HTTPS with SSL certificate

---

## 📊 Monitoring

### Docker Health Checks

Backend includes automatic health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 5
```

### Metrics Endpoint

```bash
curl http://localhost:8000/metrics
```

Returns:
- Total sessions
- Active sessions
- Total messages
- Average response time
- Uptime

---

## 🧪 Testing

### Frontend Tests
```powershell
cd frontend
npm run test
```

### Backend Tests
```powershell
pytest
```

### Integration Tests
```powershell
# Start services
docker-compose up -d

# Test frontend -> backend connection
curl -X POST http://localhost:8000/api/v1/sessions
```

---

## 📝 Development Workflow

1. **Make changes** to frontend or backend
2. **Test locally** without Docker
3. **Lint and build**
   ```powershell
   cd frontend
   npm run lint
   npm run build
   ```
4. **Test with Docker**
   ```powershell
   docker-compose up --build
   ```
5. **Commit and push**

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📞 Support

- **Backend API Docs**: http://localhost:8000/docs
- **GitHub**: Check README.md for repository link
- **Issues**: Report bugs via GitHub Issues

---

## 🎉 Summary

You now have a fully Dockerized full-stack application:

✅ **Frontend**: Next.js 16 with TypeScript  
✅ **Backend**: FastAPI with Groq LLM  
✅ **Database**: ChromaDB (RAG) + SQLite (chat history)  
✅ **Docker**: Multi-container setup with docker-compose  
✅ **WebSocket**: Real-time chat communication  
✅ **Health Checks**: Automatic service monitoring  

**Start the entire stack:**
```powershell
docker-compose up --build
```

**Access the app:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

Enjoy building with Debenture! 🚀

