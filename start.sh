#!/usr/bin/env bash
# Starts the Airescents app and prints the link that actually works.
# Run it with:   bash start.sh      (stop the app with Ctrl+C)

cd "$(dirname "$0")"

if [ -n "$CODESPACE_NAME" ]; then
  URL="https://${CODESPACE_NAME}-8501.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
else
  URL="http://localhost:8501"
fi

echo ""
echo "=================================================================="
echo "  🕯️  Airescents Insights is starting"
echo ""
echo "  Open your app here (Cmd+click or copy into your browser):"
echo ""
echo "      $URL"
echo ""
if [ -n "$CODESPACE_NAME" ]; then
echo "  ⚠️  Ignore the 'localhost' links Streamlit prints below."
echo "     They point to the Codespace's computer, not yours."
echo ""
echo "  💤 Your Codespace sleeps after ~30 minutes without activity."
echo "     Nothing is lost: reopen it and run  bash start.sh  again."
fi
echo "=================================================================="
echo ""

exec streamlit run app.py
