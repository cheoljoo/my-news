# 📰 NEWS ARCADE

## 📋 요구사항 (원본 프롬프트)

> gmail에서 메일을 읽어서 제목이 **"좋은 프로젝트"** 이거나, **"경제 뉴스 정리"** 인 경우,
> 각각의 내용을 json으로 정리해 달라.
> 이후 정리된 내용을 web으로 개시할수 있게 만들어 달라.
> 각 메일에는 기본적으로 url이 들어가고 그 뒤에 뭔가 정리된 내용이 나오며, 의견 부분이 들어가게 된다.
> 각 내용을 만들때 tag를 자동으로 만들어 넣도록한다.
> web에서 검색시 tag기준으로 검색이 잘되게 하기 위해서이다.
> web site는 아주 재미나게 pixel 같은 것으로 만든 사이트를 여러개 추천하면 이중 선택할 것이다.
> 선택한 것으로 구현을 해 달라.
> 메일을 가져올때 한번 처리된 것은 다시 가져올 필요는 없다.

---

## 🎨 웹사이트 스타일 선택

다음 5가지 픽셀 아트 테마를 추천하였고, **🎮 8-bit Arcade** 스타일이 선택되었습니다.

| # | 테마 | 설명 |
|---|------|------|
| 1 | **🎮 8-bit Arcade** ✅ | 레트로 게임 스타일, 픽셀 폰트, 점수판 레이아웃, 애니메이션 캐릭터 |
| 2 | 📺 CRT Terminal | 구형 모니터 스캔라인 효과, 녹색/호박 형광 글로우, 클래식 터미널 느낌 |
| 3 | 🌈 Pixel Rainbow | 밝고 알록달록한 픽셀 블록, 레인보우 그라디언트, 귀엽고 경쾌한 느낌 |
| 4 | 🌃 Cyberpunk Neon | 어두운 배경에 네온 픽셀 아트, 글리치 효과, 미래적인 분위기 |
| 5 | 🗺️ RPG Quest Board | RPG 게임 UI, 나무/돌 텍스처 픽셀 테두리, 퀘스트 게시판 레이아웃 |

---

## 🗂️ 프로젝트 구조

```
my-news/
├── fetch_news.py           # Gmail 읽기 + JSON 파싱 + 태그 자동 생성
├── serve.py                # HTTP 서버 실행 (포트 8080)
├── pyproject.toml          # 의존성 정의
├── credentials.json        # (직접 준비) Google OAuth 클라이언트 파일
├── token.json              # (자동 생성) OAuth 인증 토큰
├── data/
│   ├── news.json           # 파싱된 뉴스 데이터 (자동 생성)
│   └── processed_ids.json  # 처리 완료된 메일 ID — 중복 방지 (자동 생성)
└── web/
    └── index.html          # 🎮 8-bit 아케이드 웹사이트
```

---

## ⚙️ 설치 및 설정

### 1. 의존성 설치

```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Gmail API 활성화 및 credentials.json 준비

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스 → 라이브러리** → `Gmail API` 검색 후 **사용 설정**
4. **API 및 서비스 → 사용자 인증 정보** → **사용자 인증 정보 만들기 → OAuth 클라이언트 ID**
5. 애플리케이션 유형: **데스크톱 앱** 선택
6. 생성된 JSON 파일을 `credentials.json` 이름으로 프로젝트 루트에 저장

---

## 🚀 사용법

### Step 1 — Gmail에서 뉴스 가져오기

```bash
python3 fetch_news.py
```

**처음 실행 시 OAuth 인증 절차:**

```
브라우저를 자동 실행하지 않습니다.
아래 URL을 PC 브라우저에서 직접 열어서 승인해주세요:

https://accounts.google.com/o/oauth2/auth?...

승인 후 localhost 접속 오류 페이지가 떠도 정상입니다.
주소창의 전체 URL 또는 code 값만 복사해 붙여 넣어주세요.

