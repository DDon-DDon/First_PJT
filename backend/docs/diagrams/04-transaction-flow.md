# 트랜잭션 (Transaction) 플로우

## 입고 처리 시퀀스

```mermaid
sequenceDiagram
    autonumber
    actor Worker as 작업자
    participant Client as 클라이언트
    participant API as Transaction API
    participant Service as Inventory Service
    participant DB as Database

    Worker->>Client: 바코드 스캔 + 수량 입력
    Client->>API: POST /transactions/inbound
    Note over Client,API: { productId, storeId, quantity, note }
    
    API->>API: Depends(get_current_user)
    API->>Service: process_inbound(data, user)
    
    Service->>DB: SELECT current_stock<br/>WHERE product_id = ? AND store_id = ?
    
    alt 재고 레코드 없음
        DB-->>Service: null
        Service->>DB: INSERT current_stocks<br/>(product_id, store_id, quantity=0)
        DB-->>Service: 새 CurrentStock
    else 재고 레코드 존재
        DB-->>Service: CurrentStock
    end
    
    Service->>DB: INSERT INTO inventory_transactions<br/>(product_id, store_id, user_id,<br/>type='INBOUND', quantity=+30, note)
    
    Service->>DB: UPDATE current_stocks<br/>SET quantity = quantity + 30
    
    DB-->>Service: 커밋 완료
    Service-->>API: (transaction, new_stock=55, safety_alert=false)
    
    API-->>Client: 201 Created + TransactionResultResponse
    Client-->>Worker: "입고 완료: 현재 재고 55개"
```

---

## 출고 처리 시퀀스

```mermaid
sequenceDiagram
    autonumber
    actor Worker as 작업자
    participant Client as 클라이언트
    participant API as Transaction API
    participant Service as Inventory Service
    participant DB as Database

    Worker->>Client: 바코드 스캔 + 출고 수량 입력
    Client->>API: POST /transactions/outbound
    Note over Client,API: { productId, storeId, quantity, note }
    
    API->>API: Depends(get_current_user)
    API->>Service: process_outbound(data, user)
    
    Service->>DB: SELECT current_stock + product<br/>WHERE product_id = ? AND store_id = ?
    
    alt 재고 레코드 없음
        Service->>DB: CREATE current_stock (qty=0)
    end
    
    DB-->>Service: CurrentStock (quantity=50)
    
    alt 재고 부족 (quantity < requested)
        Service-->>API: InsufficientStockException
        API-->>Client: 400 Bad Request
        Note over Client: { code: "INSUFFICIENT_STOCK",<br/>currentStock: 5, requestedQuantity: 10 }
        Client-->>Worker: "재고가 부족합니다<br/>현재: 5개, 요청: 10개"
    else 재고 충분
        Service->>DB: INSERT INTO inventory_transactions<br/>(type='OUTBOUND', quantity=-10)
        
        Service->>DB: UPDATE current_stocks<br/>SET quantity = quantity - 10
        
        DB-->>Service: 커밋 완료
        
        Service->>Service: 안전재고 체크<br/>new_qty < safety_stock?
        
        alt 안전재고 이하
            Service-->>API: safety_alert = true
        else 안전재고 초과
            Service-->>API: safety_alert = false
        end
        
        API-->>Client: 201 Created
        Client-->>Worker: "출고 완료: 현재 재고 40개"
        
        opt safety_alert = true
            Client-->>Worker: "⚠️ 안전재고 이하입니다"
        end
    end
```

---

