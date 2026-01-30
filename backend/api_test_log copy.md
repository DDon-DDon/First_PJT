# API Test & Log Report
Generated at: 2026-01-19T00:02:00.748485

Target Server: http://localhost:8000

Waiting for server to be ready...
Server is ready!
## 1. System Health
### GET /health
**Status Code**: 200
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

## 2. Store Management
### Check Existing Stores (GET /api/v1/stores)
### POST /api/v1/stores (Create Store)
**Request Body**: 
```json
{
  "code": "STORE-ea7444da",
  "name": "테스트매장-STORE-ea7444da",
  "address": "서울시 강남구 테헤란로",
  "phone": "02-555-0000"
}
```
**Status Code**: 201
```json
{
  "code": "STORE-ea7444da",
  "name": "테스트매장-STORE-ea7444da",
  "address": "서울시 강남구 테헤란로",
  "phone": "02-555-0000",
  "isActive": true,
  "id": "45a3596d-df08-4b08-9408-480e843cc236"
}
```

## 3. Product Management
### POST /api/v1/categories (Create Category)
**Request Body**: 
```json
{
  "code": "CAT-2da4",
  "name": "테스트카테고리-CAT-2da4",
  "sort_order": 1
}
```
**Status Code**: 201
```json
{
  "id": "f19d1ec7-2413-4dd2-b19d-3ebd0d1c6c29",
  "code": "CAT-2da4",
  "name": "테스트카테고리-CAT-2da4",
  "sortOrder": 1
}
```

### POST /api/v1/products (Create Product)
**Request Body**: 
```json
{
  "barcode": "8803272475977",
  "name": "테스트제품-SAMPLE",
  "category_id": "f19d1ec7-2413-4dd2-b19d-3ebd0d1c6c29",
  "safety_stock": 50
}
```
**Status Code**: 201
```json
{
  "id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "barcode": "8803272475977",
  "name": "테스트제품-SAMPLE",
  "categoryId": "f19d1ec7-2413-4dd2-b19d-3ebd0d1c6c29",
  "safetyStock": 50,
  "imageUrl": null,
  "memo": null,
  "isActive": true,
  "createdAt": "2026-01-18T15:02:01.558102",
  "updatedAt": null
}
```

## 4. Inventory Transaction
### POST /api/v1/transactions/inbound (Inbound Stock)
**Request Body**: 
```json
{
  "product_id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "store_id": "45a3596d-df08-4b08-9408-480e843cc236",
  "quantity": 100,
  "note": "API 테스트 입고"
}
```
**Status Code**: 201
```json
{
  "id": "a98eba99-dd0d-4a8a-a8de-c088ce8da343",
  "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
  "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
  "type": "INBOUND",
  "quantity": 100,
  "reason": null,
  "note": "API 테스트 입고",
  "createdAt": "2026-01-18T15:02:01.591890",
  "syncedAt": null,
  "newStock": 100,
  "safetyAlert": false
}
```

### POST /api/v1/transactions/outbound (Outbound Stock)
**Request Body**: 
```json
{
  "product_id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "store_id": "45a3596d-df08-4b08-9408-480e843cc236",
  "quantity": 20,
  "note": "API 테스트 출고"
}
```
**Status Code**: 201
```json
{
  "id": "33643587-0ded-40c2-81a5-40f0abc9d7be",
  "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
  "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
  "type": "OUTBOUND",
  "quantity": -20,
  "reason": null,
  "note": "API 테스트 출고",
  "createdAt": "2026-01-18T15:02:01.651629",
  "syncedAt": null,
  "newStock": 80,
  "safetyAlert": false
}
```

### POST /api/v1/transactions/adjust (Adjust Stock)
**Request Body**: 
```json
{
  "product_id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "store_id": "45a3596d-df08-4b08-9408-480e843cc236",
  "quantity": -5,
  "reason": "DAMAGED",
  "note": "API 테스트 조정 (파손)"
}
```
**Status Code**: 201
```json
{
  "id": "d12827ad-9576-47cc-a6f7-c0c8f633c1ed",
  "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
  "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
  "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
  "type": "ADJUST",
  "quantity": -5,
  "reason": "DAMAGED",
  "note": "API 테스트 조정 (파손)",
  "createdAt": "2026-01-18T15:02:01.677785",
  "syncedAt": null,
  "newStock": 75,
  "safetyAlert": false
}
```

