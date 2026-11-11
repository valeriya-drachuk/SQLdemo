"""
Airescents Insights: ask questions about Airescents marketing performance in plain English.

Run it with:   streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

import ai
import db
from skill_menu import show_skill_menu

st.set_page_config(page_title="Airescents Insights", page_icon="🕯️", layout="wide")

EXAMPLE_QUESTIONS = [
    "How much did we spend on each platform in 2025?",
    "What was our ROAS on Meta each month?",
    "Which 5 ads had the best click-through rate?",
    "How did Google Search spend compare to budget each month?",
]

# ---------------------------------------------------------------- skills
# A skill is a saved set of instructions for a task people ask for often.
# Each skill is a markdown file in the skills/ folder: skills/platform-checkup.md
# becomes the command /platform-checkup. To add a skill, add a file. No code needed.
SKILLS_DIR = Path(__file__).parent / "skills"


def load_skills() -> dict:
    """Read every skill file. Returns {"platform-checkup": {"description", "instructions"}}."""
    skills = {}
    for file in sorted(SKILLS_DIR.glob("*.md")):
        if file.stem.upper() == "README":
            continue  # the how-to guide, not a skill
        text = file.read_text()
        # The "Description:" line is the one-liner shown in the sidebar
        description = next(
            (line.split(":", 1)[1].strip() for line in text.splitlines()
             if line.lower().startswith("description:")),
            "",
        )
        skills[file.stem] = {"description": description, "instructions": text}
    return skills


def expand_skill(question: str) -> str:
    """If the question starts with /skill-name, swap in that skill's instructions.

    "/platform-checkup TikTok" becomes the skill's instructions plus "TikTok".
    Anything that doesn't start with / is returned unchanged.
    """
    if not question.startswith("/"):
        return question
    name, _, request = question[1:].partition(" ")
    skills = load_skills()
    if name not in skills:
        available = ", ".join(f"/{s}" for s in skills) or "none yet"
        raise UnknownSkillError(f"There's no skill called /{name}. Skills you can use: {available}.")
    return (
        f"Follow these skill instructions:\n\n{skills[name]['instructions']}\n\n"
        f"The user's request: {request.strip() or '(nothing extra; use the defaults above)'}"
    )


class UnknownSkillError(Exception):
    """Someone typed /something that isn't in the skills/ folder."""


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🕯️ Airescents Insights")
    st.caption("Airescents is a fictional brand. All data is made up for learning.")

    st.subheader("Try asking")
    for q in EXAMPLE_QUESTIONS:
        if st.button(q, width="stretch"):
            st.session_state.pending_question = q

    st.subheader("Skills")
    st.caption("Type / and a skill name in the chat box, e.g. /platform-checkup TikTok")
    for name, skill in load_skills().items():
        if st.button(f"/{name}", help=skill["description"], width="stretch"):
            st.session_state.pending_question = f"/{name}"

    with st.expander("What's in the data?"):
        for table, note in db.TABLE_NOTES.items():
            st.markdown(f"**{table}**: {note}")

    with st.expander("How does this work?"):
        st.markdown(
            "1. Claude turns your question into a SQL query\n"
            "2. The app runs that query on the database\n"
            "3. If the query fails, Claude gets the error and tries to fix it once\n"
            "4. Claude explains the results in plain English"
        )

    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------------------------------------------- helpers
def show_chart(df: pd.DataFrame):
    """If the result is a trend over time (by month, week or day), draw a line chart."""
    time_col = next((c for c in ("month", "week", "date", "day") if c in df.columns), None)
    if time_col is None or len(df) < 3:
        return
    numeric = df.select_dtypes("number").columns.tolist()
    others = [c for c in df.columns if c not in numeric and c != time_col]
    if not numeric:
        return
    if len(others) == 1 and df[others[0]].nunique() <= 10:
        chart_df = df.pivot_table(index=time_col, columns=others[0], values=numeric[0], aggfunc="sum")
    elif not others:
        chart_df = df.set_index(time_col)[numeric[:3]]
    else:
        return
    st.line_chart(chart_df)


def show_turn(turn: dict):
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        if turn.get("error"):
            what, fix = turn["error"]
            st.error(f"**{what}**\n\n{fix}")
            return
        if turn.get("skill"):
            st.caption(f"⚡ Answered with the /{turn['skill']} skill")
        st.markdown(turn["answer"])
        df = turn["data"]
        show_chart(df)
        with st.expander(f"See the data ({len(df)} rows)"):
            st.dataframe(df, width="stretch")
        with st.expander("See the SQL"):
            st.code(turn["sql"], language="sql")
            if turn.get("was_fixed"):
                st.caption("The first query failed, so Claude fixed it automatically.")


def answer(question: str) -> dict:
    turn = {"question": question}  # the chat shows what was typed, e.g. "/platform-checkup TikTok"
    try:
        if question.startswith("/"):
            turn["skill"] = question[1:].split(" ")[0]
        # From here on Claude sees the full skill instructions instead of the short command
        question = expand_skill(question)
        with st.spinner("Writing a query..."):
            sql = ai.write_sql(question, [t for t in st.session_state.history if "sql" in t])
        try:
            with st.spinner("Running it..."):
                df = db.run_query(sql)
        except Exception as query_error:
            with st.spinner("That query failed, asking Claude to fix it..."):
                sql = ai.fix_sql(question, sql, str(query_error))
                df = db.run_query(sql)
                turn["was_fixed"] = True
        with st.spinner("Explaining the results..."):
            turn["answer"] = ai.summarize(question, sql, df)
        turn["sql"], turn["data"] = sql, df
    except UnknownSkillError as err:
        turn["error"] = ("Unknown skill.", str(err))
    except Exception as err:
        turn["error"] = ai.friendly_error(err)
    return turn


# ---------------------------------------------------------------- main
st.header("Ask anything about our marketing performance")

for turn in st.session_state.history:
    show_turn(turn)

question = st.chat_input("e.g. Which TikTok ads had the lowest CPA in March? Or type / for skills")
show_skill_menu(load_skills())  # the menu that pops up when you type /
question = question or st.session_state.pop("pending_question", None)

if question:
    turn = answer(question)
    st.session_state.history.append(turn)
    show_turn(turn)
