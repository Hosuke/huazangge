#!/usr/bin/env python3
"""并发编译 — 10 workers 优先四书五经"""

import sys
import time
import threading
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tools.config import load_config, ensure_dirs
from tools.llm import chat
from tools.compile import compile_new, _find_uncompiled, SYSTEM_PROMPT, _parse_compile_response, _write_article, rebuild_index

import frontmatter

BASE = Path(".")
CFG = load_config(BASE)
ensure_dirs(CFG)
RAW_DIR = Path(CFG["paths"]["raw"])
CONCEPTS_DIR = Path(CFG["paths"]["concepts"])

lock = threading.Lock()
total_compiled = 0


def get_next_uncompiled():
    """Get next uncompiled doc, prioritizing 四书."""
    with lock:
        for d in sorted(RAW_DIR.iterdir()):
            if not d.is_dir():
                continue
            idx = d / "index.md"
            if not idx.exists():
                continue
            post = frontmatter.load(str(idx))
            if post.metadata.get("compiled"):
                continue
            # Prioritize 四书
            name = d.name
            is_sishu = any(k in name for k in ["论语", "孟子", "大学", "中庸", "Legge-Vol1", "Legge-Vol2"])
            return (idx, post, is_sishu)
    return None


def compile_one(worker_id: int):
    """Compile a single document."""
    global total_compiled

    result = get_next_uncompiled()
    if not result:
        return False

    idx_path, post, is_sishu = result
    title = post.metadata.get("title", idx_path.parent.name)
    content = post.content

    if not content.strip() or len(content) < 20:
        # Mark empty docs as compiled to skip
        with lock:
            post.metadata["compiled"] = True
            idx_path.write_text(frontmatter.dumps(post), encoding="utf-8")
        return True

    existing = [f.stem for f in CONCEPTS_DIR.glob("*.md")]

    prompt = f"""I have a raw document titled "{title}" that needs to be compiled into wiki articles.

Source document:
---
{content[:15000]}
---

Existing concepts in the wiki: {', '.join(existing[:30]) if existing else 'None yet'}

Please:
1. Identify the key concepts from this document (1-5 concepts)
2. For each concept, produce a TRILINGUAL wiki article in this exact format:

===ARTICLE===
slug: concept-name-here
title: English Title / 中文标题
summary: One-line summary in English
tags: tag1, tag2, tag3
---
## English

Full article content in English. Use [[Other Concept]] for cross-references.

## 中文

完整的中文文章内容。使用中文学术风格撰写，不是简单翻译。使用 [[Other Concept]] 进行交叉引用。

## 日本語

完全な日本語の記事内容。学術的な日本語で記述する。[[Other Concept]] でクロスリファレンスを使用する。
===END===

Focus on extracting knowledge, not just summarizing. Each language section should be substantive, not a mere translation."""

    try:
        response = chat(prompt, system=SYSTEM_PROMPT, max_tokens=CFG["llm"]["max_tokens"])
        articles = _parse_compile_response(response)

        with lock:
            for article in articles:
                _write_article(article, CONCEPTS_DIR)

            post.metadata["compiled"] = True
            from datetime import datetime, timezone
            post.metadata["compiled_at"] = datetime.now(timezone.utc).isoformat()
            idx_path.write_text(frontmatter.dumps(post), encoding="utf-8")
            total_compiled += 1

        tag = "四书" if is_sishu else "other"
        print(f"[W{worker_id}] ✓ {title[:30]} ({len(articles)} articles) [{tag}]", flush=True)
        return True

    except Exception as e:
        print(f"[W{worker_id}] ✗ {title[:30]}: {str(e)[:50]}", flush=True)
        # Mark as compiled to avoid infinite retry on bad docs
        with lock:
            post.metadata["compiled"] = True
            idx_path.write_text(frontmatter.dumps(post), encoding="utf-8")
        return True


def worker(worker_id: int):
    """Worker thread."""
    while True:
        if not compile_one(worker_id):
            break
        time.sleep(0.5)
    print(f"[W{worker_id}] Finished", flush=True)


def main():
    global total_compiled
    num_workers = 10
    print(f"华藏阁 — 并发编译 ({num_workers} workers)")
    print(f"Articles before: {len(list(CONCEPTS_DIR.glob('*.md')))}")

    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Stagger starts

    for t in threads:
        t.join()

    rebuild_index(BASE)
    print(f"\n✓ Done! Compiled {total_compiled} documents")
    print(f"Articles after: {len(list(CONCEPTS_DIR.glob('*.md')))}")


if __name__ == "__main__":
    main()