### GET /api/v1/transactions?store_id=45a3596d-df08-4b08-9408-480e843cc236&product_id=1f271b89-a2a9-426a-9e08-885e8549fbe8
**Status Code**: 200
```json
{
  "items": [
    {
      "id": "d12827ad-9576-47cc-a6f7-c0c8f633c1ed",
      "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
      "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
      "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
      "type": "ADJUST",
      "quantity": -5,
      "reason": "DAMAGED",
      "note": "API 테스트 조정 (파손)",
      "createdAt": "2026-01-18T15:02:01.677785",
      "syncedAt": null
    },
    {
      "id": "33643587-0ded-40c2-81a5-40f0abc9d7be",
      "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
      "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
      "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
      "type": "OUTBOUND",
      "quantity": -20,
      "reason": null,
      "note": "API 테스트 출고",
      "createdAt": "2026-01-18T15:02:01.651629",
      "syncedAt": null
    },
    {
      "id": "a98eba99-dd0d-4a8a-a8de-c088ce8da343",
      "productId": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
      "storeId": "45a3596d-df08-4b08-9408-480e843cc236",
      "userId": "b4f19a93-0904-4482-8b24-5645b61cbb17",
      "type": "INBOUND",
      "quantity": 100,
      "reason": null,
      "note": "API 테스트 입고",
      "createdAt": "2026-01-18T15:02:01.591890",
      "syncedAt": null
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 3,
    "totalPages": 1
  }
}
```

## 5. Inventory Check
### GET /api/v1/inventory/stocks?store_id=45a3596d-df08-4b08-9408-480e843cc236
**Status Code**: 200
```json
{
  "items": [
    {
      "product": {
        "id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
        "barcode": "8803272475977",
        "name": "테스트제품-SAMPLE",
        "safetyStock": 50
      },
      "store": {
        "id": "45a3596d-df08-4b08-9408-480e843cc236",
        "name": "테스트매장-STORE-ea7444da",
        "code": "STORE-ea7444da"
      },
      "quantity": 75,
      "status": "NORMAL",
      "lastAlertedAt": null
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

### GET /api/v1/inventory/stocks/1f271b89-a2a9-426a-9e08-885e8549fbe8 (Admin Detail)
**Status Code**: 200
```json
{
  "product": {
    "id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
    "barcode": "8803272475977",
    "name": "테스트제품-SAMPLE",
    "categoryId": "f19d1ec7-2413-4dd2-b19d-3ebd0d1c6c29",
    "safetyStock": 50,
    "imageUrl": null,
    "memo": null,
    "isActive": true,
    "createdAt": "2026-01-18T15:02:01.558102",
    "updatedAt": null
  },
  "stocks": [
    {
      "product": {
        "id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
        "barcode": "8803272475977",
        "name": "테스트제품-SAMPLE",
        "safetyStock": 50
      },
      "store": {
        "id": "45a3596d-df08-4b08-9408-480e843cc236",
        "name": "테스트매장-STORE-ea7444da",
        "code": "STORE-ea7444da"
      },
      "quantity": 75,
      "status": "NORMAL",
      "lastAlertedAt": null
    }
  ],
  "totalQuantity": 75
}
```

## 6. Additional Product Queries
### GET /api/v1/products (List)
**Status Code**: 200
```json
{
  "items": [
    {
      "id": "1f271b89-a2a9-426a-9e08-885e8549fbe8",
      "barcode": "8803272475977",
      "name": "테스트제품-SAMPLE",
      "categoryId": "f19d1ec7-2413-4dd2-b19d-3ebd0d1c6c29",
      "safetyStock": 50,
      "imageUrl": null,
      "memo": null,
      "isActive": true,
      "createdAt": "2026-01-18T15:02:01.558102",
      "updatedAt": null
    },
    {
      "id": "7d01094e-e412-47db-a357-dc6736a89696",
      "barcode": "8808224731820",
      "name": "테스트제품-SAMPLE",
      "categoryId": "c81882ca-2c67-4de4-953c-b8854a1827d0",
      "safetyStock": 50,
      "imageUrl": null,
      "memo": null,
      "isActive": true,
      "createdAt": "2026-01-18T15:00:43.570733",
      "updatedAt": null
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 9,
    "totalPages": 1
  }
}
... (truncated)
```

## 7. Admin Features
### GET /api/v1/admin/alerts/low-stock
**Status Code**: 200
```json
[]
```

