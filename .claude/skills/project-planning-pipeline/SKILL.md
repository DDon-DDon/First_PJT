---
name: project-planning-pipeline
description: 데이터 기반 프로젝트 기획 검증 파이프라인 가이드. 솔루션 아이디어의 수요 검증, 페인포인트 분석, 기술 가능성 판단을 위한 체계적인 분석 프레임워크 제공. (1) 새로운 프로젝트/솔루션 아이디어 검증, (2) MVP 방향 수립, (3) 시장 수요/페인포인트 분석, (4) 웹 스크래핑 기반 근거 수집, (5) 기획서/PRD 작성을 위한 데이터 기반 근거 확보 시 사용.
license: MIT
---

# Project Planning Pipeline

데이터 기반으로 프로젝트 아이디어를 검증하고 기획 근거를 확보하는 파이프라인 가이드.

## 핵심 프레임워크: 3축 데이터 분석

기획 검증 데이터는 3개 축으로 수집하여 분석:

| 축 | 목적 | 주요 소스 |
|---|---|---|
| **수요 신호** | 사람들이 찾는가? | Google Trends, 키워드 플래너 |
| **불만 신호** | 어디가 아픈가? | G2 리뷰, 커뮤니티, VOC |
| **공급/기술 신호** | 가능한가? | 기술 문서, 논문, 경쟁사 분석 |

## 1주 실행 템플릿

### Day 1-2: 문제 후보 선정
- Google Trends로 상승 주제 10개 추출
- 키워드 플래너로 상업성/키워드 묶음 정리

### Day 3-4: 페인포인트 추출
- 리뷰/문의/VOC 텍스트 수집
- 빈도/감성/군집으로 "반복 불만 Top N" 도출

### Day 5-6: 트렌드로 정당화
- Gartner/McKinsey/CB Insights 리포트 참조
- "왜 지금 가능한가/필요한가" 근거 확보

### Day 7: 기획 산출물 변환
- "페인포인트 → 원인 가설 → 해결안 → KPI" 형태로 정리

## 관련 참조 문서

상세 내용은 `references/` 폴더의 문서 참조:

- **[analysis_methodology.md](references/analysis_methodology.md)**: 3축 분석 방법론 상세, 키워드 전략, VOC 분석 기법
- **[tech_implementation_guide.md](references/tech_implementation_guide.md)**: 웹 스크래핑 파이프라인, JSON 스키마, 폴더 구조
- **[domain_small_retail.md](references/domain_small_retail.md)**: 소규모 리테일 도메인 특화 키워드 30개 세트, KPI, 시나리오

## 산출물 유형별 활용

### MVP 기획서
1. `analysis_methodology.md`로 수요/페인포인트 분석
2. `tech_implementation_guide.md`의 Evidence Card 스키마로 근거 정리
3. 도메인별 참조 문서로 키워드/KPI 설정

### PRD 작성
1. Evidence Card에서 claim + snippet 추출
2. Insight 객체로 기회/리스크/요구사항 구조화
3. 문장 + 출처 형태로 PRD에 인용

### 기술 리스크 레지스터
1. 기술 가능성 축 데이터에서 실패 요인 추출
2. "가정 → 검증 실험 → 완화책" 형태로 문서화

## 키워드
프로젝트 기획, MVP, 수요 검증, 페인포인트, VOC 분석, Google Trends, 키워드 플래너, 웹 스크래핑, PRD, 기획서, 시장 분석, 경쟁 분석, 기술 검증
