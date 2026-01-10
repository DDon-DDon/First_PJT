# 똔똔(DoneDone) 향후 개발 로드맵 (Future Roadmap)

**작성일**: 2026-01-10
**현재 상태**: 백엔드 MVP 핵심 기능 구현 완료 (Auth 제외)

---

## 📅 전체 일정 개요

| 단계 | 목표 | 주요 작업 | 예상 기간 |
|:---:|:---|:---|:---:|
| **Phase 2** | **인증/보안 완성** | JWT 구현, 로그인/로그아웃, 보안 강화 | 1주 |
| **Phase 9** | **프론트엔드 (Worker)** | 모바일 웹 앱, 바코드 스캐너, 입출고 UI | 2주 |
| **Phase 10** | **프론트엔드 (Admin)** | PC 대시보드, 제품 관리, 재고 리포트 | 2주 |
| **Phase 11** | **DevOps & 배포** | Docker 최적화, CI/CD, 클라우드 배포 | 1주 |
| **Phase 12** | **고도화 (Advanced)** | 이미지 업로드, 알림 발송, 통계 분석 | 2주 |

---

## 🚀 상세 로드맵

### 🔐 Phase 2: 인증 시스템 완성 (Technical Debt)
현재 Mocking으로 처리된 인증 로직을 실제 JWT 기반 보안 시스템으로 교체합니다.

- [ ] **JWT 로직 구현**: `python-jose` 활용 Access/Refresh Token 발급 및 검증
- [ ] **로그인 API**: `POST /auth/login` (이메일/비번 검증)
- [ ] **토큰 갱신 API**: `POST /auth/refresh` (Refresh Token Rotation)
- [ ] **미들웨어 적용**: API 엔드포인트에 실제 `Depends(get_current_user)` 적용 및 권한 테스트
- [ ] **비밀번호 관리**: 회원가입(초기 Admin 생성) 스크립트 및 비번 변경 기능

### 📱 Phase 9: 현장 작업자용 모바일 웹 앱 (Frontend - Worker)
매장에서 바코드를 스캔하고 즉시 재고를 처리하는 모바일 중심의 웹 애플리케이션입니다.

- [ ] **기술 스택**: Next.js (App Router), Tailwind CSS, Shadcn UI
- [ ] **PWA 적용**: 오프라인 지원을 위한 Service Worker 및 Manifest 설정
- [ ] **바코드 스캔**: 모바일 카메라 연동 (e.g., `html5-qrcode` 또는 `react-qr-reader`)
- [ ] **오프라인 저장소**: `IndexedDB` (Dexie.js) 활용하여 트랜잭션 로컬 저장
- [ ] **동기화 로직**: 네트워크 복구 시 백엔드 `Sync API` 호출 구현

### 🖥️ Phase 10: 관리자 대시보드 (Frontend - Admin)
매장 전체 현황을 파악하고 마스터 데이터를 관리하는 PC 웹입니다.

- [ ] **대시보드 UI**: `Recharts` 활용 재고 추이 그래프, 부족 알림 위젯
- [ ] **데이터 그리드**: `TanStack Table` 활용 제품/재고 목록 조회 및 필터링
- [ ] **엑셀 연동**: 백엔드 엑셀 다운로드 API 연동
- [ ] **제품 관리**: 제품 등록/수정 모달 및 폼 구현

### ☁️ Phase 11: 인프라 및 배포 (DevOps)
로컬 개발 환경을 넘어 실제 운영 가능한 환경을 구축합니다.

- [ ] **Docker Compose**: Frontend + Backend + DB 통합 구성
- [ ] **CI/CD**: GitHub Actions를 통한 자동 테스트 및 빌드
- [ ] **클라우드 배포**: Railway 또는 AWS/GCP 배포 (HTTPS 적용)
- [ ] **모니터링**: Sentry (에러 추적) 및 Prometheus/Grafana (성능 모니터링) 도입 검토

### 💎 Phase 12: 기능 고도화 (Advanced Features)
사용자 경험을 향상시키는 부가 기능입니다.

- [ ] **이미지 업로드**: S3 또는 로컬 스토리지 연동 제품 이미지 등록
- [ ] **알림 시스템**: 안전재고 미만 시 이메일/Slack/SMS 알림 발송 (Background Task)
- [ ] **통계 분석**: 기간별 입출고 추이, 회전율 분석 API
- [ ] **멀티 테넌시**: 여러 회사(브랜드)가 사용할 수 있도록 구조 확장 검토

---

## 📝 논의 사항 (Discussion Points)

1. **프론트엔드 착수 시점**: 백엔드 Auth(Phase 2)를 먼저 끝내고 시작할지, 병렬로 진행할지 결정 필요. (Mock API 활용 가능)
2. **오프라인 동기화 전략**: 클라이언트 측 `IndexedDB` 설계 및 충돌 해결 UI 기획 필요.
3. **배포 환경**: 비용 효율적인 호스팅 서비스 선정 (Vercel + Railway 조합 추천).
