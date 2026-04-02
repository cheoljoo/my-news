---
description: nginx 설정 변경 또는 서버 배포 관련 작업 시 참고
---

# 스킬: nginx / 배포

## nginx 설정
- 설정 파일: `/etc/nginx/sites-available/news-arcade`
- 심볼릭 링크: `/etc/nginx/sites-enabled/news-arcade`
- sudo 비밀번호: 별도 확인 필요 (코드에 저장 금지)
- 웹 루트: `/home/cheoljoo/code/my-news/web/`
- 데이터 경로: `/home/cheoljoo/code/my-news/data/`

## URL 매핑
- `/news/` → `web/` (alias)
- `/news/data/` → `data/` (alias)
- `root` 대신 반드시 `alias` 사용 (경로 중복 방지)

## 파일 권한
- www-data가 접근하려면: `chmod o+x /home/cheoljoo` 및 프로젝트 파일 `o+rX`

## nginx 재시작
```bash
sudo nginx -t && sudo systemctl reload nginx
```
