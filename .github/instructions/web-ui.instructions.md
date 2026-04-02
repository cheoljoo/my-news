---
description: web/index.html UI 수정, 카드/모달/필터/티커 관련 작업 시 참고
---

# 스킬: 웹 UI

## 기술 스택
- 순수 HTML/CSS/JS (프레임워크 없음)
- 폰트: Press Start 2P (Google Fonts) — 8-bit 아케이드 스타일
- 데이터: `fetch('/news/data/news.json')` 로 로드

## 카테고리 4종
| key | label | 메일 subject |
|-----|-------|-------------|
| `project` | 🚀 프로젝트 | 좋은 프로젝트 |
| `economy` | 📈 경제뉴스 | 경제 뉴스 정리 |
| `idea` | 💡 아이디어 | 아이디어 |
| `todo` | ✅ 처리해야할일 | 처리해야 할 일 |

## 주요 JS 함수
- `renderNews()` — 필터/검색/페이지 적용 후 카드 렌더링
- `renderCard(item)` — 카드 HTML 생성
- `openModal(id)` — 전체 내용 모달 표시
- `closeModal()` — ESC / X 키로 닫기
- `goPage(p)` — 페이지 이동 (PAGE_SIZE = 18)
- `toggleTag(tag)` — 태그 필터 토글
- `updateTicker()` — 명언 티커 초기화

## 티커
- 28개 명언 × 2 복제 → `translateX(0)` → `translateX(-50%)`, 360s loop
- 수정 시 `QUOTES` 배열과 animation duration 함께 조정

## 폰트 크기 규칙
- 최소 12px (Press Start 2P는 작아 보여서 px 단위 사용, rem 사용 금지)
