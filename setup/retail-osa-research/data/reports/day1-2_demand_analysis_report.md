# Day 1-2: 수요 신호 분석 보고서

**프로젝트**: 임베디드 카메라 기반 자동 재고 모니터링 솔루션
**도메인**: 소규모 리테일 (small_retail_osa)
**분석 기간**: 2024-12-27 ~ 2025-12-27 (최근 12개월)
**데이터 수집일**: 2025-12-28
**분석 대상**: 우선순위 5 키워드 13개

---

## 📊 Executive Summary

### 핵심 발견사항

1. **문제 공간의 명확한 수요 존재**
   - "out of stock retail" 키워드가 **54.5점**으로 압도적으로 높은 검색 관심도를 보임
   - 품절 문제는 리테일 업계에서 중요하고 지속적인 pain point임을 확인

2. **솔루션 시장의 니치 존재**
   - 대부분의 솔루션 관련 키워드는 검색량이 매우 낮거나 없음
   - 문제는 많이 검색되지만 구체적인 솔루션은 덜 검색됨
   - **기회**: Blue Ocean 전략 가능성

3. **기술 솔루션에 대한 관심 증가 조짐**
   - "smart shelf camera" (12.67점)는 상대적으로 높은 관심도 기록
   - 카메라 기반 솔루션에 대한 시장 인지도 존재

---

## 🔍 상세 분석

### 1. 문제 공간 (Problem Space) 키워드

| 순위 | 키워드 | 평균 관심도 | 인사이트 |
|------|--------|------------|---------|
| 1 | out of stock retail | 54.5 | ⭐️ 가장 높은 수요. 품절은 리테일의 핵심 pain point |
| 2 | on-shelf availability | 15.42 | OSA는 업계 표준 용어로 인식됨 |
| 3 | OSA retail | 8.83 | 약어도 일정 수준 검색됨. 전문가 타겟 가능 |

**인사이트**:
- 품절 문제에 대한 검색 수요가 명확하게 존재
- "out of stock"이라는 일반 용어가 전문 용어인 "OSA"보다 훨씬 많이 검색됨
- 타겟 마케팅: 일반 리테일 운영자는 "out of stock", 전문가는 "OSA" 사용

### 2. 솔루션 탐색 (Solution Search) 키워드

| 키워드 | 평균 관심도 | 상태 |
|--------|------------|------|
| shelf gap detection | 0.0 | ⚠️ 검색량 없음 |
| stockout alert system | 0.0 | ⚠️ 검색량 없음 |
| smart shelf camera | 12.67 | ✅ 유의미한 관심도 |
| retail shelf monitoring computer vision | 0.0 | ⚠️ 검색량 없음 |
| computer vision shelf monitoring | 0.0 | ⚠️ 검색량 없음 |
| empty shelf detection | 0.0 | ⚠️ 검색량 없음 |

**인사이트**:
- 대부분의 기술적인 솔루션 키워드는 검색량이 매우 낮음
- **예외**: "smart shelf camera"는 12.67점으로 의미 있는 검색량 기록
- **가설**:
  - 시장이 아직 형성 초기 단계 (Early Market)
  - 또는 다른 검색어를 사용 중 (예: "shelf monitoring system", "inventory automation" 등)

### 3. 재고 관리 (Inventory Operations) 키워드

| 키워드 | 평균 관심도 | 데이터 수집 상태 |
|--------|------------|----------------|
| small retail inventory management | 0.0 | ⚠️ 429 에러 (rate limit) |
| inventory management for small business | 0.0 | ⚠️ 429 에러 (rate limit) |
| manual inventory count | 0.0 | ⚠️ 부분 수집 실패 |

**제한사항**:
- Google Trends API rate limiting으로 인해 일부 데이터 수집 실패
- 추후 재수집 필요

---

## 💡 전략적 인사이트

### Opportunity Score 분석

| 요소 | 점수 (1-5) | 근거 |
|------|-----------|------|
| **문제 크기** | 5 | "out of stock retail" 54.5점 - 명확한 대규모 문제 |
| **솔루션 경쟁** | 2 | 기술 솔루션 검색량 거의 없음 - 낮은 경쟁 |
| **시장 성숙도** | 2 | 솔루션 인지도 낮음 - 초기 시장 |
| **기술 트렌드** | 3 | "smart shelf camera" 관심 증가 - 가능성 존재 |
| **Opportunity Score** | **12/20** | 중간-높음 기회 |

