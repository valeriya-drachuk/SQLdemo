# Set up your project board

You'll track your work on Airescents Insights the way product teams do: every bug and
every improvement is a **GitHub Issue**, issues are grouped into **milestones** (one per
class), and a **project board** shows what's next, what's in progress and what's done.

This file is the plan for your board. You'll create the board yourself, then have Claude
Code add the board fields, milestones and issues from this file.

There are no labels yet. We'll decide on them together in class.

---

## Step 1: Create your project board (by hand)

1. On GitHub, open your Airescents repo and click the **Projects** tab, then **New project**.
2. Choose the **Board** layout and name it `Airescents Insights`.
3. Rename the columns to: **Backlog**, **Next**, **Doing**, **Done**.

## Step 2: Have Claude Code set up the board

Paste this into Claude Code:

> *"Read `docs/BOARD_SETUP.md`. On my 'Airescents Insights' project board, add every field
> in the 'Board fields' section. Then create every milestone and issue in the 'Milestones'
> and 'Class task issues' sections on my GitHub repo, and add the issues to the board in the
> Backlog column. Don't create any labels, and delete GitHub's default labels from my repo.
> Show me the list first and wait for my OK before creating anything. If you need extra
> GitHub permission for the board, walk me through it step by step."*

Read Claude's list before you say OK. Does it match this file? Nothing extra?

## Step 3: Check your board

Open your project board. You should see 6 class task issues in Backlog. Open one: on the
right you should see **Start date**, **Target date**, **Priority** and **Effort**, ready to
fill in. Open **Milestones** under the Issues tab: you should see 6 milestones, each with
one issue. **Labels** under the Issues tab should be empty.

From now on, each bug or improvement you find becomes its own issue (use **New issue**
and pick **Bug report** or **Improvement brief**), added to the milestone for the class
you'll fix it in.

---

## Board fields

Every issue on the board gets these four fields. Fill them in as you plan each class.

| Field | Type | Options |
|---|---|---|
| Start date | Date | |
| Target date | Date | |
| Priority | Single select | High, Medium, Low |
| Effort | Single select | Small, Medium, Large |

## Milestones

| Milestone | Done means |
|---|---|
| Class 1: App verified | The app runs, `TEAM_QUESTIONS.md` is checked, and every wrong or confusing answer is logged as an issue. |
| Class 2: Known bugs fixed | Every bug issue from class 1 is closed or deliberately moved to a later milestone. |
| Class 3: First improvements shipped | 1–2 improvement issues are closed, each with a brief and a test. |
| Class 4: Skills added | At least one `/skill` command works, and your capstone idea is chosen. |
| Class 5: Own data loaded | CSV upload works, and your capstone dataset is prepared. |
| Class 6–7: Capstone and demo | Capstone built; README, screenshots and demo video done; demo day delivered. |

## Class task issues

Create each one as an issue with this title, in this milestone, with this checklist as its
description.

### Class 1: Verify the app
Milestone: Class 1: App verified
- [ ] Run the app and ask your first question
- [ ] Ask Claude Code to explain the repo in plain English
- [ ] Push your copy to GitHub
- [ ] Check every question in `TEAM_QUESTIONS.md` and record your score (e.g. 9/15)
- [ ] File a Bug report issue for every answer that's wrong or confusing

### Class 2: Fix what's broken
Milestone: Class 2: Known bugs fixed
- [ ] Reproduce one bug from your list, following its "Steps to repeat"
- [ ] Write your first bug report by hand using the Bug report form
- [ ] Have Claude Code draft your next bug report, and review it before it's posted
- [ ] Fix one bug with Claude Code (plan first, then build)
- [ ] Re-check: repeat the steps, then ask 3 team questions to make sure nothing else broke
- [ ] Close the fixed issue; move any bug you're not fixing yet to a later milestone

### Class 3: Find what's missing
Milestone: Class 3: First improvements shipped
- [ ] Brainstorm what the app lacks and file each idea as an Improvement brief issue
- [ ] Put your improvement issues in priority order on the board (top of Next = most important)
- [ ] Build one improvement together in class
- [ ] Build 1–2 more from the top of your board
- [ ] Re-score `TEAM_QUESTIONS.md` and note the change (e.g. 9/15 → 13/15)

### Class 4: Add skills
Milestone: Class 4: Skills added
- [ ] Try the built-in `/platform-checkup` skill and read its file in `skills/`
- [ ] Build the report-builder skill together in class
- [ ] Write an Improvement brief issue for one skill of your own
- [ ] Build and test your skill
- [ ] Choose your capstone idea and dataset

### Class 5: Bring your own data
Milestone: Class 5: Own data loaded
- [ ] Upload a CSV file and ask a question about it
- [ ] Explain in one sentence what data gets sent to Claude, and when
- [ ] Prepare your capstone dataset

### Class 6–7: Capstone and demo
Milestone: Class 6–7: Capstone and demo
- [ ] Build your capstone
- [ ] Write your README, with screenshots
- [ ] Record a short demo video
- [ ] Demo what you found, what you improved and your capstone
- [ ] Share it: resume, LinkedIn, GitHub
