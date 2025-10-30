# ☁️ Cloud Deployment Guide - Esoteric AI Loan Sales Assistant

Complete guide for deploying Esoteric to major cloud platforms.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Compose Deployment](#docker-compose-deployment)
- [AWS Deployment](#aws-deployment)
- [Google Cloud Deployment](#google-cloud-deployment)
- [Azure Deployment](#azure-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Environment Configuration](#environment-configuration)
- [Security Best Practices](#security-best-practices)
- [Monitoring & Logging](#monitoring--logging)

---

## Prerequisites

### Required Tools
```bash
# Docker & Docker Compose
docker --version
docker-compose --version

# Cloud CLI tools (install as needed)
aws --version          # AWS CLI
gcloud --version       # Google Cloud SDK
az --version           # Azure CLI
kubectl --version      # Kubernetes CLI
```

### Required Secrets
- **GROQ_API_KEY**: ✅ **Hardcoded in application** - No setup needed!
- **SECRET_KEY**: Generate strong random key for production (optional)
- **Database credentials** (if using managed databases)
- **SSL certificates** (for HTTPS)

---

## Docker Compose Deployment

### Production Deployment

1. **Configure environment**
```bash
cp .env.production .env.prod
# Edit .env.prod with your production values
```

2. **Deploy with Docker Compose**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Verify deployment**
```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Test health endpoint
curl http://localhost:8000/health
```

4. **Access application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## AWS Deployment

### Option 1: AWS ECS (Elastic Container Service)

#### Step 1: Build and Push Images to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repositories
aws ecr create-repository --repository-name esoteric-backend
aws ecr create-repository --repository-name esoteric-frontend

# Build and push images
docker build -f Dockerfile.fastapi -t <account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-backend:latest .
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-backend:latest

cd frontend
docker build -t <account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-frontend:latest .
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-frontend:latest
```

#### Step 2: Create ECS Task Definition

Create `ecs-task-definition.json`:
```json
{
  "family": "esoteric-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-backend:latest",
      "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"}
      ],
      "secrets": [
        {"name": "GROQ_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:groq-api-key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/esoteric",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "backend"
        }
      }
    },
    {
      "name": "frontend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-frontend:latest",
      "portMappings": [{"containerPort": 3000, "protocol": "tcp"}],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/esoteric",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "frontend"
        }
      }
    }
  ]
}
```

#### Step 3: Deploy to ECS
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create ECS cluster
aws ecs create-cluster --cluster-name esoteric-cluster

# Create service
aws ecs create-service \
  --cluster esoteric-cluster \
  --service-name esoteric-service \
  --task-definition esoteric-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 2: AWS App Runner

```bash
# Create App Runner service for backend
aws apprunner create-service \
  --service-name esoteric-backend \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/esoteric-backend:latest",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "ENVIRONMENT": "production"
        }
      },
      "ImageRepositoryType": "ECR"
    },
    "AutoDeploymentsEnabled": true
  }' \
  --instance-configuration '{
    "Cpu": "2 vCPU",
    "Memory": "4 GB"
  }'
```

---

## Google Cloud Deployment

### Option 1: Cloud Run

#### Step 1: Build and Push to Container Registry

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push images
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/esoteric-backend -f Dockerfile.fastapi .
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/esoteric-frontend ./frontend
```

#### Step 2: Deploy to Cloud Run

```bash
# Deploy backend
gcloud run deploy esoteric-backend \
  --image gcr.io/YOUR_PROJECT_ID/esoteric-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars ENVIRONMENT=production \
  --set-secrets GROQ_API_KEY=groq-api-key:latest

# Deploy frontend
gcloud run deploy esoteric-frontend \
  --image gcr.io/YOUR_PROJECT_ID/esoteric-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --set-env-vars NEXT_PUBLIC_API_URL=https://esoteric-backend-xxx-uc.a.run.app

# Get URLs
gcloud run services list
```

### Option 2: GKE (Google Kubernetes Engine)

```bash
# Create GKE cluster
gcloud container clusters create esoteric-cluster \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --region us-central1

# Get credentials
gcloud container clusters get-credentials esoteric-cluster --region us-central1

# Deploy using kubectl
kubectl apply -f k8s/deployment.yaml
```

---

## Azure Deployment

### Option 1: Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name esoteric-rg --location eastus

# Create container registry
az acr create --resource-group esoteric-rg --name esotericacr --sku Basic
az acr login --name esotericacr

# Build and push images
docker tag esoteric-backend esotericacr.azurecr.io/esoteric-backend:latest
docker push esotericacr.azurecr.io/esoteric-backend:latest

# Deploy container group
az container create \
  --resource-group esoteric-rg \
  --name esoteric-app \
  --image esotericacr.azurecr.io/esoteric-backend:latest \
  --cpu 2 \
  --memory 4 \
  --registry-login-server esotericacr.azurecr.io \
  --registry-username $(az acr credential show --name esotericacr --query username -o tsv) \
  --registry-password $(az acr credential show --name esotericacr --query passwords[0].value -o tsv) \
  --dns-name-label esoteric-app \
  --ports 8000 \
  --environment-variables ENVIRONMENT=production
