# 인증 (Auth) 플로우

## 로그인 시퀀스

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Client as 클라이언트
    participant API as Auth API
    participant Service as Auth Service
    participant DB as Database

    User->>Client: 이메일/비밀번호 입력
    Client->>API: POST /auth/login
    API->>Service: authenticate(email, password)
    
    Service->>DB: SELECT user WHERE email = ?
    
    alt 사용자 없음
        DB-->>Service: null
        Service-->>API: AuthenticationError
        API-->>Client: 401 Unauthorized
        Client-->>User: "이메일 또는 비밀번호가 올바르지 않습니다"
    else 사용자 존재
        DB-->>Service: User 객체
        Service->>Service: verify_password(password, hash)
        
        alt 비밀번호 불일치
            Service-->>API: AuthenticationError
            API-->>Client: 401 Unauthorized
            Client-->>User: "이메일 또는 비밀번호가 올바르지 않습니다"
        else 비밀번호 일치
            Service->>Service: create_access_token(user_id)
            Service->>Service: create_refresh_token(user_id)
            Service->>DB: SELECT stores WHERE user_id = ?
            DB-->>Service: 배정된 매장 목록
            Service-->>API: TokenResponse
            API-->>Client: 200 OK + tokens + user info
            Client->>Client: 토큰 로컬 저장
            Client-->>User: 로그인 성공, 대시보드 이동
        end
    end
```

---

## JWT 토큰 검증 플로우

```mermaid
sequenceDiagram
    autonumber
    participant Client as 클라이언트
    participant API as FastAPI
    participant Deps as get_current_user
    participant JWT as JWT Utils

    Client->>API: Request + Authorization: Bearer {token}
    API->>Deps: Depends(get_current_user)
    Deps->>Deps: Extract token from header
    
    alt 토큰 없음
        Deps-->>API: 401 Unauthorized
        API-->>Client: "인증이 필요합니다"
    else 토큰 존재
        Deps->>JWT: decode_token(token)
        
        alt 토큰 만료/유효하지 않음
            JWT-->>Deps: InvalidTokenError
            Deps-->>API: 401 Unauthorized
            API-->>Client: "토큰이 만료되었거나 유효하지 않습니다"
        else 토큰 유효
            JWT-->>Deps: payload (user_id, role)
            Deps->>Deps: get_user_from_db(user_id)
            Deps-->>API: User 객체
            API->>API: 요청 처리 계속
        end
    end
```

---

## 권한 체크 플로우차트

```mermaid
flowchart TD
    Start([API 요청]) --> CheckAuth{인증 토큰<br/>존재?}
    
    CheckAuth -->|No| Deny401[401 Unauthorized]
    CheckAuth -->|Yes| ValidateToken{토큰 유효?}
    
    ValidateToken -->|No| Deny401
    ValidateToken -->|Yes| GetRole{사용자 역할<br/>확인}
    
    GetRole --> CheckEndpoint{엔드포인트<br/>권한 요구사항}
    
    CheckEndpoint -->|ADMIN Only| IsAdmin{ADMIN?}
    CheckEndpoint -->|All Users| CheckStore{매장 접근<br/>권한 체크}
    
    IsAdmin -->|Yes| CheckStore
    IsAdmin -->|No| Deny403[403 Forbidden]
    
    CheckStore --> IsWorker{WORKER?}
    
    IsWorker -->|Yes| AssignedStore{배정된 매장<br/>요청?}
    IsWorker -->|No| Allow[요청 처리]
    
    AssignedStore -->|Yes| Allow
    AssignedStore -->|No| Deny403
    
    Allow --> End([응답 반환])
    Deny401 --> End
    Deny403 --> End
```

---

## 역할별 기능 매트릭스

| 기능 | WORKER | ADMIN |
|------|--------|-------|
| 로그인 | ✅ | ✅ |
| 배정 매장 재고 조회 | ✅ | ✅ |
| 전체 매장 재고 조회 | ❌ | ✅ |
| 입고/출고/조정 처리 | ✅ (배정 매장) | ✅ (전체) |
| 신규 제품 등록 | ❌ | ✅ |
| 안전재고 알림 조회 | ❌ | ✅ |
| 엑셀 내보내기 | ❌ | ✅ |
