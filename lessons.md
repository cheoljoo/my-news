# 교훈 및 발견 (Lessons Learned)

팀원들과 공유할 중요한 기술적 발견과 교훈을 기록합니다.

---

## 2026-04-03 — 설정 파일 기반 동적 UI

- 하드코딩된 카테고리를 JSON 설정 파일(`fetch.config.json`)로 분리하면
  Python 스크립트와 웹 UI 양쪽을 한 번에 제어할 수 있다.
- 웹 UI에서 `data/categories.json`을 fetch해 CSS·버튼·통계를 동적 생성하면
  소스 코드 수정 없이 카테고리 추가/삭제가 가능하다.
- categories.json 없을 때 news.json의 category 필드에서 자동 추론하는 fallback을
  함께 두면 하위 호환성이 유지된다.

## 2026-04-03 — emoji 참조 시스템

- emoji를 문자열로 직접 입력하면 복붙이 어렵고 잘못 입력되기 쉽다.
- 코드에 숫자 인덱스 목록(`EMOJI_LIST`)을 정의하고 설정 파일에서는
  숫자(`"emoji": 130`)로만 지정하면 오타 없이 안전하게 emoji를 선택할 수 있다.
- 문자열도 fallback으로 허용해두면 이전 설정과 호환된다.

---

## 2026-04-03 — Gmail Reply/Forward 인용 제거 전략

**문제**: Reply/Forward 메일은 이전 내용이 누적되어 본문이 수십만 자까지 불어난다.
단순 HTML 태그 제거만으로는 인용 블록이 그대로 남는다.

**해결 2단계 전략**:
1. **HTML 단계**: `gmail_attr`, `gmail_quote` div와 `blockquote` 태그를 마커(`\x00REPLY_CUT\x00`)로 치환 후 마커 이전만 남김. `.*?` 패턴 대신 마커 방식을 써야 중첩 div에서 안전하다.
2. **Plain text 단계**: 한국어 `2026년 N월 N일 ... 님이 작성:` 패턴, `>` 인용 줄, 구분선(`---`, `___`) 순서로 감지해 이후 전체 제거.

**교훈**: HTML과 Plain text 두 경로를 모두 처리해야 한다. `.*?` DOTALL 정규식은 중첩 태그에서 오작동하므로 마커 방식이 더 안전하다.

---

## 2026-04-03 — worklog 파일 크기 관리 전략

**문제**: worklog.md / worklog.json 을 계속 append하면 파일이 무한정 커져 관리가 어려워진다.

**해결**: 월별 분리 + 자동 아카이브 전략
- `worklog.md` / `data/worklog.json` 은 **이번 달만** 유지
- 매월 초 첫 "일을 정리해주세요" 시 지난달 파일을 `worklog/YYYY-MM.md`, `data/worklog/YYYY-MM.json` 으로 자동 이동
- 전체 조회 필요 시 `"워크로그 통합해줘"` → `data/worklog_all.json` 생성

**교훈**: 로그성 파일은 처음 설계할 때 분리/아카이브 전략을 포함해야 한다.
나중에 파일이 커진 후 분리하면 기존 데이터 마이그레이션 비용이 발생한다.

---

## 2026-04-03 — AI 툴별 session_id로 작업 이력 추적

**배경**: 한 사람이 Copilot CLI, Claude Code, VS Code Copilot 등 여러 AI 툴을 동시에 사용할 수 있다.
각 툴은 독립적인 세션을 가지며, 같은 날 여러 툴로 작업하면 worklog가 분산된다.

**해결**: worklog.json에 `tool` + `session_id` 필드 추가
- 동일 세션 중복 기록 방지
- 여러 툴의 기록을 날짜 기준으로 합산 가능
- 어떤 툴로 어떤 작업을 했는지 사후 분석 가능

**교훈**: 여러 도구를 병행 사용하는 환경에서는 출처(tool+session)를 메타데이터로 남겨야
나중에 데이터를 의미있게 집계할 수 있다.

---

## 2026-04-02 — Copilot CLI instructions 인식 범위

