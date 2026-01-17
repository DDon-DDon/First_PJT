# Claude Code 문서

이 폴더는 Claude Code의 Skills와 Plugins 사용법에 대한 한국어 문서를 포함하고 있습니다.

## 📚 문서 목록

### 1. [SKILLS_AND_PLUGINS.md](./SKILLS_AND_PLUGINS.md)
Skills와 Plugins의 개념, 차이점, 사용 방법을 설명하는 종합 가이드입니다.

**포함 내용**:
- Skills란 무엇인가?
- Plugins란 무엇인가?
- Skills vs Plugins 비교
- 설치 및 사용 방법
- 현재 프로젝트의 구성 (28개 Skills)
- 공식 문서 링크

### 2. [SKILLS_EXAMPLES.md](./SKILLS_EXAMPLES.md)
실제로 사용 가능한 Skills 예제와 실습 가이드입니다.

**포함 내용**:
- 기본 Skill 예제 (코드 리뷰, Git 커밋 메시지)
- 고급 Skill 예제 (API 문서 생성, 테스트 코드 생성)
- 실전 활용 시나리오
- 트러블슈팅 가이드

---

## 🚀 빠른 시작

### Skills 사용해보기

1. **사용 가능한 Skills 확인**
```bash
ls .claude/skills/
```

2. **Claude에게 작업 요청**
```
"블로그 포스트 초안을 작성해줘"
→ content-research-writer Skill이 자동으로 적용됨

"이 코드를 리뷰해줘"
→ 프로젝트에 code-review Skill이 있다면 자동 적용됨
```

3. **직접 Skill 만들기**
```bash
mkdir -p .claude/skills/my-skill
```

`.claude/skills/my-skill/SKILL.md` 파일 생성:
```markdown
---
name: my-skill
description: 언제 이 Skill을 사용할지 구체적으로 설명
---

# 내 커스텀 Skill

Claude가 따라야 할 지침...
```

### 현재 사용 가능한 Skills 카테고리

이 프로젝트에는 **28개의 Skills**가 설치되어 있습니다:

- **비즈니스 & 마케팅** (5개): 브랜드 가이드라인, 경쟁사 분석, 도메인 네임, 내부 커뮤니케이션, 리드 리서치
- **커뮤니케이션 & 작성** (2개): 콘텐츠 작성, 미팅 분석
- **크리에이티브 & 미디어** (6개): 디자인, 이미지 향상, GIF 생성, 테마, 비디오 다운로드
- **개발** (7개): 아티팩트 빌더, 체인지로그, 개발자 분석, MCP 빌더, Skill 생성, 웹앱 테스팅
- **생산성 & 조직** (8개): 파일 정리, 인보이스 정리, 추첨, 문서 작업 (DOCX, PDF, PPTX, XLSX)

---

## 💡 주요 개념

### Skills는 자동으로 작동합니다
- 사용자가 명령어를 입력할 필요 없음
- Claude가 요청 내용을 보고 적절한 Skill을 자동 선택
- `description` 필드가 중요 (Claude가 이를 보고 판단)

### Plugins는 여러 기능을 묶습니다
- Slash Commands, Skills, Agents, Hooks를 하나로 패키징
- 버전 관리 가능
- 팀 공유 및 마켓플레이스 배포 가능

---

## 📖 사용 예시

### 예시 1: 개발 워크플로우

```bash
# 1. 기능 구현
"사용자 로그인 기능을 구현해줘"

# 2. 테스트 작성 (test-generator Skill 자동 적용)
"방금 만든 함수의 테스트를 작성해줘"

# 3. 코드 리뷰 (code-review Skill 자동 적용)
"작성한 코드를 리뷰해줘"

# 4. 커밋 (git-commit Skill 자동 적용)
"커밋 메시지를 작성해줘"
```

### 예시 2: 콘텐츠 작성

```bash
# content-research-writer Skill 자동 적용
"AI와 개발자의 미래에 대한 블로그 포스트를 작성해줘"

# brand-guidelines Skill 자동 적용
"Anthropic 브랜드 가이드라인을 적용해서 프레젠테이션을 만들어줘"
```

### 예시 3: 파일 정리

```bash
# file-organizer Skill 자동 적용
"Downloads 폴더의 파일들을 정리해줘"

# invoice-organizer Skill 자동 적용
"영수증 파일들을 세금 신고용으로 정리해줘"
```

---

## 🔧 고급 활용

### 1. Skill 제한하기

특정 작업에 안전한 제약을 두고 싶다면:

```yaml
---
name: safe-skill
description: 안전한 읽기 전용 Skill
allowed-tools: [Read, Grep, Glob]  # Write, Bash 제외
---
```

### 2. 여러 파일로 구성하기

복잡한 Skill은 여러 파일로 나눌 수 있습니다:

```
.claude/skills/complex-skill/
├── SKILL.md          # 메인 지침 (500줄 이하)
├── reference.md      # 상세 레퍼런스
├── examples.md       # 예제 모음
└── templates/        # 템플릿 파일들
```

SKILL.md에서 다른 파일 참조:
```markdown
상세한 내용은 reference.md를 참고하세요.
```

### 3. Plugin으로 패키징하기

여러 Skills를 묶어서 배포하고 싶다면:

