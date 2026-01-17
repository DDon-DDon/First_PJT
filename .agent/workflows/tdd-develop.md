---
description: 테스트 주도 개발(TDD) 방법론을 적용하여 코드의 안정성, 유지보수성, 문서화 효과를 극대화한다. "실패하는 테스트 작성 -> 코드 구현 -> 리팩토링"의 주기를 엄격히 준수.
---

# TDD (Test-Driven Development) Skill

## 🎯 목표

테스트 주도 개발(TDD) 방법론을 적용하여 코드의 안정성, 유지보수성, 문서화 효과를 극대화한다. "실패하는 테스트 작성 -> 코드 구현 -> 리팩토링"의 주기를 엄격히 준수한다.

## 🔄 TDD 워크플로우 (Red-Green-Refactor)

### 1. 🔴 Red: 실패하는 테스트 작성

- **목표**: 구현하려는 기능의 요구사항을 테스트 코드로 정의한다.
- **행동**:
  1. 요구사항(PRD, Task 문서)을 분석한다.
  2. `tests/` 디렉토리에 적절한 테스트 파일(`test_*.py`)을 생성하거나 연다.
  3. 원하는 동작을 검증하는 테스트 함수를 작성한다.
  4. 테스트를 실행하여 **예상대로 실패하는지** 확인한다. (컴파일 에러나 로직 에러가 아닌, `AssertionError` 등 의도된 실패여야 함)
- **명명 규칙**: `test_<기능명>_<상황>_<예상결과>` (예: `test_create_product_duplicate_barcode_fails`)

### 2. 🟢 Green: 테스트 통과를 위한 최소한의 코드 작성

- **목표**: 테스트를 통과시키는 것만을 목표로 가장 빠르게 코드를 작성한다.
- **행동**:
  1. 실제 구현 파일(Service, Router 등)을 수정한다.
  2. 더럽더라도(Dirty) 일단 테스트가 통과되도록 로직을 작성한다.
  3. 테스트를 실행하여 **성공(Pass)**하는지 확인한다.

### 3. 🔵 Refactor: 리팩토링

- **목표**: 코드의 구조를 개선하고 중복을 제거한다. (기능 동작은 유지)
- **행동**:
  1. 코드의 가독성을 높인다 (변수명 변경, 함수 분리).
  2. 중복 코드를 제거한다.
  3. 효율적이지 않은 로직을 개선한다.
  4. **중요**: 리팩토링 후에도 테스트가 여전히 통과해야 한다.

---

## 🛠️ 도구 및 환경

### Python (Backend)

- **프레임워크**: `pytest`
- **비동기 지원**: `pytest-asyncio`
- **실행 명령어**:
  ```bash
  # 전체 테스트 실행
  pytest

  # 특정 파일 실행
  pytest tests/test_auth.py

  # 상세 출력 및 로컬 변수 확인
  pytest -vv -l
  ```

---

## 📜 테스트 작성 원칙 (FIRST)

1. **F (Fast)**: 테스트는 빠르게 실행되어야 한다. (DB 등 무거운 작업은 Fixture나 Mocking 활용)
2. **I (Independent)**: 각 테스트는 서로 의존하지 않고 독립적이어야 한다. 실행 순서에 영향을 받지 않아야 한다.
3. **R (Repeatable)**: 어떤 환경(로컬, CI 서버)에서 실행해도 동일한 결과가 나와야 한다.
4. **S (Self-validating)**: 테스트 성공/실패 여부를 자동으로 판단할 수 있어야 한다. (수동 확인 금지)
5. **T (Timely)**: 프로덕션 코드보다 **먼저** 작성해야 한다.

---

## 💡 Best Practices

- **Fixture 활용**: 공통적인 설정(DB 세션 연결, 테스트 유저 생성 등)은 `conftest.py`의 fixture로 관리하여 중복을 줄인다.
- **Happy Path vs Edge Case**: 정상 동작(Happy Path)뿐만 아니라, 예외 상황(Edge Case, 입력값 오류, 권한 없음 등)도 반드시 테스트한다.
- **Given-When-Then 패턴**:
  ```python
  async def test_example(db_session):
      # Given: 테스트 준비
      user = await create_test_user(db_session)

      # When: 테스트 실행
      response = await client.post("/api/login", json={...})

      # Then: 결과 검증
      assert response.status_code == 200
      assert "token" in response.json()
  ```
