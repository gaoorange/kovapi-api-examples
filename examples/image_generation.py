"""NezhaGate image generation (Nano Banana Pro) — async job: submit -> poll -> url.

Text-to-image needs only `prompt`; pass `image` (URL / data: URI / base64) to switch to
true image-to-image. `size` accepts aspect ratios (1:1, 3:4, 2:3, 9:16, 4:3, 3:2, 16:9)
or pixel sizes (1024x1024 / 1024x1536 / ...). Failed jobs are never billed.

    export NEZHAGATE_API_KEY=sk-xxxx
    python image_generation.py
"""
import os
import time

import requests

BASE = "https://nezhagate.com/v1"
HEADERS = {
    "Authorization": "Bearer " + os.environ["NEZHAGATE_API_KEY"],
    "Content-Type": "application/json",
}

# 1) submit -> HTTP 202 {"id": "img_...", "status": "queued"}
job = requests.post(f"{BASE}/images/generations", headers=HEADERS, json={
    "model": "nano-banana-pro",       # or: nano-banana-2 / gpt-image-2
    "prompt": "a serene ink-wash poster, lots of negative space",
    "size": "3:4",
    # "image": "https://example.com/ref.png",   # uncomment for image-to-image
}, timeout=60).json()
print("submitted:", job)

# 2) poll until succeeded, result in data[0].url (re-hosted, stable link)
while True:
    time.sleep(5)
    j = requests.get(f"{BASE}/images/jobs/{job['id']}", headers=HEADERS, timeout=30).json()
    print("status:", j.get("status"))
    if j.get("status") == "succeeded":
        print("image url:", j["data"][0]["url"])
        break
    if j.get("status") in ("failed", "cancelled"):
        print("job ended:", j)   # failed jobs are not billed
        break
