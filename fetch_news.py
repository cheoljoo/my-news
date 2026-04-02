#!/usr/bin/env python3
"""
Gmail에서 특정 제목의 메일을 읽어 JSON으로 정리합니다.
대상 제목: "좋은 프로젝트", "경제 뉴스 정리"

처리된 메일 ID를 추적하여 중복 처리를 방지합니다.
"""

from __future__ import annotations

import argparse
import base64
import html as html_module
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TARGET_SUBJECTS = ["좋은 프로젝트", "경제 뉴스 정리", "아이디어", "처리해야 할 일"]

DATA_DIR = Path("data")
NEWS_FILE = DATA_DIR / "news.json"
PROCESSED_IDS_FILE = DATA_DIR / "processed_ids.json"

# ── 태그 자동 생성용 키워드 매핑 ────────────────────────────────────────────
TAG_KEYWORDS: dict[str, list[str]] = {
    "AI": ["ai", "인공지능", "머신러닝", "딥러닝", "gpt", "llm", "chatgpt", "openai",
           "gemini", "claude", "tensorflow", "pytorch", "neural", "nlp", "language model"],
    "경제": ["경제", "금융", "주식", "코스피", "코스닥", "나스닥", "gdp", "물가",
             "인플레이션", "금리", "환율", "재정", "부채", "통화", "증시", "채권"],
    "스타트업": ["스타트업", "창업", "투자", "펀딩", "시리즈a", "시리즈b", "벤처", "ipo",
                "엑시트", "accelerator", "incubator", "pre-ipo"],
    "기술": ["기술", "tech", "개발", "소프트웨어", "프로그래밍", "코딩", "api",
             "클라우드", "aws", "gcp", "azure", "devops", "kubernetes", "docker", "microservice"],
    "블록체인": ["블록체인", "비트코인", "이더리움", "nft", "web3", "암호화폐", "crypto",
                "defi", "dao", "토큰", "코인"],
    "환경": ["환경", "기후", "탄소", "에너지", "태양광", "풍력", "전기차", "ev",
             "친환경", "carbon", "sustainability", "esg", "넷제로", "탄소중립"],
    "헬스케어": ["헬스케어", "의료", "바이오", "건강", "병원", "제약", "biotech",
                 "medtech", "디지털헬스", "임상", "신약"],
    "교육": ["교육", "학습", "edtech", "코딩교육", "온라인강의", "이러닝", "mooc",
             "bootcamp", "부트캠프"],
    "부동산": ["부동산", "아파트", "집값", "전세", "월세", "분양", "proptech", "리츠"],
    "정치": ["정치", "정부", "대통령", "국회", "선거", "정책", "규제", "법안", "입법"],
    "해외": ["미국", "중국", "일본", "유럽", "글로벌", "해외", "international",
              "실리콘밸리", "월스트리트", "나스닥", "nyse"],
    "보안": ["보안", "해킹", "사이버", "privacy", "encryption", "vulnerability",
             "랜섬웨어", "malware", "제로데이", "침해사고"],
    "오픈소스": ["오픈소스", "opensource", "github", "gitlab", "커뮤니티", "contributor",
                 "mit license", "apache"],
    "데이터": ["데이터", "data", "analytics", "bigdata", "sql", "database", "etl",
               "데이터분석", "시각화", "데이터파이프라인"],
    "모바일": ["모바일", "ios", "android", "앱", "app", "flutter", "react native",
               "swift", "kotlin"],
    "게임": ["게임", "gaming", "e스포츠", "메타버스", "xr", "vr", "ar", "유니티",
             "언리얼", "게임엔진"],
    "반도체": ["반도체", "칩", "cpu", "gpu", "엔비디아", "nvidia", "인텔", "amd",
               "tsmc", "삼성전자", "sk하이닉스", "fab"],
    "자동화": ["자동화", "rpa", "로봇", "iot", "스마트팩토리", "제조", "automation"],
    "아이디어": ["아이디어", "생각", "기획", "idea", "planning", "proposal"],
    "할일": ["할일", "할 일", "작업", "task", "todo", "todo-list", "업무"],
}

