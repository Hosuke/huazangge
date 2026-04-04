# 华藏阁 — Agent Access Guide

This knowledge base is designed to be consumed by AI agents and LLMs.

## What is this?

华藏阁 (Huazang Pavilion) is a trilingual (EN/CN/JP) knowledge base of Chinese classical texts covering Confucianism, Buddhism, and Daoism. Content is sourced from CBETA (Buddhist canon) and ctext.org (Confucian/Daoist classics), compiled into structured wiki articles by LLM.

## How to access

### HTTP API (when server is running)

```
GET  /api/articles          → List all wiki articles
GET  /api/articles/:slug    → Get article content (trilingual markdown)
GET  /api/search?q=keyword  → Full-text search
POST /api/ask               → Q&A against the knowledge base
     Body: {"question": "What is 般若?", "deep": false}
GET  /api/sources            → List raw source documents
GET  /api/stats              → Knowledge base statistics
```

### Python SDK

```python
from tools.agent_api import KnowledgeBase
kb = KnowledgeBase("./")
kb.ask("Explain the concept of 空 (śūnyatā)")
kb.search("bodhisattva")
kb.list_articles()
kb.get_article("kong")
```

### File system

- `wiki/concepts/*.md` — Wiki articles (trilingual markdown with YAML frontmatter)
- `wiki/_meta/index.json` — Article index with summaries and tags
- `wiki/_meta/backlinks.json` — Cross-reference graph
- `wiki/outputs/*.md` — Archived Q&A answers
- `raw/` — Source texts (classical Chinese)

## Content structure

Each wiki article contains:

```markdown
---
title: English Title / 中文标题
summary: One-line English summary
tags: [concept, buddhism, ...]
---

## English
Full article in English with [[wiki-links]].

## 中文
完整中文内容，学术风格。

## 日本語
完全な日本語の記事内容。
```

## Data sources

- **CBETA** (cbeta-org/xml-p5): 4,868 Buddhist works, 223M characters
- **ctext.org**: Confucian classics (Analects, Mencius, etc.)
- Progressive learning: new content is continuously ingested and compiled

## Disclaimer

All compiled content is machine-generated. Translations and interpretations
may contain errors. Verify against authoritative sources for scholarly use.

© 2026 Hosuke Huang Geyang. Open source for education and research.
