# **기술 구현 가이드: 데이터 파이프라인 및 아키텍처**

기획 단계에서 수집된 데이터를 구조화하고, 실제 시스템을 구축하기 위한 기술적 가이드라인입니다.

## **1. 연구용 파이프라인 폴더 구조**

retail-osa-research/

├── config/                  # 키워드 시드, 수집 정책(robots.txt)

├── data/

│   ├── raw/                 # Trends API, Scrapy 원본 (JSONL)

│   ├── normalized/          # 정규화된 문서 및 엔티티

│   └── features/            # 분석된 페인포인트 및 경쟁사 매트릭스

├── pipelines/

│   ├── collectors/          # Scrapy Spiders (Blog, Reviews, Tech)

│   ├── normalizers/         # 데이터 정제 및 Evidence Card 추출

│   └── analyzers/           # 토픽 모델링, 트렌드 스코어링

└── reports/                 # 리포트 템플릿 및 생성된 결과물

## **2. 핵심 데이터 스키마 (JSON)**

### **2.1 Evidence Card**

기획서에 즉시 인용할 수 있는 '증거'의 최소 단위입니다.

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

## **3. 웹 스크래퍼 및 수집 전략**

- **정적 페이지:** Scrapy를 활용해 HTML 파싱 후 JSON 저장.
- **동적 페이지:** Scrapy + Playwright를 활용해 JS 렌더링 대응.
- **컴플라이언스:** robots.txt 준수, rate limit 설정, PII(개인정보) 비식별화 필수.

## **4. MVP 기술 스택**

- **Edge:** Raspberry Pi / Jetson Nano + Camera Module.
- **Model:** Lightweight CNN (물품 유무 판별).
- **Backend:** MQTT / FastAPI.
- **Frontend:** React (대시보드 및 알림 패널).