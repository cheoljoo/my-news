---
description: fetch_news.py 실행, Gmail API, 데이터 파싱 관련 작업 시 참고
---

# 스킬: 뉴스 fetch

## 카테고리 설정 (fetch.config.json)
- 대상 메일 제목은 **`fetch.config.json`** 에서 관리 (하드코딩 아님)
- 새 카테고리 추가 시 이 파일만 수정하면 fetch + 웹 UI 자동 반영
- 필드: `subject`(메일 제목), `key`(CSS 클래스용), `label`(표시명), `emoji`, `color`
- `color` 가능 값: `green`, `orange`, `cyan`, `magenta`, `yellow`, `blue`
- `key`, `color`, `emoji`, `label` 미지정 시 자동 부여

```json
{
  "categories": [
    { "subject": "좋은 프로젝트",  "key": "project", "label": "프로젝트",    "emoji": "🚀", "color": "green" },
    { "subject": "경제 뉴스 정리", "key": "economy", "label": "경제뉴스",    "emoji": "📈", "color": "orange" },
    { "subject": "아이디어",        "key": "idea",    "label": "아이디어",    "emoji": "💡", "color": "cyan" },
    { "subject": "처리해야 할 일", "key": "todo",    "label": "처리해야할일", "emoji": "✅", "color": "magenta" }
  ]
}
```

## 실행
```bash
uv run python3 fetch_news.py
```

## 중복 방지
- `data/processed_ids.json` 에 처리된 메일 ID 저장
- 이미 처리된 ID는 자동 스킵
- 재처리 원할 시 해당 파일 삭제

## 데이터 출력
- `data/news.json` — 파싱된 뉴스 배열 (JSON)
- `data/categories.json` — 웹 UI용 카테고리 메타데이터 (fetch 시 자동 갱신)
- 필드: `id`, `subject`, `category`, `from`, `date`, `urls`, `summary`, `opinion`, `tags`, `fetched_at`

## 태그 자동 생성 3가지 방법
1. `TAG_KEYWORDS` 딕셔너리 키워드 매핑 (18개 카테고리)
2. URL 도메인 태그 (github.com → GitHub 등)
3. 본문 내 `#태그명` 해시태그 추출
