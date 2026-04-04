#!/usr/bin/env python3
"""Sync wiki from live server before deploying.

Pulls articles that the server learned autonomously (via worker),
merges with local wiki, then you can git push safely.

Usage:
    python sync_wiki.py                              # sync from default URL
    python sync_wiki.py https://your-app.railway.app # sync from custom URL
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

import requests
import frontmatter

WIKI_DIR = Path("wiki/concepts")
META_DIR = Path("wiki/_meta")
DEFAULT_URL = "https://huazangge-production.up.railway.app"


def sync(server_url: str):
    print(f"Syncing wiki from {server_url}...")

    resp = requests.get(f"{server_url}/api/wiki/export", timeout=30)
    resp.raise_for_status()
    data = resp.json()
    remote_articles = data.get("articles", {})

    WIKI_DIR.mkdir(parents=True, exist_ok=True)

    new_count = 0
    merged_count = 0
    skipped = 0

    for slug, remote in remote_articles.items():
        local_path = WIKI_DIR / f"{slug}.md"

        if not local_path.exists():
            # New article from server — save it
            post = frontmatter.Post(remote["content"])
            post.metadata = remote["metadata"]
            local_path.write_text(frontmatter.dumps(post), encoding="utf-8")
            print(f"  + {slug} (new from server)")
            new_count += 1
        else:
            # Exists locally — merge if server has newer/more content
            local_post = frontmatter.load(str(local_path))
            remote_content = remote["content"]
            local_content = local_post.content

            if len(remote_content) > len(local_content) * 1.1:
                # Server version is significantly larger — take it
                post = frontmatter.Post(remote_content)
                post.metadata = remote["metadata"]
                local_path.write_text(frontmatter.dumps(post), encoding="utf-8")
                print(f"  ↑ {slug} (server has more content)")
                merged_count += 1
            else:
                skipped += 1

    print(f"\nDone! New: {new_count}, Updated: {merged_count}, Unchanged: {skipped}")
    print(f"Local wiki now has {len(list(WIKI_DIR.glob('*.md')))} articles")
    print(f"\nNext: git add wiki/ && git commit && git push")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    sync(url)