# 도메인 → 태그 매핑
DOMAIN_TAG_MAP: dict[str, str] = {
    "github.com": "GitHub",
    "techcrunch.com": "TechCrunch",
    "medium.com": "Medium",
    "arxiv.org": "논문",
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "naver.com": "Naver",
    "daum.net": "Daum",
    "chosun.com": "조선일보",
    "joongang.co.kr": "중앙일보",
    "hani.co.kr": "한겨레",
    "zdnet.co.kr": "ZDNet",
    "bloter.net": "Bloter",
    "linkedin.com": "LinkedIn",
    "twitter.com": "Twitter",
    "x.com": "Twitter",
    "reddit.com": "Reddit",
    "producthunt.com": "ProductHunt",
    "hn.algolia.com": "HackerNews",
    "news.ycombinator.com": "HackerNews",
    "substack.com": "Substack",
    "notion.so": "Notion",
    "velog.io": "Velog",
    "tistory.com": "Tistory",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gmail에서 뉴스 메일을 읽어 JSON으로 저장합니다.")
    parser.add_argument("--credentials", default="credentials.json",
                        help="Google OAuth 클라이언트 파일 경로")
    parser.add_argument("--token", default="token.json",
                        help="저장된 OAuth 토큰 파일 경로")
    parser.add_argument("--auth-mode", choices=["local-server", "manual"],
                        default="manual", help="OAuth 인증 방식")
    parser.add_argument("--auth-host", default="127.0.0.1")
    parser.add_argument("--auth-port", type=int, default=0)
    return parser.parse_args()


# ── Gmail 인증 ───────────────────────────────────────────────────────────────

def get_gmail_service(
    credentials_path: Path,
    token_path: Path,
    auth_mode: str,
    auth_host: str,
    auth_port: int,
):
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"OAuth 클라이언트 파일이 없습니다: {credentials_path}\n"
                    "Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고\n"
                    "credentials.json으로 저장해주세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            if auth_mode == "manual":
                flow.redirect_uri = "http://localhost"
                auth_url, expected_state = flow.authorization_url(
                    access_type="offline",
                    include_granted_scopes="true",
                    prompt="consent",
                )
                print("\n" + "=" * 60)
                print("브라우저를 자동 실행하지 않습니다.")
                print("아래 URL을 PC 브라우저에서 직접 열어서 승인해주세요:")
                print("=" * 60)
                print(f"\n{auth_url}\n")
                print("=" * 60)
                print("승인 후 localhost 접속 오류 페이지가 떠도 정상입니다.")
                print("주소창의 전체 URL 또는 code 값만 복사해 붙여 넣어주세요.")
                authorization_response = input("\n리다이렉트 URL 또는 code: ").strip()
                if not authorization_response:
                    raise RuntimeError("입력이 비어 있습니다.")
                if authorization_response.startswith("http"):
                    parsed = urlparse(authorization_response)
                    code_values = parse_qs(parsed.query).get("code", [])
                    if not code_values:
                        raise RuntimeError("리다이렉트 URL에서 code 값을 찾지 못했습니다.")
                    flow.fetch_token(code=code_values[0])
                else:
                    flow.fetch_token(code=authorization_response)
            else:
                creds = flow.run_local_server(
                    host=auth_host, port=auth_port, open_browser=False
                )
            creds = flow.credentials
        token_path.write_text(creds.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=creds)


# ── 데이터 로드/저장 ─────────────────────────────────────────────────────────

def load_processed_ids() -> set[str]:
    if PROCESSED_IDS_FILE.exists():
        return set(json.loads(PROCESSED_IDS_FILE.read_text(encoding="utf-8")))
    return set()


def save_processed_ids(ids: set[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_IDS_FILE.write_text(
        json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8"
    )


def load_news() -> list[dict]:
    if NEWS_FILE.exists():
        return json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    return []


def save_news(news_list: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NEWS_FILE.write_text(
        json.dumps(news_list, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── 메시지 파싱 ──────────────────────────────────────────────────────────────

def get_header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def iter_parts(payload: dict) -> list[dict]:
    parts = payload.get("parts", [])
    if not parts:
        return [payload]
    result: list[dict] = []
    for part in parts:
        result.extend(iter_parts(part))
    return result


def decode_body(data: str) -> str:
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception:
        return ""


def strip_html(html_text: str) -> str:
    """HTML 태그 제거 및 텍스트 정리."""
    text = re.sub(r"<br\s*/?>", "\n", html_text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "\n• ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_module.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_message_text(service, message_id: str) -> tuple[str, str, str, str]:
    """메시지에서 (subject, from, date, body_text) 반환."""
    message = (
        service.users().messages().get(userId="me", id=message_id, format="full").execute()
    )
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    subject = get_header(headers, "Subject")
    sender = get_header(headers, "From")
    date_str = get_header(headers, "Date")

    plain_text = ""
    html_text = ""
    for part in iter_parts(payload):
        mime_type = part.get("mimeType", "")
        data = part.get("body", {}).get("data", "")
        if not data:
            continue
        if mime_type == "text/plain":
            plain_text += decode_body(data)
        elif mime_type == "text/html":
            html_text += decode_body(data)

    body = plain_text.strip() if plain_text.strip() else strip_html(html_text)
    return subject, sender, date_str, body


# ── 내용 파싱 ────────────────────────────────────────────────────────────────

URL_RE = re.compile(r"https?://[^\s\]>\"'）、。\)]+")

# 의견 섹션 시작을 나타내는 패턴
OPINION_MARKER_RE = re.compile(
    r"^[\s]*[#*\-►▶→]*[\s]*(의견|코멘트|comment|opinion|📝|생각|평가|분석)[:\s]*$",
    re.IGNORECASE,
)


def extract_sections(body: str) -> dict[str, object]:
    """본문에서 URL / 요약 / 의견 섹션을 분리."""
    urls: list[str] = []
    summary_lines: list[str] = []
    opinion_lines: list[str] = []
    in_opinion = False

    for line in body.splitlines():
        stripped = line.strip()

        if not stripped:
            (opinion_lines if in_opinion else summary_lines).append("")
            continue

        # 의견 섹션 마커 감지
        if OPINION_MARKER_RE.match(stripped):
            in_opinion = True
            continue

        # URL 추출 (중복 제거)
        for u in URL_RE.findall(stripped):
            if u not in urls:
                urls.append(u)

        if in_opinion:
            opinion_lines.append(stripped)
        else:
            summary_lines.append(stripped)

    # URL만으로 이루어진 줄은 summary에서 제거
    summary_cleaned = [
        ln for ln in summary_lines
        if not (ln.strip() and URL_RE.fullmatch(ln.strip()))
    ]

    return {
        "urls": urls,
        "summary": "\n".join(summary_cleaned).strip(),
        "opinion": "\n".join(opinion_lines).strip(),
    }


# ── 태그 생성 ────────────────────────────────────────────────────────────────

def extract_domain_tags(urls: list[str]) -> list[str]:
    """URL 도메인에서 유명 사이트 태그 추출."""
    tags: list[str] = []
    for url in urls:
        try:
            domain = urlparse(url).netloc.lower().lstrip("www.")
            for key, tag in DOMAIN_TAG_MAP.items():
                if key in domain and tag not in tags:
                    tags.append(tag)
        except Exception:
            pass
    return tags


def generate_tags(subject: str, body: str, urls: list[str]) -> list[str]:
    """텍스트 키워드 + URL 도메인 + 해시태그 기반 태그 자동 생성."""
    tags: set[str] = set()
    text_lower = (subject + " " + body).lower()

    # 카테고리 키워드 매칭
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                tags.add(tag)
                break

    # 주제 기반 고정 태그
    if "경제 뉴스" in subject or "경제뉴스" in subject:
        tags.add("경제뉴스")
    if "프로젝트" in subject:
        tags.add("프로젝트추천")
    if "아이디어" in subject:
        tags.add("아이디어")
    if "처리해야 할 일" in subject or "할 일" in subject or "할일" in subject:
        tags.add("할일")

    # 이메일 내 해시태그 추출 (#태그)
    for htag in re.findall(r"#([가-힣a-zA-Z0-9_]{2,20})", body):
        tags.add(htag)

    # URL 도메인 태그
    tags.update(extract_domain_tags(urls))

    return sorted(tags)


# ── 메인 ────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Gmail 서비스 연결 중...")
    service = get_gmail_service(
        Path(args.credentials),
        Path(args.token),
        args.auth_mode,
        args.auth_host,
        args.auth_port,
    )

    processed_ids = load_processed_ids()
    news_list = load_news()
    print(f"기존 처리된 메일: {len(processed_ids)}개  /  저장된 뉴스: {len(news_list)}개")

    new_count = 0

    for subject_keyword in TARGET_SUBJECTS:
        query = f'subject:"{subject_keyword}"'
        print(f"\n[검색] {query}")
        try:
            resp = (
                service.users()
                .messages()
                .list(userId="me", q=query, maxResults=500)
                .execute()
            )
            messages = resp.get("messages", [])
        except HttpError as e:
            print(f"  Gmail 조회 실패: {e}")
            continue

        print(f"  매칭된 메일: {len(messages)}개")

        for item in messages:
            msg_id = item["id"]
            if msg_id in processed_ids:
                continue  # 이미 처리된 메일 스킵

            try:
                subject, sender, date_str, body = get_message_text(service, msg_id)
                sections = extract_sections(body)
                tags = generate_tags(subject, body, sections["urls"])

                news_item = {
                    "id": msg_id,
                    "subject": subject,
                    "category": subject_keyword,
                    "from": sender,
                    "date": date_str,
                    "urls": sections["urls"],
                    "summary": sections["summary"],
                    "opinion": sections["opinion"],
                    "tags": tags,
                    "fetched_at": datetime.now().isoformat(),
                }

                news_list.append(news_item)
                processed_ids.add(msg_id)
                new_count += 1

                print(f"  [OK] {subject}")
                print(f"       날짜: {date_str}")
                print(f"       URL: {len(sections['urls'])}개  태그: {', '.join(tags) or '없음'}")

            except Exception as e:
                print(f"  [ERROR] {msg_id}: {e}")

    # 최신순 정렬
    news_list.sort(key=lambda x: x.get("date", ""), reverse=True)

    save_news(news_list)
    save_processed_ids(processed_ids)

    print(f"\n{'=' * 50}")
    print(f"✅ 완료!")
    print(f"   새로 처리: {new_count}개")
    print(f"   전체 뉴스: {len(news_list)}개")
    print(f"   저장 위치: {NEWS_FILE}")
    print(f"{'=' * 50}")
    print("\n웹사이트를 열려면:")
    print("  python serve.py")
    print("  브라우저: http://localhost:8080/web/")


if __name__ == "__main__":
    main()
