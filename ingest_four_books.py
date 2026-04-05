#!/usr/bin/env python3
"""华藏阁 — 用 Playwright 浏览器抓取四书全文 (ctext.org)

使用真实浏览器绕过反爬限制，抓取：
- 论语 (已有，跳过)
- 孟子 (补全剩余篇章)
- 大学
- 中庸
"""

import re
import time
import random
from pathlib import Path
from datetime import datetime, timezone

import frontmatter
from playwright.sync_api import sync_playwright

RAW_DIR = Path("./raw")
BASE_URL = "https://ctext.org"


def fetch_chapter_list(page, index_url: str) -> list[tuple[str, str]]:
    """Navigate to index page and extract chapter links."""
    page.goto(index_url, timeout=15000, wait_until="domcontentloaded")
    time.sleep(1)

    chapters = page.eval_on_selector_all(
        "#content3 a, #content2 a",
        """els => els
            .map(a => ({title: a.textContent.trim(), href: a.getAttribute('href')}))
            .filter(a => a.href && a.href.endsWith('/zh') && !a.href.startsWith('http'))
        """
    )
    return [(c["title"], c["href"] if c["href"].startswith("/") else "/" + c["href"]) for c in chapters]


def fetch_chapter_text(page, chapter_url: str) -> str:
    """Navigate to chapter page and extract classical text."""
    page.goto(chapter_url, timeout=15000, wait_until="domcontentloaded")
    time.sleep(1)

    texts = page.eval_on_selector_all(
        "td.ctext",
        "els => els.map(e => e.textContent.trim()).filter(t => t)"
    )
    return "\n\n".join(texts)


def already_ingested(book_name: str, chapter_name: str) -> bool:
    slug = re.sub(r"[^\w]+", "-", f"{book_name}-{chapter_name}").strip("-")
    return (RAW_DIR / slug / "index.md").exists()


def save_chapter(book_name: str, chapter_name: str, content: str, source_url: str):
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

    (doc_dir / "index.md").write_text(frontmatter.dumps(post), encoding="utf-8")


FOUR_BOOKS = [
    ("论语", "/analects/zh"),
    ("孟子", "/mengzi/zh"),
    ("大学", "/daxue/zh"),
    ("中庸", "/zhongyong/zh"),
]


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    total_new = 0
    total_skip = 0

    print("="*60)
    print("华藏阁 — 四书全文抓取 (Playwright 浏览器模式)")
    print("="*60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        for book_name, book_path in FOUR_BOOKS:
            print(f"\n📚 {book_name}")
            index_url = BASE_URL + book_path

            try:
                chapters = fetch_chapter_list(page, index_url)
            except Exception as e:
                print(f"   ✗ Failed to get chapters: {e}")
                continue

            time.sleep(1 + random.random())

            if not chapters:
                # Single-page text (大学, 中庸)
                if already_ingested(book_name, "全文"):
                    print(f"   ⏭ Already ingested")
                    total_skip += 1
                    continue
                try:
                    text = fetch_chapter_text(page, index_url)
                    if text and len(text) > 10:
                        save_chapter(book_name, "全文", text, index_url)
                        print(f"   ✓ Saved full text ({len(text)} chars)")
                        total_new += 1
                    else:
                        print(f"   ⚠ Empty content")
                except Exception as e:
                    print(f"   ✗ Failed: {e}")
                time.sleep(2 + random.random())
                continue

            print(f"   {len(chapters)} chapters")

            for i, (ch_name, ch_path) in enumerate(chapters):
                if already_ingested(book_name, ch_name):
                    print(f"   [{i+1}/{len(chapters)}] ⏭ {ch_name}")
                    total_skip += 1
                    continue

                ch_url = BASE_URL + ch_path
                try:
                    text = fetch_chapter_text(page, ch_url)
                    if text and len(text) > 10:
                        save_chapter(book_name, ch_name, text, ch_url)
                        print(f"   [{i+1}/{len(chapters)}] ✓ {ch_name} ({len(text)} chars)")
                        total_new += 1
                    else:
                        print(f"   [{i+1}/{len(chapters)}] ⚠ {ch_name} (empty)")
                except Exception as e:
                    print(f"   [{i+1}/{len(chapters)}] ✗ {ch_name}: {e}")

                time.sleep(2 + random.random() * 2)

        browser.close()

    total = len(list(RAW_DIR.glob("*/index.md")))
    print(f"\n{'='*60}")
    print(f"✓ Done! New: {total_new} | Skipped: {total_skip}")
    print(f"  Total documents in raw/: {total}")
    print(f"\nNext: llmbase compile new")


if __name__ == "__main__":
    main()
