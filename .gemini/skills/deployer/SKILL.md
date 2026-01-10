---
name: CI/CD Deployer
description: 배포 파이프라인 구축 + 배포 (Monitoring & Rollback 포함)
keywords: ["배포", "deploy", "docker", "k8s", "monitoring"]
tools: ["bash", "write", "run_command"]
---

# 🚀 배포 파이프라인 및 모니터링 (Expanded)

## 🐳 1. 컨테이너 인프라 구성
```dockerfile
# Multi-stage build for thinning image
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim-bookworm
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🛠️ 2. CI/CD 워크플로우 (Actions)
- **Lint & Test**: 모든 푸시 시 실행
- **Build & Push**: Main 브랜치 병합 시 이미지 빌드
- **Deployment**: `kubectl apply` 또는 Helm Chart 업데이트

## 📈 3. 모니터링 및 알림 (Observability)
- **Logging**: ELK (Elasticsearch, Logstash, Kibana) 기반 수집
- **Metrics**: Prometheus + Grafana 대시보드
- **Alerting**: Slack/Email 연동 (Status 5xx 발생 시)

## 🔄 4. 롤백 전략 (Rollback Strategy)
- 배포 실패 시 이전 Tag의 이미지로 즉시 롤백 명령 실행:
  ```bash
  kubectl rollout undo deployment/api-server
  ```

**완료**: 실제 Production 환경 배포 완료 후 최종 헬스체크 리포트를 작성하세요.