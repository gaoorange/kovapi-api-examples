#!/usr/bin/env bash
# NezhaGate video generation with curl -- async job: submit -> poll -> mp4 url.
#   export NEZHAGATE_API_KEY=sk-xxxx && bash examples/video_generation.sh
set -euo pipefail
BASE="https://nezhagate.com/v1"
: "${NEZHAGATE_API_KEY:?export NEZHAGATE_API_KEY first}"
AUTH="Authorization: Bearer $NEZHAGATE_API_KEY"

# 1) submit -> HTTP 202 {"id":"...","object":"video.generation.job","status":"queued"}
#    text-to-video; add  "image": "https://example.com/first-frame.png"  for image-to-video
JOB=$(curl -s "$BASE/videos/generations" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"model": "seedance-2.5", "prompt": "a cat surfing a wave at sunset, cinematic", "duration": 8, "resolution": "720P", "size": "16:9"}')
echo "submitted: $JOB"
ID=$(printf '%s' "$JOB" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

# 2) poll every ~5 s until status=succeeded, then read data[0].url (an mp4 kept for 60 days -- download it)
while :; do
  sleep 5
  R=$(curl -s "$BASE/videos/jobs/$ID" -H "$AUTH")
  S=$(printf '%s' "$R" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status"))')
  echo "  status: $S"
  case "$S" in
    succeeded) printf '%s' "$R" | python3 -c 'import json,sys; print("video url:", json.load(sys.stdin)["data"][0]["url"])'; break ;;
    failed|cancelled) echo "job ended (refunded in full): $R"; break ;;
  esac
done