**문제**: `.github/copilot-instructions.md`에 `~/.github/instructions/` 경로를 텍스트로 언급해도,
Copilot CLI는 해당 경로를 실제로 로드하지 않음. VS Code User settings는 CLI에 전달되지 않는다.

**해결**: CLI에서 전역 스킬을 사용하려면 명시적 등록 필요:
```bash
# ~/.bashrc 또는 ~/.zshrc
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$HOME/.github/instructions"
```

**교훈**: VS Code의 `github.copilot.chat.instructionFiles` 설정은 CLI와 공유되지 않는다.
두 환경을 동시에 지원하려면 환경변수 방식이 가장 관리하기 쉽다.
`/instructions` 명령으로 현재 로드된 파일 목록을 언제든지 확인할 수 있다.

---

## 2026-04-02 — 모달 외부 클릭 닫기와 stopPropagation

**문제**: modal-overlay 클릭으로 모달을 닫으려 할 때, modal-box가 overlay 안에 있어서
modal-box 클릭 이벤트가 overlay까지 버블링되어 모달 내부를 클릭해도 닫혀버리는 문제.

**해결**: modal-box에 `event.stopPropagation()` 추가
```javascript
modalBox.addEventListener('click', e => e.stopPropagation());
modalOverlay.addEventListener('click', closeModal);
```

**교훈**: 오버레이 패턴으로 클릭-외부-닫기를 구현할 때는, 내부 박스에 반드시
`stopPropagation()`을 추가해야 이벤트 버블링을 막을 수 있다.

---



**문제**: `stdscr.erase()` 후 `subwin.refresh()` → `stdscr.refresh()` 순서로 호출하면,
stdscr.refresh()가 subwin이 그린 내용을 덮어써서 화면에 아무것도 안 보이는 버그 발생.

**해결**: staged update 패턴 사용
```python
stdscr.noutrefresh()      # 배경을 가상 버퍼에 예약
list_win.noutrefresh()    # 서브윈도우를 가상 버퍼에 예약 (위에 겹침)
curses.doupdate()         # 한 번에 화면에 반영
```
**교훈**: curses에서 여러 윈도우를 동시에 그릴 때는 반드시 noutrefresh + doupdate 조합을 사용한다.

---

## 2026-04-02 — tmux escape-time과 ESC 키 충돌

**문제**: tmux 기본 `escape-time 500ms`에서 ESC 키를 누르면 500ms 내 다음 키와 합쳐져 ALT+키로 해석됨.
`bind -n M-h/j/k/l select-pane`이 있으면 vi/curses에서 ESC+hjkl → pane 이동 발생.

**해결**:
- `~/.tmux.conf`에 `set -sg escape-time 10` (전역)
- news-arcade 세션에는 `set -s escape-time 0` + `unbind -n M-h` 등 추가 해제

**교훈**: TUI 앱을 tmux 안에서 실행할 때는 escape-time을 반드시 낮춰야 한다.

---

## 2026-04-02 — CSS marquee translateX 기준

**문제**: `translateX(100%)` → `translateX(-100%)` 방식은 요소 자신의 너비 기준이라
초기 위치가 화면 밖으로 날아가거나 보이지 않는 문제 발생.

**해결**: 콘텐츠를 2배 복제 후 `translateX(0)` → `translateX(-50%)` 사용
- 시작 위치(0)가 화면 왼쪽, 끝 위치(-50%)가 정확히 한 사이클
- 2배 복제이므로 루프가 끊김 없이 이어짐

**교훈**: CSS 마퀴 구현 시 "콘텐츠 2배 복제 + 0 → -50%" 패턴이 가장 안정적이다.

---

## 2026-04-02 — nginx alias vs root 경로 설정

**문제**: nginx `location /news/data/`에서 `root` 지시어 사용 시 경로가 중첩되어
`/var/www/.../news/data/data/news.json`처럼 잘못된 경로로 매핑됨.

**해결**: `alias` 지시어 사용
```nginx
location /news/data/ {
    alias /home/cheoljoo/code/my-news/data/;
}
```
**교훈**: nginx에서 URL prefix를 제거하고 다른 경로로 매핑할 때는 `root` 대신 `alias`를 사용한다.
