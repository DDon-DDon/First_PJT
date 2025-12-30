# 🔧 GitHub 템플릿 설정 가이드

## 파일 구조

GitHub 레포지토리에 다음과 같이 파일을 배치하세요:

```
your-repo/
└── .github/
    ├── pull_request_template.md      # PR 템플릿
    └── ISSUE_TEMPLATE/
        ├── bug_report.md             # 버그 리포트 템플릿
        └── feature_request.md        # 기능 요청 템플릿
```

## 설치 방법

### 1. 레포지토리에서 .github 폴더 생성

```bash
cd your-repo
mkdir -p .github/ISSUE_TEMPLATE
```

### 2. 파일 복사

```bash
# PR 템플릿
cp pull_request_template.md .github/

# 이슈 템플릿
cp ISSUE_TEMPLATE/bug_report.md .github/ISSUE_TEMPLATE/
cp ISSUE_TEMPLATE/feature_request.md .github/ISSUE_TEMPLATE/
```

### 3. 커밋 및 푸시

```bash
git add .github/
git commit -m "chore: GitHub 템플릿 추가"
git push origin main
```

## 사용 방법

### PR 템플릿
- 새 PR 생성 시 자동으로 템플릿이 적용됩니다
- `Closes DDONE-XX` 부분에 Linear 이슈 번호를 입력하세요

### 이슈 템플릿
- 새 이슈 생성 시 템플릿 선택 화면이 나타납니다
- Bug Report 또는 Feature Request 중 선택하세요

## Linear 연동 키워드

PR 본문에 다음 키워드를 사용하면 Linear 이슈가 자동 처리됩니다:

| 키워드 | 동작 |
|--------|------|
| `Closes DDONE-XX` | PR Merge 시 이슈를 Done으로 변경 |
| `Fixes DDONE-XX` | PR Merge 시 이슈를 Done으로 변경 |
| `Resolves DDONE-XX` | PR Merge 시 이슈를 Done으로 변경 |
| `Ref DDONE-XX` | 이슈와 연결만 (상태 변경 안 함) |

## 커스터마이징

팀 상황에 맞게 템플릿을 수정하세요:

- 변경 유형 항목 추가/삭제
- 필수 체크리스트 항목 추가
- 팀 컨벤션에 맞는 섹션 추가
