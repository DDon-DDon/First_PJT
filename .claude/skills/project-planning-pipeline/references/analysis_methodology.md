# Analysis Methodology (분석 방법론)

3축 데이터 분석의 상세 방법론과 실행 가이드.

## 1. 수요 신호 분석

### Google Trends 활용
- **목적**: 키워드 관심도의 변화/시점/지역 편중 확인
- **활용법**: 지역(geo)과 기간(timeframe)을 고정하여 시계열 저장
- **주의점**: 상대지표이므로 반복 조회/전처리로 안정화 필요

**키워드 구성 전략**:
```
시드 키워드 = "도메인 용어" + "고통 표현(수동, 오류, 누락)"
```

예시 intent 태그:
- `solution_search`: 솔루션을 찾는 검색
- `problem_space`: 문제 영역 탐색
- `comparison`: 비교/평가 의도

### 키워드 플래너 활용
- **목적**: 검색량과 CPC(상업성)로 "돈이 걸린 문제인지" 판별
- **팁**: 고통이 드러나는 문장형 키워드 포함
  - "manual inventory spreadsheet"
  - "stockout alert system"

## 2. 불만 신호 분석 (대체 VOC)

### 제품 없이 VOC 확보하기
- **G2, Capterra 등 리뷰 사이트**: 경쟁 제품의 Cons/불만 수집
- **Reddit, 커뮤니티**: 실제 사용자 토론에서 반복 불만 추출
- **블로그/케이스 스터디**: 실패 사례에서 pain point 도출

### 텍스트 마이닝 기법
| 기법 | 용도 |
|-----|-----|
| TF-IDF | 키워드 빈도/중요도 추출 |
| k-means 군집화 | 유사 불만 그룹핑 |
| 감성 분석 | 부정/긍정 분류 |
| 토픽 모델링 | 주제별 불만 구조화 |

### Pain Point 분류 체계
```json
{
  "pain_point": ["manual_count", "stockout_risk", "data_sync_delay"],
  "job_to_be_done": ["know_stock_level", "prevent_stockout"],
  "workaround": ["spreadsheet", "periodic_check"]
}
```

## 3. 공급/기술 신호 분석

### 트렌드 리포트 활용
- **Gartner**: "2025년 10대 전략 기술 트렌드" - 배경 근거
- **McKinsey**: "Technology Trends Outlook" - 산업 임팩트 관점
- **CB Insights**: "Tech Trends" - 투자/스타트업 동향

### 기술 리스크 레지스터 작성
| 리스크 요인 | 가정 | 검증 실험 | 완화책 |
|------------|-----|---------|-------|
| 조명 변화 | 자연광 환경 | 다양한 조명 조건 테스트 | HDR 촬영, 조명 보정 |
| 물품 가림 | 정면 배치 | 겹침 시나리오 테스트 | 다중 카메라, 각도 조정 |
| 네트워크 지연 | 안정적 WiFi | 오프라인 모드 테스트 | 엣지 캐싱, 배치 전송 |

## 4. Opportunity 스코어링

기회 영역 랭킹 공식:
```
Opportunity Score = (트렌드 상승) × (불만 빈도/강도) × (1/경쟁 과밀도)
```

### 스코어링 매트릭스
| 항목 | 1점 | 3점 | 5점 |
|-----|-----|-----|-----|
| 트렌드 | 하락 | 보합 | 상승 |
| 불만 강도 | 언급 드묾 | 간헐적 | 반복/강함 |
| 경쟁 | 레드오션 | 중간 | 블루오션 |

## 5. Evidence Card 활용

### 좋은 Evidence Card 작성법
```json
{
  "claim": "수동 재고 점검은 노동 집약적이고 오류가 발생하기 쉬움",
  "evidence_type": "review",
  "stance": "supports",
  "snippet": {
    "text": "We waste 2 hours daily on manual counts...",
    "start_char": 1200,
    "end_char": 1280
  },
  "quality": {
    "confidence": 0.8,
    "reason": "Multiple sources corroborate"
  }
}
```

### Claim 작성 원칙
- **구체적**: "사용자가 불편해함" ❌ → "수동 입력에 평균 2시간 소요" ✅
- **검증 가능**: 출처와 연결 가능해야 함
- **기획 연결**: MVP 기능과 직접 연결되어야 함

## 6. 인사이트 도출

### Evidence → Insight 변환
```
[Evidence 1] 수동 점검에 2시간 소요
[Evidence 2] 품절 발견이 늦어 판매 손실
[Evidence 3] 스프레드시트 동기화 오류 빈발
           ↓
[Insight] MVP는 "품절 알림"에 집중해야 함
          (전체 SKU 인식보다 있다/없다 감지 우선)
```

### Insight 유형
- **Opportunity**: 시장 기회 발견
- **Risk**: 기술/시장 리스크 식별
- **Requirement**: MVP 요구사항 도출
