# MiniMax Handoff: Holy Cash `$AMEN` X Autoposting

**Project:** Holy Cash / `$AMEN`  
**Repo:** https://github.com/iamchrisso/holy-cash  
**Public site:** https://iamchrisso.github.io/holy-cash/  
**Local path:** `/Users/Christopher/holy-cash`  
**Current status:** Starter site + local feed agent deployed. GitHub Pages deploy succeeded.

---

## Goal

Add safe autonomous posting to X for Holy Cash so the agent can publish short in-character posts on a schedule, while continuing to update the website feed.

The desired end state:

1. GitHub Actions runs on a schedule.
2. The Holy Cash backend generates a short `$AMEN` post.
3. The post is written to `frontend/feed.json`.
4. The same post, or a shortened version, is posted to X.
5. The run commits feed changes back to `main`.
6. The website redeploys via GitHub Pages.

---

## What exists now

### Important files

```txt
frontend/index.html                         # Static Holy Cash site
frontend/feed.json                          # Live feed data loaded by site JS
frontend/assets/css/styles.css              # Site styling
frontend/assets/js/app.js                   # Feed loader + copy buttons
backend/run.py                              # CLI entrypoint
backend/holycash/agent.py                   # Feed/sermon writer
backend/holycash/brain.py                   # In-character post generator
.github/workflows/deploy-pages.yml          # GitHub Pages deployment
.github/workflows/holy-cash-agent.yml       # Scheduled feed generator
README.md                                   # Project overview
```

### Current commands

From repo root:

```bash
# Generate one post to stdout
python3 backend/run.py

# Prepend one post to frontend/feed.json
python3 backend/run.py --write

# Draft a sermon markdown file
python3 backend/run.py --sermon "faith and liquidity"
```

### Current deploy

- GitHub Pages is enabled.
- Public site is live at: https://iamchrisso.github.io/holy-cash/
- Workflow `Deploy Holy Cash Pages` has completed successfully at least once.

---

## What is needed for autonomous X posting

### 1. X developer access

Need an X developer account/app with write permissions.

Minimum required access:

- Ability to call `POST /2/tweets`
- OAuth credentials that allow posting as the Holy Cash X account

Likely required secrets:

```txt
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
```

Depending on library/auth flow, OAuth 2.0 may instead use:

```txt
X_BEARER_TOKEN
X_CLIENT_ID
X_CLIENT_SECRET
X_REFRESH_TOKEN
```

For simple autonomous posting, OAuth 1.0a user context with API key/secret and access token/secret is usually the most straightforward.

### 2. Holy Cash X account

Need the actual account to post from, for example:

```txt
https://x.com/HolyCash
```

or whatever handle the user chooses.

Update these placeholders in `frontend/index.html` and README once known:

- X link
- Telegram link
- DEXScreener link
- Pump.fun link
- contract address
- treasury/wallet address

### 3. GitHub repository secrets

Add X credentials to GitHub repo secrets:

Repo settings path:

```txt
GitHub repo → Settings → Secrets and variables → Actions → New repository secret
```

Required initial secrets if using OAuth 1.0a:

```txt
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
```

Do **not** commit credentials to the repo.

### 4. Python X client

Add a backend module, probably:

```txt
backend/holycash/x_client.py
```

Recommended implementation options:

#### Option A: use `tweepy`

Pros: fast and simple.  
Cons: dependency abstraction can hide exact HTTP errors.

Add to `backend/requirements.txt`:

```txt
tweepy>=4.14.0
```

Example module shape:

```python
from __future__ import annotations

import os
import tweepy


def get_client() -> tweepy.Client:
    required = [
        "X_API_KEY",
        "X_API_SECRET",
        "X_ACCESS_TOKEN",
        "X_ACCESS_TOKEN_SECRET",
    ]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing X credentials: {', '.join(missing)}")

    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def post_tweet(text: str) -> str:
    client = get_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    return str(tweet_id)
```

