# 오프라인 동기화 (Sync) 플로우

## 오프라인 동작 개요

```mermaid
flowchart TD
    subgraph Online["온라인 상태"]
        O1[정상 입출고 처리]
        O2[서버로 직접 전송]
        O3[즉시 DB 반영]
    end
    
    subgraph Offline["오프라인 상태"]
        F1[네트워크 감지]
        F2[로컬 IndexedDB 저장]
        F3[Pending Queue 추가]
        F4[동기화 대기 표시]
    end
    
    subgraph Sync["동기화 프로세스"]
        S1[네트워크 복구 감지]
        S2[Pending 항목 조회]
        S3[일괄 전송]
        S4[결과 처리]
    end
    
    Start([트랜잭션 요청]) --> CheckNetwork{네트워크<br/>상태?}
    
    CheckNetwork -->|Online| O1
    O1 --> O2
    O2 --> O3
    
    CheckNetwork -->|Offline| F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    F4 --> WaitNetwork([네트워크 대기])
    WaitNetwork --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> End([완료])
    O3 --> End
```

---

## 오프라인 트랜잭션 동기화 시퀀스

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Client as 클라이언트
    participant Local as LocalDB<br/>(IndexedDB)
    participant API as Sync API
    participant Service as Sync Service
    participant DB as Server DB

    Note over User,DB: 오프라인 상태에서 작업 수행
    
    User->>Client: 입고/출고 처리
    Client->>Client: 네트워크 상태 확인
    Client->>Local: 트랜잭션 로컬 저장<br/>(local_id 생성)
    Client-->>User: "오프라인 저장 완료<br/>동기화 대기 중 (1건)"
    
    Note over User,DB: 시간 경과... 네트워크 복구
    
    Client->>Client: 온라인 감지
    Client->>Local: Pending 트랜잭션 조회
    Local-->>Client: [tx1, tx2, tx3]
    
    Client->>API: POST /sync/transactions
    Note over Client,API: { transactions: [<br/>  { localId, type, productId, storeId,<br/>    quantity, createdAt },<br/>  ...<br/>] }
    
    API->>Service: sync_transactions(request, user)
    
    loop 각 트랜잭션
        Service->>DB: SELECT WHERE local_id = ?
        
        alt 이미 동기화됨 (중복)
            DB-->>Service: 기존 트랜잭션
            Service->>Service: synced에 추가<br/>(localId → serverId)
        else 신규 트랜잭션
            alt INBOUND
                Service->>Service: process_inbound()
            else OUTBOUND
                Service->>Service: process_outbound()
            else ADJUST
                Service->>Service: process_adjust()
            end
            
            alt 처리 성공
                Service->>DB: UPDATE tx SET<br/>local_id, synced_at
                Service->>Service: synced에 추가
            else 처리 실패
                Service->>DB: ROLLBACK
                Service->>Service: failed에 추가<br/>(localId, error)
            end
        end
    end
    
    Service-->>API: SyncResponse
    API-->>Client: 200 OK
    Note over Client: { synced: [...], failed: [...],<br/>syncedAt: timestamp }
    
    Client->>Local: synced 항목 삭제
    Client->>Local: failed 항목 유지<br/>(재시도 대상)
    
    Client-->>User: "동기화 완료 (3건 성공)"
```

---

## 중복 방지 메커니즘

```mermaid
flowchart TD
    Start([동기화 요청]) --> Loop{다음 트랜잭션}
    
    Loop --> Check[local_id로<br/>기존 트랜잭션 조회]
    
    Check --> Exists{DB에 존재?}
    
    Exists -->|Yes| Skip[건너뛰기<br/>synced 목록에 추가]
    Exists -->|No| Process[트랜잭션 처리]
    
    Process --> SetLocalId["tx.local_id = local_id<br/>tx.synced_at = now()"]
    SetLocalId --> Save[DB 저장]
    
    Save --> Success{성공?}
    
    Success -->|Yes| AddSynced[synced 목록에 추가]
    Success -->|No| Rollback[롤백]
    Rollback --> AddFailed[failed 목록에 추가]
    
    Skip --> Next{더 있음?}
    AddSynced --> Next
    AddFailed --> Next
    
    Next -->|Yes| Loop
    Next -->|No| Return[응답 반환]
    
    Return --> End([종료])
```

---

## 동기화 실패 처리

```mermaid
sequenceDiagram
    participant Client as 클라이언트
    participant API as Sync API
    participant Service as Sync Service

    Client->>API: POST /sync/transactions
    Note over Client,API: [tx1, tx2, tx3]
    
    API->>Service: sync_transactions()
    
    Note over Service: tx1: 성공
    Note over Service: tx2: 재고 부족 오류
    Note over Service: tx3: 성공
    
    Service-->>API: SyncResponse
    Note over API: synced: [tx1, tx3]<br/>failed: [{localId: tx2, error: "재고 부족"}]
    
    API-->>Client: 200 OK
    
    Client->>Client: tx1, tx3 로컬 삭제
    Client->>Client: tx2 유지 (재시도)
    
    alt 자동 재시도 (최대 3회)
        loop 재시도
            Client->>API: POST /sync/transactions [tx2]
        end
    else 모든 재시도 실패
        Client-->>Client: 사용자에게 알림<br/>"일부 항목 동기화 실패"
    end
```

---

## 동기화 상태 표시 UI

```mermaid
stateDiagram-v2
    [*] --> Online: 앱 시작
    
    Online --> Offline: 네트워크 끊김
    Offline --> Syncing: 네트워크 복구
    Syncing --> Online: 동기화 완료
    Syncing --> PartialFail: 일부 실패
    PartialFail --> Syncing: 재시도
    PartialFail --> Online: 실패 항목 포기
    
    state Online {
        [*] --> Normal
        Normal --> PendingZero: 대기 건 없음
    }
    
    state Offline {
        [*] --> Working
        Working --> Pending: 트랜잭션 저장
        Pending --> MorePending: 추가 트랜잭션
    }
    
    state Syncing {
        [*] --> Uploading
        Uploading --> Processing
        Processing --> Done
    }
```

---

## 동기화 요청/응답 스키마

### Request
```json
{
  "transactions": [
    {
      "localId": "uuid-client-generated",
      "type": "INBOUND | OUTBOUND | ADJUST",
      "productId": "uuid",
      "storeId": "uuid",
      "quantity": 30,
      "reason": "EXPIRED",  // ADJUST인 경우만
      "note": "비고",
      "createdAt": "2024-01-15T09:30:00Z"
    }
  ]
}
```

### Response
```json
{
  "synced": [
    { "localId": "...", "serverId": "uuid-server-generated" }
  ],
  "failed": [
    { "localId": "...", "error": "재고가 부족합니다" }
  ],
  "syncedAt": "2024-01-15T10:00:00Z"
}
```