```bash
my-plugin/
├── .claude-plugin/
│   └── plugin.json   # 메타데이터
├── skills/           # Skills 모음
│   ├── skill-1/
│   └── skill-2/
└── commands/         # Slash 명령어들
```

---

## 🐛 문제 해결

### Skill이 작동하지 않을 때

1. **Description 확인**
   ```yaml
   # ❌ 나쁜 예
   description: 코드 리뷰

   # ✅ 좋은 예
   description: 코드 리뷰를 요청하거나 PR을 검토할 때 사용. 보안, 성능, 코드 품질을 체크합니다.
   ```

2. **YAML 문법 확인**
   - YAML 구분자 (`---`) 확인
   - 들여쓰기 확인 (탭이 아닌 스페이스 사용)

3. **명시적으로 요청**
   ```
   "code-review skill을 사용해서 리뷰해줘"
   ```

4. **Claude Code 재시작**

---

## 📝 모범 사례

### ✅ 해야 할 것

1. **명확한 Description 작성**
   - 언제 사용하는지 구체적으로 설명
   - 트리거 키워드 포함 ("코드 리뷰", "테스트 생성" 등)

2. **간결하게 유지**
   - SKILL.md는 500줄 이하
   - 상세 내용은 별도 파일로 분리

3. **도구 권한 제한**
   - 필요한 도구만 `allowed-tools`에 포함
   - 보안이 중요한 작업은 읽기 전용으로 제한

4. **예제 포함**
   - 실제 사용 예제를 포함하여 명확성 향상

### ❌ 하지 말아야 할 것

1. **모호한 설명**
   ```yaml
   description: 유용한 기능  # ❌ 너무 모호함
   ```

2. **너무 긴 파일**
   ```markdown
   # 1000줄 이상의 SKILL.md  # ❌ 성능 저하
   ```

3. **과도한 권한**
   ```yaml
   allowed-tools: [*]  # ❌ 모든 도구 허용은 위험
   ```

---

## 🔗 추가 리소스

### 공식 문서
- [Skills 공식 문서](https://code.claude.com/docs/en/skills.md)
- [Plugins 공식 문서](https://code.claude.com/docs/en/plugins.md)
- [Claude Code 문서 전체 목록](https://code.claude.com/docs/en/claude_code_docs_map.md)

### 커뮤니티
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- [공식 디스코드](https://discord.gg/anthropic) (있다면)

### 도움말
```
Claude에게 "/help" 명령어 입력
```

---

## 📂 폴더 구조

```
First_PJT/
├── .claude/
│   ├── skills/                    # 프로젝트 Skills (28개)
│   │   ├── brand-guidelines/
│   │   ├── content-research-writer/
│   │   ├── developer-growth-analysis/
│   │   └── ... (25개 더)
│   └── .claude-plugin/
│       └── marketplace.json        # Plugin 마켓플레이스 설정
└── docs/                          # 문서 (이 폴더)
    ├── README.md                  # 이 파일
    ├── SKILLS_AND_PLUGINS.md      # 종합 가이드
    └── SKILLS_EXAMPLES.md         # 실습 예제
```

---

## 🎯 다음 단계

1. **[SKILLS_AND_PLUGINS.md](./SKILLS_AND_PLUGINS.md)** 읽기
   - Skills와 Plugins의 개념 이해
   - 현재 프로젝트의 구성 파악

2. **[SKILLS_EXAMPLES.md](./SKILLS_EXAMPLES.md)** 실습하기
   - 예제 중 하나를 선택해서 직접 만들기
   - 본인의 워크플로우에 맞게 커스터마이징

3. **기존 Skills 탐색하기**
   ```bash
   # Skill 내용 확인
   cat .claude/skills/content-research-writer/SKILL.md
   ```

4. **직접 Skill 만들기**
   - 본인의 반복 작업을 Skill로 자동화
   - 팀의 코딩 표준을 Skill로 정의

5. **팀과 공유하기**
   - 유용한 Skill을 팀원들과 공유
   - Plugin으로 패키징해서 배포

---

## ❓ 자주 묻는 질문

### Q: Skill과 Slash Command의 차이는?

**A**:
- **Skill**: Claude가 자동으로 선택하여 적용 (모델 호출)
- **Slash Command**: 사용자가 `/command-name` 형식으로 직접 호출

### Q: Skill이 너무 많으면 성능에 영향을 주나요?

**A**: 각 Skill을 500줄 이하로 유지하고, 상세 내용은 별도 파일로 분리하면 성능 영향이 적습니다.

### Q: 여러 프로젝트에서 같은 Skill을 사용하려면?

**A**:
- **개인용**: `~/.claude/skills/`에 저장 (모든 프로젝트에서 사용)
- **프로젝트용**: `.claude/skills/`에 저장 (해당 프로젝트에만 사용)
- **팀 공유**: Plugin으로 패키징하여 배포

### Q: Skill이 자동으로 적용되지 않을 때는?

**A**:
1. Description을 더 구체적으로 작성
2. 명시적으로 요청: "skill-name을 사용해서..."
3. Claude Code 재시작

---

**문서 작성일**: 2025-12-27
**버전**: 1.0.0
**문의**: Claude Code에게 직접 질문하거나 `/help` 명령어 사용