리다이렉트 URL 또는 code: [여기에 붙여넣기]
```

**두 번째 실행부터는** 저장된 `token.json`을 자동으로 사용하므로 인증 없이 바로 실행됩니다.

**실행 결과 예시:**

```
Gmail 서비스 연결 중...
기존 처리된 메일: 3개  /  저장된 뉴스: 3개

[검색] subject:"좋은 프로젝트"
  매칭된 메일: 5개
  [SKIP] abc123 (이미 처리됨)
  [OK] 좋은 프로젝트
       날짜: Mon, 31 Mar 2025 09:00:00 +0900
       URL: 2개  태그: AI, GitHub, 기술, 오픈소스, 프로젝트추천

[검색] subject:"경제 뉴스 정리"
  매칭된 메일: 3개
  [OK] 경제 뉴스 정리
       날짜: Sun, 30 Mar 2025 08:00:00 +0900
       URL: 1개  태그: 경제, 경제뉴스, 반도체, 해외

==================================================
✅ 완료!
   새로 처리: 2개
   전체 뉴스: 5개
   저장 위치: data/news.json
==================================================
```

### Step 2 — 웹사이트 실행

```bash
python3 serve.py
```

브라우저가 자동으로 열립니다: **http://localhost:8080/web/**

포트를 변경하려면:

```bash
python3 serve.py 9090
```

---

## 📧 메일 형식 (권장)

`fetch_news.py`는 다음 구조를 기준으로 메일 본문을 자동 파싱합니다.

```
https://example.com/article-url-1
https://example.com/article-url-2

[요약/본문 내용]
URL 뒤에 오는 텍스트는 자동으로 summary 섹션으로 파싱됩니다.
여러 줄도 그대로 저장됩니다.

의견
[개인 코멘트나 분석 내용]
이 부분은 별도 OPINION 섹션으로 분리됩니다.
```

**의견 섹션 시작 마커** (다음 중 하나가 한 줄에 단독으로 있으면 인식):

| 마커 | 비고 |
|------|------|
| `의견` | 기본 마커 |
| `의견:` | 콜론 포함 |
| `코멘트` / `코멘트:` | |
| `comment` / `opinion` | 대소문자 무관 |
| `📝` | 이모지 마커 |
| `생각` / `평가` / `분석` | |

---

## 🏷️ 태그 자동 생성 방식

3가지 방법으로 태그를 자동 추출합니다.

### 방법 1 — 키워드 매핑 (18개 카테고리)

| 태그 | 인식 키워드 예시 |
|------|-----------------|
| `AI` | ai, 인공지능, 머신러닝, gpt, llm, chatgpt, openai, gemini, claude |
| `경제` | 경제, 금융, 주식, 코스피, 나스닥, 물가, 인플레이션, 금리, 환율 |
| `스타트업` | 스타트업, 창업, 투자, 펀딩, 시리즈a, 벤처, ipo, 엑시트 |
| `기술` | 기술, tech, 개발, 클라우드, aws, gcp, docker, kubernetes |
| `블록체인` | 블록체인, 비트코인, 이더리움, nft, web3, 암호화폐, defi |
| `환경` | 환경, 기후, 탄소, 전기차, ev, 친환경, esg, 탄소중립 |
| `헬스케어` | 헬스케어, 의료, 바이오, 건강, 제약, biotech, 신약 |
| `교육` | 교육, edtech, 코딩교육, 온라인강의, 부트캠프, mooc |
| `부동산` | 부동산, 아파트, 집값, 전세, 월세, 분양, proptech |
| `정치` | 정치, 정부, 대통령, 국회, 선거, 정책, 규제, 법안 |
| `해외` | 미국, 중국, 일본, 유럽, 글로벌, 실리콘밸리, 월스트리트 |
| `보안` | 보안, 해킹, 사이버, 랜섬웨어, malware, 침해사고 |
| `오픈소스` | 오픈소스, opensource, github, gitlab |
| `데이터` | 데이터, analytics, bigdata, sql, 데이터분석, 시각화 |
| `모바일` | 모바일, ios, android, flutter, swift, kotlin |
| `게임` | 게임, gaming, 메타버스, vr, ar, 유니티, 언리얼 |
| `반도체` | 반도체, 엔비디아, nvidia, tsmc, 삼성전자, sk하이닉스 |
| `자동화` | 자동화, rpa, 로봇, iot, 스마트팩토리, automation |

### 방법 2 — URL 도메인 태그

| 도메인 | 태그 |
|--------|------|
| github.com | `GitHub` |
| medium.com | `Medium` |
| techcrunch.com | `TechCrunch` |
| arxiv.org | `논문` |
| youtube.com / youtu.be | `YouTube` |
| naver.com | `Naver` |
| joongang.co.kr | `중앙일보` |
| hani.co.kr | `한겨레` |
| chosun.com | `조선일보` |
| zdnet.co.kr | `ZDNet` |
| linkedin.com | `LinkedIn` |
| producthunt.com | `ProductHunt` |
| news.ycombinator.com | `HackerNews` |
| reddit.com | `Reddit` |
| velog.io | `Velog` |
| tistory.com | `Tistory` |

### 방법 3 — 이메일 내 해시태그 추출

메일 본문에 `#태그명` 형식으로 작성하면 자동으로 태그에 추가됩니다.

