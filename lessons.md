# 교훈 및 발견 (Lessons Learned)

팀원들과 공유할 중요한 기술적 발견과 교훈을 기록합니다.

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
