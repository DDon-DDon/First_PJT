# Postman Collection 사용 가이드

## 1. Collection Import

OpenAPI 스펙에서 자동으로 Collection을 생성합니다:

1. Postman 실행
2. **Import** 클릭
3. **Link** 탭 선택
4. URL 입력: `http://localhost:8000/openapi.json`
5. **Continue** → **Import**

## 2. Environment 설정

1. **Environments** 탭으로 이동
2. **Import** 클릭
3. `postman/environments/donedone-local.json` 선택
4. 우측 상단에서 `DoneDone - Local` 환경 선택

## 3. 인증 토큰 설정

로그인 후 받은 `accessToken`을 환경 변수에 설정:

1. **Environments** → `DoneDone - Local`
2. `access_token` 값에 토큰 입력
3. **Save**

또는 Collection 설정에서 자동 인증:

1. Collection 우클릭 → **Edit**
2. **Authorization** 탭
3. Type: `Bearer Token`
4. Token: `{{access_token}}`

## 4. 환경 변수 설명

| 변수 | 설명 |
|------|------|
| `base_url` | API 서버 주소 |
| `api_prefix` | API 버전 접두사 (`/api/v1`) |
| `access_token` | JWT 액세스 토큰 (로그인 후 설정) |
| `test_admin_email` | 테스트용 관리자 이메일 |
| `test_store_id` | 테스트용 매장 UUID |
| `test_product_id` | 테스트용 제품 UUID |

## 5. 요청 예시

### 제품 바코드 조회
```
GET {{base_url}}{{api_prefix}}/products/barcode/8801234567890
Authorization: Bearer {{access_token}}
```

### 재고 목록 조회
```
GET {{base_url}}{{api_prefix}}/inventory/stocks?store_id={{test_store_id}}&status=LOW
Authorization: Bearer {{access_token}}
```
