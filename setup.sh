#!/usr/bin/env bash
# One-time setup. Codespaces runs this automatically; you can also run:  bash setup.sh
set -e
echo "→ Installing Python packages..."
pip install -q -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; echo "→ Created .env (add your API key to it)"; fi
if ! command -v claude >/dev/null 2>&1; then
  echo "→ Installing Claude Code..."
  curl -fsSL https://claude.ai/install.sh | bash || npm install -g @anthropic-ai/claude-code
fi
echo ""
echo "✅ Setup done. Next: add your key to .env, run  python check_setup.py,  then  bash start.sh"
