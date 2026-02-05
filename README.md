# 똔똔 (DoneDone) 🏪

**오프라인 매장을 위한 스마트 재고 관리 시스템**

소규모 리테일 매장의 재고 현황을 실시간으로 모니터링하고, 재고 부족을 사전에 알려주는 솔루션입니다.

---

## 🚀 Quick Start

### 사전 요구사항

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 및 실행
- [Node.js](https://nodejs.org/) 18+ (프론트엔드용)
- [Python](https://www.python.org/) 3.11+ (백엔드용)
- [uv](https://github.com/astral-sh/uv) (Python 패키지 매니저, 선택)

### 원클릭 실행

```bash
# 프로젝트 클론
git clone https://github.com/DDon-DDon/First_PJT.git
cd First_PJT

# 전체 서비스 실행 (DB + Backend + Frontend)
.\run_local.bat
```

### DB 초기화 후 실행

```bash
# 기존 DB 데이터를 삭제하고 새로 시작
.\run_local.bat --reset-db

# 또는
.\run_local.bat -r
```

### 실행 후 접속

| 서비스          | URL                         | 설명                   |
| --------------- | --------------------------- | ---------------------- |
| **Frontend**    | http://localhost:3000       | 재고 관리 대시보드     |
| **Backend API** | http://localhost:8000       | REST API 서버          |
| **Swagger UI**  | http://localhost:8000/docs  | API 문서 (테스트 가능) |
| **ReDoc**       | http://localhost:8000/redoc | API 문서 (읽기 전용)   |

---

## 🗂️ 프로젝트 구조

```
First_PJT/
├── backend/                 # FastAPI 백엔드
│   ├── app/                 # 애플리케이션 코드
│   │   ├── api/v1/          # API 엔드포인트
│   │   ├── models/          # SQLAlchemy 모델
│   │   ├── schemas/         # Pydantic 스키마
│   │   ├── services/        # 비즈니스 로직
│   │   └── main.py          # FastAPI 앱 진입점
│   ├── init-db/             # DB 초기화 SQL
│   ├── scripts/             # 실행 스크립트
│   └── tests/               # 테스트 코드
│
├── stock-client/            # Next.js 프론트엔드
│   ├── app/                 # App Router 페이지
│   └── public/              # 정적 파일
│
├── docker-compose.yml       # PostgreSQL 컨테이너 설정
└── run_local.bat            # 원클릭 실행 스크립트
```

---

## 🔧 Backend (FastAPI)

### 기술 스택

| 기술       | 버전   | 용도          |
| ---------- | ------ | ------------- |
| Python     | 3.11+  | 런타임        |
| FastAPI    | 0.109+ | 웹 프레임워크 |
| SQLAlchemy | 2.0+   | 비동기 ORM    |
| PostgreSQL | 16     | 데이터베이스  |
| Pydantic   | 2.0+   | 데이터 검증   |
| JWT        | -      | 인증          |

### 개별 실행

```bash
cd backend

# 가상환경 설정 및 의존성 설치
uv sync

# 개발 서버 실행
.\scripts\dev-server.bat
```

### 주요 API

| 메서드 | 엔드포인트                   | 설명           |
| ------ | ---------------------------- | -------------- |
| GET    | `/api/v1/products`           | 제품 목록 조회 |
| GET    | `/api/v1/stores`             | 매장 목록 조회 |
| GET    | `/api/v1/inventory/stocks`   | 재고 현황 조회 |
| POST   | `/api/v1/inventory/inbound`  | 입고 처리      |
| POST   | `/api/v1/inventory/outbound` | 출고 처리      |

---

## 🎨 Frontend (Next.js)

### 기술 스택

| 기술          | 버전 | 용도             |
| ------------- | ---- | ---------------- |
| Next.js       | 16   | React 프레임워크 |
| React         | 19   | UI 라이브러리    |
| TypeScript    | 5    | 타입 시스템      |
| TailwindCSS   | 4    | 스타일링         |
| Recharts      | 3    | 차트 라이브러리  |
| Framer Motion | 12   | 애니메이션       |

### 개별 실행

```bash
cd stock-client

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 주요 화면

- **대시보드**: 매장별 재고 현황 한눈에 보기
- **제품 관리**: 제품 등록/수정/삭제
- **입출고 처리**: 바코드 스캔 기반 입출고
- **재고 알림**: 안전재고 이하 제품 알림

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
