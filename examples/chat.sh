#!/usr/bin/env bash
# NezhaGate chat examples with curl. The endpoint is OpenAI-compatible; switching models is one string.
#   export NEZHAGATE_API_KEY=sk-xxxx && bash examples/chat.sh
set -euo pipefail
BASE="https://nezhagate.com/v1"
: "${NEZHAGATE_API_KEY:?export NEZHAGATE_API_KEY first (create a key in the console at https://nezhagate.com)}"

say() { python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["message"]["content"])'; }

echo "== 1) basic chat (gpt-5.6-terra) =="
curl -s "$BASE/chat/completions" \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gpt-5.6-terra", "messages": [{"role": "user", "content": "Introduce yourself in one sentence."}]}' | say

echo; echo "== 2) same request, Claude and Gemini -- only the model string changes =="
for m in claude-opus-5 gemini-3.8-flash; do
  printf '%s: ' "$m"
  curl -s "$BASE/chat/completions" \
    -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
    -d "{\"model\": \"$m\", \"messages\": [{\"role\": \"user\", \"content\": \"Say hi in five words.\"}]}" | say
done

echo; echo "== 3) reasoning effort (gpt-5.6 / gpt-5.5 / gemini-3.1-pro accept low|medium|high) =="
curl -s "$BASE/chat/completions" \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gpt-5.6-sol", "reasoning_effort": "high", "messages": [{"role": "user", "content": "Is 1000003 prime? Answer yes or no, then explain briefly."}]}' | say

echo; echo "== 4) streaming (SSE) =="
curl -sN "$BASE/chat/completions" \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "gemini-3.6-flash-low", "stream": true, "messages": [{"role": "user", "content": "Count from 1 to 5."}]}'
echo
