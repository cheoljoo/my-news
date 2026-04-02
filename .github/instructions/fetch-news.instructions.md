---
description: fetch_news.py 실행, Gmail API, 데이터 파싱 관련 작업 시 참고
---

# 스킬: 뉴스 fetch

## 대상 메일 제목 (TARGET_SUBJECTS)
- `좋은 프로젝트`
- `경제 뉴스 정리`
- `아이디어`
- `처리해야 할 일`

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
- 필드: `id`, `subject`, `category`, `from`, `date`, `urls`, `summary`, `opinion`, `tags`, `fetched_at`

## 태그 자동 생성 3가지 방법
1. `TAG_KEYWORDS` 딕셔너리 키워드 매핑 (18개 카테고리)
2. URL 도메인 태그 (github.com → GitHub 등)
3. 본문 내 `#태그명` 해시태그 추출
