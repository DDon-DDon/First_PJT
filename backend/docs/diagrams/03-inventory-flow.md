# 재고 (Inventory) 조회 플로우

## 현재고 목록 조회

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Client as 클라이언트
    participant API as Inventory API
    participant Service as Inventory Service
    participant DB as Database

    User->>Client: 재고 현황 페이지 접근
    Client->>API: GET /inventory/stocks?store_id=xxx&category_id=xxx&status=LOW&page=1
    
    API->>API: Depends(get_current_user)
    API->>Service: get_current_stocks(user, filters)
    
    alt WORKER 사용자
        Service->>DB: SELECT store_id FROM user_stores<br/>WHERE user_id = ?
        DB-->>Service: 배정된 매장 ID 목록
        
        alt store_id 파라미터 지정
            Service->>Service: 배정 매장 목록에<br/>포함되는지 확인
            
            alt 접근 불가 매장
                Service-->>API: ForbiddenException
                API-->>Client: 403 Forbidden
                Client-->>User: "접근 권한이 없습니다"
            end
        else store_id 미지정
            Service->>Service: 배정된 모든 매장으로 조회
        end
    else ADMIN 사용자
        Service->>Service: 모든 매장 조회 가능
    end
    
    Service->>DB: SELECT current_stocks<br/>JOIN products, stores<br/>WHERE filters...
    
    alt status 필터 적용
        Note over Service,DB: LOW: quantity < safety_stock<br/>NORMAL: safety_stock <= qty < safety_stock*2<br/>GOOD: quantity >= safety_stock*2
    end
    
    DB-->>Service: 재고 목록
    
    loop 각 재고 항목
        Service->>Service: get_stock_status(quantity, safety_stock)
    end
    
    Service-->>API: (items with status, total)
    API-->>Client: 200 OK + StockListResponse
    Client-->>User: 재고 현황 테이블 표시
```

---

## 재고 상태 계산 로직

```mermaid
flowchart TD
    Start([재고 수량 확인]) --> Compare{현재고 vs<br/>안전재고}
    
    Compare -->|"quantity < safety_stock"| LOW["🔴 LOW<br/>재고 부족"]
    Compare -->|"safety_stock <= quantity < safety_stock*2"| NORMAL["🟡 NORMAL<br/>적정 재고"]
    Compare -->|"quantity >= safety_stock*2"| GOOD["🟢 GOOD<br/>재고 충분"]
    
    LOW --> Display[상태 표시<br/>하이라이트]
    NORMAL --> Display
    GOOD --> Display
```

**예시** (안전재고 = 10):
| 현재고 | 상태 |
|--------|------|
| 5 | 🔴 LOW |
| 15 | 🟡 NORMAL |
| 25 | 🟢 GOOD |

---

## 제품별 매장 재고 상세 조회 (ADMIN Only)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 관리자
    participant Client as 클라이언트
    participant API as Inventory API
    participant Service as Inventory Service
    participant DB as Database

    Admin->>Client: 특정 제품 상세 조회
    Client->>API: GET /inventory/stocks/{productId}
    
    API->>API: Depends(get_current_user)
    API->>Service: get_product_stock_detail(product_id, user)
    
    alt WORKER 사용자
        Service-->>API: ForbiddenException
        API-->>Client: 403 Forbidden
        Client-->>Admin: "관리자만 조회 가능합니다"
    else ADMIN 사용자
        Service->>DB: SELECT product WHERE id = ?
        
        alt 제품 없음
            DB-->>Service: null
            Service-->>API: (null, [])
            API-->>Client: 404 Not Found
        else 제품 존재
            DB-->>Service: Product
            
            Service->>DB: SELECT current_stocks<br/>JOIN stores<br/>WHERE product_id = ?
            DB-->>Service: 매장별 재고 목록
            
            loop 각 매장 재고
                Service->>Service: get_stock_status(qty, safety_stock)
                Service->>Service: total_quantity += qty
            end
            
            Service-->>API: ProductStockDetailResponse
            API-->>Client: 200 OK
            Client-->>Admin: 매장별 재고 현황 표시
        end
    end
```

---

## 재고 조회 권한 매트릭스

```mermaid
flowchart LR
    subgraph Request["요청"]
        R1["GET /inventory/stocks"]
        R2["GET /inventory/stocks/{productId}"]
    end
    
    subgraph WORKER["WORKER 권한"]
        W1["✅ 배정 매장만"]
        W2["❌ 접근 불가"]
    end
    
    subgraph ADMIN["ADMIN 권한"]
        A1["✅ 전체 매장"]
        A2["✅ 전체 매장"]
    end
    
    R1 --> W1
    R1 --> A1
    R2 --> W2
    R2 --> A2
```

---

## 현재고 테이블 구조 (current_stocks)

복합 PK를 사용하여 제품-매장 조합당 하나의 레코드만 존재합니다.

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `product_id` | UUID PK, FK | 제품 ID |
| `store_id` | UUID PK, FK | 매장 ID |
| `quantity` | INTEGER | 현재 재고 수량 |
| `last_alerted_at` | TIMESTAMP | 마지막 안전재고 알림 시간 |
| `updated_at` | TIMESTAMP | 마지막 업데이트 시간 |

```sql
-- 현재고 빠른 조회를 위한 인덱스
CREATE INDEX idx_current_stock_store ON current_stocks(store_id);
```
