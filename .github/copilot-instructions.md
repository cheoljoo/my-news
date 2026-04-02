# GitHub Copilot Instructions

## 프로젝트 개요
- **프로젝트명**: NEWS ARCADE
- **목적**: Gmail에서 메일을 읽어 JSON으로 파싱 후 8-bit 아케이드 스타일 웹사이트에 표시
- **주요 파일**: `fetch_news.py`, `web/index.html`, `serve.py`
- **데이터 경로**: `data/news.json`, `data/processed_ids.json`
- **서비스 URL**: http://psncs.iptime.org/news/
- **언어**: Python 3, HTML/CSS/JS (vanilla)
- **서버**: nginx (port 80), `/etc/nginx/sites-available/news-arcade`

> 스킬별 상세 지시는 `.github/instructions/` 폴더의 파일을 참고하세요.
> git commit은 직접 하지 않습니다. 사용자가 수동으로 처리합니다.
> python을 실행시 uv run 을 사용해주세요.
