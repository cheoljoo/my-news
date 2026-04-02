#!/usr/bin/env python3
"""
프로젝트 루트에서 HTTP 서버를 실행합니다.
0.0.0.0 바인딩으로 LAN/외부 접속 모두 허용합니다.

nginx와 동일한 URL 구조로 서빙합니다:
  /news/         → web/index.html
  /news/data/    → data/

사용법:
  python3 serve.py              # 포트 8080 (기본)
  python3 serve.py 9090         # 포트 지정
  python3 serve.py --no-browser # 브라우저 자동 실행 안 함 (tmux/서버 환경)
"""

import http.server
import os
import socket
import socketserver
import sys
import threading
import time
import webbrowser
from pathlib import Path

PORT = 8080
BASE_DIR = Path(__file__).parent.resolve()


def get_local_ips() -> list[str]:
    ips = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if ip not in ips and not ip.startswith("127."):
            ips.append(ip)
    except Exception:
        pass
    return ips


class NewsHandler(http.server.SimpleHTTPRequestHandler):
    """
    URL 재작성 핸들러:
      /           → 302 /news/
      /news/*     → web/*
      /news/data/ → data/
    """

    def translate_path(self, path: str) -> str:
        # 쿼리스트링 제거
        path = path.split("?", 1)[0].split("#", 1)[0]

        if path == "/" or path == "":
            return str(BASE_DIR / "web" / "index.html")
        if path.startswith("/news/data/"):
            rel = path[len("/news/data/"):]
            return str(BASE_DIR / "data" / rel)
        if path.startswith("/news/"):
            rel = path[len("/news/"):]
            return str(BASE_DIR / "web" / rel)
        if path == "/news":
            return str(BASE_DIR / "web" / "index.html")
        # 그 외는 프로젝트 루트 기준
        return str(BASE_DIR / path.lstrip("/"))

    def send_response_only(self, code, message=None):
        super().send_response_only(code, message)

    def do_GET(self):
        # 루트 → /news/ 리다이렉트
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/news/")
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith(("GET /news", "GET /data")):
            client = self.address_string()
            sys.stdout.write(f"  [{client}] {args[0]}\n")
            sys.stdout.flush()


def main():
    args = sys.argv[1:]
    no_browser = "--no-browser" in args
    port_args = [a for a in args if a.isdigit()]
    port = int(port_args[0]) if port_args else PORT

    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("0.0.0.0", port), NewsHandler) as httpd:
        local_ips = get_local_ips()

        print("=" * 55)
        print("🎮  NEWS ARCADE SERVER")
        print("=" * 55)
        print(f"  로컬:     http://localhost:{port}/news/")
        for ip in local_ips:
            print(f"  LAN:      http://{ip}:{port}/news/")
        print()
        print("  외부 접속 (nginx 80포트 — 포트포워딩 불필요):")
        print("  → http://psncs.iptime.org/news/")
        print()
        print("  tmux 터미널 뷰어:  python3 view_news.py")
        print("  종료: Ctrl+C")
        print("=" * 55)

        if not no_browser:
            def _open():
                time.sleep(0.6)
                webbrowser.open(f"http://localhost:{port}/news/")
            threading.Thread(target=_open, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")


if __name__ == "__main__":
    main()