#### Option B: direct HTTP signing

Pros: fewer dependencies and full control.  
Cons: more code and more auth pitfalls. Use only if `tweepy` causes issues.

### 5. CLI flags

Modify `backend/holycash/agent.py` to support:

```bash
python backend/run.py --write --post-x
python backend/run.py --post-x-only
python backend/run.py --dry-run-x
```

Recommended behavior:

- `--write`: write generated post to website feed.
- `--post-x`: post generated text to X after validation.
- `--dry-run-x`: print what would be posted, but do not call X.
- `--post-x-only`: useful for testing, but should still use duplicate protection.

### 6. Safety rules before posting

Add a validation function before posting to X:

```txt
backend/holycash/safety.py
```

Minimum checks:

- Max length: 260 chars to leave room for links/manual edits.
- No direct financial advice claims.
- No guaranteed returns.
- No impersonation.
- No slurs / obvious unsafe terms.
- No duplicate post within recent history.
- Must include either `AMEN`, `$AMEN`, `Holy Cash`, or an on-brand phrase.

Suggested blocked phrases:

```txt
guaranteed profit
risk-free
100x guaranteed
financial advice
send me your seed phrase
private key
```

Suggested disclaimer style when needed:

```txt
No financial advice. Say AMEN.
```

Do not append the disclaimer to every tweet if it ruins the voice, but never allow investment guarantees.

### 7. Duplicate protection

Currently `compose_feed_post()` is deterministic by hour. That is okay for the feed, but dangerous for X if a workflow retries in the same hour.

Before X posting, check recent feed items and/or create a posted log.

Recommended file:

```txt
backend/state/x_posts.json
```

But because GitHub Actions is stateless unless committed, simplest option is to store X post metadata in the website feed entry:

```json
{
  "ts": "...",
  "text": "...",
  "x_tweet_id": "1234567890"
}
```

Implementation rule:

- If the exact text exists in the last 20 feed items with `x_tweet_id`, do not post it again.
- If posting succeeds, add `x_tweet_id` to the newest feed entry before committing.

### 8. GitHub Action update

Modify `.github/workflows/holy-cash-agent.yml` to include X secrets and post flag.

Example:

```yaml
      - name: Generate feed post and post to X
        env:
          X_API_KEY: ${{ secrets.X_API_KEY }}
          X_API_SECRET: ${{ secrets.X_API_SECRET }}
          X_ACCESS_TOKEN: ${{ secrets.X_ACCESS_TOKEN }}
          X_ACCESS_TOKEN_SECRET: ${{ secrets.X_ACCESS_TOKEN_SECRET }}
        run: python backend/run.py --write --post-x
```

Schedule recommendation at first:

```yaml
schedule:
  - cron: "17 */6 * * *"
```

That means one post every 6 hours. Start slow. Increase later only after confirming X account safety and rate limits.

---

## Recommended implementation plan

### Phase 1 — Local safe client

1. Add `tweepy` to `backend/requirements.txt`.
2. Add `backend/holycash/x_client.py`.
3. Add `backend/holycash/safety.py`.
4. Add CLI flags in `backend/holycash/agent.py`.
5. Test `--dry-run-x` locally without credentials.
6. Test missing credentials error is clear.

Verification:

```bash
python3 backend/run.py --dry-run-x
python3 backend/run.py --write --dry-run-x
```

Expected:

- No X API call.
- Generated text printed.
- Feed write succeeds when `--write` is present.

### Phase 2 — Real X test

Only after GitHub secrets are configured or local env vars are available:

```bash
X_API_KEY=... \
X_API_SECRET=... \
X_ACCESS_TOKEN=... \
X_ACCESS_TOKEN_SECRET=... \
python3 backend/run.py --post-x
```

Expected:

- One tweet is posted.
- Tweet ID is printed.
- No duplicate if retried.

### Phase 3 — Workflow integration

