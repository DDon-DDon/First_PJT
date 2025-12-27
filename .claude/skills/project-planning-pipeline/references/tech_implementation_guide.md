# Tech Implementation Guide (기술 구현 가이드)

웹 스크래핑 파이프라인, 데이터 스키마, 폴더 구조 등 개발 환경 구성 가이드.

## 1. 프로젝트 폴더 구조

```
{domain}-research/
├── README.md
├── pyproject.toml
│
├── config/
│   ├── keywords.seed.{domain}.v1.json
│   ├── sources.v1.json
│   ├── crawl_policies.v1.json
│   └── schema/
│       ├── keyword.schema.json
│       ├── source.schema.json
│       ├── doc.schema.json
│       ├── evidence_card.schema.json
│       └── insight.schema.json
│
├── data/
│   ├── raw/
│   │   ├── trends/
│   │   │   ├── interest_over_time.jsonl
│   │   │   └── related_queries.jsonl
│   │   └── crawl/
│   │       ├── competitor_pages.jsonl
│   │       ├── blogs_cases.jsonl
│   │       └── review_like_sources.jsonl
│   ├── normalized/
│   │   ├── docs.jsonl
│   │   ├── evidence_cards.jsonl
│   │   └── entities.jsonl
│   ├── features/
│   │   ├── pain_points.csv
│   │   ├── keyword_metrics.csv
│   │   └── competitor_matrix.csv
│   └── reports/
│       └── {date}/
│           ├── opportunity_radar.md
│           ├── risk_register.md
│           ├── mvp_requirements.md
│           └── sources_appendix.md
│
├── pipelines/
│   ├── collectors/
│   │   ├── trends_collector.py
│   │   └── scrapy_spiders/
│   │       └── research_scraper/
│   │           ├── settings.py
│   │           ├── items.py
│   │           ├── pipelines.py
│   │           └── spiders/
│   ├── normalizers/
│   │   ├── normalize_docs.py
│   │   ├── dedupe_urls.py
│   │   ├── extract_evidence_cards.py
│   │   └── enrich_entities.py
│   ├── analyzers/
│   │   ├── pain_point_mining.py
│   │   ├── keyword_trend_scoring.py
│   │   └── competitor_feature_mining.py
│   └── reporters/
│       ├── build_reports.py
│       └── templates/
│
├── scripts/
│   ├── run_all.sh
│   ├── run_trends.sh
│   ├── run_crawl.sh
│   ├── run_normalize.sh
│   ├── run_analyze.sh
│   └── run_report.sh
│
└── logs/
    ├── runs.jsonl
    └── errors.jsonl
```

## 2. JSON 스키마 정의

### Keyword 객체
```json
{
  "version": "v1",
  "domain": "{domain_name}",
  "keywords": [
    {
      "keyword_id": "kw_{domain}_{concept}",
      "text": "검색 키워드",
      "lang": "en",
      "geo": "KR",
      "tags": ["category1", "category2"],
      "intent": "solution_search|problem_space|comparison",
      "priority": 5,
      "created_at": "2025-12-27T00:00:00+09:00"
    }
  ]
}
```

### Source 객체
```json
{
  "version": "v1",
  "sources": [
    {
      "source_id": "src_{source_name}",
      "type": "api_like|web|feed",
      "base_url": "https://example.com/",
      "allowed": true,
      "notes": "ToS/robots 확인 사항"
    }
  ]
}
```

### Doc 객체 (크롤링 결과)
```json
{
  "doc_id": "doc_sha256_of_url_and_snapshot",
  "source_id": "src_blog_case",
  "url": "https://example.com/post/123",
  "retrieved_at": "2025-12-27T01:00:00+09:00",
  "title": "문서 제목",
  "published_at": null,
  "author": null,
  "language": "en",
  "content_text": "정제된 본문 텍스트...",
  "content_html_path": "data/raw/crawl/html/doc_....html",
  "keyword_refs": ["kw_concept1"],
  "tags": ["case_study", "computer_vision"],
  "crawler": {
    "name": "scrapy",
    "version": "2.x",
    "spider": "blogs_cases_spider",
    "run_id": "run_20251227_0100"
  }
}
```

