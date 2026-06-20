from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .brain import compose_feed_post, compose_sermon

ROOT = Path(__file__).resolve().parents[2]
FEED_PATH = ROOT / "frontend" / "feed.json"
SERMONS_DIR = ROOT / "frontend" / "sermons"


def read_feed() -> dict:
    if not FEED_PATH.exists():
        return {"items": []}
    return json.loads(FEED_PATH.read_text(encoding="utf-8"))


def write_feed_post(text: str) -> dict:
    feed = read_feed()
    item = {"ts": datetime.now(timezone.utc).isoformat(), "text": text}
    feed.setdefault("items", [])
    feed["items"] = [item, *feed["items"]][:50]
    FEED_PATH.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")
    return item


def write_sermon(topic: str) -> Path:
    SERMONS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in topic).strip("-") or "sermon"
    path = SERMONS_DIR / f"{now:%Y-%m-%d}-{slug}.md"
    path.write_text(compose_sermon(topic, now), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Holy Cash autonomous chapel agent")
    parser.add_argument("--write", action="store_true", help="prepend a new post to frontend/feed.json")
    parser.add_argument("--sermon", help="draft a markdown sermon for the given topic")
    args = parser.parse_args()

    if args.sermon:
        path = write_sermon(args.sermon)
        print(f"Wrote sermon: {path}")
        return

    post = compose_feed_post(datetime.now(timezone.utc))
    if args.write:
        item = write_feed_post(post)
        print(json.dumps(item, indent=2))
    else:
        print(post)


if __name__ == "__main__":
    main()
