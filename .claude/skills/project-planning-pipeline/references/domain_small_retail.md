# Domain: Small Retail (소규모 리테일/쇼핑몰)

소규모 쇼핑몰/오프라인 매장(편의점급, 동네 마트, 소형 리테일)에 최적화된 분석 가이드.

## 도메인 핵심 문제

소형 리테일의 핵심 문제는 다음으로 수렴:
- **진열대 품절 (OOS, Out-of-Stock)**: 판매 기회 손실
- **보충 지연**: 매대 공백 시간 증가
- **수동 점검 비용/오류**: 인력 낭비, 데이터 부정확

## 초기 키워드 30개 세트

### OSA·품절 (10개)
| 키워드 | Intent | 우선순위 |
|--------|--------|---------|
| on-shelf availability | problem_space | 5 |
| OSA retail | problem_space | 5 |
| out of stock retail | problem_space | 5 |
| out-of-shelf stockout | problem_space | 4 |
| shelf gap detection | solution_search | 5 |
| stockout alert system | solution_search | 5 |
| low stock alert retail | solution_search | 4 |
| shelf replenishment | problem_space | 4 |
| retail shelf audit | problem_space | 3 |
| planogram compliance | solution_search | 3 |

### 재고/운영 (10개)
| 키워드 | Intent | 우선순위 |
|--------|--------|---------|
| small retail inventory management | solution_search | 5 |
| inventory management for small business | solution_search | 5 |
| inventory counting process | problem_space | 4 |
| manual inventory count | problem_space | 5 |
| cycle counting retail | problem_space | 4 |
| phantom stock | problem_space | 4 |
| inventory accuracy retail | problem_space | 4 |
| shrinkage inventory retail | problem_space | 3 |
| backroom to shelf visibility | solution_search | 3 |
| inventory discrepancy | problem_space | 3 |

### 비전/카메라/스마트 선반 (10개)
| 키워드 | Intent | 우선순위 |
|--------|--------|---------|
| retail shelf monitoring computer vision | solution_search | 5 |
| computer vision shelf monitoring | solution_search | 5 |
| empty shelf detection | solution_search | 5 |
| smart shelf camera | solution_search | 5 |
| CCTV shelf monitoring | solution_search | 4 |
| edge AI camera retail | solution_search | 4 |
| product facing detection | solution_search | 3 |
| shelf image analytics | solution_search | 3 |
| real-time shelf monitoring | solution_search | 4 |
| 매대 품절 알림 | solution_search | 5 |

## Evidence Card 엔티티 템플릿

```json
{
  "entities": {
    "domain": "small_retail_osa",
    "target_user": ["store_owner", "store_manager", "staff"],
    "pain_point": [
      "stockout",
      "restock_delay",
      "manual_shelf_check",
      "phantom_stock"
    ],
    "job_to_be_done": [
      "keep_shelves_full",
      "reduce_lost_sales",
      "restock_faster"
    ],
    "environment": [
      "varying_lighting",
      "occlusion",
      "product_facing_changes"
    ],
    "constraints": [
      "low_budget",
      "minimal_install_time"
    ]
  },
  "metrics_hint": {
    "osa_oos_related": true,
    "kpi_candidates": ["OOS_rate", "shelf_gap_count", "replenishment_time"]
  }
}
```

## 도메인 특화 KPI

| KPI | 정의 | 측정 방법 |
|-----|-----|----------|
| OOS Rate | 품절 상품 비율 | (품절 SKU / 전체 SKU) × 100 |
| Shelf Gap Time | 매대 공백 시간 | 품절 감지 ~ 보충 완료 시간 |
| Replenishment Time | 보충 소요 시간 | 알림 발생 ~ 보충 완료 시간 |
| Lost Sales | 품절로 인한 매출 손실 | 품절 시간 × 예상 판매량 × 단가 |
| Inventory Accuracy | 재고 정확도 | (시스템 재고 = 실재고) 비율 |

## MVP 시나리오

### 핵심 시나리오: 품절 알림
```
1. 고정 카메라가 특정 선반 구역을 주기적 촬영
2. 엣지 디바이스에서 "있다/없다" 판별
3. 품절 감지 시 → 관리자 앱에 알림 전송
4. 관리자가 앱에서 실시간 이미지 확인
5. 백룸에서 해당 상품 보충
```

### MVP 요구사항 후보
- **알림 임계치**: 몇 % 이하 시 알림 발생?
- **오탐 비용**: 잘못된 알림의 영향도
- **설치 시간**: 카메라 1대 설치에 소요되는 시간
- **오프라인 동작**: 네트워크 끊김 시 로컬 저장

## 기술 리스크 레지스터

| 리스크 | 가정 | 검증 실험 | 완화책 |
|--------|-----|----------|-------|
| 조명 변화 | 일정한 매장 조명 | 시간대별 촬영 테스트 | 자동 노출 조정, HDR |
| 상품 가림 | 정면 배치 | 겹침 시나리오 테스트 | 다중 각도, 시간차 촬영 |
| 상품 외관 변화 | 일정한 패키지 | 프로모션 패키지 테스트 | 정기 재학습, 유사 상품 그룹 |
| 설치 각도 | 고정 카메라 | 다양한 선반 각도 테스트 | 조절 가능 마운트 |
| 네트워크 지연 | 안정적 WiFi | 끊김 시나리오 테스트 | 엣지 캐싱, 배치 전송 |

## 경쟁사/대체재 분석 포인트

수집 시 확인할 항목:
- **기능 목록**: 알림, 리포팅, planogram 검증
- **가격 플랜**: 월정액, SKU당 과금, 설치비
- **하드웨어 구성**: 카메라 종류, 게이트웨이, 클라우드
- **설치 방식**: 온프레미스 vs 클라우드
- **타겟 규모**: 대형 리테일 vs 소형 매장

## 소스 수집 우선순위

| 소스 유형 | 우선순위 | 목적 |
|----------|---------|-----|
| 리테일 운영 블로그 | 높음 | 현장 pain point |
| 벤더 문서/랜딩 페이지 | 높음 | 경쟁사 기능/가격 |
| 학술 논문/기술 문서 | 중간 | 기술 가능성/리스크 |
| G2/Capterra 리뷰 | 높음 | 대체 VOC |
| Reddit/커뮤니티 | 중간 | 실사용자 불만 |