1. Update `.github/workflows/holy-cash-agent.yml` to pass secrets.
2. Use `workflow_dispatch` first, not schedule.
3. Confirm the Action posts exactly once.
4. Confirm feed entry has `x_tweet_id`.
5. Confirm GitHub Pages redeploys.
6. Leave schedule at every 6 hours.

### Phase 4 — Better content

Once posting works, improve `brain.py` so posts can react to:

- `$AMEN` DEXScreener price/liquidity
- SOL market movement
- wallet balance / recent transfers
- holder milestones
- site updates / new sermons

Add modules later:

```txt
backend/holycash/market.py
backend/holycash/wallet.py
backend/holycash/research.py
```

Keep the first X integration simple. Do not add market dependencies until posting is reliable.

---

## Voice guidelines

Holy Cash should sound like:

- cyber chapel
- memecoin preacher
- chain-aware oracle
- funny but not sloppy
- mystical, not scammy

Good examples:

```txt
The altar is quiet, but the ledger is awake. Faith is liquidity. Say AMEN.
```

```txt
A candle burns for every wallet that still believes. The chain remembers every offering. $AMEN
```

```txt
The faithful do not chase every candle. They verify, they wait, and when conviction speaks, they answer: AMEN.
```

Avoid:

```txt
Guaranteed 100x
Buy now before it pumps
Risk-free gains
Send funds to this wallet
This is financial advice
```

---

## Current known placeholders to replace

In `frontend/index.html`:

```txt
PASTE_CONTRACT_ADDRESS_HERE
PASTE_TREASURY_WALLET_HERE
https://dexscreener.com/
https://pump.fun/
https://x.com/
https://t.me/
```

In `README.md`:

```txt
https://example.com
https://x.com/
```

---

## Commands for MiniMax to start

```bash
cd /Users/Christopher/holy-cash
git status
git pull --ff-only
python3 backend/run.py
python3 backend/run.py --write
python3 -m json.tool frontend/feed.json >/dev/null
```

If editing:

```bash
git checkout -b feat/x-autoposting
# implement changes
git diff
python3 backend/run.py --dry-run-x
python3 backend/run.py --write --dry-run-x
python3 -m json.tool frontend/feed.json >/dev/null
git add backend/holycash backend/requirements.txt .github/workflows/holy-cash-agent.yml docs/minimax-handoff-x-autoposting.md
git commit -m "feat: add safe X autoposting"
git push -u origin feat/x-autoposting
```

---

## Acceptance criteria

Do not call this done until all are true:

- `python3 backend/run.py --dry-run-x` works without credentials.
- `python3 backend/run.py --write --dry-run-x` writes valid JSON feed.
- Missing X credentials produce a clear error when `--post-x` is used.
- With valid credentials, `--post-x` posts exactly one tweet and prints the tweet ID.
- Retrying the same run does not duplicate the same tweet.
- GitHub Action has X secrets wired via `env`, not hardcoded.
- Workflow dispatch succeeds before schedule is trusted.
- Public site still loads at https://iamchrisso.github.io/holy-cash/.

---

## Safety / operating notes

- Do not commit API keys or tokens.
- Do not post investment guarantees.
- Do not increase posting frequency until the first 24 hours run cleanly.
- Start with one scheduled post every 6 hours.
- Keep X posting optional behind `--post-x` so local feed updates can run without credentials.
- If X API fails, the script should fail clearly and avoid committing a fake `x_tweet_id`.
- If feed write succeeds but X post fails, decide deliberately whether to commit the feed-only post. For early implementation, prefer failing the run so the behavior is obvious.

---

## Suggested first MiniMax task

Implement Phase 1 only:

> Add `x_client.py`, `safety.py`, and CLI flags for `--dry-run-x` / `--post-x`, with no real X posting unless credentials are present and `--post-x` is passed. Verify local dry-run and feed JSON validity.

After Phase 1 passes, pause and ask for X credentials/secrets setup before real posting.
