---
description: 프로젝트 감사(Auditor) 및 교차 검증 - 구현된 코드가 초기 명세서와 일치하는지 검증
---

# Auditor Cross-Verification Workflow (감사 및 교차 검증)

이 워크플로우는 **'제3자 감사자(Auditor)'**의 관점에서 현재 구현된 백엔드 시스템이 초기 기획 의도와 기술 명세를 정확히 준수하고 있는지 검증하는 절차입니다.

## 1. 감사 자료 로드 (Context Loading)

감사를 시작하기 위해 기준이 되는 **'초기 명세서'**와 검증 대상인 **'구현 문서 및 코드'**를 파악하십시오.

### 1.1 초기 명세서 (Reference)

프로젝트의 '헌법'에 해당하는 초기 기획 문서들입니다. 이 내용이 검증의 기준(Source of Truth)이 됩니다.
경로: `.agent/workflows/references/`

- **PRD**: `prd.md` (기획 의도, 핵심 기능)
- **API Spec**: `api-spec.md` (인터페이스 규격)
- **ERD**: `erd.md`, `db-schema-postgres.sql` (데이터 구조)
- **Test Cases**: `test-cases.md` (요구되는 품질 기준)

### 1.2 구현 현황 문서 (Implementation Docs)

개발팀(Worker)이 작성한 로드맵과 구현 내역입니다.
경로: `backend/docs/`

- **Roadmap**: `backend/docs/roadmap/` (또는 `tdd-roadmap.md`) - 개발 진행 상황
- **Implemented**: `backend/docs/implemented/` - 상세 구현 내용 및 결정 사항
- **Manual**: `backend/docs/manual/` - 기술 매뉴얼

### 1.3 소스 코드 (Source Code)

실제 검증 대상입니다.
경로: `backend/app/`

- `models/`: 데이터 모델 구현체
- `api/`: API 엔드포인트 구현체
- `schemas/`: Pydantic 스키마
- `services/` or `crud/`: 비즈니스 로직

---

## 2. 역공학 검증 (Reverse Engineering Verification)

코드를 보고 문서를 유추하여 원본 문서와 비교합니다.

1.  **모델 역설계**: `backend/app/models`의 코드를 보고 ERD를 유추한 뒤, `erd.md`와 **Column 타입, 제약 조건(Nullable, FK), 관계 설정**이 일치하는지 확인하십시오.
2.  **API 역설계**: `backend/app/api`의 라우터 코드를 보고 API 명세를 유추한 뒤, `api-spec.md`의 **Endpoint URL, HTTP Method, Request/Response Schema**와 일치하는지 확인하십시오.

---

## 3. 로직 및 구조 시각화 (Visual Visualization)

1.  **주요 플로우 시각화**: 핵심 비즈니스 로직(예: 재고 차감, 주문 생성 등)에 대해 Mermaid Sequence Diagram을 생성하여 로직의 흐름이 PRD의 요구사항과 부합하는지 확인하십시오.
2.  **구조 대조**: 파일 구조와 모듈 의존성이 `tech-spec.md`나 아키텍처 설계와 일치하는지 점검하십시오.

---

## 4. 결함 리포트 작성 (Defect Reporting)

위의 과정을 통해 발견된 불일치 사항이나 잠재적 문제를 아래 형식으로 리포팅하십시오.

**[Auditor Report]**

- **검증 대상**: (예: API Endpoint - POST /items)
- **발견된 불일치**: (예: 명세서에는 `price`가 필수값이나 코드에서는 Optional로 처리됨)
- **중요도**: [Critical / Major / Minor]
  - _Critical_: 비즈니스 로직 오류 또는 실행 불가
  - _Major_: 명세 불일치, 기능 누락
  - _Minor_: 네이밍, 컨벤션, 주석 누락
- **권장 수정 사항**: (구체적인 수정 방향 제안)

---

## 5. 실행 지침 (Instruction)

에이전트는 이 워크플로우를 실행할 때 다음 태도를 유지해야 합니다.

- **비판적 사고 (Critical Thinking)**: "코드는 거짓말을 하지 않는다"는 전제하에, 주석이나 문서의 설명보다 **실제 코드의 동작**을 우선하여 판단하십시오.
- **적대적 검증 (Adversarial Verification)**: 개발자가 놓쳤을 법한 예외 케이스(Edge Case)를 중심으로 코드를 공격적으로 분석하십시오.
