// NezhaGate video generation in Node.js -- async job: submit -> poll -> mp4 url (plain fetch, no SDK).
//   export NEZHAGATE_API_KEY=sk-xxxx
//   node examples/video_generation.mjs
const BASE = "https://nezhagate.com/v1";
const HEADERS = {
  Authorization: "Bearer " + process.env.NEZHAGATE_API_KEY,
  "Content-Type": "application/json",
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function submit(body) {
  const r = await fetch(`${BASE}/videos/generations`, { method: "POST", headers: HEADERS, body: JSON.stringify(body) });
  const job = await r.json();
  if (r.status !== 202) throw new Error(`rejected (${r.status}): ${JSON.stringify(job)}`); // nothing was charged
  console.log("submitted:", job); // {"id": "...", "object": "video.generation.job", "status": "queued"}
  return job.id;
}

async function waitFor(jobId, everyMs = 5000) {
  // Poll GET /v1/videos/jobs/{id}; never read `data` right after submitting.
  for (;;) {
    await sleep(everyMs);
    const j = await (await fetch(`${BASE}/videos/jobs/${jobId}`, { headers: HEADERS })).json();
    console.log("  status:", j.status);
    if (["succeeded", "failed", "cancelled"].includes(j.status)) return j;
  }
}

// 1) text-to-video, billed per second (8 s on seedance-2.5)
let id = await submit({
  model: "seedance-2.5",
  prompt: "a cat surfing a wave at sunset, cinematic, golden hour",
  duration: 8,
  resolution: "720P",
  size: "16:9",
});
let done = await waitFor(id);
console.log(done.status === "succeeded" ? "video url: " + done.data[0].url : done);

// 2) image-to-video: add `image`, the picture becomes the first frame
id = await submit({
  model: "minimax-h3", // 1080P with native audio; or wan3.0-video / seedance-2.0 / grok-imagine-video-1.5
  prompt: "the logo slowly rotates while soft light sweeps across it",
  image: "https://nezhagate.com/static/img/logo-mark.png",
  duration: 5,
  resolution: "1080P",
  size: "1:1",
});
done = await waitFor(id);
console.log(done.status === "succeeded" ? "video url: " + done.data[0].url : done);
