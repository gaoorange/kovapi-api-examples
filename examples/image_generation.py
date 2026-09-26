"""NezhaGate image generation -- async job: submit -> poll -> url.

Text-to-image needs only `prompt`. Image-to-image: POST /images/edits with `image` (a public URL, a data: URI or
raw base64) and a prompt; `images` takes several references. `size` accepts aspect ratios (1:1, 3:4, 2:3, 9:16, 4:3,
3:2, 16:9) or pixel sizes such as 1024x1024 / 1024x1536; `resolution` is 1K (default), 2K or 4K.
Models: gpt-image-2 / gpt-image-2.5-flare / gpt-image-2.5-sunburst / nano-banana-2 / nano-banana-pro.
Failed jobs are never billed. Results stay on img.nezhagate.com for 60 days -- download what you want to keep.

    pip install requests
    export NEZHAGATE_API_KEY=sk-xxxx
    python examples/image_generation.py
"""
import os
import time

import requests

BASE = "https://nezhagate.com/v1"
HEADERS = {"Authorization": "Bearer " + os.environ["NEZHAGATE_API_KEY"], "Content-Type": "application/json"}


def wait_for(job_id: str) -> dict:
    """Poll GET /v1/images/jobs/{id} until the job leaves the queue. Images usually take seconds."""
    while True:
        time.sleep(3)
        j = requests.get(f"{BASE}/images/jobs/{job_id}", headers=HEADERS, timeout=30).json()
        print("  status:", j.get("status"))
        if j.get("status") in ("succeeded", "failed", "cancelled"):
            return j


# 1) text-to-image -> HTTP 202 {"id": "img_...", "object": "image.generation.job", "status": "queued"}
job = requests.post(f"{BASE}/images/generations", headers=HEADERS, json={
    "model": "gpt-image-2",                     # or gpt-image-2.5-flare / nano-banana-2 / nano-banana-pro
    "prompt": "a serene ink-wash poster, lots of negative space",
    "size": "3:4",
    "resolution": "1K",
}, timeout=60).json()
print("submitted:", job)
done = wait_for(job["id"])
if done["status"] == "succeeded":
    print("image url:", done["data"][0]["url"])      # kept for 60 days, download it
else:
    print("job ended:", done)                       # not billed

# 2) image-to-image: same flow on /images/edits, the reference goes in `image`
job = requests.post(f"{BASE}/images/edits", headers=HEADERS, json={
    "model": "nano-banana-pro",
    "prompt": "replace the background with a starry sky",
    "image": "https://nezhagate.com/static/img/logo-mark.png",
    "size": "1:1",
}, timeout=60).json()
print("submitted:", job)
done = wait_for(job["id"])
print("result:", done["data"][0]["url"] if done["status"] == "succeeded" else done)
