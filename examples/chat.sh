#!/usr/bin/env bash
# NezhaGate chat examples (curl). Base URL is OpenAI-compatible.
#   export NEZHAGATE_API_KEY=sk-xxxx && ./chat.sh
set -euo pipefail
BASE="https://nezhagate.com/v1"

echo "== 1) basic chat (claude-opus-4-8) =="
curl -s "$BASE/chat/completions" \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "messages": [{"role": "user", "content": "用一句话介绍你自己"}]
  }' | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["message"]["content"])'

echo
echo "== 2) streaming (gpt-5.5) =="
curl -sN "$BASE/chat/completions" \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.5",
    "stream": true,
    "messages": [{"role": "user", "content": "数到 5"}]
  }'
echo
