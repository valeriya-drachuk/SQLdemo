# 🕯️ Airescents Insights

An AI analytics app for the marketing team at **Airescents**, a fictional brand that sells
candles, diffusers and room sprays online. Ask a question in plain English ("What was our
ROAS on Meta last quarter?") and get back an answer, a chart, the data, and the exact SQL behind it.

> All companies, campaigns and numbers here are made up for learning.

## What's inside

- **A realistic fake dataset**: a full year (2025) of daily ad results on Meta, Google Search,
  TikTok and YouTube (impressions, clicks, conversions, spend and revenue), plus campaigns,
  creatives, monthly budgets and the store's own order records.
- **A chat app** where Claude turns questions into SQL, runs them, fixes its own mistakes
  once, and explains the results.
- **Friendly errors.** When something breaks, the app tells you what happened and what to try.

## Getting started (GitHub Codespaces)

1. **Make your own repo with the app in it.**
   - On github.com, click **+ → New repository**. Name it `airescents`, tick
     **Add a README file**, then click **Create repository**.
   - On the new repo's page, click **Code → Codespaces → Create codespace**. Wait 2–4 minutes.
   - Drag `airescents-student.zip` from your computer into the file list on the left.
     (Drag the .zip itself. Don't unzip it first.)
   - In the terminal at the bottom, run:
     ```
     unzip -o airescents-student.zip && rm airescents-student.zip && bash setup.sh
     ```
     When it's done, `app.py` is in the file list.
2. Get an API key at **console.anthropic.com** → API Keys. **Set a monthly spend limit**
   (a few dollars is plenty for this project).
3. Open the `.env` file and paste your key after `AIRESCENTS_ANTHROPIC_KEY=`
4. In the terminal, run:
   ```
   python check_setup.py
   ```
   Fix anything marked ❌. Each line tells you what to do.
5. Start the app:
   ```
   bash start.sh
   ```
   It prints a box with **your app's link**. Cmd+click it (or copy it into your browser).

   > ⚠️ **Don't use the `localhost` link** Streamlit prints underneath. It points to the
   > Codespace's computer in the cloud, not yours, so it will never open.

### Good to know
- **Your Codespace falls asleep** after about 30 minutes without activity, and the app stops
  with it. Nothing is lost. Reopen it from github.com/codespaces and run `bash start.sh` again.
- **Keep the app in its own terminal.** It stays busy while the app runs. Open a second terminal
  (the **+** button) for Claude Code.
- **To stop the app**, click its terminal and press **Ctrl+C**.
- **Save your work to GitHub often.** Ask Claude Code: *"Commit everything and push to GitHub."*

### Using Claude Code
In the terminal, type `claude` and log in with your Claude account (Pro or Max).
Try: *"Explain this project to me like I'm new to coding."*

> ⚠️ **Don't name your key `ANTHROPIC_API_KEY`.** If you do, Claude Code bills the key
> instead of your subscription. This project uses `AIRESCENTS_ANTHROPIC_KEY` on purpose.

## Running on your own computer instead
Needs Python 3.10+.
```
bash setup.sh
python check_setup.py
bash start.sh
```

## Project files

| File | What it does |
|---|---|
| `app.py` | The web app: chat, sidebar, charts |
| `ai.py` | Talks to Claude: writes SQL, fixes SQL, explains results |
| `db.py` | Reads the database (read-only) and describes the tables |
| `data/airescents.duckdb` | The marketing database (read-only) |
| `check_setup.py` | Checks that everything's ready |
| `start.sh` | Starts the app and prints the right link |
| `CLAUDE.md` | Instructions Claude Code reads automatically |