```
이번 주 #AI 관련 프로젝트가 주목받고 있습니다. #스타트업 #투자
```

→ 태그: `AI`, `스타트업`, `투자`

---

## 📦 data/news.json 구조

```json
[
  {
    "id": "메일고유ID",
    "subject": "좋은 프로젝트",
    "category": "좋은 프로젝트",
    "from": "sender@example.com",
    "date": "Mon, 31 Mar 2025 09:00:00 +0900",
    "urls": [
      "https://github.com/example/project",
      "https://techcrunch.com/2025/..."
    ],
    "summary": "요약 본문 내용\n여러 줄도 유지됩니다.",
    "opinion": "개인 의견 또는 분석 내용",
    "tags": ["AI", "GitHub", "기술", "오픈소스", "프로젝트추천"],
    "fetched_at": "2025-03-31T09:00:00"
  }
]
```

---

## 🌐 웹사이트 기능

### 🎮 8-bit 아케이드 UI

- **Press Start 2P** 픽셀 폰트 (Google Fonts)
- 검은 배경 + 스캔라인 오버레이 효과
- 헤더 별빛 배경 애니메이션
- 네온 컬러 팔레트 (노랑, 청록, 마젠타, 초록, 주황)
- 카드 호버 시 픽셀 이동 + 네온 글로우 효과
- **명언 티커**: 세계의 유명 명언 28개를 천천히 흘려 보여주는 마퀴 (360s/cycle)
- **카드 클릭 → 상세 모달**: 카드 본문 클릭 시 전체 내용을 팝업으로 표시 (ESC / X 키 / ✕ 버튼 / 모달 외부 클릭으로 닫기)
- **고정 카드 크기**: 높이 400px 고정, 글자 최소 12px

### 🔍 검색 및 필터링

| 기능 | 설명 |
|------|------|
| **키워드 검색** | 제목 · 요약 · 의견 · URL · 태그 전체 통합 검색 |
| **카테고리 필터** | ALL / 🚀 프로젝트 / 📈 경제뉴스 / 💡 아이디어 / ✅ 처리해야할일 |
| **태그 필터** | POWER-UPS 영역에서 태그 클릭 → 해당 태그 포함 뉴스만 표시 |
| **복합 필터** | 카테고리 + 태그 + 키워드 동시 적용 가능 |
| **CLR 버튼** | 모든 필터 및 검색어 초기화 + 페이지 리셋 |
| **페이지네이션** | 한 페이지에 18개씩 표시, PREV / NEXT / 페이지 번호 버튼 |

### 📰 카드 구성

