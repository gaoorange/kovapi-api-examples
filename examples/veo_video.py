"""NezhaGate Veo 3.1 video generation — async job: submit -> poll -> mp4 url.

One model, parameter-controlled: no `image` = text-to-video, with `image` (first frame)
= image-to-video. tier=lite/fast/quality, resolution=720p/1080p (1080p quality-tier only),
size=16:9/9:16, duration=4s/6s/8s. Per-clip billing, full refund on failure.

    export NEZHAGATE_API_KEY=sk-xxxx
    python veo_video.py
"""
import os
import time

import requests

BASE = "https://nezhagate.com/v1"
HEADERS = {
    "Authorization": "Bearer " + os.environ["NEZHAGATE_API_KEY"],
    "Content-Type": "application/json",
}

# 1) submit -> HTTP 202 {"id": "...", "status": "queued"}
job = requests.post(f"{BASE}/videos/generations", headers=HEADERS, json={
    "model": "veo-3.1",
    "prompt": "a cat surfing a wave at sunset, cinematic",
    "tier": "quality",
    "resolution": "1080p",
    "size": "16:9",
    "duration": "8s",
    # "image": "https://example.com/first-frame.png",   # uncomment for image-to-video
}, timeout=60).json()
print("submitted:", job)

# 2) poll every ~5s (a clip takes ~1-2 min); result in data[0].url (re-hosted mp4)
while True:
    time.sleep(5)
    j = requests.get(f"{BASE}/videos/jobs/{job['id']}", headers=HEADERS, timeout=30).json()
    print("status:", j.get("status"))
    if j.get("status") == "succeeded":
        print("video url:", j["data"][0]["url"])
        break
    if j.get("status") in ("failed", "cancelled"):
        print("job ended:", j)   # failed clips are fully refunded
        break
