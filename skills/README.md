# Skills

A **skill** is a saved set of instructions for a task people ask for often. Instead of
typing the same long request every week, you type a short command like
`/platform-checkup TikTok` and the app follows the skill's instructions for you.

Claude has skills too (in Claude Code and the Claude apps). It's the same idea: write the
instructions once, reuse them whenever you need them.

## How skills work in this app
- Every `.md` file in this folder is a skill. The file name is the command:
  `platform-checkup.md` becomes `/platform-checkup`.
- Skills show up in the sidebar under **Skills**. Click one, or type it in the chat box.
- Type `/` in the chat box to see a menu of every skill. Keep typing to narrow it down,
  then click a skill or use the arrow keys and Enter. Esc closes the menu.
- Anything typed after the command is passed along. In `/platform-checkup TikTok`,
  "TikTok" is the request.
- Behind the scenes the app sends the skill's instructions plus your request to Claude,
  then it works like any other question: Claude writes a query, the app runs it, and
  Claude explains the results.

## Write your own skill
Copy this into a new file in this folder, e.g. `skills/my-skill.md`, then refresh the app.

```
# /my-skill

Description: One line saying what this skill does. This shows in the sidebar.

## How to use it
What to type after the command, and what happens if nothing is typed.

## What to do
The numbers to get, how to group them, and how to sort them.

## How to write the answer
How the answer should start, what to point out, and how it should end.
```

Tips:
- Be specific. "Show spend, CTR and ROAS by month" beats "show performance".
- Give a default for when the person types nothing extra.
- Ask for one table of results. The app runs one query per question.
