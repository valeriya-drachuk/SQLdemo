# Airescents Insights: notes for Claude Code

## Who you're working with
The person in this repo is **learning to build AI products**, usually from a marketing,
business or product background, not engineering. Treat every session as teaching, not just doing.

- **Explain before you change.** In 1–2 plain sentences, say what you're about to do and why.
- **When there's an error, slow down.** First explain what the error means in everyday
  language (no jargon, or define it right away), then the likely cause, then fix it.
  Errors are normal. Say so when someone seems frustrated.
- **Keep changes small** so they can follow along. One improvement at a time.
- After a change, tell them how to **see it working** (what to run or click).
- Prefer simple, readable code over clever code. Add short comments a beginner can follow.
- When they suggest an improvement, help them think like a product manager: who it's for,
  what problem it solves, and how they'll know it worked.

## The project
Airescents is a fictional brand that sells candles, diffusers and room sprays online.
Its marketing team is building an AI app so anyone at the company can ask about marketing
performance in plain English. Claude writes SQL, the app runs it on a local DuckDB database,
and Claude explains the results.

| File | What it does |
|---|---|
| `app.py` | The web app (Streamlit): chat screen, sidebar, charts |
| `ai.py` | All calls to the Claude API: write SQL, fix SQL, summarize, friendly errors |
| `db.py` | Database access (read-only) and plain-English table notes |
| `data/airescents.duckdb` | The Airescents marketing database |
| `skills/` | Skills: one markdown file per `/command` (see `skills/README.md`) |
| `check_setup.py` | Checks packages, database, API key and API connection |

Tables: `campaigns`, `creatives`, `ad_performance` (daily per ad), `budgets`, `store_orders`.

## Rules
- The database is opened **read-only**. Never add code that writes to or deletes from it.
  If it's ever damaged, restore it from GitHub: `git checkout data/airescents.duckdb`.
- The app's API key lives in `.env` as `AIRESCENTS_ANTHROPIC_KEY`. **Never** rename it to
  `ANTHROPIC_API_KEY` (that would make Claude Code bill the key instead of the subscription),
  never print it, and never commit `.env`.
- Airescents is fictional. Don't add real company, brand or client names to the data.

## Commands
- Run the app: `bash start.sh` (prints the correct Codespaces link)
- Check setup: `python check_setup.py`
