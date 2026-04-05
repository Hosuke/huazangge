#!/usr/bin/env python3
"""Batch ingest Confucian classics from ctext.org into the knowledge base."""

import time
import re
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
import frontmatter

RAW_DIR = Path("./raw")
BASE_URL = "https://ctext.org"

# Core Confucian texts to ingest
BOOKS = {
    # ─── 四书 ───
    "论语": {"index": "/analects/zh", "chapters": [
        ("学而", "/analects/xue-er/zh"), ("为政", "/analects/wei-zheng/zh"),
        ("八佾", "/analects/ba-yi/zh"), ("里仁", "/analects/li-ren/zh"),
        ("公冶长", "/analects/gong-ye-chang/zh"), ("雍也", "/analects/yong-ye/zh"),
        ("述而", "/analects/shu-er/zh"), ("泰伯", "/analects/tai-bo/zh"),
        ("子罕", "/analects/zi-han/zh"), ("乡党", "/analects/xiang-dang/zh"),
        ("先进", "/analects/xian-jin/zh"), ("颜渊", "/analects/yan-yuan/zh"),
        ("子路", "/analects/zi-lu/zh"), ("宪问", "/analects/xian-wen/zh"),
        ("卫灵公", "/analects/wei-ling-gong/zh"), ("季氏", "/analects/ji-shi/zh"),
        ("阳货", "/analects/yang-huo/zh"), ("微子", "/analects/wei-zi/zh"),
        ("子张", "/analects/zi-zhang/zh"), ("尧曰", "/analects/yao-yue/zh"),
    ]},
    "孟子": {"index": "/mengzi/zh"},
    # ─── 五经相关 ───
    "礼记": {"index": "/liji/zh"},
    "孝经": {"index": "/xiao-jing/zh"},
    # ─── 先秦儒家 ───
    "荀子": {"index": "/xunzi/zh"},
    # ─── 汉代儒家 ───
    "说苑": {"index": "/shuo-yuan/zh"},
    "春秋繁露": {"index": "/chun-qiu-fan-lu/zh"},
    "孔子家语": {"index": "/kongzi-jiayu/zh"},
    "论衡": {"index": "/lunheng/zh"},
}

HEADERS = {"User-Agent": "LLMBase/1.0 (research)"}


def fetch_page(url: str) -> str:
    """Fetch page and extract main text content."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # ctext.org puts text in <td class="ctext"> elements
    text_blocks = soup.select("td.ctext")
    if text_blocks:
        paragraphs = []
        for td in text_blocks:
            text = td.get_text(strip=True)
            if text:
                paragraphs.append(text)
        return "\n\n".join(paragraphs)

    # Fallback: get all text from main content area
    main = soup.find("div", id="content3") or soup.find("div", class_="container") or soup.body
    if main:
        return main.get_text(separator="\n\n", strip=True)
    return ""


def fetch_chapter_list(index_url: str) -> list[tuple[str, str]]:
    """Fetch chapter list from a book's index page."""
    resp = requests.get(index_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    chapters = []
    # ctext.org lists chapters as links in the content area
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


def save_raw(book_name: str, chapter_name: str, content: str, source_url: str):
    """Save content as a raw document."""
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


def ingest_book(book_name: str, book_info: dict):
    """Ingest all chapters of a book."""
    index_url = BASE_URL + book_info["index"]
    print(f"\n{'='*60}")
    print(f"📚 {book_name}")
    print(f"   Index: {index_url}")

    # Get chapter list
    if "chapters" in book_info:
        chapters = book_info["chapters"]
    else:
        print(f"   Fetching chapter list...")
        chapters = fetch_chapter_list(index_url)
        time.sleep(1)

    if not chapters:
        # If no chapters found, ingest the index page itself
        print(f"   No chapters found, ingesting index page...")
        content = fetch_page(index_url)
        if content:
            path = save_raw(book_name, "全文", content, index_url)
            print(f"   ✓ Saved: {path}")
        return

    print(f"   Found {len(chapters)} chapters")

    for i, (ch_name, ch_path) in enumerate(chapters):
        ch_url = BASE_URL + ch_path
        try:
            content = fetch_page(ch_url)
            if content and len(content) > 10:
                path = save_raw(book_name, ch_name, content, ch_url)
                print(f"   [{i+1}/{len(chapters)}] ✓ {ch_name} ({len(content)} chars)")
            else:
                print(f"   [{i+1}/{len(chapters)}] ⚠ {ch_name} (empty)")
        except Exception as e:
            print(f"   [{i+1}/{len(chapters)}] ✗ {ch_name}: {e}")

        # Be respectful to the server
        time.sleep(1.5)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print("LLMBase — Confucian Classics Ingestion")
    print(f"Target: {len(BOOKS)} books from ctext.org")

    for book_name, book_info in BOOKS.items():
        ingest_book(book_name, book_info)

    # Count results
    total = len(list(RAW_DIR.glob("*/index.md")))
    print(f"\n{'='*60}")
    print(f"✓ Done! {total} documents ingested into raw/")
    print(f"  Next: run 'llmbase compile new' to build the wiki")


if __name__ == "__main__":
    main()
