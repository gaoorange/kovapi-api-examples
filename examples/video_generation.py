"""NezhaGate video generation -- async job: submit -> poll -> mp4 url. The part most people get wrong.

One endpoint for every video model; the request body selects the mode:
  - no `image`          -> text-to-video
  - `image` (URL)       -> image-to-video, the image is the first frame (Wan 3.0 also takes a list, first+last frame,
                           multi-image reference or a reference video -- see the model page)
Common fields: prompt, duration (seconds, integer), resolution (480P / 720P / 1080P per model), size (aspect ratio).

Per-second models: seedance-2.5 (4-30 s), seedance-2.0 / -fast (5-15 s), wan3.0-video / -prime (2-30 s),
minimax-h3 (5-15 s, 1080P, native audio). Per-clip models: grok-imagine-video-1.5 (4-15 s), seedance-2.5-30s (30 s).
A failed or timed-out job is refunded in full. Clips take one to a few minutes; long clips longer.
The mp4 stays on img.nezhagate.com for 60 days -- download what you want to keep.

    pip install requests
    export NEZHAGATE_API_KEY=sk-xxxx
    python examples/video_generation.py
"""
import os
import time

import requests

BASE = "https://nezhagate.com/v1"
HEADERS = {"Authorization": "Bearer " + os.environ["NEZHAGATE_API_KEY"], "Content-Type": "application/json"}


def submit(body: dict) -> str:
    r = requests.post(f"{BASE}/videos/generations", headers=HEADERS, json=body, timeout=60)
    job = r.json()
    if r.status_code != 202:
        raise SystemExit(f"rejected ({r.status_code}): {job}")     # nothing was charged
    print("submitted:", job)                                        # {"id": "...", "object": "video.generation.job", "status": "queued"}
    return job["id"]


def wait_for(job_id: str, every: int = 5) -> dict:
    """Poll GET /v1/videos/jobs/{id}. Never read `data` right after submitting."""
    while True:
        time.sleep(every)
        j = requests.get(f"{BASE}/videos/jobs/{job_id}", headers=HEADERS, timeout=30).json()
        print("  status:", j.get("status"))
        if j.get("status") in ("succeeded", "failed", "cancelled"):
            return j


# 1) text-to-video, per-second billing: 8 s x $0.158 on seedance-2.5
job_id = submit({
    "model": "seedance-2.5",
    "prompt": "a cat surfing a wave at sunset, cinematic, golden hour",
    "duration": 8,
    "resolution": "720P",
    "size": "16:9",
})
done = wait_for(job_id)
print("video url:", done["data"][0]["url"] if done["status"] == "succeeded" else done)

# 2) image-to-video: add `image`; the picture becomes the first frame
job_id = submit({
    "model": "wan3.0-video",                     # or minimax-h3 / seedance-2.0 / grok-imagine-video-1.5 ...
    "prompt": "the logo slowly rotates while soft light sweeps across it",
    "image": "https://nezhagate.com/static/img/logo-mark.png",
    "duration": 5,
    "resolution": "720P",
    "size": "1:1",
})
done = wait_for(job_id)
print("video url:", done["data"][0]["url"] if done["status"] == "succeeded" else done)
