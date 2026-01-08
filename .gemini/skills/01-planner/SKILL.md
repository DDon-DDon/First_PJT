---
name: Development Planner
description: 프로젝트 요구사항 분석 → 상세 계획 수립 (PRD & 리스크 분석 포함)
keywords: ["계획", "plan", "roadmap", "분석", "설계", "PRD"]
tools: ["read", "glob", "grep_search"]
priority: high
---

# 🗺️ 개발 계획 수립 워크플로우 (Expanded)

**입력**: {{input}}

## 📋 1단계: 요구사항 명확화 (PRD Template)
- **목표**: 프로젝트의 최종 성공 모습 정의
- **핵심 기능**:
  - [ ] 기능 A: 세부 설명 및 사용자 가치
  - [ ] 기능 B: 세부 설명 및 사용자 가치
- **비기능 요구사항**:
  - 성능: 응답 속도 < 200ms, 동시 접속자 1000명 처리
  - 보안: JWT 기반 인증, 데이터 암호화
  - 확장성: 마이크로서비스 확장이 용이한 구조

## ⚠️ 2단계: 리스크 분석 & 대응
| 리스크 요인 | 영향도 | 대응 전략 |
| :--- | :---: | :--- |
| 외부 API 미비 | 고 | Mock 서버 구축 및 인터페이스 선정의 |
| 기술 스택 숙련도 | 중 | 초기 1~2일 R&D 기간 확보 및 프로토타이핑 |
| 일정 지연 | 고 | MVP 위주 우선순위 배정 (MoSCoW 기법) |

## 📊 3단계: 태스크 분해 & 마일스톤
```yaml
milestones:
  - Week 1: 아키텍처 설계 및 핵심 API 구현
  - Week 2: 프론트엔드 통합 및 테스트 완료
  - Week 3: 실환경 배포 및 모니터링 구축

tasks:
  - stage: 02-architect
    description: "시스템 아키텍처 & DB 스키마 설계"
  - stage: 03-coder  
    description: "TDD 기반 핵심 로직 및 API 구현"
  - stage: 04-tester
    description: "QA 및 리그레션 테스트 자동화"
  - stage: 05-reviewer
    description: "시니어 코드 리뷰 및 보안 취약점 점검"
  - stage: 06-deployer
    description: "CI/CD 파이프라인 및 가속화 배포"
```

**다음 스킬**: `architect` 스킬을 호출하여 구체적인 아키텍처를 설계하세요.