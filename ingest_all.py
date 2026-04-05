#!/usr/bin/env python3
"""Robust batch ingestion from ctext.org with anti-blocking measures."""

import random
import time
import re
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
import frontmatter

RAW_DIR = Path("./raw")
BASE_URL = "https://ctext.org"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
})

# All Confucian books to ingest
BOOKS = [
    # 四书
    ("孟子", "/mengzi/zh"),
    # 五经相关
    ("礼记", "/liji/zh"),
    ("孝经", "/xiao-jing/zh"),
    # 先秦
    ("荀子", "/xunzi/zh"),
    # 汉代
    ("说苑", "/shuo-yuan/zh"),
    ("春秋繁露", "/chun-qiu-fan-lu/zh"),
    ("韩诗外传", "/han-shi-wai-zhuan/zh"),
    ("大戴礼记", "/da-dai-li-ji/zh"),
    ("白虎通德论", "/bai-hu-tong/zh"),
    ("新书", "/xin-shu/zh"),
    ("新序", "/xin-xu/zh"),
    ("孔子家语", "/kongzi-jiayu/zh"),
    ("潜夫论", "/qian-fu-lun/zh"),
    ("论衡", "/lunheng/zh"),
    ("孔丛子", "/kongcongzi/zh"),
    ("新语", "/xinyu/zh"),
]


def polite_delay():
    """Random delay between 3-6 seconds to be respectful."""
    time.sleep(3 + random.random() * 3)


def fetch_with_retry(url: str, max_retries: int = 3) -> str:
    """Fetch URL with retry and exponential backoff."""
    for attempt in range(max_retries):
        try:
            resp = SESSION.get(url, timeout=30)
            if resp.status_code == 403:
                wait = 30 * (attempt + 1) + random.random() * 10
                print(f"      ⏳ 403 Forbidden, waiting {wait:.0f}s before retry...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.text
        except requests.exceptions.HTTPError as e:
            if "403" in str(e) and attempt < max_retries - 1:
                wait = 30 * (attempt + 1) + random.random() * 10
                print(f"      ⏳ Blocked, waiting {wait:.0f}s...")
                time.sleep(wait)
                continue
            raise
    raise requests.exceptions.HTTPError(f"Failed after {max_retries} retries: {url}")


def extract_text(html: str) -> str:
    """Extract classical text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("td.ctext")
    if blocks:
        parts = [td.get_text(strip=True) for td in blocks if td.get_text(strip=True)]
        return "\n\n".join(parts)
    main = soup.find("div", id="content3") or soup.body
    return main.get_text(separator="\n\n", strip=True) if main else ""


def get_chapters(index_url: str) -> list[tuple[str, str]]:
    """Get chapter list from index page."""
    html = fetch_with_retry(index_url)
    soup = BeautifulSoup(html, "html.parser")
    chapters = []
    content = soup.find("div", id="content3") or soup.find("div", id="content2") or soup.body
    if not content:
        return chapters
    for a in content.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)
        if title and href.endswith("/zh") and not href.startswith("http"):
            if not href.startswith("/"):
                href = "/" + href
            chapters.append((title, href))
    return chapters


def already_ingested(book_name: str, chapter_name: str) -> bool:
    """Check if this chapter was already ingested."""
    slug = re.sub(r"[^\w]+", "-", f"{book_name}-{chapter_name}").strip("-")
    return (RAW_DIR / slug / "index.md").exists()


def save_chapter(book_name: str, chapter_name: str, content: str, source_url: str) -> Path:
    """Save chapter to raw/."""
    slug = re.sub(r"[^\w]+", "-", f"{book_name}-{chapter_name}").strip("-")
    doc_dir = RAW_DIR / slug
    doc_dir.mkdir(parents=True, exist_ok=True)

    post = frontmatter.Post(content)
    post.metadata["title"] = f"{book_name} · {chapter_name}"
    post.metadata["source"] = source_url
    post.metadata["ingested_at"] = datetime.now(timezone.utc).isoformat()
    post.metadata["type"] = "classical_text"
    post.metadata["book"] = book_name
    post.metadata["chapter"] = chapter_name
    post.metadata["compiled"] = False

    doc_path = doc_dir / "index.md"
    doc_path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return doc_path


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    total_new = 0
    total_skip = 0
    total_fail = 0

    for book_name, book_path in BOOKS:
        print(f"\n{'='*60}")
        print(f"📚 {book_name}")

        index_url = BASE_URL + book_path
        try:
            chapters = get_chapters(index_url)
        except Exception as e:
            print(f"   ✗ Failed to get chapter list: {e}")
            polite_delay()
            continue

        polite_delay()

        if not chapters:
            # Single-page text
            if already_ingested(book_name, "全文"):
                print(f"   ⏭ Already ingested")
                total_skip += 1
                continue
            try:
                html = fetch_with_retry(index_url)
                content = extract_text(html)
                if content and len(content) > 10:
                    save_chapter(book_name, "全文", content, index_url)
                    print(f"   ✓ Saved (full text, {len(content)} chars)")
                    total_new += 1
            except Exception as e:
                print(f"   ✗ Failed: {e}")
                total_fail += 1
            polite_delay()
            continue

        print(f"   {len(chapters)} chapters")

        for i, (ch_name, ch_path) in enumerate(chapters):
            if already_ingested(book_name, ch_name):
                print(f"   [{i+1}/{len(chapters)}] ⏭ {ch_name} (exists)")
                total_skip += 1
                continue

            ch_url = BASE_URL + ch_path
            try:
                html = fetch_with_retry(ch_url)
                content = extract_text(html)
                if content and len(content) > 10:
                    save_chapter(book_name, ch_name, content, ch_url)
                    print(f"   [{i+1}/{len(chapters)}] ✓ {ch_name} ({len(content)} chars)")
                    total_new += 1
                else:
                    print(f"   [{i+1}/{len(chapters)}] ⚠ {ch_name} (empty)")
            except Exception as e:
                print(f"   [{i+1}/{len(chapters)}] ✗ {ch_name}: {e}")
                total_fail += 1

            polite_delay()

    total_docs = len(list(RAW_DIR.glob("*/index.md")))
    print(f"\n{'='*60}")
    print(f"✓ Done!")
    print(f"  New: {total_new} | Skipped: {total_skip} | Failed: {total_fail}")
    print(f"  Total documents in raw/: {total_docs}")


if __name__ == "__main__":
    main()
