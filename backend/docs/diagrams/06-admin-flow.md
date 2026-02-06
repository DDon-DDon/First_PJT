# 관리자 (Admin) 기능 플로우

## 안전재고 이하 알림 조회

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 관리자
    participant Client as 클라이언트
    participant API as Admin API
    participant Service as Report Service
    participant DB as Database

    Admin->>Client: 대시보드 접근
    Client->>API: GET /alerts/low-stock
    
    API->>API: Depends(get_current_user)
    
    alt WORKER 사용자
        API-->>Client: 403 Forbidden
        Client-->>Admin: "관리자만 접근 가능합니다"
    else ADMIN 사용자
        API->>Service: get_low_stock_alerts()
        
        Service->>DB: SELECT current_stocks<br/>JOIN products, stores<br/>WHERE quantity < safety_stock
        
        DB-->>Service: 안전재고 이하 목록
        
        loop 각 항목
            Service->>Service: shortage 계산<br/>= safety_stock - quantity
        end
        
        Service-->>API: LowStockAlertList
        API-->>Client: 200 OK
        
        Client-->>Admin: 안전재고 이하 제품 목록<br/>(하이라이트 표시)
    end
```

---

## 안전재고 알림 대시보드 뷰

```mermaid
flowchart TD
    subgraph Dashboard["관리자 대시보드"]
        Header[/"안전재고 이하 목록<br/>(총 5건)"/]
        
        subgraph List["제품 목록"]
            P1["🔴 수분크림 50ml<br/>강남 1호점: 8개 (부족 2개)"]
            P2["🔴 선크림 30ml<br/>홍대점: 3개 (부족 7개)"]
            P3["🔴 클렌징폼<br/>강남 1호점: 5개 (부족 5개)"]
        end
        
        Actions["📥 엑셀 다운로드"]
    end
    
    Header --> List
    List --> Actions
```

---

## 엑셀 내보내기 플로우

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 관리자
    participant Client as 클라이언트
    participant API as Admin API
    participant Service as Report Service
    participant DB as Database

    Admin->>Client: "엑셀 다운로드" 클릭
    Client->>API: GET /exports/low-stock
    
    API->>API: Depends(get_current_user)
    
    alt 권한 없음
        API-->>Client: 403 Forbidden
    else ADMIN 확인
        API->>Service: export_low_stock_excel()
        
        Service->>DB: SELECT 안전재고 이하 목록
        DB-->>Service: 데이터
        
        Service->>Service: Excel 파일 생성<br/>(openpyxl/xlsxwriter)
        
        Service-->>API: Excel 바이트 스트림
        
        API-->>Client: Content-Type:<br/>application/vnd.openxmlformats-...<br/>Content-Disposition:<br/>attachment; filename="low_stock_YYYYMMDD.xlsx"
        
        Client-->>Admin: 파일 다운로드 시작
    end
```

---

## 권한 체크 플로우차트

```mermaid
flowchart TD
    Start([관리자 API 요청]) --> Auth{인증됨?}
    
    Auth -->|No| 401[401 Unauthorized]
    Auth -->|Yes| GetRole[사용자 역할 확인]
    
    GetRole --> CheckAdmin{role == ADMIN?}
    
    CheckAdmin -->|No| 403[403 Forbidden<br/>"Only ADMIN can access"]
    CheckAdmin -->|Yes| Process[요청 처리]
    
    Process --> Success[200 OK]
    
    401 --> End([종료])
    403 --> End
    Success --> End
```

---

## 안전재고 알림 트리거

출고 처리 시 자동으로 안전재고 체크가 수행됩니다.

```mermaid
sequenceDiagram
    participant Service as Inventory Service
    participant DB as Database
    participant AlertQueue as 알림 큐<br/>(향후 구현)

    Note over Service: 출고 처리 완료
    
    Service->>DB: 현재 재고 조회
    DB-->>Service: quantity = 8
    
    Service->>DB: 안전재고 조회
    DB-->>Service: safety_stock = 10
    
    Service->>Service: safety_alert = (8 < 10) = true
    
    alt safety_alert = true
        Service->>DB: UPDATE current_stocks<br/>SET last_alerted_at = NOW()
        
        opt 향후 기능
            Service->>AlertQueue: 알림 발송 요청
            Note over AlertQueue: - 이메일<br/>- 푸시 알림<br/>- 슬랙 등
        end
    end
    
    Service-->>Service: 응답에 safety_alert 포함
```

---

## 관리자 전용 API 목록

| 엔드포인트 | 메서드 | 설명 | 응답 |
|------------|--------|------|------|
| `/alerts/low-stock` | GET | 안전재고 이하 목록 | JSON |
| `/exports/low-stock` | GET | 안전재고 이하 엑셀 | Excel 파일 |
| `/inventory/stocks/{productId}` | GET | 제품별 전체 매장 재고 | JSON |
| `/products` | POST | 신규 제품 등록 | JSON |
| `/products/generate-barcode` | POST | 내부 바코드 생성 | JSON |

---

## 안전재고 알림 응답 스키마

```json
{
  "success": true,
  "data": [
    {
      "product": {
        "id": "uuid",
        "name": "수분크림 50ml",
        "safetyStock": 10
      },
      "store": {
        "id": "uuid",
        "name": "강남 1호점"
      },
      "currentStock": 8,
      "shortage": 2
    }
  ]
}
```
