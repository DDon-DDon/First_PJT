# Skills 실습 예제 가이드

이 문서는 Claude Code Skills를 직접 만들고 사용하는 실습 예제를 제공합니다.

## 목차
1. [기본 Skill 만들기](#기본-skill-만들기)
2. [고급 Skill 예제](#고급-skill-예제)
3. [실전 활용 예제](#실전-활용-예제)
4. [트러블슈팅](#트러블슈팅)

---

## 기본 Skill 만들기

### 예제 1: 코드 리뷰 Skill

팀의 코드 리뷰 기준을 Claude에게 가르치는 Skill을 만들어봅시다.

**파일 위치**: `.claude/skills/code-review/SKILL.md`

```markdown
---
name: code-review
description: 코드 리뷰를 요청하거나 PR 리뷰가 필요할 때 사용. 팀의 코딩 표준과 베스트 프랙티스를 적용합니다.
allowed-tools: [Read, Grep, Glob]
---

# 코드 리뷰 가이드

## 리뷰 체크리스트

### 1. 코드 품질
- [ ] 변수명이 명확하고 의미가 있는가?
- [ ] 함수는 단일 책임 원칙을 따르는가?
- [ ] 중복 코드가 없는가?
- [ ] 매직 넘버 대신 상수를 사용했는가?

### 2. 보안
- [ ] SQL Injection 취약점이 없는가?
- [ ] XSS 공격에 안전한가?
- [ ] 민감한 정보가 하드코딩되지 않았는가?
- [ ] 입력값 검증이 충분한가?

### 3. 성능
- [ ] 불필요한 반복문이 없는가?
- [ ] 메모리 누수 가능성은 없는가?
- [ ] 적절한 자료구조를 사용했는가?

### 4. 테스트
- [ ] 단위 테스트가 작성되었는가?
- [ ] 엣지 케이스를 고려했는가?
- [ ] 테스트 커버리지가 충분한가?

## 리뷰 프로세스

1. 변경된 파일들을 모두 읽어 전체 맥락 파악
2. 위 체크리스트에 따라 코드 검토
3. 문제점과 개선 제안을 구체적으로 작성
4. 긍정적인 부분도 언급하여 균형 잡힌 피드백 제공

## 피드백 형식

### 🔴 Critical (즉시 수정 필요)
보안 취약점, 심각한 버그 등

### 🟡 Important (수정 권장)
성능 이슈, 코드 품질 개선 등

### 🟢 Suggestion (선택적 개선)
더 나은 접근 방법, 리팩토링 제안 등

### 👍 Good Practice
잘 작성된 부분 칭찬
```

**사용 예제**:
```
사용자: "방금 작성한 login.js 파일 코드 리뷰 해줘"
Claude: [code-review Skill을 자동으로 적용하여 체크리스트에 따라 리뷰 진행]
```

---

### 예제 2: Git 커밋 메시지 Skill

일관된 커밋 메시지 작성을 돕는 Skill입니다.

**파일 위치**: `.claude/skills/git-commit/SKILL.md`

```markdown
---
name: git-commit
description: Git 커밋 메시지를 작성할 때 사용. Conventional Commits 형식을 따릅니다.
allowed-tools: [Bash, Read]
---

# Git 커밋 메시지 가이드

## Conventional Commits 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type 종류

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 변경
- **style**: 코드 포맷팅, 세미콜론 누락 등 (기능 변경 없음)
- **refactor**: 코드 리팩토링 (기능 변경 없음)
- **test**: 테스트 코드 추가/수정
- **chore**: 빌드 프로세스, 패키지 매니저 설정 등

## 작성 규칙

1. **Subject**
   - 50자 이내로 작성
   - 명령문 사용 (예: "Add feature" not "Added feature")
   - 마침표 제외
   - 영어는 첫 글자 대문자

2. **Body** (선택사항)
   - 72자마다 줄바꿈
   - 무엇을, 왜 변경했는지 설명
   - 어떻게 변경했는지는 코드를 보면 알 수 있으므로 생략

3. **Footer** (선택사항)
   - Breaking Changes: `BREAKING CHANGE: 설명`
   - 이슈 참조: `Closes #123`

## 예제

```
feat(auth): add Google OAuth login

사용자가 Google 계정으로 로그인할 수 있는 기능 추가.
기존 이메일/비밀번호 로그인과 병행 가능.

Closes #456
```

## 커밋 메시지 작성 프로세스

1. `git diff`로 변경 사항 확인
2. 변경의 성격에 맞는 type 선택
3. 핵심 변경 사항을 한 줄로 요약
4. 필요시 body에 상세 설명 추가
5. 관련 이슈가 있다면 footer에 참조 추가
```

**사용 예제**:
```
사용자: "커밋 메시지 작성해줘"
Claude: [git-commit Skill을 적용하여 git diff 확인 후 Conventional Commits 형식으로 메시지 생성]
```

---

## 고급 Skill 예제

### 예제 3: API 문서 자동 생성 Skill

코드에서 API 엔드포인트를 분석하여 문서를 생성하는 Skill입니다.

**파일 위치**: `.claude/skills/api-docs/SKILL.md`

```markdown
---
name: api-docs
description: API 엔드포인트를 분석하고 문서를 생성할 때 사용. OpenAPI 스펙 기반으로 작성합니다.
allowed-tools: [Read, Grep, Glob, Write]
---

# API 문서 생성 가이드

## 문서 포맷

각 API 엔드포인트는 다음 정보를 포함해야 합니다:

### 1. 기본 정보
- HTTP Method (GET, POST, PUT, DELETE, PATCH)
- Endpoint URL
- 간단한 설명

### 2. Request
- Path Parameters
- Query Parameters
- Request Headers
- Request Body (with JSON schema)

### 3. Response
- Success Response (2xx)
  - Status Code
  - Response Body
  - Example
- Error Responses (4xx, 5xx)
  - Status Code
  - Error Message Format
  - Example

### 4. 인증
- 필요한 인증 방식 (Bearer Token, API Key, etc.)
- 권한 레벨

### 5. 예제
- cURL 예제
- JavaScript/Python 코드 예제

## 문서 템플릿

```markdown
## [HTTP Method] [Endpoint]

[간단한 설명]

### Authentication
- Type: Bearer Token
- Required: Yes

### Request

**Path Parameters**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | User ID |

**Query Parameters**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| limit | number | No | 10 | Number of items |

**Request Body**
\`\`\`json
{
  "name": "string",
  "email": "string"
}
\`\`\`

### Response

**Success (200 OK)**
\`\`\`json
{
  "id": "user_123",
  "name": "John Doe",
  "email": "john@example.com"
}
\`\`\`

**Error (400 Bad Request)**
\`\`\`json
{
  "error": "Invalid email format",
  "code": "INVALID_EMAIL"
}
\`\`\`

### Examples

**cURL**
\`\`\`bash
curl -X GET https://api.example.com/users/123 \\
  -H "Authorization: Bearer YOUR_TOKEN"
\`\`\`

**JavaScript**
\`\`\`javascript
const response = await fetch('https://api.example.com/users/123', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});
const data = await response.json();
\`\`\`
```

## 문서 생성 프로세스

1. 프로젝트에서 라우트 파일들 찾기 (예: `routes/*.js`, `api/*.py`)
2. 각 엔드포인트의 코드 분석
3. JSDoc, Python docstring 등 주석 정보 추출
4. 위 템플릿에 맞춰 문서 작성
5. `docs/api/` 디렉토리에 저장
```

---

### 예제 4: 테스트 코드 생성 Skill

**파일 위치**: `.claude/skills/test-generator/SKILL.md`

```markdown
---
name: test-generator
description: 함수나 컴포넌트의 단위 테스트 코드를 생성할 때 사용. Jest, Pytest 등 프로젝트에 맞는 테스트 프레임워크 사용.
allowed-tools: [Read, Grep, Glob, Write]
---

# 테스트 코드 생성 가이드

## 테스트 작성 원칙

### AAA 패턴
1. **Arrange**: 테스트 환경 설정
2. **Act**: 테스트할 동작 실행
3. **Assert**: 결과 검증

### 커버리지 목표
- 정상 케이스 (Happy Path)
- 엣지 케이스 (Edge Cases)
- 에러 케이스 (Error Cases)
- 경계값 테스트 (Boundary Tests)

## JavaScript/TypeScript (Jest)

### 함수 테스트 템플릿

\`\`\`javascript
describe('functionName', () => {
  // 정상 케이스
  it('should return expected result for valid input', () => {
    // Arrange
    const input = validInput;

    // Act
    const result = functionName(input);

    // Assert
    expect(result).toBe(expectedOutput);
  });

  // 엣지 케이스
  it('should handle edge case correctly', () => {
    const input = edgeInput;
    const result = functionName(input);
    expect(result).toBe(expectedEdgeOutput);
  });

  // 에러 케이스
  it('should throw error for invalid input', () => {
    const invalidInput = null;
    expect(() => functionName(invalidInput)).toThrow(ErrorType);
  });
});
\`\`\`

### React 컴포넌트 테스트 템플릿

\`\`\`javascript
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('should handle user interaction', () => {
    render(<ComponentName />);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(screen.getByText('Result Text')).toBeInTheDocument();
  });

  it('should handle props correctly', () => {
    const props = { value: 'test' };
    render(<ComponentName {...props} />);
    expect(screen.getByText('test')).toBeInTheDocument();
  });
});
\`\`\`

## Python (Pytest)

### 함수 테스트 템플릿

\`\`\`python
import pytest
from module import function_name

class TestFunctionName:
    def test_valid_input(self):
        """정상 케이스 테스트"""
        # Arrange
        input_data = valid_input
        expected = expected_output

        # Act
        result = function_name(input_data)

        # Assert
        assert result == expected

    def test_edge_case(self):
        """엣지 케이스 테스트"""
        input_data = edge_input
        result = function_name(input_data)
        assert result == expected_edge_output

    def test_invalid_input_raises_error(self):
        """에러 케이스 테스트"""
        invalid_input = None
        with pytest.raises(ValueError):
            function_name(invalid_input)

    @pytest.mark.parametrize("input_value,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_multiple_cases(self, input_value, expected):
        """파라미터화된 테스트"""
        result = function_name(input_value)
        assert result == expected
\`\`\`

## 테스트 생성 프로세스

1. 테스트할 함수/컴포넌트의 코드 읽기
2. 입력과 출력 타입 파악
3. 가능한 엣지 케이스와 에러 케이스 식별
4. AAA 패턴에 따라 테스트 작성
5. 모든 경로(코드 브랜치)가 커버되도록 테스트 추가
6. 테스트 파일명: `[원본파일명].test.js` 또는 `test_[원본파일명].py`

## 좋은 테스트의 특징

- **독립적**: 다른 테스트에 의존하지 않음
- **반복 가능**: 실행할 때마다 같은 결과
- **자명적**: 테스트 이름만 봐도 무엇을 테스트하는지 알 수 있음
- **빠름**: 빠르게 실행되어야 함
- **완전함**: 모든 경로와 경계값을 테스트
```

---

## 실전 활용 예제

### 시나리오 1: 새로운 기능 개발 워크플로우

1. **기능 구현**
```
사용자: "사용자 인증 기능을 구현해줘"
Claude: [코드 작성]
```

2. **테스트 생성**
```
사용자: "방금 만든 인증 함수의 테스트 코드를 만들어줘"
Claude: [test-generator Skill 자동 적용 → 테스트 코드 생성]
```

3. **코드 리뷰**
```
사용자: "작성한 코드 리뷰해줘"
Claude: [code-review Skill 자동 적용 → 체크리스트 기반 리뷰]
```

4. **커밋**
```
사용자: "커밋 메시지 작성해줘"
Claude: [git-commit Skill 자동 적용 → Conventional Commits 형식으로 메시지 생성]
```

---

### 시나리오 2: API 개발 및 문서화

1. **API 엔드포인트 구현**
```
사용자: "사용자 목록을 조회하는 GET /api/users 엔드포인트 만들어줘"
Claude: [코드 작성]
```

2. **API 문서 생성**
```
사용자: "방금 만든 API의 문서를 만들어줘"
Claude: [api-docs Skill 자동 적용 → OpenAPI 스펙 기반 문서 생성]
```

3. **통합 테스트 작성**
```
사용자: "이 API의 통합 테스트를 작성해줘"
Claude: [test-generator Skill 적용 → API 테스트 코드 생성]
```

---

## 트러블슈팅

### Skill이 자동으로 적용되지 않을 때

**문제**: Skill을 만들었는데 자동으로 적용되지 않습니다.

**해결 방법**:
1. `description` 필드가 충분히 구체적인지 확인
2. 트리거 키워드를 명확하게 포함했는지 확인
3. Claude에게 명시적으로 요청해보기: "code-review skill을 사용해서 리뷰해줘"

**좋은 description 예시**:
```yaml
# ❌ 나쁜 예
description: 코드를 리뷰합니다

# ✅ 좋은 예
description: 코드 리뷰를 요청하거나 PR 검토가 필요할 때 사용. 보안, 성능, 코드 품질을 체크리스트에 따라 검토합니다.
```

---

### Skill이 너무 많은 도구에 접근할 때

**문제**: Skill이 필요 이상의 파일을 읽거나 수정합니다.

**해결 방법**: `allowed-tools` 필드로 권한 제한

```yaml
---
name: readonly-skill
description: 읽기 전용 스킬
allowed-tools: [Read, Grep, Glob]  # Write, Bash 제외
---
```

---

### 여러 Skill이 동시에 적용될 때

**문제**: 두 개 이상의 Skill이 동시에 적용되어 혼란스럽습니다.

**해결 방법**:
1. 각 Skill의 `description`을 더 명확하게 구분
2. 특정 Skill을 명시적으로 지정: "git-commit skill만 사용해서 커밋 메시지 작성해줘"

---

### Skill이 업데이트되지 않을 때

**문제**: Skill 파일을 수정했는데 변경사항이 반영되지 않습니다.

**해결 방법**:
1. Claude Code를 재시작
2. 캐시 초기화 (설정에서 가능)
3. Skill 파일의 YAML 문법이 올바른지 확인

---

## 다음 단계

1. **실습**: 위 예제 중 하나를 선택해서 직접 만들어보세요
2. **커스터마이징**: 본인의 워크플로우에 맞게 수정하세요
3. **팀 공유**: 유용한 Skill을 팀원들과 공유하세요
4. **Plugin 만들기**: 여러 Skill을 묶어서 Plugin으로 패키징하세요

더 많은 예제와 템플릿은 `.claude/skills/` 디렉토리의 기존 Skills를 참고하세요!
