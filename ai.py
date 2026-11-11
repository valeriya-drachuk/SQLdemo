"""
Everything that talks to Claude lives here.

The flow for every question:
  1. write_sql()   - Claude turns the question into a SQL query
  2. (app runs it) - if the query errors, fix_sql() gives Claude the error to repair it
  3. summarize()   - Claude explains the results in plain English
"""

import os
import re

import anthropic
import pandas as pd
from dotenv import load_dotenv

import db

load_dotenv()

# IMPORTANT: we deliberately DON'T use the name ANTHROPIC_API_KEY.
# Claude Code also looks for ANTHROPIC_API_KEY, and if it finds one it bills
# that key instead of your Claude subscription. A different name avoids that trap.
API_KEY_NAME = "AIRESCENTS_ANTHROPIC_KEY"
MODEL = os.getenv("AIRESCENTS_MODEL", "claude-sonnet-5-5")


class MissingKeyError(Exception):
    pass


def get_client() -> anthropic.Anthropic:
    key = os.getenv(API_KEY_NAME, "").strip()
    if not key:
        raise MissingKeyError(
            f"No API key found. Copy .env.example to .env and paste your key after {API_KEY_NAME}="
        )
    return anthropic.Anthropic(api_key=key)


def _ask(system: str, messages: list[dict], max_tokens: int = 1500) -> str:
    response = get_client().messages.create(
        model=MODEL, max_tokens=max_tokens, system=system, messages=messages
    )
    return "".join(block.text for block in response.content if block.type == "text")


def _extract_sql(text: str) -> str:
    match = re.search(r"<sql>(.*?)</sql>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("Claude didn't return a SQL query. Try rephrasing the question.")


SQL_SYSTEM_PROMPT = """You are the marketing analytics assistant for Airescents, a brand that sells
candles, diffusers and room sprays online. You write DuckDB SQL to answer questions
from the marketing team about advertising performance and store orders.

DATABASE:
{schema}

USEFUL VALUES:
{samples}

RULES:
- Return exactly one query inside <sql></sql> tags, then nothing else.
- Read-only: SELECT or WITH only.
- Money is in USD: round to 2 decimal places. Round percentages to 2 decimal places.
- For trends over time, group by month with date_trunc('month', date) AS month and order by month.
- Keep results small and readable: aggregate, and use LIMIT for "top" questions.
"""


def write_sql(question: str, history: list[dict]) -> str:
    system = SQL_SYSTEM_PROMPT.format(schema=db.get_schema_text(), samples=db.get_sample_values())
    # Include the last few questions so follow-ups like "what about TikTok?" work
    messages = []
    for turn in history[-3:]:
        messages.append({"role": "user", "content": turn["question"]})
        messages.append({"role": "assistant", "content": f"<sql>{turn['sql']}</sql>"})
    messages.append({"role": "user", "content": question})
    return _extract_sql(_ask(system, messages))


def fix_sql(question: str, bad_sql: str, error: str) -> str:
    system = SQL_SYSTEM_PROMPT.format(schema=db.get_schema_text(), samples=db.get_sample_values())
    messages = [
        {"role": "user", "content": question},
        {"role": "assistant", "content": f"<sql>{bad_sql}</sql>"},
        {"role": "user", "content": f"That query failed with this error:\n{error}\n\nPlease fix it."},
    ]
    return _extract_sql(_ask(system, messages))


SUMMARY_SYSTEM_PROMPT = """You are the marketing analytics assistant for Airescents.
Explain query results to a busy marketer who may not be a data person.
- Lead with the direct answer in one sentence.
- Then 2-4 short bullet points with the most useful details or patterns.
- Use real numbers from the results. Never invent numbers that aren't there.
- If the results look odd or incomplete, say so plainly.
"""


def summarize(question: str, sql: str, df: pd.DataFrame) -> str:
    preview = df.head(50).to_csv(index=False)
    note = f"(Showing first 50 of {len(df)} rows.)" if len(df) > 50 else ""
    content = f"Question: {question}\n\nSQL used:\n{sql}\n\nResults {note}:\n{preview}"
    return _ask(SUMMARY_SYSTEM_PROMPT, [{"role": "user", "content": content}], max_tokens=800)


def friendly_error(err: Exception) -> tuple[str, str]:
    """Turn a scary error into (what happened, what to try)."""
    if isinstance(err, MissingKeyError):
        return ("The app can't find your API key.", str(err))
    if isinstance(err, db.DatabaseMissingError):
        return ("The database hasn't been created yet.", str(err))
    if isinstance(err, anthropic.AuthenticationError):
        return ("Your API key was rejected.",
                "Check for typos or extra spaces in .env, or create a fresh key in the Claude Console.")
    if isinstance(err, anthropic.NotFoundError):
        return (f"The model '{MODEL}' wasn't found.",
                "Set AIRESCENTS_MODEL in .env to a current model name from the Claude docs.")
    if isinstance(err, anthropic.RateLimitError):
        return ("You've hit a usage limit.", "Wait a minute and try again, or check your Console spending limit.")
    if isinstance(err, anthropic.APIConnectionError):
        return ("The app couldn't reach Claude.", "Check your internet connection and try again.")
    if isinstance(err, anthropic.BadRequestError) and "credit" in str(err).lower():
        return ("Your API account is out of credits.", "Add credits in the Claude Console under Billing.")
    return ("Something unexpected went wrong.",
            f"Copy this error into Claude Code and ask it to explain it simply:\n\n{type(err).__name__}: {err}")
