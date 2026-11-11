"""
Checks that everything is ready to go. Run it with:   python check_setup.py

Each check prints ✅ or ❌ with what to do next. If you get stuck, paste the
output into Claude Code and ask: "explain what's wrong in simple terms".
"""

import importlib.util
import sys

ok = True


def check(label, fn):
    global ok
    try:
        detail = fn()
        print(f"✅ {label}" + (f": {detail}" if detail else ""))
    except Exception as e:
        ok = False
        print(f"❌ {label}\n   → {e}")


def packages():
    missing = [p for p in ("duckdb", "streamlit", "anthropic", "pandas", "dotenv")
               if importlib.util.find_spec(p) is None]
    if missing:
        raise RuntimeError(f"Missing: {', '.join(missing)}. Run:  pip install -r requirements.txt")


def database():
    import db
    df = db.run_query("SELECT COUNT(*) AS n FROM ad_performance")
    return f"{int(df['n'][0]):,} rows of ad performance"


def api_key():
    import ai
    ai.get_client()
    return f"found {ai.API_KEY_NAME}"


def api_call():
    import ai
    reply = ai._ask("Reply with exactly: ready", [{"role": "user", "content": "Are you there?"}], max_tokens=10)
    return f"Claude says '{reply.strip()}' (model: {ai.MODEL})"


print(f"Python {sys.version.split()[0]}\n")
check("Python packages installed", packages)
check("Database found", database)
check("API key set", api_key)
if ok:
    check("Claude API reachable", api_call)

print("\nAll set! Run:  streamlit run app.py" if ok else "\nFix the ❌ items above, then run this again.")
