# 🚀 DDon-DDon Backend 기술 메뉴얼

이 메뉴얼은 프로젝트에서 사용된 백엔드 기술의 **개념**, **사용법**, **구조 설계 이유**를 단계별로 학습할 수 있도록 구성되었습니다.

---

## 📖 학습 순서

순서대로 학습하시면 백엔드 아키텍처를 완벽히 이해할 수 있습니다.

| 순서 | 문서                                           | 내용                                       |
| ---- | ---------------------------------------------- | ------------------------------------------ |
| 1    | [기술 스택 개요](./01_tech_stack.md)           | Python, FastAPI, SQLAlchemy, Pydantic 소개 |
| 2    | [프로젝트 구조](./02_project_structure.md)     | 레이어 아키텍처와 폴더 구성 이유           |
| 3    | [비동기 프로그래밍](./03_async_programming.md) | async/await와 비동기 패턴                  |
| 4    | [SQLAlchemy 가이드](./04_sqlalchemy_guide.md)  | ORM, 모델 정의, 관계, 쿼리                 |
| 5    | [Pydantic 가이드](./05_pydantic_guide.md)      | 스키마, 데이터 검증, 변환                  |
| 6    | [FastAPI 가이드](./06_fastapi_guide.md)        | 라우팅, 의존성 주입, 미들웨어              |
| 7    | [커스텀 타입과 유틸리티](./07_custom_types.md) | GUID, 예외 처리, 공통 패턴                 |
| 8    | [테스트 가이드](./08_testing_guide.md)         | pytest, 비동기 테스트, 모킹                |

---

## 🎯 학습 목표

이 메뉴얼을 완료하면:

1. **FastAPI + SQLAlchemy + Pydantic** 조합의 이해
2. **레이어 아키텍처** 설계 이유와 적용법
3. **비동기 I/O**를 활용한 고성능 API 개발
4. **타입 안전성**과 **데이터 검증**의 중요성
5. **TDD 기반** 백엔드 개발 방법론

---

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [Pydantic V2 문서](https://docs.pydantic.dev/latest/)
- [Python asyncio 문서](https://docs.python.org/3/library/asyncio.html)

---

> **다음 단계**: [1. 기술 스택 개요](./01_tech_stack.md)
