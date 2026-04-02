# 작업 로그 (Work Log)

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