### Evidence Card 객체 (핵심)
```json
{
  "evidence_id": "ev_20251227_000001",
  "claim": "기획에 인용할 주장 문장",
  "evidence_type": "review|blog|paper|pricing|forum",
  "stance": "supports|contradicts|neutral",
  "snippet": {
    "text": "1-2 문장 발췌/패러프레이즈",
    "start_char": 1200,
    "end_char": 1400
  },
  "source": {
    "doc_id": "doc_sha256_of_url_and_snapshot",
    "url": "https://example.com/post/123",
    "retrieved_at": "2025-12-27T01:00:00+09:00"
  },
  "entities": {
    "domain": "{domain_name}",
    "target_user": ["user_role1", "user_role2"],
    "pain_point": ["pain1", "pain2"],
    "job_to_be_done": ["jtbd1", "jtbd2"],
    "constraints": ["constraint1", "constraint2"]
  },
  "quality": {
    "confidence": 0.7,
    "reason": "Repeated across multiple sources"
  },
  "tags": ["mvp_relevant", "alerting"],
  "created_at": "2025-12-27T02:00:00+09:00",
  "pipeline": {
    "extractor": "extract_evidence_cards.py",
    "run_id": "run_20251227_0200"
  }
}
```

### Insight 객체
```json
{
  "insight_id": "ins_20251227_0001",
  "type": "opportunity|risk|requirement",
  "title": "인사이트 제목",
  "summary": "여러 evidence를 종합한 결론",
  "evidence_refs": ["ev_20251227_000001", "ev_20251227_000014"],
  "score": {
    "impact": 4,
    "confidence": 3,
    "effort": 2,
    "opportunity": 12
  },
  "created_at": "2025-12-27T03:00:00+09:00"
}
```

## 3. 웹 스크래핑 구현

### Scrapy 기본 설정
```python
# settings.py
BOT_NAME = "research_scraper"
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 8

FEEDS = {
    "data/raw/crawl/%(name)s.jsonl": {
        "format": "jsonlines",
        "encoding": "utf8",
    }
}
```

### 스크래핑 옵션별 도구
| 페이지 유형 | 도구 | 용도 |
|-----------|-----|-----|
| 정적 HTML | Scrapy | 가격표, 기능표, 블로그 |
| JS 렌더링 | Scrapy + Playwright | 리뷰, 무한 스크롤 |
| API 제공 | requests | 공식 데이터 |

### 컴플라이언스 체크리스트
- [ ] robots.txt 확인
- [ ] ToS(이용약관) 검토
- [ ] 수집 목적/범위 문서화
- [ ] rate limit 설정 (2초 이상 딜레이)
- [ ] 429 응답 시 감속/중단 로직
- [ ] PII(개인식별정보) 최소 수집

## 4. 파이프라인 실행 순서

### 일일/주간 루틴
```bash
# 매일: 트렌드 수집
./scripts/run_trends.sh

# 주 1회: 크롤링 → 정규화 → 분석 → 리포트
./scripts/run_crawl.sh
./scripts/run_normalize.sh
./scripts/run_analyze.sh
./scripts/run_report.sh
```

### 데이터 흐름
```
[수집] → [정규화] → [분석] → [리포트]
  │         │          │         │
  ▼         ▼          ▼         ▼
raw/    normalized/  features/  reports/
```

## 5. 저장 형식 가이드

### 초기 단계
- **JSONL**: append/증분 수집에 강함
- **CSV**: 분석 결과 export용

### 확장 단계 (데이터 증가 시)
- **SQLite/Postgres**: 중복 제거, 검색, 버전 관리 필요 시
- **Elasticsearch**: 텍스트 검색 고도화 시

### 파일 네이밍 규칙
```
{source_type}_{date}_{batch}.jsonl
예: reviews_20251227_001.jsonl
```