```
┌─────────────────────────────────────────┐
│ [🚀 프로젝트]              2025-03-31   │
├─────────────────────────────────────────┤
│ 카드 제목 (메일 subject)                │
│                                         │
│ ▶ LINKS                                 │
│   github.com/example/project            │
│   techcrunch.com/2025/...               │
│                                         │
│ ▶ SUMMARY                               │
│   요약 본문 내용...                      │
│                                         │
│ ▶ OPINION                               │
│   개인 의견 또는 분석...                 │
│                                         │
│ #AI  #GitHub  #기술  #프로젝트추천      │
├─────────────────────────────────────────┤
│                             [▼ MORE]    │
└─────────────────────────────────────────┘
```

- **▼ MORE / ▲ LESS**: 긴 요약 내용 펼치기/접기
- **카드 클릭**: 전체 내용 모달 팝업 (링크·태그 제외 영역 클릭)
- **#태그 클릭**: 해당 태그로 즉시 필터링
- **LINKS 클릭**: 새 탭에서 원문 열기 (카드에는 최대 3개 표시)

---

## 🔄 중복 처리 방지

`data/processed_ids.json`에 처리 완료된 메일 ID가 저장됩니다.

```json
["abc123def456", "ghi789jkl012", ...]
```

`fetch_news.py` 실행 시 이미 저장된 ID의 메일은 자동으로 건너뜁니다.
이 파일을 삭제하면 전체 메일을 다시 처리합니다.

---

## 🛠️ CLI 옵션 (fetch_news.py)

```bash
python3 fetch_news.py [옵션]

옵션:
  --credentials PATH    OAuth 클라이언트 파일 경로 (기본: credentials.json)
  --token PATH          OAuth 토큰 파일 경로 (기본: token.json)
  --auth-mode MODE      인증 방식: manual(기본) | local-server
  --auth-host HOST      local-server 모드 바인딩 호스트 (기본: 127.0.0.1)
  --auth-port PORT      local-server 모드 포트 (기본: 0, 임의 포트)
```

**`manual` 모드 (기본)**: URL을 복사해 브라우저에서 직접 승인
**`local-server` 모드**: localhost 콜백 서버 자동 실행 (GUI 환경 필요)

---

## 📝 의존성 (pyproject.toml)

```toml
[project]
name = "gmail"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
  "google-api-python-client>=2.0",
  "google-auth-httplib2>=0.2",
  "google-auth-oauthlib>=1.0",
]
```

---

## ❓ 자주 묻는 질문

**Q. credentials.json은 어디서 받나요?**
A. Google Cloud Console → API 및 서비스 → 사용자 인증 정보에서 OAuth 2.0 클라이언트 ID(데스크톱 앱)를 생성하고 JSON을 다운로드하세요.

**Q. token.json이 생성됩니다. 안전한가요?**
A. `token.json`에는 Gmail 읽기 전용 토큰만 포함됩니다. `.gitignore`에 추가하여 공개 저장소에 올리지 않도록 주의하세요.

**Q. 메일을 다시 가져오고 싶습니다.**
A. `data/processed_ids.json`을 삭제하거나 특정 ID를 제거한 뒤 `fetch_news.py`를 다시 실행하세요.

**Q. 태그가 잘 인식되지 않습니다.**
A. `fetch_news.py` 상단의 `TAG_KEYWORDS` 딕셔너리에 원하는 키워드를 직접 추가할 수 있습니다.

**Q. 포트 8080이 이미 사용 중입니다.**
A. `python3 serve.py 9090` 처럼 다른 포트 번호를 인수로 전달하세요.

---

## 🌍 외부 접속 (psncs.iptime.org:8080)

### 서버 바인딩 확인

`serve.py`는 `0.0.0.0`으로 바인딩되므로 LAN 및 외부 접속이 기본 허용됩니다.

```bash
# 브라우저 없이 실행 (서버/tmux 환경 권장)
python3 serve.py --no-browser
```

실행 시 내부 IP가 자동으로 표시됩니다:

