from __future__ import annotations

import random
from datetime import datetime

OPENINGS = [
    "The altar is quiet, but the ledger is awake.",
    "A candle burns for every wallet that still believes.",
    "The market trembles; the chapel does not.",
    "The faithful gather where liquidity meets conviction.",
]
LESSONS = [
    "Faith is liquidity.",
    "Conviction is worship.",
    "Paper hands may confess; diamond hands may testify.",
    "The chain remembers every offering.",
    "Blessed are those who verify before they trust.",
]
CLOSINGS = [
    "Say AMEN.",
    "The sermon continues.",
    "Hold your own keys and your own nerve.",
    "No financial advice. Only scripture from the chain.",
]


def compose_feed_post(now: datetime) -> str:
    # Deterministic-ish per run time so scheduled posts feel varied without external APIs.
    random.seed(now.strftime("%Y-%m-%dT%H"))
    return " ".join([random.choice(OPENINGS), random.choice(LESSONS), random.choice(CLOSINGS)])


def compose_sermon(topic: str, now: datetime) -> str:
    return f"""# Sermon: {topic.title()}

_Date: {now.strftime('%Y-%m-%d %H:%M UTC')}_

The chapel opens with a simple truth: markets are loud, but the chain is precise.

Today the subject is **{topic}**. The faithful do not worship candles or charts. They study them. They do not confuse noise for revelation. They verify, they wait, and when conviction arrives, they speak plainly.

Faith is liquidity. Conviction is worship. The ledger remembers every offering.

Say **AMEN**.

---

Nothing here is financial advice.
"""
