# 프로젝트 기획 파이프라인 Skill - 세션 핸드오프 문서

## 📋 프로젝트 개요

**목적**: 데이터 기반으로 프로젝트 아이디어를 검증하고 기획 근거를 확보하는 Claude Skill 개발

**배경**: 사용자가 "임베디드 카메라 기반 자동 재고 모니터링 솔루션" 아이디어에 대해 수요 검증, 페인포인트 분석, 기술 가능성 판단을 위한 체계적인 분석 프레임워크가 필요했음. 이를 재사용 가능한 Claude Skill로 패키징함.

---

## 🎯 핵심 프레임워크: 3축 데이터 분석

기획 검증 데이터는 3개 축으로 수집하여 분석:

| 축 | 목적 | 주요 소스 |
|---|---|---|
| **수요 신호** | 사람들이 찾는가? | Google Trends, 키워드 플래너 |
| **불만 신호** | 어디가 아픈가? | G2 리뷰, 커뮤니티, VOC |
| **공급/기술 신호** | 가능한가? | 기술 문서, 논문, 경쟁사 분석 |

---

## 📁 생성된 Skill 구조

```
project-planning-pipeline/
├── SKILL.md                              # 메인 가이드 (트리거 + 핵심 프레임워크)
├── references/
│   ├── analysis_methodology.md           # 3축 분석 방법론 상세
│   ├── tech_implementation_guide.md      # 웹 스크래핑 파이프라인, JSON 스키마
│   └── domain_small_retail.md            # 소규모 리테일 특화 키워드 30개 + KPI
├── assets/
│   ├── keywords.seed.small_retail.sample.json  # 키워드 시드 템플릿
│   └── evidence_card.schema.json         # Evidence Card JSON 스키마
└── scripts/
    └── init_project.py                   # 프로젝트 폴더 구조 초기화 스크립트
```

---

## 📄 각 문서 상세 내용

### 1. SKILL.md (메인 가이드)

**트리거 조건**: 새로운 프로젝트/솔루션 아이디어 검증, MVP 방향 수립, 시장 수요/페인포인트 분석, 웹 스크래핑 기반 근거 수집, 기획서/PRD 작성

**핵심 내용**:
- 3축 데이터 분석 프레임워크 요약
- 1주 실행 템플릿 (Day 1-7)
- 참조 문서 안내 및 링크
- 산출물 유형별 활용 가이드 (MVP 기획서, PRD, 기술 리스크 레지스터)

### 2. analysis_methodology.md (분석 방법론)

**내용**:
- Google Trends 활용법 (키워드 구성 전략, intent 태그)
- 키워드 플래너 활용법 (상업성 판별)
- 대체 VOC 확보 방법 (제품 없이 페인포인트 검증)
- 텍스트 마이닝 기법 (TF-IDF, k-means, 감성분석, 토픽모델링)
- Pain Point 분류 체계
- 트렌드 리포트 활용 (Gartner, McKinsey, CB Insights)
- 기술 리스크 레지스터 작성법
- Opportunity 스코어링 공식
- Evidence Card 작성법
- Evidence → Insight 변환 방법

### 3. tech_implementation_guide.md (기술 구현 가이드)

**내용**:
- 프로젝트 폴더 구조 (config, data, pipelines, scripts, logs)
- JSON 스키마 정의:
  - Keyword 객체
  - Source 객체
  - Doc 객체 (크롤링 결과)
  - Evidence Card 객체 (핵심)
  - Insight 객체
- 웹 스크래핑 구현 (Scrapy 설정, 도구 선택)
- 컴플라이언스 체크리스트
- 파이프라인 실행 순서
- 저장 형식 가이드 (JSONL, CSV, SQLite)

### 4. domain_small_retail.md (소규모 리테일 도메인)

**내용**:
- 도메인 핵심 문제 (OOS, 보충 지연, 수동 점검)
- 초기 키워드 30개 세트 (OSA·품절 10개, 재고/운영 10개, 비전/카메라 10개)
- Evidence Card 엔티티 템플릿
- 도메인 특화 KPI (OOS Rate, Shelf Gap Time, Replenishment Time 등)
- MVP 시나리오 (품절 알림 흐름)
- MVP 요구사항 후보
- 기술 리스크 레지스터 (조명 변화, 상품 가림, 네트워크 지연 등)
- 경쟁사/대체재 분석 포인트
- 소스 수집 우선순위

---

## 🔧 주요 스키마 정의

### Evidence Card (핵심 데이터 단위)

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
    "domain": "small_retail_osa",
    "target_user": ["store_owner", "store_manager"],
    "pain_point": ["stockout", "manual_shelf_check"],
    "job_to_be_done": ["keep_shelves_full", "reduce_lost_sales"],
    "constraints": ["low_budget", "minimal_install_time"]
  },
  "quality": {
    "confidence": 0.7,
    "reason": "Repeated across multiple sources"
  },
  "tags": ["mvp_relevant", "alerting"],
  "created_at": "2025-12-27T02:00:00+09:00"
}
```

### Insight (분석 결과)

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
  }
}
```

---

## 📊 1주 실행 템플릿

| Day | 활동 | 산출물 |
|-----|-----|-------|
| 1-2 | Google Trends로 상승 주제 10개 추출, 키워드 플래너로 상업성 정리 | 키워드 목록 |
| 3-4 | 리뷰/VOC 텍스트 수집, 반복 불만 Top N 도출 | Pain Point 목록 |
| 5-6 | Gartner/McKinsey 리포트 참조, "왜 지금" 근거 확보 | 트렌드 근거 |
| 7 | 페인포인트 → 원인 가설 → 해결안 → KPI 정리 | 기획 문서 |

---

## 🚀 사용 방법

1. **Skill 등록**: `.skill` 파일을 Claude에 업로드하여 skill로 등록
2. **자동 트리거**: 프로젝트 기획/MVP 검증/수요 분석 관련 질문 시 자동 활성화
3. **프로젝트 초기화**: `init_project.py`로 실제 리서치 프로젝트 폴더 구조 생성

```bash
python init_project.py retail-osa-research --domain small_retail_osa --path ./projects
```

---

## 📝 추가 개발 가능 영역

1. **다른 도메인 참조 문서 추가**: 실험실 시약장, 공구실, 물류창고 등
2. **자동화 스크립트 강화**: trends_collector.py, pain_point_mining.py 등 구현체 추가
3. **리포트 템플릿**: Jinja2 기반 opportunity_radar.md.j2, risk_register.md.j2 등
4. **MCP 서버 연동**: Google Trends API, G2 리뷰 수집 등 자동화

---

## 📎 원본 대화 컨텍스트

- **사용자 목표**: 임베디드 카메라 기반 자동 재고 모니터링 솔루션의 기획 검증
- **MVP 정의**: 특정 위치에 물품이 "있다/없다" 판별 + 웹 관리자 페이지 + 재고 부족 알림
- **타겟 도메인**: 소규모 쇼핑몰/오프라인 매장 (편의점급, 동네 마트, 소형 리테일)
- **핵심 문제**: 진열대 품절(OOS), 보충 지연, 수동 점검 비용/오류

---

## 🔗 파일 위치

- **패키징된 Skill**: `project-planning-pipeline.skill`
- **개별 문서**: `project-planning-pipeline/` 폴더 내 각 파일

이 문서를 새 Claude 세션에 전달하면 전체 컨텍스트를 이해하고 이어서 작업할 수 있습니다.