```
═══════════════════════════════════════════════════════
🎮  NEWS ARCADE SERVER
═══════════════════════════════════════════════════════
  로컬:     http://localhost:8080/web/
  LAN:      http://192.168.0.10:8080/web/

  외부 접속 (iptime 공유기 포트포워딩 설정 필요):
  → 외부IP:8080 → 내부IP(192.168.0.10):8080
```

### iptime 공유기 포트포워딩 설정

1. 브라우저에서 `http://192.168.0.1` 접속 (iptime 관리 페이지)
2. **고급 설정 → NAT/라우터 관리 → 포트포워드 설정**
3. 아래와 같이 규칙 추가:

| 항목 | 값 |
|------|-----|
| 규칙 이름 | news-arcade |
| 내부 IP | 서버 IP (예: 192.168.0.10) |
| 내부 포트 | 8080 |
| 외부 포트 | 8080 |
| 프로토콜 | TCP |

4. 저장 후 외부에서 `http://psncs.iptime.org:8080/web/` 접속

### 방화벽 포트 오픈 (필요한 경우)

```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

> ⚠️ **보안 주의**: 외부에 노출되는 포트이므로, 필요하지 않을 때는 서버를 종료하거나 방화벽으로 차단하세요.

---

## 🖥️ tmux 터미널 뷰어 (view_news.py)

`w3m` 같은 터미널 브라우저는 JavaScript를 실행하지 못해 NEWS ARCADE 페이지가 동작하지 않습니다.  
대신 전용 터미널 뷰어 `view_news.py`를 제공합니다.

### tmux 추천 레이아웃

```
┌──────────────────────┬──────────────────────┐
│                      │                      │
│   pane 1             │   pane 2             │
│   python3 serve.py   │   python3            │
│   --no-browser       │   view_news.py       │
│   (서버 로그)         │   (뉴스 탐색)         │
│                      │                      │
└──────────────────────┴──────────────────────┘
```

```bash
# tmux 두 pane으로 나누기
tmux split-window -h

# pane 1: 서버 실행 (브라우저 자동 오픈 없이)
python3 serve.py --no-browser

# pane 2: 터미널 뷰어
python3 view_news.py
```

### view_news.py 사용법

```bash
# 전체 목록
python3 view_news.py

# 카테고리 필터
python3 view_news.py --cat project      # 🚀 좋은 프로젝트만
python3 view_news.py --cat economy      # 📈 경제 뉴스 정리만

# 태그 필터
python3 view_news.py --tag AI
python3 view_news.py --tag 반도체

# 키워드 검색
python3 view_news.py --search 스타트업
python3 view_news.py --search github

# 상세 보기
python3 view_news.py --num 3            # 목록의 3번째 항목
python3 view_news.py --id <메일ID>      # ID로 직접 지정

# 전체 태그 목록 보기
python3 view_news.py --tags
```

### 출력 예시

```
════════════════════════════════════════════════════════
▓░░░░░░░░░░░░ 📰 NEWS ARCADE  —  총 4건 ░░░░░░░░░░░░░▓
════════════════════════════════════════════════════════

  [  1] [🚀 프로젝트]  2025-03-31 09:00
        좋은 프로젝트
        #AI  #GitHub  #오픈소스  #기술  #스타트업 ...
         🔗 2개 URL

  [  2] [📈 경제뉴스]  2025-03-30 08:00
        경제 뉴스 정리
        #경제  #경제뉴스  #반도체  #AI  #중앙일보 ...
         🔗 2개 URL
```

---

## 🖥️ tmux 인터랙티브 TUI 뷰어

`tui_news.py`는 tmux pane에서 웹사이트와 동일한 내용을 터미널로 탐색하는  
완전한 인터랙티브 TUI(Terminal UI)입니다.

### 실행 방법

```bash
# 방법 1: tmux 레이아웃 자동 생성 (권장)
./tmux_news.sh              # TUI + nginx 로그 (2 pane)
./tmux_news.sh tui          # TUI 단독 (1 pane)
./tmux_news.sh full         # TUI + nginx 로그 + fetch 패널 (3 pane)

