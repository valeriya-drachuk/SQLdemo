# Course map

**The story:** you're on the marketing team at Airescents, a fictional brand that sells
candles, diffusers and room sprays online. The company wants an AI app that shows its
marketing performance in one place, simple enough for anyone to use. The base app already
works. Your job is to act as its product manager: check that it's right, find what's
missing, and build the improvements.

Classes 1–5 build this one app together. Classes 6–7 are about your own capstone and portfolio.

| # | Theme | In class | Homework |
|---|---|---|---|
| 0 (optional) | Setup hour | GitHub account, Codespace, Claude login, API key with a spend limit | Run `python check_setup.py` until everything is ✅ |
| 1 | Kickoff and verify | Marketing in 5 minutes; setup; Claude Code explains the repo; run the app; push to GitHub; check a few answers together | Check the rest of `TEAM_QUESTIONS.md`; note every answer that looks wrong or confusing |
| 2 | Fix what's broken | How to reproduce, describe, fix and re-check a bug; the bug report; log bugs as GitHub Issues; fix one together | Write bug reports for and fix 1–2 bugs from your class 1 log |
| 3 | Find what's missing | Brainstorm what the app lacks; the improvement brief; the project board and how to prioritize; build one small improvement together | Write briefs for and build 1–2 improvements from the board |
| 4 | Skills | What skills are and why they automate repeat work; try `/platform-checkup`; build a report-builder skill together | Design and build one skill of your own; choose your capstone idea and dataset |
| 5 | Bring your own data | Upload CSV files; what data gets sent to Claude, and when | Prepare your capstone dataset |
| 6 | Capstone workshop | Build your capstone; make your repo recruiter-ready | Finish your capstone; README, screenshots, demo video |
| 7 | Demo day | Demo what you found, what you improved and your capstone | Share it: resume, LinkedIn, GitHub |

## Marketing in 5 minutes

| Term | Means | How it's calculated |
|---|---|---|
| Impressions | Times an ad was shown | Counted by the ad platform |
| CTR (click-through rate) | Share of people who clicked after seeing the ad | clicks ÷ impressions |
| CPC (cost per click) | What each click cost | spend ÷ clicks |
| CPM (cost per mille) | What 1,000 impressions cost | spend ÷ impressions × 1,000 |
| Conversion | A sale that came from an ad | Reported by the ad platform |
| CPA (cost per acquisition) | What each sale cost | spend ÷ conversions |
| ROAS (return on ad spend) | Revenue earned for every $1 spent on ads | revenue ÷ spend |

The data is a year (2025) of digital advertising on Meta, Google Search, TikTok and YouTube,
plus the store's own order records. Everything is made up, but shaped like the real thing.

## How each improvement works

Every bug and every improvement is a GitHub Issue, tracked on your project board
(Backlog → Next → Doing → Done). Click **New issue** on GitHub and pick a form:
**Bug report** or **Improvement brief**. If you can't fill in every box, you're not ready to build.

- **Bugs:** reproduce → bug report → fix → re-check.
- **Improvements:** review → brief → plan → build → test.

**Plan before you build.** Paste the issue into Claude Code and ask:
*"Here's my issue. Propose a plan and wait for my approval before changing anything."*
(Or press **Shift+Tab** until Claude Code shows "plan mode".) Push back on anything bigger than the issue.

**Test, then re-check.** Do exactly what the issue's "How I'll test" or "Fixed means" says, then
ask a few of the team's questions again to make sure nothing else broke.

**Save a checkpoint before each build:** *"Commit everything and push to GitHub."*

See `BOARD_SETUP.md` to set up your board, and `BEFORE_YOU_ACCEPT.md` for how to judge what Claude Code builds.
