# API 명세서

## 기본 정보

- **Base URL**: `https://api.donedone.app/v1`
- **인증**: Bearer Token (JWT)
- **Content-Type**: `application/json`

## 공통 응답 형식

### 성공 응답
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T09:30:00Z"
  }
}
```

### 에러 응답
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "재고가 부족합니다",
    "details": { "current": 5, "requested": 10 }
  }
}
```

### HTTP 상태 코드

| 코드 | 설명 |
|------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 409 | 충돌 (중복) |
| 500 | 서버 오류 |

---

## 인증 API

### POST /auth/login

로그인

**Request**:
```json
{
  "email": "worker@example.com",
  "password": "password123"
}
```

**Response** (200):
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "worker@example.com",
      "name": "김작업",
      "role": "WORKER",
      "stores": [
        { "id": "store-uuid", "name": "강남 1호점" }
      ]
    }
  }
}
```

---

## 제품 API

### GET /products

제품 목록 조회

**Query Parameters**:
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| page | integer | N | 페이지 번호 (default: 1) |
| limit | integer | N | 페이지당 개수 (default: 20) |
| search | string | N | 검색어 (제품명, 바코드) |
| category_id | uuid | N | 카테고리 필터 |

**Response** (200):
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "product-uuid",
        "barcode": "8801234567890",
        "name": "수분크림 50ml",
        "category": { "id": "cat-uuid", "name": "스킨케어" },
        "safetyStock": 10,
        "imageUrl": "https://...",
        "isActive": true
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

### GET /products/barcode/{barcode}

바코드로 제품 조회 (스캔용)

**Response** (200):
```json
{
  "success": true,
  "data": {
    "id": "product-uuid",
    "barcode": "8801234567890",
    "name": "수분크림 50ml",
    "category": { "id": "cat-uuid", "name": "스킨케어" },
    "safetyStock": 10,
    "imageUrl": "https://..."
  }
}
```

**Response** (404):
```json
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "등록되지 않은 제품입니다"
  }
}
```

### POST /products

제품 등록 (ADMIN 전용)

**Request**:
```json
{
  "barcode": "8801234567890",
  "name": "수분크림 50ml",
  "categoryId": "category-uuid",
  "safetyStock": 10,
  "memo": "신상품"
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "new-product-uuid",
    "barcode": "8801234567890",
    "name": "수분크림 50ml",
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

### POST /products/generate-barcode

내부 바코드 생성 (ADMIN 전용)

**Request**:
```json
{
  "categoryCode": "SK"
}
```

**Response** (200):
```json
{
  "success": true,
  "data": {
    "barcode": "DON-SK-00042"
  }
}
```

---

## 재고 API

### GET /inventory/stocks

현재고 목록 조회

**Query Parameters**:
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| store_id | uuid | N | 매장 필터 (WORKER는 자동) |
| category_id | uuid | N | 카테고리 필터 |
| status | string | N | LOW, NORMAL, GOOD |
| page | integer | N | 페이지 번호 |
| limit | integer | N | 페이지당 개수 |

**Response** (200):
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "product": {
          "id": "product-uuid",
          "barcode": "8801234567890",
          "name": "수분크림 50ml",
          "safetyStock": 10
        },
        "store": { "id": "store-uuid", "name": "강남 1호점" },
        "quantity": 8,
        "status": "LOW",
        "updatedAt": "2024-01-15T09:30:00Z"
      }
    ],
    "pagination": { ... }
  }
}
```

### GET /inventory/stocks/{productId}

제품별 매장 재고 조회

**Response** (200):
```json
{
  "success": true,
  "data": {
    "product": {
      "id": "product-uuid",
      "barcode": "8801234567890",
      "name": "수분크림 50ml",
      "safetyStock": 10
    },
    "stocks": [
      {
        "store": { "id": "store-uuid", "name": "강남 1호점" },
        "quantity": 25,
        "status": "GOOD"
      },
      {
        "store": { "id": "store-uuid-2", "name": "홍대점" },
        "quantity": 8,
        "status": "LOW"
      }
    ],
    "totalQuantity": 33
  }
}
```

---

## 트랜잭션 API

### POST /transactions/inbound

입고 처리

**Request**:
```json
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": 30,
  "note": "정기 입고"
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "transactionId": "tx-uuid",
    "type": "INBOUND",
    "quantity": 30,
    "newStock": 55,
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

### POST /transactions/outbound

출고 처리

**Request**:
```json
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": 10,
  "note": "고객 판매"
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "transactionId": "tx-uuid",
    "type": "OUTBOUND",
    "quantity": -10,
    "newStock": 45,
    "safetyAlert": false,
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

**Response** (400 - 재고 부족):
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "재고가 부족합니다",
    "details": {
      "currentStock": 5,
      "requestedQuantity": 10
    }
  }
}
```

