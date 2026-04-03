---
description: "일을 정리 해주세요" 트리거 — README, worklog, lessons 자동 정리
---

# 스킬: 작업 정리

사용자가 **"일을 정리 해주세요"** 또는 **"일을 정리 해줘"** 라고 입력하면
아래 순서대로 수행한다.

---

## 사전 단계 A — 월별 아카이브 체크 (매월 초 자동 처리)

현재 날짜의 **월(YYYY-MM)** 과 `worklog.md` 첫 줄의 월이 다르면 (= 새 달):

1. `worklog.md` → `worklog/YYYY-MM.md` 로 이동 (YYYY-MM = 지난달)
2. `data/worklog.json` → `data/worklog/YYYY-MM.json` 으로 이동
3. `worklog.md` 새로 생성 (빈 파일 + 헤더)
4. `data/worklog.json` 새로 생성 (`[]`)
5. `worklog/` 및 `data/worklog/` 디렉토리가 없으면 생성

이 체크는 "일을 정리 해주세요" 를 트리거로 자동 수행한다.

---

## 사전 단계 B — 작업 시간 및 툴 정보 확인

1. **작업 시작 시간**: 
  - 시작 시간을 copilot의 입력된 시간으로 산출
  - 일이 여러가지로 변하면 입력한 기준으로 변화 시작 시간으로 산정

2. **툴 및 세션 ID** 자동 감지:
   - Copilot CLI → `tool: "copilot-cli"`, session_id: 현재 세션 ID
   - Claude Code → `tool: "claude-code"`, session_id: 대화 ID
   - VS Code Copilot → `tool: "vscode-copilot"`, session_id: 대화 ID
   - 확인 불가 → `tool: "unknown"`, session_id: null

---

## 작업 1 — README.md 업데이트
- 프로젝트의 현재 상태를 반영하여 `README.md`를 업데이트한다.

## 작업 2 — worklog.md에 작업 내역 추가 (이번 달 파일)
- `worklog.md` 파일 **맨 위에** 추가한다.
- 형식:
  ```
  ## YYYY-MM-DD HH:MM ~ HH:MM (Xh Ym) [tool: copilot-cli / session: xxxx-xxxx]
  - 작업 내용 1
  - 작업 내용 2
  ```

## 작업 3 — data/worklog.json에 구조화 데이터 추가 (이번 달 파일)
- `data/worklog.json` 배열에 항목을 **append** 한다.
- 형식:
  ```json
  {
    "date": "YYYY-MM-DD",
    "start": "HH:MM",
    "end": "HH:MM",
    "duration": "Xh Ym",
    "tool": "copilot-cli",
    "session_id": "세션-ID",
    "tasks": [
      { "title": "작업 제목", "detail": "상세 내용" , "start": "HH:MM" , "end": "HH:MM" , "duration": "Xh Ym"}
    ],
    "project": "프로젝트명"
  }
  ```

## 작업 4 — lessons.md에 중요 교훈 기록
- 형식:
  ```
  ## YYYY-MM-DD — [주제]
  - 교훈 내용
  ```

## 작업 5 — mm.md에 commit msg 기록
- 형식:
  ```
  짧은 summary 1줄

  상세한 내용
  ```

---

## 전체 합산 방법 (필요 시 안내)

사용자가 "전체 워크로그 합쳐줘" 또는 "워크로그 통합해줘" 라고 하면:

```bash
# 전체 JSON 통합 (날짜순 정렬)
cat data/worklog/*.json data/worklog.json 2>/dev/null \
  | jq -s 'add | sort_by(.date)' > data/worklog_all.json

# 전체 MD 열람
cat worklog/*.md worklog.md 2>/dev/null | less
```

---

## 파일 구조 (참고)
```
worklog.md                  ← 이번 달만
worklog/
  2026-03.md                ← 지난달 아카이브
  2026-02.md
data/worklog.json           ← 이번 달만
data/worklog/
  2026-03.json
  2026-02.json
data/worklog_all.json       ← 통합 시에만 생성 (임시)
```

## 공통 규칙
- git add / commit / push 는 하지 않는다. 사용자가 직접 처리한다.
