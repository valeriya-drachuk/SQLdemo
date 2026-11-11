# Before you click Accept

When Claude Code builds something, it shows you changes and asks for permission, often in
technical language. You don't need to understand the code. You need to judge the change.
Three steps make that easy.

---

## 1. Ask for a plain-English explanation

If Claude Code's message is full of jargon, ask it to translate. You can ask at any point:

> *"Explain what you just did like I'm a product manager, not an engineer."*

> *"Before I approve this, explain in one sentence what it does and why."*

A good explanation tells you:
- **What changed:** what someone using the app will notice.
- **Which files:** where the change lives.
- **Why:** how it connects to your brief.
- **How to see it working:** what to run or click.
- **Anything risky:** what could break.

If a technical term still doesn't make sense, ask: *"What does ___ mean, in one sentence?"*
Asking isn't a sign you're behind. It's how this job is done.

---

## 2. The three-question check

Before you approve a change, check three things.

**Which file is it changing?**
- `app.py`, `ai.py`, `db.py` or a new file for your feature: normal.
- `.env` (your API key), the database, or anything in `.devcontainer/`: stop and ask why.

**Is it in the brief?**
- If it's doing what your plan said, go ahead.
- If it's doing something extra ("I also refactored…", "I also added…"), ask why. Extra
  changes are the most common way things break.

**Is it installing or deleting something?**
- Installing a package or deleting a file isn't automatically bad, but ask what and why first.

If all three answers make sense, approve it. If any don't, ask before you click.

---

## 3. The safety net

You can approve with confidence because two habits catch anything that goes wrong.

**Before building: save a checkpoint.**

> *"Commit everything and push to GitHub."*

If a change goes badly, you can always get back to the version that worked:

> *"Undo everything since my last commit."*

**After building: test it.**
1. Restart the app (Ctrl+C in the app's terminal, then `bash start.sh`).
2. Do exactly what the "How I'll test it" line in your brief says.
3. Ask 3–4 of the team's questions to make sure answers still come out right.

If the test passes, save another checkpoint. If it fails, describe what you see to
Claude Code and ask it to fix it, or undo to your last checkpoint.

---

## The short version

You approve based on the **plan**. You verify based on the **result**.
You don't need to read every line of code. Check the plan, check which files it touches,
and test what it built.
