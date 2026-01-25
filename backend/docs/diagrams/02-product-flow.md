# 제품 (Product) 플로우

## 바코드 스캔 제품 조회

```mermaid
sequenceDiagram
    autonumber
    actor Worker as 작업자
    participant Scanner as 바코드 스캐너
    participant Client as 클라이언트
    participant API as Product API
    participant Service as Product Service
    participant DB as Database

    Worker->>Scanner: 바코드 스캔
    Scanner->>Client: 바코드 번호 전달
    Client->>API: GET /products/barcode/{barcode}
    
    API->>Service: get_product_by_barcode(barcode)
    Service->>DB: SELECT product + category<br/>WHERE barcode = ?
    
    alt 제품 없음
        DB-->>Service: null
        Service-->>API: null
        API-->>Client: 404 Not Found
        Client-->>Worker: "등록되지 않은 제품입니다"
        
        Note over Worker,Client: ADMIN인 경우<br/>신규 등록 화면으로 이동 가능
    else 제품 존재
        DB-->>Service: Product 객체
        Service-->>API: ProductResponse
        API-->>Client: 200 OK + 제품 정보
        Client-->>Worker: 제품명, 카테고리, 안전재고 표시
    end
```

---

## 제품 목록 조회 (검색/필터)

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant Client as 클라이언트
    participant API as Product API
    participant Service as Product Service
    participant DB as Database

    User->>Client: 검색어 입력 또는 카테고리 선택
    Client->>API: GET /products?search=xxx&category_id=xxx&page=1&limit=20
    
    API->>Service: list_products(search, category_id, page, limit)
    
    Service->>DB: SELECT products<br/>WHERE name ILIKE '%xxx%'<br/>OR barcode ILIKE '%xxx%'<br/>AND category_id = xxx<br/>ORDER BY created_at DESC<br/>LIMIT 20 OFFSET 0
    
    Service->>DB: SELECT COUNT(*) FROM products<br/>WHERE ...
    
    DB-->>Service: 제품 목록 + 총 개수
    Service-->>API: (items, total)
    
    API->>API: pagination 계산<br/>totalPages = ceil(total/limit)
    
    API-->>Client: 200 OK + ProductListResponse
    Client-->>User: 제품 목록 테이블 렌더링
```

---

## 신규 제품 등록 (ADMIN Only)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 관리자
    participant Client as 클라이언트
    participant API as Product API
    participant Service as Product Service
    participant DB as Database

    Admin->>Client: 바코드, 제품명, 카테고리,<br/>안전재고 입력
    Client->>API: POST /products
    
    API->>API: Depends(get_current_user)
    
    alt 권한 없음 (WORKER)
        API-->>Client: 403 Forbidden
        Client-->>Admin: "관리자만 등록 가능합니다"
    else ADMIN 권한 확인
        API->>Service: create_product(data)
        
        Service->>DB: SELECT product WHERE barcode = ?
        
        alt 바코드 중복
            DB-->>Service: 기존 제품
            Service-->>API: ConflictException
            API-->>Client: 409 Conflict
            Client-->>Admin: "이미 존재하는 바코드입니다"
        else 바코드 신규
            DB-->>Service: null
            
            Service->>DB: SELECT category WHERE id = ?
            
            alt 카테고리 없음
                DB-->>Service: null
                Service-->>API: NotFoundException
                API-->>Client: 404 Not Found
                Client-->>Admin: "카테고리를 찾을 수 없습니다"
            else 카테고리 존재
                DB-->>Service: Category
                
                Service->>DB: INSERT INTO products<br/>(barcode, name, category_id, safety_stock, ...)
                DB-->>Service: 생성된 Product
                
                Service-->>API: Product
                API-->>Client: 201 Created
                Client-->>Admin: "제품이 등록되었습니다"
            end
        end
    end
```

---

## 내부 바코드 생성 플로우

바코드가 없는 제품의 경우 내부 바코드를 자동 생성합니다.

```mermaid
flowchart TD
    Start([제품 등록 시작]) --> HasBarcode{외부 바코드<br/>있음?}
    
    HasBarcode -->|Yes| UseExternal[외부 바코드 사용]
    HasBarcode -->|No| SelectCategory[카테고리 선택]
    
    SelectCategory --> GetCode[카테고리 코드 조회<br/>ex: SK, MU, HC]
    GetCode --> CountProducts[해당 카테고리<br/>제품 수 조회]
    CountProducts --> GenerateBarcode["내부 바코드 생성<br/>DON-{카테고리코드}-{순번}"]
    
    GenerateBarcode --> Example["예: DON-SK-00042"]
    
    UseExternal --> CheckDuplicate{중복 체크}
    Example --> CheckDuplicate
    
    CheckDuplicate -->|중복| Error[409 Conflict 반환]
    CheckDuplicate -->|신규| Register[제품 등록]
    
    Register --> End([등록 완료])
    Error --> End
```

---

## 제품 관련 테이블 구조

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `id` | UUID | 고유 식별자 |
| `barcode` | VARCHAR(50) | 바코드 (유니크) |
| `name` | VARCHAR(200) | 제품명 |
| `category_id` | UUID FK | 카테고리 |
| `safety_stock` | INTEGER | 안전재고 임계값 |
| `image_url` | VARCHAR(500) | 제품 이미지 |
| `memo` | TEXT | 메모 |
| `is_active` | BOOLEAN | 활성화 여부 |