```

### Option 2: Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name esoteric-plan \
  --resource-group esoteric-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group esoteric-rg \
  --plan esoteric-plan \
  --name esoteric-backend \
  --deployment-container-image-name esotericacr.azurecr.io/esoteric-backend:latest

# Configure app settings
az webapp config appsettings set \
  --resource-group esoteric-rg \
  --name esoteric-backend \
  --settings ENVIRONMENT=production GROQ_API_KEY=your-key-here
```

---

## Kubernetes Deployment

### Step 1: Prepare Cluster

```bash
# Apply namespace and configurations
kubectl apply -f k8s/deployment.yaml

# Create secrets
kubectl create secret generic esoteric-secrets \
  --from-literal=GROQ_API_KEY=your-groq-api-key \
  --from-literal=SECRET_KEY=your-secret-key \
  -n esoteric
```

### Step 2: Deploy Application

```bash
# Deploy all resources
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n esoteric
kubectl get services -n esoteric
kubectl get ingress -n esoteric

# View logs
kubectl logs -f deployment/esoteric-backend -n esoteric
```

### Step 3: Configure Ingress (with cert-manager)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create Let's Encrypt issuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

---

## Environment Configuration

### Production Environment Variables

Create `.env.production` with:

```bash
# Note: GROQ_API_KEY is hardcoded in app/config.py - no need to set!

# Optional: Only set if you want to customize
SECRET_KEY=generate_strong_random_key_here

# API URLs (for frontend)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com

# Security (optional)
ALLOWED_ORIGINS=["https://yourdomain.com"]
RATE_LIMIT_ENABLED=true

# Environment (optional)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

---

## Security Best Practices

### 1. Secrets Management

**AWS Secrets Manager:**
```bash
aws secretsmanager create-secret \
  --name esoteric/groq-api-key \
  --secret-string "your-groq-api-key"
```

**Google Cloud Secret Manager:**
```bash
echo -n "your-groq-api-key" | gcloud secrets create groq-api-key --data-file=-
```

**Azure Key Vault:**
```bash
az keyvault create --name esoteric-kv --resource-group esoteric-rg --location eastus
az keyvault secret set --vault-name esoteric-kv --name groq-api-key --value "your-key"
```

### 2. SSL/TLS Configuration

Use Let's Encrypt with cert-manager or cloud provider SSL certificates.

### 3. Network Security

- Configure security groups/firewall rules
- Enable VPC/VNet isolation
- Use private subnets for databases
- Implement rate limiting

---

## Monitoring & Logging

### Health Checks

All deployments include health checks at:
- Backend: `http://your-domain:8000/health`
- Frontend: `http://your-domain:3000/`

### Logging

**CloudWatch (AWS):**
```bash
aws logs tail /ecs/esoteric --follow
```

**Cloud Logging (GCP):**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

**Azure Monitor:**
```bash
az monitor log-analytics query \
  --workspace esoteric-workspace \
  --analytics-query "ContainerLog | limit 50"
```

### Metrics

Access metrics at: `http://your-domain:8000/metrics`

---

## Rollback Procedures

### Docker Compose
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl rollout undo deployment/esoteric-backend -n esoteric
kubectl rollout undo deployment/esoteric-frontend -n esoteric
```

### Cloud Run
```bash
gcloud run services update-traffic esoteric-backend --to-revisions=PREVIOUS_REVISION=100
```

---

## Cost Optimization

### Recommended Configurations

**Small Scale (< 100 users/day):**
- AWS: ECS Fargate (0.5 vCPU, 1GB RAM)
- GCP: Cloud Run (1 vCPU, 1GB RAM)
- Azure: Container Instances (1 vCPU, 1.5GB RAM)
- **Estimated Cost: $30-50/month**

**Medium Scale (100-1000 users/day):**
- AWS: ECS Fargate (1 vCPU, 2GB RAM) x2
- GCP: Cloud Run (2 vCPU, 2GB RAM) autoscale 1-10
- Azure: App Service (B2 tier)
- **Estimated Cost: $100-200/month**

**Large Scale (1000+ users/day):**
- Kubernetes cluster with autoscaling
- Load balancers
- Managed databases
- **Estimated Cost: $500+/month**

---

## Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
kubectl logs deployment/esoteric-backend -n esoteric

# Check environment variables
kubectl describe pod <pod-name> -n esoteric
```

**API connectivity issues:**
- Verify security groups/firewall rules
- Check CORS configuration
- Validate environment variables

**Performance issues:**
- Increase CPU/memory limits
- Enable horizontal pod autoscaling
- Check Groq API rate limits

---

## Support & Resources

- **GitHub Actions**: Automated CI/CD configured in `.github/workflows/deploy.yml`
- **Kubernetes**: Full manifests in `k8s/deployment.yaml`
- **Docker Compose**: Production config in `docker-compose.prod.yml`
- **Nginx**: Reverse proxy config in `nginx/nginx.conf`

---

## Quick Deploy Commands

### AWS ECS Fargate
```bash
./scripts/deploy-aws.sh
```

### Google Cloud Run
```bash
./scripts/deploy-gcp.sh
```

### Azure Container Instances
```bash
./scripts/deploy-azure.sh
```

### Kubernetes (any cluster)
```bash
kubectl apply -f k8s/deployment.yaml
```

---

**Ready to deploy! Choose your cloud platform and follow the guide above.** ☁️

