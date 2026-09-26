// NezhaGate image generation in Node.js -- async job: submit -> poll -> url (no SDK needed, plain fetch).
//   export NEZHAGATE_API_KEY=sk-xxxx
//   node examples/image_generation.mjs
const BASE = "https://nezhagate.com/v1";
const HEADERS = {
  Authorization: "Bearer " + process.env.NEZHAGATE_API_KEY,
  "Content-Type": "application/json",
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitFor(jobId) {
  // Poll GET /v1/images/jobs/{id} until the job leaves the queue; images usually take seconds.
  for (;;) {
    await sleep(3000);
    const j = await (await fetch(`${BASE}/images/jobs/${jobId}`, { headers: HEADERS })).json();
    console.log("  status:", j.status);
    if (["succeeded", "failed", "cancelled"].includes(j.status)) return j;
  }
}

// 1) text-to-image -> HTTP 202 {"id": "img_...", "status": "queued"}
let job = await (await fetch(`${BASE}/images/generations`, {
  method: "POST",
  headers: HEADERS,
  body: JSON.stringify({
    model: "gpt-image-2",                        // or gpt-image-2.5-flare / nano-banana-2 / nano-banana-pro
    prompt: "a serene ink-wash poster, lots of negative space",
    size: "3:4",
    resolution: "1K",
  }),
})).json();
console.log("submitted:", job);
let done = await waitFor(job.id);
console.log(done.status === "succeeded" ? "image url: " + done.data[0].url : done); // kept for 60 days, download it

// 2) image-to-image on /images/edits: the reference goes in `image`
job = await (await fetch(`${BASE}/images/edits`, {
  method: "POST",
  headers: HEADERS,
  body: JSON.stringify({
    model: "nano-banana-pro",
    prompt: "replace the background with a starry sky",
    image: "https://nezhagate.com/static/img/logo-mark.png",
    size: "1:1",
  }),
})).json();
console.log("submitted:", job);
done = await waitFor(job.id);
console.log(done.status === "succeeded" ? "image url: " + done.data[0].url : done);
