---
description: 기술 구현 가이드 - 데이터 파이프라인 구축 및 MVP 기술 스택 설정
---

# 기술 구현 워크플로우

기획 단계에서 수집된 데이터를 구조화하고 시스템을 구축하기 위한 가이드입니다.

## 1. 연구용 파이프라인 폴더 구조 생성

```bash
# 프로젝트 폴더 구조 생성
mkdir -p retail-osa-research/{config,data/{raw,normalized,features},pipelines/{collectors,normalizers,analyzers},reports}

# 구조 확인
tree retail-osa-research/
```

### 폴더 구조 설명

```
retail-osa-research/
├── config/                  # 키워드 시드, 수집 정책(robots.txt)
├── data/
│   ├── raw/                 # Trends API, Scrapy 원본 (JSONL)
│   ├── normalized/          # 정규화된 문서 및 엔티티
│   └── features/            # 분석된 페인포인트 및 경쟁사 매트릭스
├── pipelines/
│   ├── collectors/          # Scrapy Spiders (Blog, Reviews, Tech)
│   ├── normalizers/         # 데이터 정제 및 Evidence Card 추출
│   └── analyzers/           # 토픽 모델링, 트렌드 스코어링
└── reports/                 # 리포트 템플릿 및 생성된 결과물
```

## 2. Evidence Card 스키마 예시

```json
{
  "evidence_id": "ev_20251227_001",
  "claim": "수동 재고 조사는 인적 오류가 빈번하며 실시간 대응이 불가능함",
  "evidence_type": "review|blog|paper",
  "snippet": "매번 손님이 물어볼 때야 물건이 없는 걸 알게 됩니다...",
  "entities": {
    "pain_point": ["manual_count", "accuracy_error"],
    "job_to_be_done": ["real_time_visibility"]
  },
  "source": { "url": "https://...", "retrieved_at": "2025-12-27" }
}
```

## 3. 웹 스크래퍼 환경 설정

```bash
# Scrapy 설치
pip install scrapy playwright

# Playwright 브라우저 설치
playwright install chromium

# 스크래퍼 프로젝트 생성
cd retail-osa-research/pipelines/collectors
scrapy startproject retail_scraper
```

### 수집 전략
- **정적 페이지:** Scrapy로 HTML 파싱 후 JSON 저장
- **동적 페이지:** Scrapy + Playwright로 JS 렌더링 대응
- **컴플라이언스:** robots.txt 준수, rate limit 설정, PII 비식별화

## 4. MVP 기술 스택 설정

```bash
# Backend 환경 설정
pip install fastapi uvicorn paho-mqtt

# Frontend 환경 설정 (React 대시보드)
npx -y create-react-app dashboard --template typescript

echo "=== MVP 기술 스택 ==="
echo "Edge: Raspberry Pi / Jetson Nano + Camera Module"
echo "Model: Lightweight CNN (물품 유무 판별)"
echo "Backend: MQTT / FastAPI"
echo "Frontend: React (대시보드 및 알림 패널)"
```

## 5. 기술 문서 확인

```bash
cat docs/tech_implementation_guide.md
```
