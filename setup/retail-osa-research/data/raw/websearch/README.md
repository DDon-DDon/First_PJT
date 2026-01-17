# WebSearch Results - Day 3-4 v1.0

## 데이터 수집 방법론

**수집 도구**: Claude Code의 WebSearch 도구
**수집 일시**: 2025-12-28
**데이터 특성**: 2차 자료 (Secondary Sources)

## 중요 제한사항

⚠️ **이 데이터는 1차 자료가 아닙니다**

- WebSearch 도구를 통해 수집된 데이터는 **일시적(ephemeral)** 특성을 가짐
- 원본 HTML, JSON 등의 raw data가 저장되지 않음
- 검색 결과의 스냅샷만 보고서에 반영됨
- 재현성(reproducibility)이 보장되지 않음

## v1.0에서 수집한 정보 출처

### 1. G2 리뷰 정보
- **수집 방법**: WebSearch를 통한 간접 수집
- **한계**:
  - 실제 G2 플랫폼 크롤링 없음
  - 리뷰 원문 미보관
  - 통계적 분석 불가능

### 2. Reddit 커뮤니티 정보
- **수집 방법**: WebSearch를 통한 간접 수집
- **한계**:
  - Reddit API 사용 안 함
  - 게시물 원문 미보관
  - 시계열 분석 불가능
  - 커뮤니티 sentiment 정량화 불가

### 3. Amazon 리뷰 정보
- **수집 방법**: WebSearch를 통한 간접 수집
- **한계**:
  - 웹 스크래핑 없음
  - 리뷰 데이터 미보관
  - 별점 통계 분석 불가능

## v2.0 개선 계획

다음 데이터 수집기들을 구현하여 1차 자료 확보 예정:

### 1. Reddit Collector (`reddit_collector.py`)
- **도구**: PRAW (Python Reddit API Wrapper)
- **타겟 서브레딧**:
  - r/retailmanagement
  - r/smallbusiness
  - r/inventory
- **수집 데이터**:
  - 게시물 제목, 본문, 점수, 댓글 수
  - 작성 시간, 작성자 (익명화)
  - 댓글 내용
- **저장 형식**: JSONL (한 줄당 하나의 게시물)
- **파일 경로**: `data/raw/reddit/posts_YYYYMMDD_HHMMSS.jsonl`

### 2. G2 Web Scraper (`g2_scraper.py`)
- **도구**: Scrapy 또는 BeautifulSoup + Requests
- **타겟 제품**:
  - Inventory management software
  - Shelf monitoring solutions
  - Retail analytics platforms
- **수집 데이터**:
  - 리뷰 제목, 본문, 별점
  - 리뷰어 회사 규모, 산업군
  - Pros/Cons
  - 작성 날짜
- **저장 형식**: JSON
- **파일 경로**: `data/raw/g2/reviews_YYYYMMDD_HHMMSS.json`
- **주의사항**: G2 ToS 준수, robots.txt 확인 필요

### 3. Amazon Review Collector (`amazon_scraper.py`)
- **도구**: Scrapy + Selenium (동적 콘텐츠 처리)
- **타겟 제품**:
  - 소규모 리테일용 inventory scanners
  - Shelf cameras
  - Smart shelf systems
- **수집 데이터**:
  - 리뷰 제목, 본문, 별점
  - Verified Purchase 여부
  - 작성 날짜
  - Helpful votes
- **저장 형식**: JSON
- **파일 경로**: `data/raw/amazon/reviews_YYYYMMDD_HHMMSS.json`
- **주의사항**: Amazon ToS 준수, rate limiting 고려

## 데이터 저장 규칙

### 파일명 컨벤션
```
{source}_{content_type}_{YYYYMMDD}_{HHMMSS}.{ext}
```

예시:
- `reddit_posts_20251228_120000.jsonl`
- `g2_reviews_20251228_120500.json`
- `amazon_reviews_20251228_121000.json`

### 메타데이터 포함
모든 수집 파일은 다음 메타데이터를 포함해야 함:
```json
{
  "collected_at": "2025-12-28T12:00:00",
  "collector_version": "v1.0",
  "source": "reddit|g2|amazon",
  "target": "subreddit_name|product_id|asin",
  "total_items": 0,
  "data": []
}
```

## Evidence Card Schema

수집된 데이터는 다음 Evidence Card 형식으로 변환됨:
```json
{
  "claim_id": "pain_001",
  "claim": "소규모 리테일은 수동 재고 확인으로 인한 인건비 부담이 크다",
  "evidence_type": "customer_review|community_post|expert_opinion",
  "source": "reddit|g2|amazon",
  "source_url": "https://...",
  "quote": "원문 인용",
  "sentiment": "negative|neutral|positive",
  "author_type": "small_business_owner|retail_manager|...",
  "collected_at": "2025-12-28T12:00:00",
  "relevance_score": 0.85
}
```

---

**작성자**: Claude (project-planning-pipeline skill)
**작성일**: 2025-12-28
**버전**: v1.0
