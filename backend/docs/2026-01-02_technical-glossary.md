# 똔똔 프로젝트 기술 용어 사전

**작성일**: 2026-01-02
**대상**: 비개발자 및 초급 개발자
**목적**: 프로젝트에서 사용하는 모든 기술 용어를 쉽게 설명

---

## 목차

### 프로그래밍 언어
- [Python](#python)
- [TypeScript](#typescript)
- [JavaScript](#javascript)

### 백엔드 기술
- [FastAPI](#fastapi)
- [uvicorn](#uvicorn)
- [SQLAlchemy](#sqlalchemy)
- [Alembic](#alembic)
- [Pydantic](#pydantic)

### 프론트엔드 기술
- [Next.js](#nextjs)
- [React](#react)
- [Tailwind CSS](#tailwind-css)

### 데이터베이스
- [PostgreSQL](#postgresql)
- [SQLite](#sqlite)
- [ORM](#orm)
- [마이그레이션 (Migration)](#마이그레이션-migration)
- [인덱스 (Index)](#인덱스-index)

### 인증/보안
- [JWT](#jwt)
- [bcrypt](#bcrypt)
- [OAuth](#oauth)

### 테스트
- [TDD](#tdd)
- [pytest](#pytest)
- [Fixture](#fixture)
- [Mock](#mock)

### 인프라/DevOps
- [Docker](#docker)
- [Docker Compose](#docker-compose)
- [CI/CD](#cicd)

### 개발 개념
- [API](#api)
- [REST API](#rest-api)
- [CRUD](#crud)
- [비동기 (Async/Await)](#비동기-asyncawait)
- [UUID/GUID](#uuidguid)
- [Enum](#enum)
- [Soft Delete](#soft-delete)
- [Append-Only](#append-only)

### 아키텍처 패턴
- [레이어 분리 (Layered Architecture)](#레이어-분리-layered-architecture)
- [의존성 주입 (Dependency Injection)](#의존성-주입-dependency-injection)
- [서비스 레이어 패턴](#서비스-레이어-패턴)

---

## 프로그래밍 언어

### Python

**무엇인가?**
- 읽기 쉽고 배우기 쉬운 고급 프로그래밍 언어
- 똔똔 프로젝트의 백엔드 서버를 만드는 데 사용

**왜 선택했는가?**
- 문법이 간결하고 읽기 쉬움 (영어 문장처럼)
- 웹 개발에 필요한 라이브러리가 풍부
- FastAPI, SQLAlchemy 같은 강력한 도구 사용 가능
- 데이터 분석, AI 분야에서도 많이 사용 (미래 확장 가능)

**유사 기술**
- Node.js (JavaScript 기반 백엔드)
- Java (Spring Boot)
- Go (Gin, Fiber)
- Ruby (Ruby on Rails)

**장점**
- 초보자도 배우기 쉬움
- 코드가 짧고 명확함
- 라이브러리 생태계가 풍부

**단점**
- 실행 속도가 Java, Go보다 느림 (하지만 웹 서버에서는 큰 문제 없음)
- 비동기 처리가 복잡할 수 있음

**예시 코드**
```python
# Python은 이렇게 간결합니다
def greet(name):
    return f"안녕하세요, {name}님!"

result = greet("홍길동")
print(result)  # 안녕하세요, 홍길동님!
```

---

### TypeScript

**무엇인가?**
- JavaScript에 **타입(Type)**을 추가한 언어
- 똔똔 프로젝트의 프론트엔드(웹 화면)를 만드는 데 사용

**왜 선택했는가?**
- JavaScript의 오류를 미리 잡을 수 있음
- 코드 작성 시 자동완성이 잘 됨
- 큰 프로젝트에서 유지보수가 쉬움

**JavaScript와의 차이**
```javascript
// JavaScript - 타입 없음
function add(a, b) {
    return a + b;
}
add(1, "2");  // "12" (문자열 결합, 버그 발생 가능)

// TypeScript - 타입 있음
function add(a: number, b: number): number {
    return a + b;
}
add(1, "2");  // ❌ 에러! 숫자만 받음
```

**유사 기술**
- JavaScript (타입 없는 버전)
- Flow (Facebook의 타입 체커)
- Dart (Flutter에서 사용)

**장점**
- 실수로 인한 버그를 미리 발견
- IDE에서 자동완성이 강력함
- 리팩토링이 안전함

**단점**
- 학습 곡선이 있음 (타입 시스템 이해 필요)
- JavaScript로 컴파일 과정 필요

---

### JavaScript

**무엇인가?**
- 웹 브라우저에서 실행되는 프로그래밍 언어
- 웹 페이지에 동작(버튼 클릭, 애니메이션 등)을 추가

**특징**
- 모든 웹 브라우저에서 실행됨
- Node.js를 사용하면 서버에서도 실행 가능

---

## 백엔드 기술

### FastAPI

**무엇인가?**
- Python으로 빠르게 **API 서버**를 만들 수 있는 웹 프레임워크
- "Fast"라는 이름처럼 성능이 빠름

**왜 선택했는가?**
- **비동기 처리** 지원 → 동시 요청 처리 능력 우수
- **자동 문서화** → API 문서를 자동으로 생성 (Swagger UI)
- **타입 검증** → Pydantic으로 데이터 자동 검증
- **현대적** → 최신 Python 기능 활용 (async/await, type hints)

**유사 기술**
- **Django REST Framework** (Django 기반, 더 무겁지만 기능 많음)
- **Flask** (더 가볍지만 기능 적음)
- **Express.js** (Node.js 기반)
- **Spring Boot** (Java 기반)
- **Gin** (Go 기반)

**장단점 비교**

| 항목 | FastAPI | Django | Flask |
|------|---------|--------|-------|
| 성능 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 학습 난이도 | 쉬움 | 중간 | 쉬움 |
| 비동기 지원 | ✅ 기본 지원 | ✅ 부분 지원 | ❌ 제한적 |
| 자동 문서화 | ✅ | ❌ | ❌ |
| Admin 패널 | ❌ | ✅ | ❌ |

**예시 코드**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "안녕하세요!"}

# 서버 실행하면 자동으로 http://localhost:8000/docs 문서 생성
```

**자동 생성되는 API 문서 예시**
- Swagger UI: 모든 API를 브라우저에서 테스트 가능
- ReDoc: 깔끔한 문서 형식

---

### uvicorn

**무엇인가?**
- FastAPI 애플리케이션을 실행하는 **ASGI 서버**
- 웹 서버의 엔진 역할

**비유**
- FastAPI = 자동차 설계도
- uvicorn = 자동차 엔진

**왜 필요한가?**
- FastAPI 코드만으로는 서버가 실행되지 않음
- uvicorn이 HTTP 요청을 받아 FastAPI로 전달

**유사 기술**
- **Gunicorn** (동기 처리용 WSGI 서버)
- **Hypercorn** (또 다른 ASGI 서버)
- **Daphne** (Django Channels용)

**실행 방법**
```bash
uvicorn app.main:app --reload
# app.main.py 파일의 app 객체를 실행
# --reload: 코드 변경 시 자동 재시작
```

---

### SQLAlchemy

**무엇인가?**
- Python에서 데이터베이스를 쉽게 다루기 위한 **ORM (Object-Relational Mapping)** 라이브러리
- SQL 문을 Python 코드로 작성 가능

**ORM이란?**
- **Object**: Python의 클래스/객체
- **Relational**: 관계형 데이터베이스 (PostgreSQL, MySQL 등)
- **Mapping**: 둘을 연결

**왜 사용하는가?**
- SQL을 직접 작성하지 않아도 됨
- Python 코드로 데이터베이스 조작
- 데이터베이스 변경 시 코드 수정 최소화

**SQL vs SQLAlchemy**
```python
# SQL 직접 작성
cursor.execute("SELECT * FROM users WHERE email = 'test@example.com'")

# SQLAlchemy (Python 코드)
user = session.query(User).filter(User.email == "test@example.com").first()
```

**유사 기술**
- **Django ORM** (Django 전용)
- **Peewee** (더 가벼운 ORM)
- **Prisma** (Node.js/TypeScript용)
- **TypeORM** (TypeScript용)
- **Hibernate** (Java용)

**장점**
- SQL 몰라도 데이터베이스 조작 가능
- 데이터베이스 변경 시 코드 변경 최소화
- 타입 안전성 (IDE 자동완성)

**단점**
- 복잡한 쿼리는 SQL이 더 간단할 수 있음
- 성능 최적화가 어려울 수 있음
- 학습 곡선 존재

**예시 코드**
```python
# 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    name = Column(String(100))

# 데이터 조회
users = session.query(User).filter(User.name.like("김%")).all()
# SQL: SELECT * FROM users WHERE name LIKE '김%'
```

---

### Alembic

**무엇인가?**
- 데이터베이스 **마이그레이션 (Migration)** 도구
- 데이터베이스 스키마 변경 이력을 관리

**비유**
- Git이 코드 변경 이력을 관리하듯
- Alembic은 데이터베이스 구조 변경 이력을 관리

**왜 필요한가?**
- 테이블 구조 변경 시 이력 추적
- 팀원 간 데이터베이스 동기화
- 롤백 가능 (문제 발생 시 이전 버전으로)

**사용 예시**
```bash
# 1. 컬럼 추가가 필요함
# User 모델에 phone 컬럼 추가

# 2. 마이그레이션 파일 생성
alembic revision --autogenerate -m "Add phone to users"

# 3. 데이터베이스 적용
alembic upgrade head

# 4. 문제 발생 시 롤백
alembic downgrade -1
```

**유사 기술**
- **Django Migrations** (Django 내장)
- **Flyway** (Java용)
- **Liquibase** (다중 언어 지원)
- **Prisma Migrate** (Prisma용)

---

### Pydantic

**무엇인가?**
- Python 데이터 **검증 (Validation)** 라이브러리
- 잘못된 데이터가 들어오면 자동으로 에러 발생

**왜 사용하는가?**
- API 요청 데이터 자동 검증
- 타입 안전성 보장
- 자동 문서화 지원

**예시**
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr  # 이메일 형식 검증
    password: str = Field(min_length=6)  # 최소 6자
    age: int = Field(ge=0, le=150)  # 0~150 사이

# 사용
user = UserCreate(
    email="test@example.com",
    password="123456",
    age=25
)  # ✅ 통과

user = UserCreate(
    email="invalid-email",  # ❌ ValidationError
    password="12",  # ❌ 너무 짧음
    age=200  # ❌ 범위 초과
)
```

**유사 기술**
- **marshmallow** (Python용)
- **Joi** (Node.js용)
- **Zod** (TypeScript용)
- **Yup** (JavaScript용)

**장점**
- 자동 검증 → 버그 방지
- 타입 힌트 활용 → IDE 자동완성
- FastAPI와 완벽 호환

---

## 프론트엔드 기술

### Next.js

**무엇인가?**
- React 기반 **웹 애플리케이션 프레임워크**
- 웹사이트를 쉽고 빠르게 만들 수 있게 해주는 도구

**왜 선택했는가?**
- **SSR (Server-Side Rendering)**: 서버에서 HTML 생성 → SEO 유리
- **파일 기반 라우팅**: 폴더 구조가 곧 URL 구조
- **성능 최적화**: 이미지, 폰트 자동 최적화
- **TypeScript 지원**: 기본 지원

**React vs Next.js**
- **React**: 라이브러리 (UI만 담당)
- **Next.js**: 프레임워크 (라우팅, SSR, API 등 포함)

**유사 기술**
- **Remix** (React 기반, 더 새로운 프레임워크)
- **Nuxt.js** (Vue.js 기반)
- **SvelteKit** (Svelte 기반)
- **Gatsby** (정적 사이트 생성기)

**파일 기반 라우팅 예시**
```
app/
├── page.tsx          → /
├── login/
│   └── page.tsx      → /login
└── products/
    └── page.tsx      → /products
```

**버전**: Next.js 16.1.1 (똔똔 프로젝트)

---

### React

**무엇인가?**
- Facebook(Meta)에서 만든 **UI 라이브러리**
- 웹 페이지의 화면(UI)을 컴포넌트 단위로 만듦

**핵심 개념**
- **컴포넌트**: 재사용 가능한 UI 조각
- **상태 (State)**: 변하는 데이터
- **Props**: 부모 → 자식으로 데이터 전달

**왜 인기가 많은가?**
- 배우기 쉬움
- 생태계가 거대함 (라이브러리, 도구 많음)
- 성능이 좋음 (Virtual DOM)

**유사 기술**
- **Vue.js** (더 쉬운 문법)
- **Angular** (Google, 더 무거움)
- **Svelte** (컴파일 방식)

**예시 코드**
```tsx
// 버튼 컴포넌트
function Button({ text, onClick }) {
    return (
        <button onClick={onClick}>
            {text}
        </button>
    );
}

// 사용
<Button text="로그인" onClick={() => console.log("클릭!")} />
```

**버전**: React 19.2.3 (똔똔 프로젝트)

---

### Tailwind CSS

**무엇인가?**
- **유틸리티 우선 (Utility-First) CSS 프레임워크**
- HTML에 클래스명만 추가해서 스타일 적용

**기존 CSS vs Tailwind CSS**
```html
<!-- 기존 CSS -->
<style>
.button {
    background-color: blue;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
}
</style>
<button class="button">클릭</button>

<!-- Tailwind CSS -->
<button class="bg-blue-500 text-white px-4 py-2 rounded">
    클릭
</button>
```

**왜 사용하는가?**
- CSS 파일을 별도로 작성하지 않아도 됨
- 클래스명 고민 불필요
- 일관된 디자인 시스템

**유사 기술**
- **Bootstrap** (컴포넌트 중심)
- **Material UI** (Google Material Design)
- **Ant Design** (엔터프라이즈용)
- **Chakra UI** (React 전용)

**장점**
- 빠른 개발 속도
- CSS 파일 크기 작음 (사용하지 않는 스타일은 제거됨)
- 반응형 디자인 쉬움

**단점**
- HTML이 길어짐
- 처음엔 클래스명 외우기 어려움

**버전**: Tailwind CSS 4 (똔똔 프로젝트)

---

## 데이터베이스

### PostgreSQL

**무엇인가?**
- 세계에서 가장 많이 쓰이는 **오픈소스 관계형 데이터베이스**
- "Postgres"라고 부르기도 함

**왜 선택했는가?**
- **안정성**: 금융권에서도 사용할 정도로 안정적
- **기능 풍부**: JSON, UUID, 전문 검색 등 고급 기능 지원
- **오픈소스**: 무료
- **확장성**: 대용량 데이터 처리 가능

**유사 기술**
- **MySQL** (더 단순, 웹 호스팅에서 많이 사용)
- **MariaDB** (MySQL 포크)
- **Oracle Database** (유료, 엔터프라이즈)
- **Microsoft SQL Server** (유료, Windows 중심)

**PostgreSQL vs MySQL**

| 항목 | PostgreSQL | MySQL |
|------|------------|-------|
| ACID 준수 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 복잡한 쿼리 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| JSON 지원 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 속도 (단순 쿼리) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 학습 난이도 | 중간 | 쉬움 |

**특징**
- **ACID**: 데이터 무결성 보장
- **MVCC**: 동시 접속 처리 우수
- **확장 가능**: PostGIS(지리 정보), TimescaleDB(시계열) 등 확장 설치 가능

**버전**: PostgreSQL 16 (똔똔 프로젝트)

---

### SQLite

**무엇인가?**
- **파일 기반** 경량 데이터베이스
- 별도 서버 없이 파일 하나로 동작

**왜 사용하는가? (테스트용)**
- 설치 불필요 (Python에 내장)
- 메모리에서 실행 가능 → 테스트 속도 빠름
- 설정 간단

**PostgreSQL vs SQLite**

| 항목 | PostgreSQL | SQLite |
|------|------------|--------|
| 서버 필요 | ✅ | ❌ (파일만 있으면 됨) |
| 동시 접속 | 많음 | 제한적 |
| 용량 | 대용량 가능 | 소규모 |
| 용도 | 프로덕션 | 개발/테스트/모바일 |

**똔똔 프로젝트에서 사용**
- **프로덕션**: PostgreSQL
- **테스트**: SQLite (빠른 속도)

---

### ORM

**무엇인가?**
- **Object-Relational Mapping**
- 객체(Object)와 관계형 DB(Relational)를 연결(Mapping)

**비유**
- 번역기 같은 역할
- Python 코드 → SQL 문으로 자동 변환

**왜 사용하는가?**
- SQL을 몰라도 데이터베이스 조작 가능
- 데이터베이스 변경 시 코드 수정 최소화
- 보안 (SQL Injection 방지)

**ORM 없이 (Raw SQL)**
```python
cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)",
               ("test@example.com", "홍길동"))
# SQL Injection 위험 존재
```

**ORM 사용 (SQLAlchemy)**
```python
user = User(email="test@example.com", name="홍길동")
session.add(user)
# 안전하게 자동 변환
```

---

### 마이그레이션 (Migration)

**무엇인가?**
- 데이터베이스 스키마(구조) 변경을 추적하고 관리하는 방법

**비유**
- Git의 커밋처럼, 데이터베이스 변경 이력을 저장

**왜 필요한가?**
- 팀원 간 DB 구조 동기화
- 변경 이력 추적
- 롤백 가능 (문제 발생 시)

**마이그레이션 흐름**
```
1. 개발자 A: User 테이블에 phone 컬럼 추가
2. 마이그레이션 파일 생성 (0002_add_phone.py)
3. Git에 커밋
4. 개발자 B: Git Pull
5. 마이그레이션 실행 (alembic upgrade head)
6. 개발자 B도 동일한 DB 구조 적용됨
```

**마이그레이션 파일 예시**
```python
# 0002_add_phone.py
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20)))

def downgrade():
    op.drop_column('users', 'phone')
```

---

### 인덱스 (Index)

**무엇인가?**
- 데이터베이스에서 **빠른 검색**을 위한 자료구조
- 책의 색인과 같은 역할

**비유**
- 사전에서 단어 찾기
  - 인덱스 없음: 첫 페이지부터 끝까지 읽기 (느림)
  - 인덱스 있음: 색인 보고 바로 찾기 (빠름)

**성능 차이**
```
100만 건의 데이터에서 검색

인덱스 없을 때:
- Full Table Scan
- 1,000,000건 모두 확인
- 시간: 1초

인덱스 있을 때:
- Index Seek
- 약 20번 비교 (log2(1,000,000))
- 시간: 0.001초
```

**언제 사용하는가?**
- 자주 검색하는 컬럼 (WHERE, JOIN에 사용)
- 정렬 (ORDER BY)에 사용하는 컬럼

**주의사항**
- 인덱스는 검색은 빠르지만 INSERT/UPDATE는 느려짐
- 너무 많은 인덱스는 오히려 성능 저하

**똔똔 프로젝트 인덱스**
```sql
CREATE INDEX idx_products_barcode ON products(barcode);
-- 바코드 검색이 가장 빈번하므로 인덱스 생성
```

---

## 인증/보안

### JWT

**무엇인가?**
- **JSON Web Token**
- 사용자 인증 정보를 담은 **암호화된 토큰**

**왜 사용하는가?**
- 서버가 세션을 저장하지 않아도 됨 (Stateless)
- 여러 서버에서 사용 가능 (확장성 좋음)
- 모바일 앱에서도 사용 가능

**작동 방식**
```
1. 로그인 성공
2. 서버가 JWT 토큰 발급
3. 클라이언트가 토큰 저장 (localStorage, Cookie)
4. 이후 모든 요청에 토큰 포함
5. 서버가 토큰 검증
```

**JWT 구조**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZXhwIjoxNjQwOTk1MjAwfQ.abc123
│                                      │                                                      │
Header (알고리즘)                       Payload (데이터)                                     Signature (서명)
```

**유사 기술**
- **Session Cookie** (전통적 방식)
- **OAuth** (외부 인증, 소셜 로그인)
- **SAML** (기업용)

**장점**
- Stateless (서버 부담 적음)
- 확장성 좋음
- 다양한 플랫폼 지원

**단점**
- 토큰 탈취 시 위험 (만료 시간 설정 필요)
- 토큰 크기가 Session보다 큼
- 즉시 무효화 어려움

---

### bcrypt

**무엇인가?**
- 비밀번호를 **해싱(Hashing)**하는 알고리즘
- 단방향 암호화 (복호화 불가능)

**왜 사용하는가?**
- 비밀번호를 평문(Plain Text)으로 저장하면 위험
- DB 해킹 시에도 원본 비밀번호 노출 방지

**작동 방식**
```python
# 회원가입
password = "password123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# 결과: $2b$12$abcdefg... (해시값)
# DB에 해시값 저장

# 로그인
input_password = "password123"
stored_hash = "$2b$12$abcdefg..."
bcrypt.checkpw(input_password, stored_hash)  # True
```

**유사 기술**
- **Argon2** (더 최신, 권장)
- **PBKDF2** (Python 표준 라이브러리)
- **scrypt** (메모리 집약적)

**특징**
- Salt 자동 생성 (같은 비밀번호도 다른 해시)
- Work Factor 조정 가능 (보안 수준 조절)

**bcrypt vs 일반 해시**
```python
# MD5 (위험) - 너무 빠름
"password123" → "482c811da5d5b4bc6d497ffa98491e38"
# 1초에 수십억 번 시도 가능 (브루트포스 취약)

# bcrypt (안전) - 의도적으로 느림
"password123" → "$2b$12$abcdefg..."
# 1초에 수천 번만 시도 가능 (브루트포스 방어)
```

---

### OAuth

**무엇인가?**
- 외부 서비스로 로그인하는 **인증 프로토콜**
- "Google로 로그인", "카카오로 로그인" 등

**왜 사용하는가?**
- 사용자가 비밀번호를 직접 입력하지 않아도 됨
- 신뢰할 수 있는 외부 서비스의 인증 활용

**흐름**
```
1. "Google로 로그인" 버튼 클릭
2. Google 로그인 페이지로 이동
3. Google에 로그인
4. Google이 인증 코드 발급
5. 우리 서버가 코드로 사용자 정보 요청
6. Google이 사용자 정보 전달
7. 우리 서버가 회원 가입/로그인 처리
```

**똔똔 프로젝트에서는?**
- Phase 1에서는 사용 안 함
- 추후 확장 가능 (Google, 카카오 로그인 추가)

---

## 테스트

### TDD

**무엇인가?**
- **Test-Driven Development (테스트 주도 개발)**
- 코드보다 **테스트를 먼저** 작성하는 개발 방법론

**Red-Green-Refactor 사이클**
```
🔴 RED: 실패하는 테스트 작성
   ↓
🟢 GREEN: 테스트를 통과하는 최소 코드 작성
   ↓
🔵 REFACTOR: 코드 개선
   ↓
반복
```

**왜 사용하는가?**
- 명확한 요구사항 정의
- 버그 조기 발견
- 리팩토링 시 안전성 보장
- 테스트 자체가 문서 역할

**기존 개발 vs TDD**
```
기존 개발:
1. 코드 작성
2. 수동 테스트
3. 버그 발견
4. 수정
5. 반복...

TDD:
1. 테스트 작성 (이 함수는 이렇게 동작해야 함)
2. 구현
3. 테스트 실행 (자동)
4. 통과하면 완료
```

**예시**
```python
# 🔴 RED: 테스트 먼저 작성
def test_login_success():
    response = client.post("/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "accessToken" in response.json()["data"]

# 실행 → FAILED (아직 /auth/login 없음)

# 🟢 GREEN: 최소 구현
@app.post("/auth/login")
async def login(email: str, password: str):
    # 일단 돌아가게만
    return {"data": {"accessToken": "fake-token"}}

# 실행 → PASSED

# 🔵 REFACTOR: 개선
@app.post("/auth/login")
async def login(credentials: LoginRequest):
    user = await authenticate_user(credentials)
    token = create_access_token(user)
    return {"data": {"accessToken": token}}
```

---

### pytest

**무엇인가?**
- Python의 가장 인기 있는 **테스트 프레임워크**

**왜 선택했는가?**
- 문법이 간단
- Fixture 시스템 강력
- 플러그인 생태계 풍부 (pytest-asyncio 등)

**유사 기술**
- **unittest** (Python 내장, 더 복잡함)
- **nose2** (pytest와 유사)
- **Jest** (JavaScript용)
- **JUnit** (Java용)

**예시**
```python
# test_calculator.py
def test_add():
    assert 1 + 1 == 2

def test_divide():
    assert 10 / 2 == 5

# 실행
pytest test_calculator.py
```

**유용한 명령어**
```bash
pytest                  # 전체 테스트
pytest -v               # 상세 출력
pytest -x               # 첫 실패 시 중단
pytest --cov=app        # 커버리지 측정
pytest -k "login"       # 이름에 "login" 포함된 테스트만
```

---

### Fixture

**무엇인가?**
- 테스트 실행 전 **준비 작업**을 수행하는 함수
- 테스트에 필요한 환경, 데이터 설정

**비유**
- 시험 보기 전 책상 정리, 연필 준비하는 것

**왜 사용하는가?**
- 테스트마다 중복 코드 방지
- 일관된 테스트 환경 제공
- 테스트 격리 (서로 영향 없음)

**예시**
```python
# conftest.py
@pytest.fixture
async def db_session():
    """테스트용 DB 세션"""
    # 테이블 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 제공
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    # 테이블 삭제 (테스트 격리)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# test_models.py
async def test_create_user(db_session):
    # db_session 자동으로 제공됨
    user = User(email="test@example.com")
    db_session.add(user)
    await db_session.commit()
```

**Fixture Scope**
- `function`: 테스트마다 실행 (기본값)
- `module`: 파일당 1번
- `session`: 전체 테스트에서 1번

---

### Mock

**무엇인가?**
- 테스트에서 **가짜 객체**를 만드는 기법
- 실제 객체 대신 가짜로 대체

**왜 사용하는가?**
- 외부 서비스 의존성 제거 (결제 API, 이메일 발송 등)
- 테스트 속도 향상
- 특정 상황 재현 (네트워크 오류 등)

**예시**
```python
# 실제 코드
async def send_email(to, subject, body):
    # 실제 이메일 발송 (시간 걸림, 비용 발생)
    ...

# 테스트 (Mock 사용)
@pytest.fixture
def mock_email(mocker):
    return mocker.patch("app.services.email.send_email")

async def test_user_signup(mock_email):
    # 회원가입 테스트
    await signup(email="test@example.com")

    # 이메일 발송 함수가 호출되었는지만 확인
    mock_email.assert_called_once()
    # 실제로 이메일은 발송되지 않음
```

**유사 개념**
- **Stub**: 미리 정의된 답변 반환
- **Spy**: 호출 여부 감시
- **Fake**: 간단한 구현체

---

## 인프라/DevOps

### Docker

**무엇인가?**
- **컨테이너 기술**을 사용한 가상화 플랫폼
- 애플리케이션과 실행 환경을 하나로 패키징

**비유**
- 배송 컨테이너처럼 어디서든 동일하게 실행

**왜 사용하는가?**
- "내 컴퓨터에서는 되는데..." 문제 해결
- 환경 설정 자동화
- 배포 간편화

**VM vs Docker**

| 항목 | 가상 머신 (VM) | Docker |
|------|---------------|--------|
| 무게 | 무거움 (GB) | 가벼움 (MB) |
| 부팅 시간 | 분 단위 | 초 단위 |
| 성능 | 느림 | 빠름 |
| OS | 각자 OS 필요 | 호스트 OS 공유 |

**Dockerfile 예시**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**유사 기술**
- **Podman** (Docker 대체)
- **LXC/LXD** (컨테이너)
- **rkt** (Rocket, 단종)

---

### Docker Compose

**무엇인가?**
- 여러 Docker 컨테이너를 **한 번에 관리**하는 도구

**왜 사용하는가?**
- 복잡한 애플리케이션 (DB + 백엔드 + 프론트엔드) 한 번에 실행
- 설정 파일로 관리 (재현 가능)

**똔똔 프로젝트 구성**
```yaml
services:
  postgres:    # 데이터베이스
  pgadmin:     # DB 관리 도구
  # 추후: backend, frontend 추가 가능
```

**명령어**
```bash
docker-compose up -d      # 시작 (백그라운드)
docker-compose down       # 중지
docker-compose logs       # 로그 확인
docker-compose ps         # 상태 확인
```

**유사 기술**
- **Kubernetes** (더 크고 복잡한 시스템)
- **Docker Swarm** (Docker 기본 오케스트레이션)
- **Nomad** (HashiCorp)

---

### CI/CD

**무엇인가?**
- **Continuous Integration / Continuous Deployment**
- 지속적 통합 / 지속적 배포

**CI (Continuous Integration)**
- 코드를 자주 통합 (Git Push)
- 자동으로 테스트 실행
- 문제 조기 발견

**CD (Continuous Deployment)**
- 테스트 통과하면 자동 배포
- 수동 배포 과정 제거

**흐름**
```
1. 개발자가 코드 커밋
2. Git Push
3. CI 서버가 자동으로:
   - 코드 빌드
   - 테스트 실행
   - 린트 검사
4. 모두 통과하면:
   - 자동으로 서버에 배포
```

**도구**
- **GitHub Actions** (GitHub 내장)
- **GitLab CI/CD** (GitLab 내장)
- **Jenkins** (오픈소스, 자체 서버)
- **CircleCI** (클라우드)
- **Travis CI** (클라우드)

**똔똔 프로젝트에서는?**
- Phase 1에서는 미사용
- Phase 8에서 GitHub Actions 설정 예정

---

## 개발 개념

### API

**무엇인가?**
- **Application Programming Interface**
- 애플리케이션 간 소통하는 **약속된 규칙**

**비유**
- 식당의 메뉴판
  - 고객(클라이언트)이 메뉴(API)를 보고 주문
  - 주방(서버)이 요리 제공

**예시**
```
웹 브라우저 → "제품 목록 주세요" → 서버
           ← [제품1, 제품2, 제품3] ←
```

**API 요청/응답 예시**
```http
# 요청
GET /api/v1/products HTTP/1.1
Host: api.donedone.com

# 응답
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": [
    {"id": 1, "name": "제품1"},
    {"id": 2, "name": "제품2"}
  ]
}
```

---

### REST API

**무엇인가?**
- **REpresentational State Transfer**
- HTTP를 잘 활용하는 API 설계 방식

**REST 원칙**
1. **리소스 중심**: URL이 명사 (동사 아님)
2. **HTTP 메서드**: GET, POST, PUT, DELETE 사용
3. **Stateless**: 요청마다 독립적

**RESTful 예시**
```
# ✅ RESTful
GET    /products         # 제품 목록 조회
GET    /products/123     # 제품 1개 조회
POST   /products         # 제품 생성
PUT    /products/123     # 제품 수정
DELETE /products/123     # 제품 삭제

# ❌ Non-RESTful
GET  /getProducts
POST /createProduct
POST /updateProduct
POST /deleteProduct
```

**유사 개념**
- **GraphQL** (쿼리 언어, 더 유연함)
- **gRPC** (바이너리 프로토콜, 더 빠름)
- **SOAP** (XML 기반, 구식)

---

### CRUD

**무엇인가?**
- 데이터 처리의 기본 4가지 작업
- **C**reate, **R**ead, **U**pdate, **D**elete

**예시**
```
게시판 기능:
- Create: 글 쓰기
- Read: 글 읽기
- Update: 글 수정
- Delete: 글 삭제
```

**HTTP 메서드와 매핑**
```
POST   /products  → Create (생성)
GET    /products  → Read   (조회)
PUT    /products/123 → Update (수정)
DELETE /products/123 → Delete (삭제)
```

---

### 비동기 (Async/Await)

**무엇인가?**
- **논블로킹 (Non-Blocking)** 방식의 프로그래밍
- 한 작업이 끝나길 기다리지 않고 다음 작업 진행

**비유**
```
동기 (Synchronous):
- 세탁기 돌리기 → 완료될 때까지 대기 (30분)
- 설거지 시작 → 완료될 때까지 대기 (10분)
- 총 40분

비동기 (Asynchronous):
- 세탁기 돌리기 시작 → 설거지 바로 시작
- 세탁기, 설거지 동시 진행
- 총 30분 (최대 시간만큼)
```

**코드 예시**
```python
# 동기 (Sync)
def get_user(id):
    user = db.query(User).get(id)  # 100ms 대기
    return user

def get_product(id):
    product = db.query(Product).get(id)  # 100ms 대기
    return product

user = get_user(1)     # 100ms
product = get_product(1)  # 100ms
# 총 200ms

# 비동기 (Async)
async def get_user(id):
    user = await db.query(User).get(id)  # 100ms 대기
    return user

async def get_product(id):
    product = await db.query(Product).get(id)  # 100ms 대기
    return product

user, product = await asyncio.gather(
    get_user(1),
    get_product(1)
)
# 총 100ms (동시 실행)
```

**왜 사용하는가?**
- 성능 향상 (I/O 대기 시간 활용)
- 동시 요청 처리 능력 증가
- 서버 리소스 효율적 사용

**주의사항**
- 코드가 복잡해질 수 있음
- 디버깅이 어려울 수 있음
- CPU 집약적 작업에는 효과 없음

---

### UUID/GUID

**무엇인가?**
- **Universally Unique Identifier / Globally Unique Identifier**
- 전 세계에서 유일한 식별자

**형식**
```
550e8400-e29b-41d4-a716-446655440000
│      │ │  │ │  │ │
8자리-4자리-4자리-4자리-12자리 (총 36자, 하이픈 포함)
```

**왜 사용하는가?**
- 고유성 보장 (중복 확률 극히 낮음)
- 분산 시스템에서 ID 충돌 방지
- 보안 (순차적 ID보다 추측 어려움)

**Auto Increment vs UUID**

| 항목 | Auto Increment | UUID |
|------|---------------|------|
| 예시 | 1, 2, 3, 4... | 550e8400-e29b-... |
| 고유성 | 테이블 내 | 전 세계 |
| 크기 | 작음 (4~8 bytes) | 큼 (16 bytes) |
| 보안 | 낮음 (추측 가능) | 높음 |
| 정렬 | 시간순 자동 | 무작위 |

**똔똔 프로젝트 사용 이유**
- 오프라인 동기화 시 ID 충돌 방지
- 여러 매장에서 독립적으로 데이터 생성 가능

---

### Enum

**무엇인가?**
- **Enumeration (열거형)**
- 미리 정의된 상수 집합

**왜 사용하는가?**
- 오타 방지
- 자동완성 (IDE 지원)
- 타입 안전성

**예시**
```python
# ❌ 문자열 하드코딩 (오타 위험)
if transaction.type == "INBOND":  # 오타!
    ...

# ✅ Enum 사용
class TransactionType(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    ADJUST = "ADJUST"

if transaction.type == TransactionType.INBOUND:  # 오타 불가능
    ...
```

**DB에서 사용**
```sql
CREATE TYPE transaction_type AS ENUM ('INBOUND', 'OUTBOUND', 'ADJUST');

-- 'INVALID' 입력 시 에러 발생
```

---

### Soft Delete

**무엇인가?**
- 데이터를 실제로 삭제하지 않고 **비활성화**하는 방식

**Hard Delete vs Soft Delete**

**Hard Delete** (물리적 삭제):
```sql
DELETE FROM users WHERE id = 123;
-- 데이터 영구 삭제, 복구 불가능
```

**Soft Delete** (논리적 삭제):
```sql
UPDATE users SET is_active = false WHERE id = 123;
-- 데이터 남아있음, 복구 가능
```

**왜 사용하는가?**
- 데이터 복구 가능
- 이력 추적 (누가 삭제했는지)
- 외래 키 무결성 유지 (관련 데이터 남아있음)

**똔똔 프로젝트 적용**
```python
class User(Base):
    is_active = Column(Boolean, default=True)

class Product(Base):
    is_active = Column(Boolean, default=True)

# 삭제 시
user.is_active = False

# 조회 시 (활성 사용자만)
users = session.query(User).filter(User.is_active == True).all()
```

---

### Append-Only

**무엇인가?**
- 데이터를 **추가만** 하고 수정/삭제하지 않는 패턴
- 이벤트 소싱 (Event Sourcing)의 기본 원칙

**왜 사용하는가?**
- 모든 이력 추적 가능
- 감사 (Audit) 용이
- 데이터 무결성 보장

**똔똔 프로젝트 적용 - inventory_transactions**
```python
# ✅ 입고 30개
INSERT INTO inventory_transactions (type, quantity)
VALUES ('INBOUND', 30);

# ✅ 출고 10개
INSERT INTO inventory_transactions (type, quantity)
VALUES ('OUTBOUND', -10);

# ❌ 수정/삭제 금지
UPDATE inventory_transactions ...  # 절대 안 함
DELETE FROM inventory_transactions ...  # 절대 안 함

# 잘못 입력한 경우 → 역트랜잭션 추가
INSERT INTO inventory_transactions (type, quantity, note)
VALUES ('ADJUST', -30, '잘못된 입고 보정');
```

**장점**
- 완벽한 이력 추적
- 데이터 무결성
- 시간 여행 (특정 시점 재고 계산 가능)

**단점**
- 데이터 크기 증가
- 현재 상태 조회 시 계산 필요 (캐시 테이블로 해결)

---

## 아키텍처 패턴

### 레이어 분리 (Layered Architecture)

**무엇인가?**
- 애플리케이션을 **여러 계층**으로 나누는 설계 방식
- 각 계층은 하나의 책임만 가짐

**똔똔 프로젝트 레이어**
```
┌─────────────────────┐
│  API Layer          │ ← 요청/응답 처리
│  (api/)             │
├─────────────────────┤
│  Schema Layer       │ ← 데이터 검증
│  (schemas/)         │
├─────────────────────┤
│  Service Layer      │ ← 비즈니스 로직
│  (services/)        │
├─────────────────────┤
│  Model Layer        │ ← DB 접근
│  (models/)          │
└─────────────────────┘
```

**왜 사용하는가?**
- 관심사 분리 (Separation of Concerns)
- 테스트 용이
- 유지보수 쉬움
- 재사용성 향상

**예시**
```python
# API Layer - 요청/응답만 처리
@router.post("/inbound")
async def create_inbound(
    data: InboundTransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    service = InventoryService(db)
    result = await service.process_inbound(data)
    return TransactionResponse.from_orm(result)

# Service Layer - 비즈니스 로직
class InventoryService:
    async def process_inbound(self, data):
        # 제품 조회
        product = await self.get_product(data.productId)
        # 트랜잭션 생성
        transaction = InventoryTransaction(...)
        # 현재고 업데이트
        await self.update_stock(...)
        return transaction
```

---

### 의존성 주입 (Dependency Injection)

**무엇인가?**
- 객체가 필요한 의존성을 **외부에서 주입**받는 패턴

**왜 사용하는가?**
- 테스트 용이 (Mock 객체 주입 가능)
- 결합도 낮춤
- 재사용성 향상

**FastAPI에서 사용**
```python
# deps.py - 의존성 정의
async def get_db():
    async with async_session() as session:
        yield session

# API에서 사용
@router.get("/products")
async def get_products(
    db: AsyncSession = Depends(get_db)  # 의존성 주입
):
    products = await db.query(Product).all()
    return products

# 테스트에서 Mock DB 주입
async def test_get_products():
    mock_db = MockDB()
    result = await get_products(db=mock_db)
```

---

### 서비스 레이어 패턴

**무엇인가?**
- 비즈니스 로직을 **서비스 클래스**에 모으는 패턴

**왜 사용하는가?**
- API 라우터가 복잡해지지 않음
- 재사용 가능 (다른 API에서도 사용)
- 테스트 용이

**예시**
```python
# services/inventory.py
class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_inbound(self, product_id, quantity):
        # 복잡한 비즈니스 로직
        ...

    async def process_outbound(self, product_id, quantity):
        # 재고 검증
        # 안전재고 체크
        # 알림 발송
        ...

# api/v1/transactions.py
@router.post("/inbound")
async def create_inbound(data, db):
    service = InventoryService(db)
    return await service.process_inbound(...)
```

---

## 부록

### 추가 학습 자료

**백엔드**
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 튜토리얼](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Real Python - FastAPI 튜토리얼](https://realpython.com/fastapi-python-web-apis/)

**프론트엔드**
- [Next.js 공식 문서](https://nextjs.org/docs)
- [React 공식 문서](https://react.dev/)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)

**데이터베이스**
- [PostgreSQL 튜토리얼](https://www.postgresqltutorial.com/)
- [SQL 기초 강의 (생활코딩)](https://opentutorials.org/course/3883)

**테스트**
- [pytest 공식 문서](https://docs.pytest.org/)
- [TDD by Example (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

**Docker**
- [Docker 공식 튜토리얼](https://docs.docker.com/get-started/)
- [Docker Compose 문서](https://docs.docker.com/compose/)

---

**작성자**: Claude Code
**최종 업데이트**: 2026-01-02
**문서 버전**: 1.0

**질문이 있다면 언제든 물어보세요!** 💡
