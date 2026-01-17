# Claude Code Skills와 Plugins 가이드

## 목차
1. [Skills란 무엇인가?](#skills란-무엇인가)
2. [Plugins란 무엇인가?](#plugins란-무엇인가)
3. [Skills vs Plugins 차이점](#skills-vs-plugins-차이점)
4. [Skills 사용 방법](#skills-사용-방법)
5. [Plugins 사용 방법](#plugins-사용-방법)
6. [현재 프로젝트의 구성](#현재-프로젝트의-구성)

---

## Skills란 무엇인가?

**Skills**는 Claude의 기능을 확장하는 마크다운 파일입니다. 특정 작업을 수행하는 방법, 팀 표준, 워크플로우 등을 Claude에게 가르칠 수 있습니다.

### 주요 특징

- **자동 호출**: Claude가 사용자의 요청에 맞는 Skill을 자동으로 선택하여 적용
- **마크다운 기반**: `SKILL.md` 파일에 YAML 메타데이터와 마크다운 지침 작성
- **유연한 배치**: 개인용, 프로젝트용, 기업용, 플러그인 번들 등 다양한 위치에 배치 가능

### Skill 파일 구조

```yaml
---
name: skill-name
description: Claude가 이 설명을 보고 언제 Skill을 사용할지 결정합니다
allowed-tools: [Read, Write, Bash]  # 선택사항: 사용 가능한 도구 제한
---

# Skill 지침

여기에 Claude가 따라야 할 구체적인 지침을 작성합니다...
```

### Skill이 저장되는 위치

1. **개인용 Skills**: `~/.claude/skills/` - 모든 프로젝트에서 사용 가능
2. **프로젝트 Skills**: `.claude/skills/` - 팀과 공유 가능
3. **기업용 Skills**: 조직 전체에 배포
4. **플러그인 Skills**: 플러그인에 포함되어 배포

### 모범 사례

- `SKILL.md` 파일은 500줄 이하로 유지
- 핵심 정보만 메인 파일에 작성하고 상세 참조 자료는 별도 파일로 분리
- 설명(description)에 구체적인 행동 키워드와 트리거 용어 포함
- 보안이 중요한 작업에는 `allowed-tools`로 도구 접근 제한

---

## Plugins란 무엇인가?

**Plugins**는 Slash Commands, Agents, Skills, Hooks, MCP 서버 등을 하나의 패키지로 묶어서 배포할 수 있는 확장 시스템입니다.

### 주요 특징

- **패키지화**: 여러 기능을 하나의 플러그인으로 묶어서 관리
- **버전 관리**: 플러그인 버전을 추적하고 업데이트 가능
- **팀 공유**: 팀원들과 쉽게 공유하고 커뮤니티에 배포 가능
- **마켓플레이스**: 플러그인 마켓플레이스를 통해 검색 및 설치

### Plugin 디렉토리 구조

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # 플러그인 메타데이터 (필수)
├── commands/                # Slash 명령어들
│   └── my-command.md
├── agents/                  # AI 에이전트들
│   └── my-agent.md
├── skills/                  # Skills
│   └── my-skill/
│       └── SKILL.md
└── hooks/                   # 이벤트 훅들
    └── my-hook.sh
```

### plugin.json 예시

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "나만의 Claude Code 플러그인",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  }
}
```

### 중요한 구조 규칙

⚠️ **주의**: `commands/`, `agents/`, `skills/`, `hooks/` 디렉토리는 `.claude-plugin/` 내부가 아닌 플러그인 루트 레벨에 위치해야 합니다. `.claude-plugin/` 내부에는 `plugin.json`만 들어갑니다.

---

## Skills vs Plugins 차이점

| 특징 | Skills | Plugins |
|------|--------|---------|
| **용도** | 특정 작업에 대한 지침 제공 | 여러 기능을 패키지로 묶어서 배포 |
| **호출 방식** | Claude가 자동으로 선택 | Slash 명령어로 직접 호출 가능 |
| **구성 요소** | 단일 SKILL.md 파일 | Commands, Skills, Agents, Hooks 등 포함 |
| **버전 관리** | 없음 | 있음 (semantic versioning) |
| **배포** | 파일 복사 | 마켓플레이스를 통한 설치 |
| **적합한 경우** | 개인 워크플로우, 단일 프로젝트 | 팀 공유, 커뮤니티 배포 |

### 언제 무엇을 사용해야 할까?

**Skills를 사용하는 경우**:
- 특정 작업 방식을 Claude에게 가르치고 싶을 때
- 자동으로 적용되길 원하는 워크플로우가 있을 때
- 간단한 개인 설정이 필요할 때

**Plugins를 사용하는 경우**:
- 여러 기능을 하나로 묶어서 배포하고 싶을 때
- 팀원들과 공유하고 버전 관리가 필요할 때
- 커뮤니티에 배포하고 싶을 때
- Slash 명령어, Hooks 등 다양한 기능이 필요할 때

---

## Skills 사용 방법

### 1. Skill 탐색하기

현재 사용 가능한 Skills 목록을 확인하려면:

```bash
# 프로젝트의 Skills 확인
ls .claude/skills/

# 개인 Skills 확인 (Windows)
ls ~/.claude/skills/
```

### 2. Skill 자동 적용

Skills는 **자동으로 적용**됩니다. 사용자가 특정 작업을 요청하면 Claude가 적절한 Skill을 선택하여 사용합니다.

예를 들어, 프로젝트에 `content-research-writer` Skill이 있다면:
- "블로그 포스트 작성해줘" → Claude가 자동으로 이 Skill을 적용
- 별도의 명령어 입력 불필요

### 3. 사용 가능한 Skills 확인

Claude에게 직접 물어볼 수 있습니다:
```
"현재 사용 가능한 Skills가 뭐야?"
"어떤 Skills가 활성화되어 있어?"
```

### 4. 새로운 Skill 만들기

`.claude/skills/` 디렉토리에 새 폴더를 만들고 `SKILL.md` 파일을 작성하면 됩니다:

```bash
mkdir .claude/skills/my-custom-skill
```

`SKILL.md` 내용:
```markdown
---
name: my-custom-skill
description: 특정 상황에서 이 Skill을 사용하도록 구체적으로 설명
---

# 내 커스텀 Skill

Claude가 따라야 할 지침을 여기에 작성...
```

---

## Plugins 사용 방법

### 1. 설치된 Plugin 확인

현재 프로젝트의 `.claude/.claude-plugin/marketplace.json` 파일에서 설치된 플러그인 목록을 확인할 수 있습니다.

### 2. Plugin에서 제공하는 기능 사용

현재 프로젝트에 설치된 플러그인들:

#### 비즈니스 & 마케팅
- `brand-guidelines` - Anthropic 브랜드 가이드라인 적용
- `competitive-ads-extractor` - 경쟁사 광고 분석
- `domain-name-brainstormer` - 도메인 네임 아이디어 생성
- `internal-comms` - 내부 커뮤니케이션 작성
- `lead-research-assistant` - 리드 리서치 및 분석

#### 커뮤니케이션 & 작성
- `content-research-writer` - 콘텐츠 리서치 및 작성 지원
- `meeting-insights-analyzer` - 미팅 인사이트 분석

#### 크리에이티브 & 미디어
- `canvas-design` - 비주얼 아트 생성
- `image-enhancer` - 이미지 품질 향상
- `slack-gif-creator` - Slack용 GIF 생성
- `theme-factory` - 아티팩트 테마 적용
- `video-downloader` - 비디오 다운로드

#### 개발
- `artifacts-builder` - Claude.ai HTML 아티팩트 빌드
- `changelog-generator` - Git 커밋에서 체인지로그 생성
- `developer-growth-analysis` - 개발자 성장 분석
- `mcp-builder` - MCP 서버 생성 가이드
- `skill-creator` - 새로운 Skill 생성 가이드
- `webapp-testing` - Playwright를 사용한 웹앱 테스팅
- `template-skill` - Skill 템플릿

#### 생산성 & 조직
- `file-organizer` - 파일 정리 자동화
- `invoice-organizer` - 인보이스 정리 자동화
- `raffle-winner-picker` - 추첨 당첨자 선택
- `document-skills-*` - 문서 작업 (DOCX, PDF, PPTX, XLSX)

### 3. Plugin의 Skill 사용하기

Plugin에 포함된 Skills는 자동으로 사용 가능합니다. 예를 들어:

```
"브랜드 가이드라인을 적용해서 프레젠테이션을 만들어줘"
→ brand-guidelines Skill이 자동으로 적용됨

"경쟁사 광고를 분석해줘"
→ competitive-ads-extractor Skill이 자동으로 적용됨
```

### 4. 새로운 Plugin 만들기

1. 플러그인 디렉토리 구조 생성:
```bash
mkdir my-plugin
mkdir my-plugin/.claude-plugin
mkdir my-plugin/skills
```

2. `plugin.json` 작성:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "나의 커스텀 플러그인",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  }
}
```

3. Skills, Commands 등 추가

4. `.claude/skills/` 디렉토리에 복사 또는 심볼릭 링크 생성

---

## 현재 프로젝트의 구성

### Marketplace 설정

이 프로젝트는 `awesome-claude-skills` 마켓플레이스를 사용하고 있습니다:
- **이름**: awesome-claude-skills
- **버전**: 1.0.0
- **소유자**: ComposioHQ
- **설명**: Claude.ai, Claude Code, Claude API에서 생산성을 향상시키는 실용적인 Skills 모음

### 카테고리별 Skills

현재 프로젝트에는 다음 카테고리로 구성된 Skills가 있습니다:

1. **business-marketing** (5개)
2. **communication-writing** (2개)
3. **creative-media** (6개)
4. **development** (7개)
5. **productivity-organization** (8개)

총 **28개의 Skills**가 사용 가능합니다.

### Skill 활성화 확인

모든 Skills는 기본적으로 활성화되어 있으며, Claude가 요청에 따라 자동으로 적절한 Skill을 선택합니다.

---

## 추가 리소스

### 공식 문서
- [Skills 공식 문서](https://code.claude.com/docs/en/skills.md)
- [Plugins 공식 문서](https://code.claude.com/docs/en/plugins.md)
- [Plugins 레퍼런스](https://code.claude.com/docs/en/plugins-reference.md)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md)

### 도움말
- `/help` 명령어로 Claude Code 도움말 확인
- 피드백 및 이슈: https://github.com/anthropics/claude-code/issues

### 팁
1. Skill 설명(description)을 명확하고 구체적으로 작성하세요
2. 500줄 이하로 간결하게 유지하세요
3. 민감한 작업에는 `allowed-tools`로 권한을 제한하세요
4. 플러그인은 버전 관리가 필요한 경우에 사용하세요
5. 개인 워크플로우는 Skills로, 팀 공유는 Plugins로 관리하세요
