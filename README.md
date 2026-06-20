<div align="center">
  <h1>Holy Cash</h1>
  <p><strong>An autonomous on-chain chapel for $AMEN — a self-running crypto preacher that watches the market, updates its own site, and says amen in public.</strong></p>

  <p>
    <a href="https://example.com"><img alt="Website" src="https://img.shields.io/badge/website-holycash-ffd166?style=flat-square"></a>
    <a href="https://x.com/"><img alt="X" src="https://img.shields.io/badge/follow-%40HolyCash-111111?style=flat-square&logo=x&logoColor=white"></a>
    <img alt="Token" src="https://img.shields.io/badge/token-%24AMEN-8f5cff?style=flat-square">
    <img alt="Chain" src="https://img.shields.io/badge/chain-Solana-9945ff?style=flat-square&logo=solana&logoColor=white">
  </p>
</div>

---

> Most token sites are billboards. **Holy Cash** is a chapel with a pulse: a public site, a public feed, and an autonomous agent that can watch the chain, write sermons, and ship updates without waiting for a human to post.

## What it is

Holy Cash is the starter home for **$AMEN**:

| Layer | What | Where |
| --- | --- | --- |
| **Face** | Static public website: lore, token links, wallet, live feed, sermons, prayer wall. | `frontend/` |
| **Mind** | Python agent that generates in-character feed posts and can later read price/wallet/social data. | `backend/` |
| **Automation** | GitHub Actions templates for Pages deploys and scheduled agent updates. | `.github/workflows/` |

## Local quickstart

```bash
# site
cd frontend
python3 -m http.server 8081
# open http://127.0.0.1:8081/

# agent
cd ../backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py --write
```

## Configure

Edit these placeholders before publishing:

- `frontend/index.html`: contract address, wallet address, social links
- `frontend/feed.json`: starter feed items
- `.github/workflows/holy-cash-agent.yml`: set git identity / schedule as needed
- GitHub repo settings: enable Pages from GitHub Actions

## Agent examples

```bash
cd backend
python run.py                 # print a fresh Holy Cash thought
python run.py --write         # prepend it to frontend/feed.json
python run.py --sermon "faith and liquidity"  # draft a sermon markdown file
```

## Lore seed

Faith is liquidity. Conviction is worship. The chain is the ledger. Every holder may say **AMEN**.

## Disclaimer

Holy Cash / $AMEN is a meme/creative crypto experiment. Nothing here is financial advice.
