---
description: 프로젝트 가이드 설정 - 자동 재고 모니터링 솔루션 프로젝트 개요 및 MVP 방향 확인
---

# 프로젝트 가이드 워크플로우

이 워크플로우는 **임베디드 카메라 기반 자동 재고 관리 시스템** 프로젝트의 전체 개요를 설정합니다.

## 1. 프로젝트 개요 확인

프로젝트 마스터 가이드 문서를 참고하여 전체 방향을 파악합니다.

```bash
cat docs/project_guide.md
```

## 2. MVP 핵심 구성 요소

- **하드웨어:** 선반 구역 촬영용 임베디드 카메라 1대
- **핵심 로직:** 물품의 "있다/없다"를 판별하는 Binary Classification 모델
- **사용자 접점:** 웹 관리자 페이지, 재고 부족 푸시 알림

## 3. 분석 프레임워크 (3축 분석)

기획 품질을 높이기 위해 다음 세 가지 신호를 분석합니다:

| 축 | 설명 | 도구/소스 |
|---|---|---|
| **수요 신호 (Demand)** | 실제 검색 및 해결 시도 확인 | Google Trends, Google Ads |
| **불만 신호 (Pain)** | 기존 솔루션의 리뷰/커뮤니티 분석 | G2, Capterra, Reddit |
| **공급 신호 (Supply)** | 기술적 실현 가능성 증명 | Gartner, McKinsey 리포트 |

## 4. 관련 문서 탐색

각 상세 문서로 이동하여 심화 내용을 확인합니다:

```bash
# 분석 방법론 확인
cat docs/analysis_methodology.md

# 기술 구현 가이드 확인
cat docs/tech_implementation_guide.md

# 도메인 분석 확인
cat docs/domain_small_retail_analysis.md
```

## 5. 최종 산출물 (Evidence Package)

기획 단계 완료 시 확보해야 할 산출물:

1. **수요 근거:** Trends 그래프 및 상업적 키워드 리스트
2. **페인포인트 근거:** 실제 사용자들의 '불만 문장' 인용구 모음
3. **기술 청사진:** 엣지-클라우드 연동 구성도 및 리스크 대응표
