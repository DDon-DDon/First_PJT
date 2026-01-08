---
name: CI/CD Deployer
description: Docker 기반 배포 파이프라인 구축 및 모니터링 설정
keywords: ["배포", "deploy", "docker", "k8s", "ci/cd", "컨테이너", "production"]
tools: ["bash", "write", "read"]
---

# 배포 파이프라인 및 인프라 구성

**프로젝트**: DoneDone 재고 관리 시스템
**배포 전략**: Docker Compose (dev) → Kubernetes (prod)

## 1. Docker 컨테이너화

### Dockerfile (Multi-stage Build)

**위치**: `backend/Dockerfile`

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.pytest_cache/
.coverage
htmlcov/
.env
.env.local
*.db
*.sqlite
.git/
.gitignore
README.md
tests/
docs/
```

### Docker Build & Run
```bash
# Build image
cd backend
docker build -t donedone-api:latest .

# Run container
docker run -d \
    --name donedone-api \
    -p 8000:8000 \
    -e DATABASE_URL="postgresql+asyncpg://user:pass@db:5432/donedone" \
    -e SECRET_KEY="your-secret-key-min-32-chars" \
    -e ALLOWED_ORIGINS="http://localhost:3000" \
    donedone-api:latest

# Check logs
docker logs -f donedone-api

# Health check
curl http://localhost:8000/health
```

## 2. Docker Compose (Development)

**위치**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:16-alpine
    container_name: donedone-db
    environment:
      POSTGRES_USER: donedone
      POSTGRES_PASSWORD: donedone123
      POSTGRES_DB: donedone
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/init-db:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U donedone"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: donedone-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Backend
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: donedone-api
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: "postgresql+asyncpg://donedone:donedone123@db:5432/donedone"
      SECRET_KEY: "${SECRET_KEY:-dev-secret-key-please-change-in-production}"
      ALLOWED_ORIGINS: "http://localhost:3000,http://localhost:5173"
      REDIS_URL: "redis://redis:6379/0"
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app  # Hot reload for development
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Next.js Frontend (optional)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: donedone-frontend
    depends_on:
      - api
    environment:
      NEXT_PUBLIC_API_BASE_URL: "http://api:8000/api/v1"
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next

volumes:
  postgres_data:

networks:
  default:
    name: donedone-network
```

### 실행 명령어
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Database migration
docker-compose exec api alembic upgrade head

# Run tests in container
docker-compose exec api pytest app/tests/
```

## 3. GitHub Actions CI/CD

**위치**: `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/donedone-api

jobs:
  # Job 1: Test
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run pytest
        run: |
          cd backend
          pytest app/tests/ -v --cov=app --cov-report=xml --cov-fail-under=80

      - name: Run bandit (security scan)
        run: |
          cd backend
          bandit -r app/ -ll --exit-zero

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  # Job 2: Build & Push Docker Image
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  # Job 3: Deploy to Production (optional)
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

## 4. Kubernetes 배포 (Production)

### Deployment
**위치**: `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: donedone-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: donedone-api
  template:
    metadata:
      labels:
        app: donedone-api
    spec:
      containers:
      - name: api
        image: ghcr.io/your-org/donedone-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: donedone-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: donedone-secrets
              key: jwt-secret
        - name: ALLOWED_ORIGINS
          value: "https://donedone.example.com"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service
**위치**: `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: donedone-api
  namespace: production
spec:
  selector:
    app: donedone-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: donedone-ingress
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.donedone.example.com
    secretName: donedone-tls
  rules:
  - host: api.donedone.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: donedone-api
            port:
              number: 80
```

### Secrets
```bash
# Create secrets in Kubernetes
kubectl create secret generic donedone-secrets \
  --from-literal=database-url='postgresql+asyncpg://user:pass@postgres:5432/db' \
  --from-literal=jwt-secret='your-super-secret-key-min-32-chars' \
  -n production

# Verify secrets
kubectl get secrets -n production
```

## 5. 모니터링 및 로깅

### Prometheus + Grafana (선택적)
```yaml
# k8s/monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: donedone-api
spec:
  selector:
    matchLabels:
      app: donedone-api
  endpoints:
  - port: metrics
    interval: 30s
```

### Application Metrics
```python
# backend/app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)  # /metrics endpoint
```

### Logging (Structured)
```python
import logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()
logger.info("comment_created", comment_id=str(comment.id), post_id=str(post.id))
```

## 6. 롤백 전략

### Docker Compose
```bash
# Rollback to previous version
docker-compose down
docker pull donedone-api:previous-tag
docker-compose up -d
```

### Kubernetes
```bash
# Rollback deployment
kubectl rollout undo deployment/donedone-api -n production

# Check rollout status
kubectl rollout status deployment/donedone-api -n production

# View rollout history
kubectl rollout history deployment/donedone-api -n production
```

## 7. 환경 변수 체크리스트

### 필수 환경 변수 (.env)
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Security
SECRET_KEY=your-secret-key-min-32-chars-required
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=https://donedone.example.com,https://www.donedone.example.com

# Redis (optional)
REDIS_URL=redis://redis:6379/0

# Monitoring (optional)
SENTRY_DSN=https://...
```

### .env.example 파일
```bash
# Copy this file to .env and fill in your values
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/donedone
SECRET_KEY=change-me-to-a-secure-random-key
ALLOWED_ORIGINS=http://localhost:3000
REDIS_URL=redis://localhost:6379/0
```

## 8. 배포 완료 체크리스트

### 배포 전
- [ ] 모든 테스트 통과 (pytest, coverage 80%+)
- [ ] 보안 스캔 통과 (bandit, pip-audit)
- [ ] Docker 이미지 빌드 성공
- [ ] .env 파일 설정 완료
- [ ] Database migration 준비 (alembic)

### 배포 후
- [ ] Health check 통과 (`/health` endpoint)
- [ ] API 엔드포인트 정상 동작 (`/api/v1/docs`)
- [ ] Database connection 확인
- [ ] Redis connection 확인 (optional)
- [ ] Logs 확인 (에러 없음)
- [ ] Monitoring dashboard 확인

### 롤백 준비
- [ ] 이전 버전 이미지 보관
- [ ] Rollback 명령어 준비
- [ ] Database backup 완료

## 다음 단계

**배포 성공 시**:
```
✅ Production 배포 완료

배포 정보:
- Image: ghcr.io/your-org/donedone-api:latest
- Replicas: 3
- Health Check: ✅ Passing
- API Docs: https://api.donedone.example.com/docs

모니터링:
- Logs: kubectl logs -f deployment/donedone-api -n production
- Metrics: https://grafana.donedone.example.com

다음: 모니터링 대시보드 확인 및 사용자 피드백 수집
```

**배포 실패 시**:
```
❌ 배포 실패

문제:
- Health check 실패 (503 Service Unavailable)

조치:
1. Logs 확인: docker logs donedone-api
2. Database connection 검증
3. 환경 변수 확인
4. Rollback: kubectl rollout undo deployment/donedone-api

다음: 문제 수정 후 재배포
```