# 방법 2: 현재 pane에서 바로 실행
python3 tui_news.py
```

### 화면 구성

**목록 화면:**
```
╔══════════════════════════════════════════════════════╗
║ 🎮 NEWS ARCADE              TOTAL:4 PROJECT:2 ECONOMY:2 ║
║ ALL  결과: 4건                                        ║
╠══════════════════════════════════════════════════════╣
║ ┌─ LIST ──────────────────────────────────────────┐  ║
║ │►🚀 2025-03-31  좋은 프로젝트                    │  ║
║ │ �� 2025-03-30  경제 뉴스 정리                   │  ║
║ │ 🚀 2025-03-29  좋은 프로젝트                    │  ║
║ │ 📈 2025-03-28  경제 뉴스 정리                   │  ║
║ └─────────────────────────────────────────────────┘  ║
╠══════════════════════════════════════════════════════╣
║ [↑↓]이동 [Enter]상세 [/]검색 [c]카테고리 [t]태그 [q]종료 ║
╚══════════════════════════════════════════════════════╝
```

**Enter 누르면 분할 화면:**
```
┌─ LIST ───────────┬─ DETAIL ─────────────────────────┐
│►🚀 2025-03-31    │ [🚀 프로젝트]  2025-03-31         │
│ 📈 2025-03-30    │ 좋은 프로젝트                     │
│ 🚀 2025-03-29    │                                   │
│ 📈 2025-03-28    │ ▶ LINKS                           │
│                  │   → github.com/microsoft/autogen  │
│                  │   → techcrunch.com/2025/...        │
│                  │                                   │
│                  │ ▶ SUMMARY                         │
│                  │   AutoGen은 Microsoft에서 만든     │
│                  │   멀티 에이전트 AI 프레임워크...   │
│                  │                                   │
│                  │ ▶ OPINION                         │
│                  │   LLM 오케스트레이션 도구 중...     │
│                  │                                   │
│                  │ ▶ TAGS                            │
│                  │   #AI #GitHub #기술 #오픈소스      │
└──────────────────┴───────────────────────────────────┘
```

### 키보드 단축키

| 키 | 동작 |
|----|------|
| `↑` / `k` | 위로 이동 |
| `↓` / `j` | 아래로 이동 |
| `PageUp` | 5칸 위로 |
| `PageDown` | 5칸 아래로 |
| `Enter` | 상세 보기 (분할 화면) |
| `Tab` | 목록 ↔ 상세 포커스 전환 |
| `Esc` / `q` | 상세 닫기 / 종료 |
| `/` | 검색 모드 진입 |
| `c` | 카테고리 순환 (ALL → 🚀 프로젝트 → 📈 경제뉴스 → 💡 아이디어 → ✅ 처리해야할일) |
| `t` | 태그 필터 팝업 |
| `r` | 데이터 새로고침 |
| `?` | 도움말 |

### tmux 레이아웃 (./tmux_news.sh full)

```
┌──────────────────────────┬─────────────────────┐
│                          │                     │
│   pane 0                 │   pane 1            │
│   python3 tui_news.py    │   nginx 접속 로그   │
│   (TUI 뉴스 뷰어)         ├─────────────────────┤
│                          │   pane 2            │
│                          │   fetch 실행 대기   │
└──────────────────────────┴─────────────────────┘
```

> tmux_news.sh를 두 번 실행하면 기존 세션에 자동으로 재접속됩니다.

---

## 🤖 Copilot 자동화 스킬

`.github/copilot-instructions.md`에 트리거 기반 자동화 작업이 정의되어 있습니다.

| 트리거 | 동작 |
|--------|------|
| **"일을 정리 해주세요"** | README 업데이트 + worklog.md 추가 + lessons.md 기록 |

---

## 🌐 서비스 URL

| 환경 | URL |
|------|-----|
| 외부 접속 | http://psncs.iptime.org/news/ |
| nginx 설정 | `/etc/nginx/sites-available/news-arcade` |
| 데이터 경로 | `/news/data/news.json` |
