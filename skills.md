# Copilot Instructions (Skills) 관리 가이드

GitHub Copilot에 커스텀 지시사항(스킬)을 등록하는 방법을 VS Code와 Copilot CLI 두 환경 모두 정리합니다.

---

## 1. 인식되는 파일 위치 (공통)

| 파일/경로 | VS Code | Copilot CLI | 범위 |
|-----------|:-------:|:-----------:|------|
| `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` | ✅ | ✅ | 프로젝트 (git root & cwd) |
| `.github/copilot-instructions.md` | ✅ | ✅ | 프로젝트 |
| `.github/instructions/**/*.instructions.md` | ✅ | ✅ | 프로젝트 |
| `~/.copilot/copilot-instructions.md` | ❌ | ✅ | 전역 (CLI만) |
| `~/.github/instructions/*.md` | ✅ (설정 필요) | ❌ | 전역 (VS Code만) |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` 환경변수 경로 | ❌ | ✅ | 전역 (CLI만) |

---

## 2. VS Code — 전역 Instructions 설정

### 방법: User settings에 경로 등록

`~/.vscode/settings.json` (또는 VS Code UI → User Settings):

```json
{
  "github.copilot.chat.instructionFiles": [
    {
      "path": "~/.github/instructions/*.instructions.md",
      "scope": "user"
    }
  ]
}
```

### 전역 instructions 파일 위치
```
~/.github/instructions/
├── git-commit.instructions.md     # git commit 메시지 규칙
└── worklog.instructions.md        # 작업 정리 규칙
```

### 파일 헤더 형식 (`.instructions.md`)
```markdown
---
description: 언제 이 스킬을 참고할지 설명 (Copilot이 자동 판단에 활용)
---

# 스킬: 제목
...내용...
```

> `description` 필드는 Copilot이 관련 작업 시 자동으로 해당 파일을 참고할지 판단하는 데 사용됩니다.

---

## 3. Copilot CLI — 전역 Instructions 설정

### 방법 A: `~/.copilot/copilot-instructions.md` (단일 파일)

```bash
mkdir -p ~/.copilot
# 여러 파일을 하나로 합치거나 직접 작성
cat ~/.github/instructions/*.md > ~/.copilot/copilot-instructions.md
```

### 방법 B: 환경변수로 디렉토리 지정 (권장, 여러 파일 유지 가능)

`~/.bashrc` 또는 `~/.zshrc`에 추가:

```bash
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$HOME/.github/instructions"
```

적용:
```bash
source ~/.bashrc   # 또는 source ~/.zshrc
```

### 로드 확인

Copilot CLI 세션 내에서:
```
/instructions
```

---

## 4. 프로젝트별 Instructions 설정 (VS Code & CLI 공통)

프로젝트 루트 `.github/` 아래에 파일을 배치합니다.

```
.github/
├── copilot-instructions.md          # 프로젝트 전체 개요 및 공통 규칙
└── instructions/
    ├── web-ui.instructions.md       # Web UI 작업 시 참고
    ├── fetch-news.instructions.md   # 뉴스 fetch 작업 시 참고
    └── nginx.instructions.md        # nginx/배포 작업 시 참고
```

`.github/copilot-instructions.md` 예시:
```markdown
# GitHub Copilot Instructions

## 프로젝트 개요
- 프로젝트명, 목적, 주요 파일 등 기재

> 프로젝트 스킬은 `.github/instructions/` 폴더의 파일을 참고하세요.
> git commit은 직접 하지 않습니다. 사용자가 수동으로 처리합니다.
```

---

## 5. 현재 프로젝트(my-news) 구성 예시

```
~/.github/instructions/                          # 전역 (VS Code User settings 등록)
├── git-commit.instructions.md                   # 모든 프로젝트 공통 commit 규칙
└── worklog.instructions.md                      # "일을 정리 해주세요" 트리거 처리

my-news/.github/
├── copilot-instructions.md                      # 프로젝트 개요
└── instructions/
    ├── web-ui.instructions.md
    ├── fetch-news.instructions.md
    └── nginx.instructions.md
```

### CLI에서 전역 스킬도 함께 사용하려면

```bash
# ~/.bashrc 또는 ~/.zshrc
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$HOME/.github/instructions"
```

---

## 6. 요약 — 환경별 설정 체크리스트

### VS Code
- [ ] `~/.github/instructions/` 에 전역 `.instructions.md` 파일 작성
- [ ] VS Code User settings에 `github.copilot.chat.instructionFiles` 경로 등록
- [ ] 프로젝트별 `.github/instructions/*.instructions.md` 작성

### Copilot CLI
- [ ] `~/.bashrc`에 `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` 환경변수 추가
- [ ] 또는 `~/.copilot/copilot-instructions.md` 에 전역 지시사항 작성
- [ ] 프로젝트별 `.github/instructions/*.instructions.md` 작성 (CLI도 자동 인식)
- [ ] `/instructions` 명령으로 로드 여부 확인