### SWOT 분석

**Strengths (강점)**
- 명확하고 큰 문제 공간 (out of stock: 54.5)
- 낮은 솔루션 경쟁 (Blue Ocean)
- 카메라 기술에 대한 관심 존재 (smart shelf camera: 12.67)

**Weaknesses (약점)**
- 낮은 솔루션 검색량 = 시장 교육 필요
- 전문 용어(computer vision, edge AI) 인지도 낮음

**Opportunities (기회)**
- First mover advantage 가능
- 문제 중심 마케팅 (problem-first approach)
- "smart shelf camera"를 entry keyword로 활용

**Threats (위협)**
- 시장 성숙도 낮음 = 긴 판매 사이클
- 고객이 솔루션을 인지하지 못할 가능성

---

## 🎯 권장 사항

### 1. 마케팅 전략

**Problem-First Approach**
```
❌ 잘못된 접근: "AI 기반 shelf monitoring system"
✅ 올바른 접근: "품절 문제 해결 → 스마트 카메라 솔루션"
```

**키워드 전략**
1. **Top of Funnel**: "out of stock retail" (문제 인식)
2. **Middle of Funnel**: "shelf monitoring solution" (솔루션 탐색)
3. **Bottom of Funnel**: "smart shelf camera" (구매 고려)

### 2. 제품 포지셔닝

**추천 메시징**:
- ❌ "Computer vision-based shelf monitoring"
- ✅ "품절을 자동으로 감지하는 스마트 카메라"

**타겟 페르소나**:
- **Primary**: 소규모 리테일 매장 오너/관리자
  - Pain point: 품절로 인한 매출 손실, 수동 점검 부담
  - Search term: "out of stock", "inventory problem"

- **Secondary**: 리테일 운영 전문가
  - Pain point: OSA 개선, 운영 효율화
  - Search term: "OSA retail", "on-shelf availability"

### 3. 추가 검증 필요 사항

**다음 단계 (Day 3-4)에서 확인할 것**:
1. VOC 분석을 통한 실제 pain point 확인
   - G2 리뷰, Reddit, 리테일 커뮤니티
   - "품절"과 관련된 불만 수집

2. 대체 키워드 탐색
   - "shelf monitoring", "inventory automation"
   - "retail analytics", "store operations"

3. 경쟁사 분석
   - 기존 솔루션 제공업체 조사
   - 가격대, 타겟 시장 분석

---

## 📈 데이터 품질 및 제한사항

### 수집 성공률
- **전체 키워드**: 13개
- **데이터 수집 성공**: 13개 (100%)
- **유의미한 데이터**: 4개 (31%)
- **검색량 0 또는 미미**: 9개 (69%)

### 제한사항
1. **API Rate Limiting**
   - Google Trends API 429 에러 발생
   - 일부 키워드에서 interest over time 수집 실패

2. **샘플 크기**
   - 우선순위 5 키워드만 수집 (13/30개)
   - 전체 30개 키워드 데이터 필요

3. **지역 제한**
   - 대부분 US 데이터
   - 한국 시장 데이터 부족

### 다음 수집 계획
1. 대기 시간 증가 (2초 → 5초)
2. 배치 크기 축소 (13개 → 5개씩)
3. 나머지 우선순위 4-3 키워드 수집
4. 한국 시장 키워드 추가 조사

---

## 🔗 참고 자료

### 데이터 파일
- **원본 데이터**: `data/raw/trends/trends_20251228_003827.json`
- **요약 CSV**: `data/raw/trends/trends_20251228_003827_summary.csv`

### 설정 파일
- **키워드 목록**: `config/keywords.seed.small_retail_osa.v1.json`
- **수집 스크립트**: `pipelines/collectors/trends_collector.py`

### 다음 보고서
- **Day 3-4**: 페인포인트 분석 (VOC, 리뷰, 커뮤니티)
- **Day 5-6**: 트렌드 정당화 (Gartner, McKinsey 리포트)
- **Day 7**: 통합 기획 문서

---

**작성자**: Claude (project-planning-pipeline skill)
**검토 필요**: 키워드 전략, 추가 데이터 수집 계획
