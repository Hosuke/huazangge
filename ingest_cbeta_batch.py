#!/usr/bin/env python3
"""华藏阁 — 12-hour CBETA batch ingestion.

Progressively ingests sutras from the 大正藏 (T) and 卍续藏 (X),
running in batches with polite delays. Safe to interrupt and resume.

Usage:
    python ingest_cbeta_batch.py              # Default: batch of 20, loop until done
    python ingest_cbeta_batch.py --hours 12   # Run for up to 12 hours
    python ingest_cbeta_batch.py --batch 50   # Larger batches
"""

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure we can import from tools/
import sys
sys.path.insert(0, str(Path(__file__).parent))

from tools.cbeta import learn, status, list_categories, CATEGORIES


def main():
    parser = argparse.ArgumentParser(description="华藏阁 CBETA batch ingestion")
    parser.add_argument("--hours", type=float, default=12, help="Max hours to run")
    parser.add_argument("--batch", type=int, default=20, help="Sutras per batch")
    parser.add_argument("--category", type=str, default=None, help="Specific category")
    args = parser.parse_args()

    start = time.time()
    max_seconds = args.hours * 3600
    total_new = 0
    round_num = 0

    # If no category specified, cycle through all
    categories = [args.category] if args.category else list(CATEGORIES.keys())

    print(f"{'='*60}")
    print(f"华藏阁 — CBETA 渐进式学习")
    print(f"{'='*60}")
    print(f"  Max runtime: {args.hours} hours")
    print(f"  Batch size:  {args.batch}")
    print(f"  Categories:  {', '.join(categories)}")
    s = status()
    print(f"  Already ingested: {s['total_ingested']} sutras")
    print(f"  Started at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")

    cat_idx = 0

    while True:
        elapsed = time.time() - start
        if elapsed > max_seconds:
            print(f"\n⏰ Time limit reached ({args.hours}h)")
            break

        cat = categories[cat_idx % len(categories)]
        cat_name = CATEGORIES.get(cat, (None, cat))[1]
        round_num += 1

        hours_left = (max_seconds - elapsed) / 3600
        print(f"\n[Round {round_num}] {cat_name} | batch={args.batch} | {hours_left:.1f}h remaining")

        try:
            results = learn(category=cat, batch_size=args.batch)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            cat_idx += 1
            time.sleep(5)
            continue

        if results:
            total_new += len(results)
            print(f"  ✓ Ingested {len(results)} sutras: {', '.join(results[:5])}{'...' if len(results)>5 else ''}")
            print(f"  📊 Session total: {total_new} new | Overall: {status()['total_ingested']}")
        else:
            print(f"  ⏭ Category {cat_name} complete, moving to next")
            cat_idx += 1
            if cat_idx >= len(categories):
                print(f"\n🎉 All categories processed!")
                break

        # Brief pause between batches
        time.sleep(2)

    elapsed = time.time() - start
    s = status()
    print(f"\n{'='*60}")
    print(f"✓ 华藏阁 ingestion complete")
    print(f"  Runtime: {elapsed/3600:.1f} hours")
    print(f"  New sutras this session: {total_new}")
    print(f"  Total in knowledge base: {s['total_ingested']}")
    print(f"{'='*60}")
    print(f"\nNext step: llmbase compile new")


if __name__ == "__main__":
    main()
