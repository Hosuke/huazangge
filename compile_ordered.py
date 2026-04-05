#!/usr/bin/env python3
"""按优先级编译：论语 → 大学 → 中庸 → 孟子 → 五经 → 其他"""

import sys
import time
import re
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))

import frontmatter
from tools.config import load_config, ensure_dirs
from tools.llm import chat
from tools.compile import SYSTEM_PROMPT, _parse_compile_response, _write_article, _list_existing_concepts, rebuild_index

BASE = Path(".")
CFG = load_config(BASE)
ensure_dirs(CFG)
RAW_DIR = Path(CFG["paths"]["raw"])
CONCEPTS_DIR = Path(CFG["paths"]["concepts"])

# Priority order
PRIORITY = [
    ("论语", ["论语"]),
    ("大学", ["大学"]),
    ("中庸", ["中庸"]),
    ("孟子", ["孟子"]),
    ("诗经", ["诗经", "Legge-Vol4", "shijing"]),
    ("尚书", ["尚书", "Legge-Vol3", "shangshu", "Shoo_King"]),
    ("礼记", ["礼记", "Li_Ki"]),
    ("周易", ["周易", "I_Ching", "zhouyi"]),
    ("春秋", ["春秋", "Chunqiu"]),
]


def get_ordered_docs():
    """Get uncompiled docs sorted by priority."""
    all_docs = []
    for d in sorted(RAW_DIR.iterdir()):
        if not d.is_dir():
            continue
        idx = d / "index.md"
        if not idx.exists():
            continue
        post = frontmatter.load(str(idx))
        if post.metadata.get("compiled"):
            continue
        all_docs.append((d.name, idx, post))

    # Sort by priority
    ordered = []
    seen = set()

    for label, keywords in PRIORITY:
        for name, idx, post in all_docs:
            if name in seen:
                continue
            if any(k in name for k in keywords):
                ordered.append((label, name, idx, post))
                seen.add(name)

    # Add remaining
    for name, idx, post in all_docs:
        if name not in seen:
            ordered.append(("其他", name, idx, post))

    return ordered


def compile_doc(name, idx_path, post):
    """Compile a single document with trilingual output."""
    title = post.metadata.get("title", name)
    content = post.content

    if not content or len(content.strip()) < 20:
        post.metadata["compiled"] = True
        idx_path.write_text(frontmatter.dumps(post), encoding="utf-8")
        return 0

    existing = _list_existing_concepts(CONCEPTS_DIR)

    prompt = f"""I have a raw document titled "{title}" that needs to be compiled into wiki articles.

Source document:
---
{content[:15000]}
---

Existing concepts in the wiki (REUSE these slugs if the concept matches, do NOT create duplicates): {', '.join(existing[:40]) if existing else 'None yet'}

IMPORTANT: If a concept already exists above, use ===UPDATE=== with the existing slug instead of creating a new ===ARTICLE===.

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

Full article content in English with scholarly depth. Use [[Other Concept]] for cross-references.

## 中文

完整的中文文章内容。使用中文学术风格撰写。使用 [[Other Concept]] 进行交叉引用。

## 日本語

完全な日本語の記事内容。学術的な日本語で記述する。[[Other Concept]] でクロスリファレンスを使用する。
===END===

Focus on extracting knowledge with depth and precision. Each language section should be substantive."""

    try:
        response = chat(prompt, system=SYSTEM_PROMPT, max_tokens=CFG["llm"]["max_tokens"])
        articles = _parse_compile_response(response)
        for article in articles:
            _write_article(article, CONCEPTS_DIR)

        post.metadata["compiled"] = True
        post.metadata["compiled_at"] = datetime.now(timezone.utc).isoformat()
        idx_path.write_text(frontmatter.dumps(post), encoding="utf-8")
        return len(articles)
    except Exception as e:
        print(f"    Error: {str(e)[:60]}", flush=True)
        return 0


def main():
    docs = get_ordered_docs()
    print(f"华藏阁 — 有序编译 (按四书五经优先)")
    print(f"Total uncompiled: {len(docs)}")
    print(f"Articles before: {len(list(CONCEPTS_DIR.glob('*.md')))}")
    print(f"{'='*60}\n")

    # Show priority breakdown
    groups = {}
    for label, name, _, _ in docs:
        groups.setdefault(label, []).append(name)
    for label, names in groups.items():
        print(f"  {label}: {len(names)} docs")
    print()

    total_articles = 0
    for i, (label, name, idx, post) in enumerate(docs):
        print(f"[{i+1}/{len(docs)}] {label} | {name}", flush=True)
        n = compile_doc(name, idx, post)
        total_articles += n
        if n:
            print(f"    → {n} articles created", flush=True)
        time.sleep(1)

    rebuild_index(BASE)
    print(f"\n{'='*60}")
    print(f"✓ Done! {total_articles} total articles created")
    print(f"Articles after: {len(list(CONCEPTS_DIR.glob('*.md')))}")


if __name__ == "__main__":
    main()
