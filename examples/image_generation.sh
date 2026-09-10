#!/usr/bin/env bash
# NezhaGate image generation with curl -- async job: submit -> poll -> url.
#   export NEZHAGATE_API_KEY=sk-xxxx && bash examples/image_generation.sh
set -euo pipefail
BASE="https://nezhagate.com/v1"
: "${NEZHAGATE_API_KEY:?export NEZHAGATE_API_KEY first}"
AUTH="Authorization: Bearer $NEZHAGATE_API_KEY"

# 1) submit -> HTTP 202 {"id":"img_...","object":"image.generation.job","status":"queued"}
JOB=$(curl -s "$BASE/images/generations" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"model": "gpt-image-2", "prompt": "a serene ink-wash poster, lots of negative space", "size": "3:4", "resolution": "1K"}')
echo "submitted: $JOB"
ID=$(printf '%s' "$JOB" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

# 2) poll GET /v1/images/jobs/{id} until status=succeeded, then read data[0].url (a stable re-hosted link)
while :; do
  sleep 3
  R=$(curl -s "$BASE/images/jobs/$ID" -H "$AUTH")
  S=$(printf '%s' "$R" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status"))')
  echo "  status: $S"
  case "$S" in
    succeeded) printf '%s' "$R" | python3 -c 'import json,sys; print("image url:", json.load(sys.stdin)["data"][0]["url"])'; break ;;
    failed|cancelled) echo "job ended (not billed): $R"; break ;;
  esac
done

# image-to-image: same flow on /images/edits with the reference in "image"
#   -d '{"model": "nano-banana-pro", "prompt": "replace the background with a starry sky", "image": "https://example.com/ref.png"}'
