# 📁 Esoteric Project Structure

Production-ready structure for cloud deployment.

## Directory Layout

```
Esoteric-ui-fix/
├── 📂 app/                          # Backend FastAPI application
│   ├── 📂 api/                      # API routes
│   ├── 📂 core/                     # Core business logic
│   │   ├── agent.py                 # AI agent implementation
│   │   ├── rag.py                   # RAG knowledge base
│   │   └── session.py               # Session management
│   ├── 📂 utils/                    # Utility functions
│   │   └── logger.py                # Logging configuration
│   ├── config.py                    # Configuration management
│   ├── main.py                      # FastAPI application entry
│   └── models.py                    # Pydantic models
│
├── 📂 frontend/                     # Next.js frontend application
│   ├── 📂 src/
│   │   ├── 📂 app/                  # Next.js app router
│   │   │   ├── about/               # About page
│   │   │   ├── contact/             # Contact page
│   │   │   ├── lu/                  # Loan UI page
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── page.tsx             # Home page
│   │   │   └── globals.css          # Global styles
│   │   ├── 📂 components/           # React components
│   │   │   ├── BlurText.tsx
│   │   │   ├── BubbleMenu.tsx
│   │   │   ├── ClickSpark.tsx
│   │   │   └── ColorBends.tsx
│   │   ├── 📂 lib/                  # Utilities
│   │   │   └── utils.ts
│   │   └── 📂 utils/
│   │       └── tilePattern.ts
│   ├── 📂 public/                   # Static assets
│   ├── package.json                 # Node dependencies
│   ├── next.config.ts               # Next.js config
│   ├── tsconfig.json                # TypeScript config
│   └── Dockerfile                   # Frontend container
│
├── 📂 k8s/                          # Kubernetes configurations
│   └── deployment.yaml              # K8s manifests
│
├── 📂 nginx/                        # Nginx reverse proxy
│   └── nginx.conf                   # Nginx configuration
│
├── 📂 .github/                      # GitHub Actions
│   └── workflows/
│       └── deploy.yml               # CI/CD pipeline
│
├── 📄 Dockerfile.fastapi            # Backend container
├── 📄 docker-compose.yml            # Development compose
├── 📄 docker-compose.prod.yml       # Production compose
│
├── 📄 .env                          # Current environment (gitignored)
├── 📄 .env.development              # Development config
├── 📄 .env.production               # Production config template
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git ignore rules
│
├── 📄 README.md                     # Main documentation
├── 📄 DEPLOY.md                     # Quick deployment guide
├── 📄 CLOUD_DEPLOYMENT.md           # Cloud platform guide
├── 📄 PROJECT_STRUCTURE.md          # This file
├── 📄 API_GUIDE.md                  # API documentation
└── 📄 FULL_STACK_GUIDE.md           # Full stack guide
```

## File Descriptions

### Backend (`app/`)

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application entry point with routes |
| `config.py` | Environment configuration and settings |
| `models.py` | Pydantic request/response models |
| `core/agent.py` | LangChain AI agent implementation |
| `core/rag.py` | ChromaDB RAG knowledge base |
| `core/session.py` | Session and chat memory management |
| `utils/logger.py` | Structured logging setup |

### Frontend (`frontend/`)

| Directory/File | Purpose |
|----------------|---------|
| `src/app/` | Next.js 14+ App Router pages |
| `src/components/` | Reusable React components |
| `src/lib/utils.ts` | Helper utilities |
| `public/` | Static assets (images, icons) |
| `package.json` | Node.js dependencies |
| `Dockerfile` | Frontend containerization |

### Infrastructure

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Local development setup |
| `docker-compose.prod.yml` | Production deployment |
| `k8s/deployment.yaml` | Kubernetes manifests |
| `nginx/nginx.conf` | Reverse proxy configuration |
| `.github/workflows/deploy.yml` | Automated CI/CD pipeline |

### Configuration

| File | Purpose |
|------|---------|
| `.env.development` | Development environment variables |
| `.env.production` | Production environment template |
| `Dockerfile.fastapi` | Backend containerization |
| `requirements.txt` | Python package dependencies |

## Key Technologies

### Backend Stack
- **Framework**: FastAPI 0.109.0
- **LLM**: Groq (Mixtral-8x7b)
- **AI Framework**: LangChain 0.2.16
- **Vector DB**: ChromaDB 0.5.5
- **Embeddings**: Sentence Transformers
- **Server**: Uvicorn with WebSocket support

### Frontend Stack
- **Framework**: Next.js 16.0.1
- **React**: 19.2.0
- **Styling**: Tailwind CSS 4
- **Animations**: GSAP 3.13, Motion 12.23
- **3D Graphics**: Three.js 0.180
- **TypeScript**: 5.x

### DevOps & Cloud
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Reverse Proxy**: Nginx
- **Cloud**: AWS, GCP, Azure ready

## Development vs Production

### Development Setup
```bash
# Uses .env.development
docker-compose up -d

# Access:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Production Setup
```bash
# Uses .env.production
docker-compose -f docker-compose.prod.yml up -d

# Includes:
# - Resource limits
# - Health checks
# - Log rotation
# - Nginx reverse proxy
# - Auto-restart policies
```

## Data Persistence

### Volumes

| Volume | Purpose | Path |
|--------|---------|------|
| `backend_data` | Application data | `/app/data` |
| `rag_data` | Vector database | `/app/loan_sales_rag.db` |
| `chat_data` | Chat history | `/app/chat_memory_loan_sales.db` |

### Database Files
- **SQLite**: `chat_memory_loan_sales.db` (session memory)
- **ChromaDB**: `loan_sales_rag.db/` (vector embeddings)

## Environment Variables

### Required for Production
```bash
GROQ_API_KEY           # Groq LLM API key
SECRET_KEY             # App secret key
NEXT_PUBLIC_API_URL    # Backend API URL
NEXT_PUBLIC_WS_URL     # WebSocket URL
ALLOWED_ORIGINS        # CORS origins
```

### Optional
```bash
REDIS_URL              # Redis for session store
RATE_LIMIT_ENABLED     # Enable rate limiting
LOG_LEVEL              # Logging verbosity
```

## Deployment Options

### 1. Docker Compose (Simple)
- Single command deployment
- Good for small to medium scale
- Easy local testing

### 2. Kubernetes (Scalable)
- Auto-scaling support
- Load balancing
- High availability
- Production-grade

### 3. Cloud Native
- **AWS**: ECS, App Runner, EKS
- **GCP**: Cloud Run, GKE
- **Azure**: Container Instances, AKS

## Security Considerations

### Secrets Management
- Never commit `.env` files
- Use cloud secrets managers in production
- Rotate API keys regularly

### Network Security
- Configure CORS properly
- Enable rate limiting
- Use HTTPS/TLS
- Implement authentication

## Monitoring & Observability

### Health Checks
- Backend: `GET /health`
- Frontend: `GET /`
- Metrics: `GET /metrics`

### Logging
- Structured JSON logs
- Log rotation enabled
- Cloud logging integration ready

## Next Steps

1. ✅ Configure `.env.production` with your secrets
2. ✅ Choose deployment platform (Docker/K8s/Cloud)
3. ✅ Follow `CLOUD_DEPLOYMENT.md` for detailed steps
4. ✅ Set up monitoring and alerting
5. ✅ Configure CI/CD pipeline

---

**Your application is now production-ready!** 🚀

