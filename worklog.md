# 작업 로그 (Work Log)

---

## 2026-04-03 ~12:07 [tool: copilot-cli / session: de842a4e]

### fetch_news.py — Reply/Forward 인용 제거
- HTML: `gmail_attr`, `gmail_quote` div, `blockquote` 마커 방식으로 안전하게 제거
- Plain text: 한국어 Gmail reply 헤더(`2026년 N월 N일 ... 님이 작성:`) 감지 추가
- Plain text: 이메일 주소 포함 헤더(`<email@domain>:`) 감지 추가
- 기존 `news.json` 53개 항목 즉시 재처리 (최대 140,714→2,017 chars 감소)

### web/index.html — 모달 닫기 키 추가
- ESC / x / X 에 **Space / Enter** 추가
- `e.preventDefault()` 적용으로 모달 내 스크롤/버튼 오작동 방지


- Copilot CLI 스킬은 **현재 프로젝트의 `.github/instructions/`** 파일만 인식
- 스킬 파일은 **Copilot CLI 재시작 시에만** 로드됨 (세션 도중 추가 불가)
- skills.md 표 및 주의사항 업데이트

---

## 2026-04-03 10:00 ~ 11:07 (1h 7m) [tool: copilot-cli / session: de842a4e]

### worklog 스킬 고도화
- worklog.instructions.md: 시간 기록 (start/end/duration) 추가
- worklog.instructions.md: tool 및 session_id 기록 추가 (copilot-cli, claude-code, vscode-copilot 구분)
- worklog.instructions.md: 월별 아카이브 전략 추가 (매월 초 자동 분리)
- data/worklog.json 초기 파일 생성 (`[]`)
- worklog/, data/worklog/ 아카이브 디렉토리 생성

### skills.md 보완
- 6번 섹션 추가: 음성 입력으로 Copilot CLI 사용하기
- Windows + H (음성 인식) 실사용 확인 내용 기록

### web UI 개선
- 카드 표시 순서: date 기준 내림차순 정렬 (최신 → 오래된 순)
- 헤더 stats에 🕐 UPDATED 표시 추가 (news.json Last-Modified 기준)

---

## 2026-04-02 (2차)

### Copilot CLI instructions 학습 및 skills.md 작성
- Copilot CLI는 `~/.github/instructions/`를 자동 인식하지 않음 확인
- CLI 전역 instructions 적용 방법 2가지 정리:
  - `~/.copilot/copilot-instructions.md` 단일 파일
  - `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` 환경변수로 디렉토리 지정 (권장)
- VS Code는 User settings `github.copilot.chat.instructionFiles`로 `~/.github/instructions/` 전역 등록 가능
- `skills.md` 신규 작성: VS Code / Copilot CLI 환경별 instructions 설정 가이드

---

## 2026-04-02

### 웹 UI 개선
- 카드 고정 높이 400px 적용, flex 레이아웃으로 내부 영역 정렬
- 전체 폰트 크기 최소 12px로 상향 (기존 0.28rem~0.4rem → 12~14px)
- 카드 LINKS 최대 3개 표시, 초과 시 "+N개 더..." 힌트 표시
- SUMMARY 섹션 카드에 표시 추가

### 모달 (전체 내용 팝업)
- 카드 본문 클릭 시 전체 내용을 8-bit 아케이드 스타일 모달로 표시
- 모달 닫기: ESC 키 / X 키 / 우상단 ✕ 버튼 / 모달 외부(overlay) 클릭
- modal-box에 `stopPropagation()` 적용하여 내부 클릭이 overlay로 버블링되지 않도록 수정
- 모달 내부: 카테고리 배지, 날짜, 발신자, 전체 링크, 요약, 의견, 태그

### 카테고리 4종으로 확장
- 기존 2개(프로젝트, 경제뉴스) → 4개 추가
- 🚀 프로젝트 / 📈 경제뉴스 / 💡 아이디어 / ✅ 처리해야할일
- fetch_news.py TARGET_SUBJECTS도 4종으로 업데이트

### 페이지네이션
- 한 페이지 18개 표시 (PAGE_SIZE = 18)
- PREV / NEXT + 페이지 번호 버튼
- 카테고리 전환·검색·CLR 시 페이지 0으로 자동 리셋

### 명언 티커
- 기존: 뉴스 제목 흘리기 → 변경: 세계 유명 명언 28개
- 애니메이션: translateX(0) → translateX(-50%), 360s/cycle (느린 속도)
- 콘텐츠 2배 복제로 끊김 없는 루프 구현

### tmux / TUI
- ESC 키 충돌 수정: `escape-time 0` (news-arcade 세션), `escape-time 10` (전역)
- ALT+hjkl 바인딩 해제 (news-arcade 세션 내에서)
- TUI 렌더링 버그 수정: `noutrefresh/doupdate` 패턴 적용

### nginx / 접속
- nginx로 http://psncs.iptime.org/news/ 서비스 (80포트)
- /news/ → web/, /news/data/ → data/ 매핑

### Copilot 자동화
- `.github/copilot-instructions.md` 생성
- 트리거: "일을 정리 해주세요" → README + worklog + lessons 자동 정리
