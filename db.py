"""
Everything that touches the database lives here.

The database is a single file: data/airescents.duckdb.
We always open it READ-ONLY from the app, so the AI can look at data but never change it.
"""

from pathlib import Path

import duckdb
import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "airescents.duckdb"
MAX_ROWS = 1000  # never pull more than this into the app

# Plain-English notes about each table. The AI reads these to understand the data,
# so better notes = better answers. (Improving these is a great exercise.)
TABLE_NOTES = {
    "campaigns": (
        "One row per ad campaign. Platform (Meta, Google Search, TikTok, YouTube), objective "
        "(Prospecting, Retargeting, Brand Search, Brand Awareness), product line, start and end dates."
    ),
    "creatives": "One row per ad (creative): its campaign, name, format (Video, Static, Carousel, Text), theme and launch date.",
    "ad_performance": (
        "THE MAIN TABLE. Daily results for each ad: impressions, clicks, conversions, spend_usd and "
        "revenue_usd. Conversions and revenue are what each ad platform reports."
    ),
    "budgets": "Planned ad spend per platform per month. 'month' is the first day of the month.",
    "store_orders": (
        "Orders recorded by the Airescents online store, per day, grouped by the channel of the "
        "customer's last click (an ad platform, Email, or Organic & Direct). Includes revenue and "
        "how many orders came from new customers."
    ),
}


class DatabaseMissingError(Exception):
    pass


def get_connection():
    if not DB_PATH.exists():
        raise DatabaseMissingError(
            "The database file is missing. Restore it from GitHub by running:  git checkout data/airescents.duckdb"
        )
    return duckdb.connect(str(DB_PATH), read_only=True)


def get_schema_text() -> str:
    """Describe every table and column so the AI knows what it can query."""
    con = get_connection()
    cols = con.execute(
        """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        ORDER BY table_name, ordinal_position
        """
    ).fetchall()
    con.close()

    tables: dict[str, list[str]] = {}
    for table, column, dtype in cols:
        tables.setdefault(table, []).append(f"  - {column} ({dtype})")

    parts = []
    for table, lines in tables.items():
        note = TABLE_NOTES.get(table, "")
        parts.append(f"TABLE {table}: {note}\n" + "\n".join(lines))
    return "\n\n".join(parts)


def get_sample_values() -> str:
    """A few real values so the AI spells platforms, objectives, etc. correctly."""
    con = get_connection()
    one = lambda sql: [r[0] for r in con.execute(sql).fetchall()]
    platforms = one("SELECT DISTINCT platform FROM campaigns ORDER BY 1")
    objectives = one("SELECT DISTINCT objective FROM campaigns ORDER BY 1")
    lines = one("SELECT DISTINCT product_line FROM campaigns ORDER BY 1")
    formats = one("SELECT DISTINCT format FROM creatives ORDER BY 1")
    channels = one("SELECT DISTINCT last_click_channel FROM store_orders ORDER BY 1")
    first, last = con.execute("SELECT MIN(date), MAX(date) FROM ad_performance").fetchone()
    con.close()
    return (
        f"Platforms: {', '.join(platforms)}\n"
        f"Objectives: {', '.join(objectives)}\n"
        f"Product lines: {', '.join(lines)}\n"
        f"Ad formats: {', '.join(formats)}\n"
        f"Store last-click channels: {', '.join(channels)}\n"
        f"Data covers {first} through {last}."
    )


def run_query(sql: str) -> pd.DataFrame:
    """Run a SELECT query and return the result as a table."""
    cleaned = sql.strip().rstrip(";")
    first_word = cleaned.split(None, 1)[0].upper() if cleaned else ""
    if first_word not in ("SELECT", "WITH"):
        raise ValueError("Only SELECT queries are allowed. The app can read data but never change it.")

    con = get_connection()
    try:
        df = con.execute(f"SELECT * FROM ({cleaned}) LIMIT {MAX_ROWS}").df()
    finally:
        con.close()
    return df
