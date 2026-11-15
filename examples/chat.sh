#!/usr/bin/env bash
# KovAPI chat examples with curl. The endpoint is OpenAI-compatible; switching models is one string.
#   export KOVAPI_API_KEY=sk-xxxx && bash examples/chat.sh
set -euo pipefail
BASE="https://kovapi.com/v1"
KOVAPI_API_KEY="${KOVAPI_API_KEY:-${NEZHAGATE_API_KEY:-}}"   # NEZHAGATE_API_KEY, the old name, still works
: "${KOVAPI_API_KEY:?export KOVAPI_API_KEY first (create a key in the console at https://kovapi.com)}"

say() { python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["message"]["content"])'; }

echo "== 1) basic chat (gpt-5.6-terra) =="
curl -s "$BASE/chat/completions" \
  -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gpt-5.6-terra", "messages": [{"role": "user", "content": "Introduce yourself in one sentence."}]}' | say

echo; echo "== 2) same request, Claude / Gemini / DeepSeek / Grok -- only the model string changes =="
for m in claude-opus-5 gemini-3.8-flash deepseek-v4.1-flash grok-4.7; do
  printf '%s: ' "$m"
  curl -s "$BASE/chat/completions" \
    -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
    -d "{\"model\": \"$m\", \"messages\": [{\"role\": \"user\", \"content\": \"Say hi in five words.\"}]}" | say
done

echo; echo "== 3) reasoning effort (GPT, Claude and gemini-3.1-pro accept low|medium|high) =="
curl -s "$BASE/chat/completions" \
  -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gpt-6-astra", "reasoning_effort": "high", "messages": [{"role": "user", "content": "Is 1000003 prime? Answer yes or no, then explain briefly."}]}' | say

echo; echo "== 4) streaming (SSE) =="
curl -sN "$BASE/chat/completions" \
  -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gemini-3.6-flash-low", "stream": true, "messages": [{"role": "user", "content": "Count from 1 to 5."}]}'
echo