### POST /transactions/adjust

재고 조정

**Request**:
```json
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": -5,
  "reason": "EXPIRED",
  "note": "유통기한 만료 폐기"
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "transactionId": "tx-uuid",
    "type": "ADJUST",
    "quantity": -5,
    "reason": "EXPIRED",
    "newStock": 40,
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

### GET /transactions

트랜잭션 이력 조회

**Query Parameters**:
| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| store_id | uuid | N | 매장 필터 |
| product_id | uuid | N | 제품 필터 |
| type | string | N | INBOUND, OUTBOUND, ADJUST |
| start_date | date | N | 시작일 |
| end_date | date | N | 종료일 |
| page | integer | N | 페이지 번호 |
| limit | integer | N | 페이지당 개수 |

**Response** (200):
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "tx-uuid",
        "type": "INBOUND",
        "quantity": 30,
        "product": { "id": "...", "name": "수분크림 50ml" },
        "store": { "id": "...", "name": "강남 1호점" },
        "user": { "id": "...", "name": "김작업" },
        "note": "정기 입고",
        "createdAt": "2024-01-15T09:30:00Z"
      }
    ],
    "pagination": { ... }
  }
}
```

---

## 동기화 API

### POST /sync/transactions

오프라인 트랜잭션 일괄 동기화

**Request**:
```json
{
  "transactions": [
    {
      "localId": "local-uuid-1",
      "type": "INBOUND",
      "productId": "product-uuid",
      "storeId": "store-uuid",
      "quantity": 30,
      "createdAt": "2024-01-15T09:30:00Z"
    },
    {
      "localId": "local-uuid-2",
      "type": "OUTBOUND",
      "productId": "product-uuid-2",
      "storeId": "store-uuid",
      "quantity": 10,
      "createdAt": "2024-01-15T09:31:00Z"
    }
  ]
}
```

**Response** (200):
```json
{
  "success": true,
  "data": {
    "synced": [
      { "localId": "local-uuid-1", "serverId": "server-uuid-1" },
      { "localId": "local-uuid-2", "serverId": "server-uuid-2" }
    ],
    "failed": [],
    "syncedAt": "2024-01-15T10:00:00Z"
  }
}
```

---

## 매장/카테고리 API

### GET /stores

매장 목록 조회

**Response** (200):
```json
{
  "success": true,
  "data": [
    { "id": "store-uuid-1", "code": "STORE-001", "name": "강남 1호점" },
    { "id": "store-uuid-2", "code": "STORE-002", "name": "홍대점" }
  ]
}
```

### GET /categories

카테고리 목록 조회

**Response** (200):
```json
{
  "success": true,
  "data": [
    { "id": "cat-uuid-1", "code": "SK", "name": "스킨케어" },
    { "id": "cat-uuid-2", "code": "MU", "name": "메이크업" },
    { "id": "cat-uuid-3", "code": "HC", "name": "헤어케어" }
  ]
}
```

---

## 알림/내보내기 API

### GET /alerts/low-stock

안전재고 이하 제품 목록 (ADMIN 전용)

**Response** (200):
```json
{
  "success": true,
  "data": [
    {
      "product": { "id": "...", "name": "수분크림 50ml", "safetyStock": 10 },
      "store": { "id": "...", "name": "강남 1호점" },
      "currentStock": 8,
      "shortage": 2
    }
  ]
}
```

### GET /exports/low-stock

안전재고 이하 목록 엑셀 다운로드 (ADMIN 전용)

**Response**: Excel 파일 (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)

---

## 권한 매트릭스

| 엔드포인트 | WORKER | ADMIN |
|------------|--------|-------|
| POST /auth/login | ✅ | ✅ |
| GET /products | ✅ (배정 매장) | ✅ (전체) |
| GET /products/barcode/{barcode} | ✅ | ✅ |
| POST /products | ❌ | ✅ |
| POST /products/generate-barcode | ❌ | ✅ |
| GET /inventory/stocks | ✅ (배정 매장) | ✅ (전체) |
| POST /transactions/inbound | ✅ (배정 매장) | ✅ |
| POST /transactions/outbound | ✅ (배정 매장) | ✅ |
| POST /transactions/adjust | ✅ (배정 매장) | ✅ |
| GET /transactions | ✅ (배정 매장) | ✅ (전체) |
| POST /sync/transactions | ✅ | ✅ |
| GET /alerts/low-stock | ❌ | ✅ |
| GET /exports/low-stock | ❌ | ✅ |