## 재고 조정 시퀀스

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 관리자/작업자
    participant Client as 클라이언트
    participant API as Transaction API
    participant Service as Inventory Service
    participant DB as Database

    Admin->>Client: 조정 사유 선택 + 수량 입력
    Note over Admin,Client: 조정 사유:<br/>EXPIRED(유통기한만료), DAMAGED(파손),<br/>CORRECTION(오류정정), OTHER(기타)
    
    Client->>API: POST /transactions/adjust
    Note over Client,API: { productId, storeId,<br/>quantity: -5, reason: "EXPIRED", note }
    
    API->>API: Depends(get_current_user)
    API->>Service: process_adjust(data, user)
    
    Service->>DB: SELECT current_stock<br/>WHERE product_id = ? AND store_id = ?
    DB-->>Service: CurrentStock (quantity=50)
    
    alt 음수 조정 시 재고 부족
        Note over Service: quantity=-60 요청<br/>current=50
        Service-->>API: InsufficientStockException
        API-->>Client: 400 Bad Request
        Client-->>Admin: "재고를 음수로 만들 수 없습니다"
    else 조정 가능
        Service->>DB: INSERT INTO inventory_transactions<br/>(type='ADJUST', quantity=-5,<br/>reason='EXPIRED', note)
        
        Service->>DB: UPDATE current_stocks<br/>SET quantity = quantity - 5
        
        DB-->>Service: 커밋 완료
        Service-->>API: (transaction, new_stock=45)
        API-->>Client: 201 Created
        Client-->>Admin: "재고 조정 완료: 현재 45개"
    end
```

---

## 트랜잭션 처리 플로우차트

```mermaid
flowchart TD
    Start([트랜잭션 요청]) --> GetStock[현재고 조회/생성]
    
    GetStock --> CheckType{트랜잭션 타입}
    
    CheckType -->|INBOUND| Inbound[수량 양수로 기록<br/>quantity = +N]
    CheckType -->|OUTBOUND| CheckOutbound{재고 충분?}
    CheckType -->|ADJUST| CheckAdjust{음수 조정 시<br/>재고 충분?}
    
    CheckOutbound -->|No| Error400[400 Bad Request<br/>INSUFFICIENT_STOCK]
    CheckOutbound -->|Yes| Outbound[수량 음수로 기록<br/>quantity = -N]
    
    CheckAdjust -->|No| Error400
    CheckAdjust -->|Yes| Adjust[수량 그대로 기록<br/>quantity = N or -N]
    
    Inbound --> UpdateStock[현재고 업데이트]
    Outbound --> UpdateStock
    Adjust --> UpdateStock
    
    UpdateStock --> CreateTx[트랜잭션 레코드 생성]
    CreateTx --> Commit[DB 커밋]
    
    Commit --> CheckSafety{출고 시<br/>안전재고 체크}
    
    CheckSafety -->|qty < safety| Alert[safety_alert = true]
    CheckSafety -->|qty >= safety| NoAlert[safety_alert = false]
    
    Alert --> Response[응답 반환]
    NoAlert --> Response
    Error400 --> End([종료])
    Response --> End
```

---

## 트랜잭션 이력 조회

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Client as 클라이언트
    participant API as Transaction API
    participant Service as Inventory Service
    participant DB as Database

    User->>Client: 이력 조회 (필터 적용)
    Client->>API: GET /transactions?store_id=xxx&product_id=xxx&type=INBOUND&page=1
    
    API->>Service: list_transactions(filters, page, limit)
    
    Service->>DB: SELECT transactions<br/>JOIN product, store, user<br/>WHERE filters...<br/>ORDER BY created_at DESC
    
    Service->>DB: SELECT COUNT(*)
    
    DB-->>Service: (items, total)
    
    Service-->>API: TransactionListResponse
    API-->>Client: 200 OK
    Client-->>User: 트랜잭션 이력 테이블 표시
```

---

## 트랜잭션 테이블 구조 (inventory_transactions)

Append-Only 패턴으로 모든 변경 이력을 보존합니다.

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `id` | UUID PK | 고유 식별자 |
| `product_id` | UUID FK | 제품 |
| `store_id` | UUID FK | 매장 |
| `user_id` | UUID FK | 처리자 |
| `type` | ENUM | INBOUND, OUTBOUND, ADJUST |
| `quantity` | INTEGER | 변화량 (+/-) |
| `reason` | ENUM | EXPIRED, DAMAGED, CORRECTION, OTHER |
| `note` | TEXT | 비고 |
| `created_at` | TIMESTAMP | 트랜잭션 시간 |
| `synced_at` | TIMESTAMP | 동기화 시간 |
| `local_id` | UUID | 오프라인 생성 ID |
