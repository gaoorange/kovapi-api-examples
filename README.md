# NezhaGate API Examples — one OpenAI-compatible endpoint for GPT, Claude, Gemini, image and video models

[![examples check](https://github.com/leizhenfacai/nezhagate-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/leizhenfacai/nezhagate-api-examples/actions/workflows/ci.yml)
[中文说明 / Chinese README](README.zh-CN.md)

> **[NezhaGate](https://nezhagate.com/en/)** is an OpenAI-compatible AI model gateway. Point `base_url` at `https://nezhagate.com/v1`, keep the official `openai` SDK, and call GPT-5.6, GPT-5.5, Claude Opus 5, Gemini 3.8 Flash, image models (GPT Image 2, Nano Banana) and video models (Seedance, Wan 3.0, MiniMax H3, Grok Imagine) through one endpoint and one API key. Pay-as-you-go; **failed requests are never billed**; video and image jobs that fail are refunded in full.

## 30-second quickstart

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://nezhagate.com/v1")
resp = client.chat.completions.create(
    model="gpt-5.6-terra",            # switching models = changing this one string
    messages=[{"role": "user", "content": "Explain OpenAI-compatible gateways in one sentence."}],
)
print(resp.choices[0].message.content)
```

```bash
curl https://nezhagate.com/v1/chat/completions \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "claude-opus-5", "messages": [{"role": "user", "content": "Hello"}]}'
```

- **Base URL**: `https://nezhagate.com/v1` — chat `/chat/completions` and `/responses`, images `/images/generations` and `/images/edits`, video `/videos/generations`; paths match OpenAI.
- **API key**: sign up at [nezhagate.com](https://nezhagate.com/en/) → console → create a key.
- **Claude natively**: the Anthropic Messages API is also served at `https://nezhagate.com/anthropic` (see below), so Claude Code and the Anthropic SDK work unchanged.

## Models

Prices are a **snapshot taken 2026-09-10 (USD)**; the live numbers are on the [pricing page](https://nezhagate.com/en/pricing) and in [llms.txt](https://nezhagate.com/en/llms.txt). Every model id links to its page with parameters, a playground and a 24-hour status bar.

### Chat (`/v1/chat/completions`, `/v1/responses`) — per 1M tokens, input / output

| Model | NezhaGate | Official list | Notes |
| --- | --- | --- | --- |
| [`gpt-5.6-sol`](https://nezhagate.com/en/model/gpt-5.6-sol) | $2.00 / $12.00 | $8 / $48 | frontier flagship, agentic coding, `reasoning_effort` |
| [`gpt-5.6-terra`](https://nezhagate.com/en/model/gpt-5.6-terra) | $1.20 / $7.00 | $5 / $30 | balanced everyday model |
| [`gpt-5.6-luna`](https://nezhagate.com/en/model/gpt-5.6-luna) | $0.80 / $4.80 | $2.5 / $15 | fast and economical |
| [`gpt-5.5`](https://nezhagate.com/en/model/gpt-5.5) | $0.70 / $4.20 | $5 / $30 | flagship chat + reasoning |
| [`claude-opus-5`](https://nezhagate.com/en/model/claude-opus-5) | $4.00 / $20.00 | — | adaptive thinking, tool use, vision, prompt caching ($0.40 cache read) |
| [`claude-fable-5`](https://nezhagate.com/en/model/claude-fable-5) | $8.00 / $40.00 | — | Fable series, narrative and long-form writing |
| [`claude-sonnet-4-6`](https://nezhagate.com/en/model/claude-sonnet-4-6) | $1.50 / $7.50 | $3 / $15 | balanced chat + code |
| [`gemini-3.1-pro`](https://nezhagate.com/en/model/gemini-3.1-pro) | $0.50 / $3.00 | $2 / $12 | low tier default; `reasoning_effort=high` → $0.50 / $3.20 |
| [`gemini-3.8-flash`](https://nezhagate.com/en/model/gemini-3.8-flash) | $0.60 / $3.60 | $0.75 / $3.75 | latest Flash, 1M context, adaptive thinking |
| [`gemini-3.7-flash`](https://nezhagate.com/en/model/gemini-3.7-flash) | $0.60 / $3.60 | $0.75 / $3.75 | previous Flash, same price |
| [`gemini-3.6-flash`](https://nezhagate.com/en/model/gemini-3.6-flash) | $0.60 / $3.60 | — | four thinking tiers: `-high` / `-low` / `-tiered`, same price |
| [`gemini-3.5-flash`](https://nezhagate.com/en/model/gemini-3.5-flash) | $0.45 / $2.70 | $1.5 / $9 | fast thinking model |
| [`gemini-3-flash-preview`](https://nezhagate.com/en/model/gemini-3-flash-preview) | $0.30 / $1.20 | $0.5 / $3 | high throughput |
| [`gemini-2.5-flash`](https://nezhagate.com/en/model/gemini-2.5-flash) | $0.30 / $1.20 | $0.3 / $2.5 | multimodal input |

### Images (`/v1/images/generations`, `/v1/images/edits`) — per image, 1K / 2K / 4K

| Model | NezhaGate | Notes |
| --- | --- | --- |
| [`gpt-image-2`](https://nezhagate.com/en/model/gpt-image-2) | $0.015 / $0.025 / $0.040 | text-to-image and image-to-image |
| [`nano-banana-2`](https://nezhagate.com/en/model/nano-banana-2) | $0.025 / $0.0375 / $0.0625 | Gemini 3.1 Flash Image, fast |
| [`nano-banana-pro`](https://nezhagate.com/en/model/nano-banana-pro) | $0.040 / $0.060 / $0.100 | Gemini 3 Pro Image, flagship quality |

### Video (`/v1/videos/generations`, async jobs)

| Model | Billing | Duration | Resolutions | Notes |
| --- | --- | --- | --- | --- |
| [`seedance-2.5`](https://nezhagate.com/en/model/seedance-2.5) | $0.158 / s | 4–30 s | 480P, 720P | native audio, up to 9 reference images |
| [`seedance-2.5-30s`](https://nezhagate.com/en/model/seedance-2.5-30s) | $1.50 / clip | fixed 30 s | 720P | long-form tier |
| [`seedance-2.0`](https://nezhagate.com/en/model/seedance-2.0) | $0.15 / s | 5–15 s | 480P, 720P, 1080P | standard tier |
| [`seedance-2.0-fast`](https://nezhagate.com/en/model/seedance-2.0-fast) | $0.10 / s | 5–15 s | 480P, 720P | fastest, cheapest Seedance |
| [`seedance-2.0-mini`](https://nezhagate.com/en/model/seedance-2.0-mini) | $0.066 / s | 5–15 s | 720P | entry tier |
| [`wan3.0-video`](https://nezhagate.com/en/model/wan3.0-video) | $0.12 / s (720P) | 2–30 s | 480P, 720P, 1080P | text / first frame / first+last / multi-image / video rewrite |
| [`wan3.0-video-prime`](https://nezhagate.com/en/model/wan3.0-video-prime) | $0.16 / s (720P) | 2–30 s | 480P, 720P, 1080P | same model, faster queue |
| [`minimax-h3`](https://nezhagate.com/en/model/minimax-h3) | $0.072 / s | 5–15 s | 1080P | native audio always on |
| [`grok-imagine-video-1.5`](https://nezhagate.com/en/model/grok-imagine-video-1.5) | $0.30 (480P) / $0.40 (720P) per clip | 4–15 s | 480P, 720P | cheapest clip on the site |

Per-second models bill `rate × duration` (Wan 3.0 also adds the declared length of any reference video). Failed or timed-out jobs are refunded in full.

### Coming soon

[`gpt-6`](https://nezhagate.com/en/model/gpt-6) (chat), [`gpt-image-2.5`](https://nezhagate.com/en/model/gpt-image-2.5) (images) and [`veo-3.1`](https://nezhagate.com/en/model/veo-3.1) (video) have pages and API references but are not callable yet; a request is rejected with HTTP 400 and nothing is charged.

## Claude through the native Anthropic API

```bash
export ANTHROPIC_BASE_URL=https://nezhagate.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # the same NezhaGate key
# models: claude-opus-5 / claude-fable-5 / claude-sonnet-4-6
```

That is all Claude Code needs. With the Anthropic SDK see [`examples/claude_native.py`](examples/claude_native.py) (`POST /anthropic/v1/messages`, `max_tokens` required).

## Async jobs (images and video)

`POST /v1/images/generations`, `POST /v1/images/edits` and `POST /v1/videos/generations` return **HTTP 202** with a job id right away:

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

Poll `GET /v1/images/jobs/{id}` (or `/v1/videos/jobs/{id}`) every few seconds until `status` is `succeeded`, then read `data[0].url` — a stable, re-hosted link. Images take seconds, clips one to a few minutes (long clips longer). Never read `data` straight after submitting; a `failed` job is not billed.

## Examples in this repo

| File | What it shows |
| --- | --- |
| [`examples/chat.sh`](examples/chat.sh) | curl: chat, streaming, `reasoning_effort`, Claude and Gemini through the same endpoint |
| [`examples/chat_python.py`](examples/chat_python.py) | Python `openai` SDK: chat, streaming, reasoning effort, vision input |
| [`examples/chat_node.mjs`](examples/chat_node.mjs) | Node.js `openai` SDK: chat and streaming |
| [`examples/claude_native.py`](examples/claude_native.py) | Anthropic SDK against `/anthropic` (what Claude Code does) |
| [`examples/image_generation.py`](examples/image_generation.py) | text-to-image and image-to-image, submit → poll → url |
| [`examples/image_generation.mjs`](examples/image_generation.mjs) | the same flow in Node.js |
| [`examples/image_generation.sh`](examples/image_generation.sh) | the same flow with curl |
| [`examples/video_generation.py`](examples/video_generation.py) | Seedance / Wan 3.0 / MiniMax H3 / Grok Imagine: submit → poll → mp4 url, text- and image-to-video |
| [`examples/video_generation.mjs`](examples/video_generation.mjs) | the same flow in Node.js |
| [`examples/video_generation.sh`](examples/video_generation.sh) | the same flow with curl |
| [`examples/langchain_chat.py`](examples/langchain_chat.py) | LangChain `ChatOpenAI` with a custom `base_url` |

```bash
export NEZHAGATE_API_KEY=sk-xxxx      # or copy .env.example to .env
python examples/chat_python.py
```

The examples only need `openai` / `anthropic` / `requests` (Python) or `openai` (Node). CI runs a syntax check on every file; no key is ever stored in this repository.

## Works with

Anything that lets you set an OpenAI base URL: **Cursor, Claude Code, Codex, n8n, Dify, LangChain, Open WebUI, LobeChat, Cherry Studio, ChatBox** and more — set Base URL to `https://nezhagate.com/v1` and paste a key from the console.

## FAQ highlights

**Am I charged for failed requests?** No. Only calls that return successfully are settled on actual usage; upstream errors and timeouts cost nothing, and failed image or video jobs are refunded in full.

**How is this different from the official APIs?** One endpoint, one key, one bill for every model, with OpenAI-compatible request shapes, and prices below the official list for most chat models (table above).

**How do I see balance and usage?** The console shows the live balance, per-key usage and a per-call log (model, time, tokens, cost). Every model page carries a public 24-hour status bar computed from real gateway traffic.

More: [nezhagate.com/en/faq](https://nezhagate.com/en/faq)

## Links

- Home: <https://nezhagate.com/en/>
- Models: <https://nezhagate.com/en/market>
- Pricing: <https://nezhagate.com/en/pricing>
- Integration guide: <https://nezhagate.com/en/docs-guide>
- FAQ: <https://nezhagate.com/en/faq>
- llms.txt for AI tools: <https://nezhagate.com/en/llms.txt> · [llms-full.txt](https://nezhagate.com/llms-full.txt)
- Changelog of the model catalogue: [CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
