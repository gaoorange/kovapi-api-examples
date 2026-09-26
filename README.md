# NezhaGate API Examples — one OpenAI-compatible endpoint for GPT, Claude, Gemini, Grok, DeepSeek, Kimi, GLM, Qwen, image and video models

[![examples check](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml)
[中文说明 / Chinese README](README.zh-CN.md)

> **[NezhaGate](https://nezhagate.com/en/)** is an OpenAI-compatible AI model gateway. Point `base_url` at `https://nezhagate.com/v1`, keep the official `openai` SDK, and call GPT-6, GPT-5.6, Claude Opus 5, Gemini 3.8 Flash, Grok 4.7, DeepSeek V4.1 Flash, Kimi K3, GLM-5.3, Qwen3.7 Max, image models (GPT Image 2 / 2.5, Nano Banana) and video models (Seedance, Wan 3.0, MiniMax H3, Grok Imagine) through one endpoint and one API key. Pay-as-you-go; **failed requests are never billed**; video and image jobs that fail are refunded in full.

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

- **Base URL**: `https://nezhagate.com/v1` — chat `/chat/completions` (every chat model) and `/responses` (GPT and Gemini models), images `/images/generations` and `/images/edits`, video `/videos/generations`; paths match OpenAI.
- **API key**: sign up at [nezhagate.com](https://nezhagate.com/en/) → console → create a key.
- **Claude natively**: the Anthropic Messages API is also served at `https://nezhagate.com/anthropic` (see below), so Claude Code and the Anthropic SDK work unchanged.

## Models

Prices are a **snapshot taken 2026-09-26 (USD)**; the live numbers are on the [pricing page](https://nezhagate.com/en/pricing) and in [llms.txt](https://nezhagate.com/en/llms.txt). Every model id links to its page with parameters and a playground.

### Chat (`/v1/chat/completions`) — per 1M tokens, input / output

| Model | Provider | NezhaGate | Official list | Notes |
| --- | --- | --- | --- | --- |
| [`gpt-6-astra`](https://nezhagate.com/en/model/gpt-6-astra) | OpenAI | $1.00 / $5.00 | $10 / $50 | GPT-6 flagship: 1.05M context, 128K output, `reasoning_effort` low → max |
| [`gpt-6-sol`](https://nezhagate.com/en/model/gpt-6-sol) | OpenAI | $0.20 / $1.00 | $2 / $10 | complex coding and agentic workflows |
| [`gpt-6-luna`](https://nezhagate.com/en/model/gpt-6-luna) | OpenAI | $0.07 / $0.40 | $0.1 / $0.5 | high-volume, low-latency steps |
| [`gpt-5.6-sol`](https://nezhagate.com/en/model/gpt-5.6-sol) | OpenAI | $0.40 / $2.00 | $4 / $20 | frontier reasoning, agentic coding |
| [`gpt-5.6-terra`](https://nezhagate.com/en/model/gpt-5.6-terra) | OpenAI | $0.20 / $1.20 | $2 / $12 | balanced everyday model |
| [`gpt-5.6-luna`](https://nezhagate.com/en/model/gpt-5.6-luna) | OpenAI | $0.07 / $0.40 | $0.2 / $1.2 | fast and economical |
| [`gpt-5.5`](https://nezhagate.com/en/model/gpt-5.5) | OpenAI | $0.50 / $3.00 | $5 / $30 | chat + reasoning |
| [`claude-opus-5`](https://nezhagate.com/en/model/claude-opus-5) | Anthropic | $4.00 / $20.00 | — | adaptive thinking, tool use, vision, prompt caching ($0.40 cache read) |
| [`claude-fable-5`](https://nezhagate.com/en/model/claude-fable-5) | Anthropic | $8.00 / $40.00 | — | Fable series, narrative and long-form writing |
| [`claude-sonnet-4-6`](https://nezhagate.com/en/model/claude-sonnet-4-6) | Anthropic | $1.50 / $7.50 | $3 / $15 | balanced chat + code |
| [`gemini-3.1-pro`](https://nezhagate.com/en/model/gemini-3.1-pro) | Google | $0.50 / $3.00 | $2 / $12 | low tier by default; `reasoning_effort=high` → $0.50 / $3.20 |
| [`gemini-3.8-flash`](https://nezhagate.com/en/model/gemini-3.8-flash) | Google | $0.60 / $3.60 | $0.75 / $3.75 | latest Flash, 1M context, adaptive thinking |
| [`gemini-3.7-flash`](https://nezhagate.com/en/model/gemini-3.7-flash) | Google | $0.60 / $3.60 | $0.75 / $3.75 | previous Flash, same price |
| [`gemini-3.6-flash`](https://nezhagate.com/en/model/gemini-3.6-flash) | Google | $0.60 / $3.60 | — | four thinking tiers: `-high` / `-low` / `-tiered`, same price |
| [`gemini-3-flash-preview`](https://nezhagate.com/en/model/gemini-3-flash-preview) | Google | $0.30 / $1.20 | $0.5 / $3 | high throughput |
| [`gemini-2.5-flash`](https://nezhagate.com/en/model/gemini-2.5-flash) | Google | $0.30 / $1.20 | $0.3 / $2.5 | multimodal input |
| [`grok-4.7`](https://nezhagate.com/en/model/grok-4.7) | xAI | $0.30 / $0.90 | $2 / $6 | always thinks; tools, JSON schema, vision; `stop` is not supported |
| [`deepseek-v4.1-flash`](https://nezhagate.com/en/model/deepseek-v4.1-flash) | DeepSeek | $0.09 / $0.36 | $0.15 / $0.6 | thinking on by default, `thinking: {"type": "disabled"}` turns it off |
| [`deepseek-v4-flash-0731`](https://nezhagate.com/en/model/deepseek-v4-flash-0731) | DeepSeek | $0.045 / $0.18 | $0.15 / $0.6 | pinned 0731 version, cheapest chat model on the site |
| [`glm-5.3`](https://nezhagate.com/en/model/glm-5.3) | Z.ai | $0.34 / $1.25 | $1.4 / $4.4 | coding, agents, Chinese and English writing |
| [`glm-5.3-flash`](https://nezhagate.com/en/model/glm-5.3-flash) | Z.ai | $0.072 / $0.25 | $0.15 / $0.5 | high-volume classification, extraction, rewriting |
| [`kimi-k3`](https://nezhagate.com/en/model/kimi-k3) | Moonshot | $1.80 / $9.00 | $3 / $15 | long documents, multi-document analysis, agents |
| [`qwen3.7-max`](https://nezhagate.com/en/model/qwen3.7-max) | Alibaba | $1.65 / $4.85 | $2.5 / $7.5 | reasoning, coding, agents, long context |

- **`/v1/responses`** serves the GPT and Gemini models; the rest are `/v1/chat/completions` only (Claude is also native at `/anthropic`). Cache-read prices are on the [pricing page](https://nezhagate.com/en/pricing).
- **Thinking**: `reasoning_effort` works on GPT, Claude and `gemini-3.1-pro`. GPT-6, Grok, DeepSeek, GLM, Kimi and Qwen return their reasoning in `message.reasoning_content`; thinking tokens bill at the output rate inside `usage.completion_tokens`.
- **Ignored parameters**: GPT models ignore `temperature`, `top_p`, `max_tokens` / `max_completion_tokens` and the penalty parameters (silently, no error) — steer them with `reasoning_effort` and the prompt, and send images as base64 `data:` URIs. Claude Opus 5 drops `temperature` / `top_p` / `top_k`; Kimi K3 uses a fixed temperature.

### Images (`/v1/images/generations`, `/v1/images/edits`) — per image, 1K / 2K / 4K

| Model | NezhaGate | Notes |
| --- | --- | --- |
| [`gpt-image-2`](https://nezhagate.com/en/model/gpt-image-2) | $0.005 / $0.01 / $0.02 | text-to-image and image-to-image, seven native aspect ratios |
| [`gpt-image-2.5-flare`](https://nezhagate.com/en/model/gpt-image-2.5-flare) | $0.005 / $0.01 / $0.02 | GPT Image 2.5, clean and smooth style branch; C2PA content credential |
| [`gpt-image-2.5-sunburst`](https://nezhagate.com/en/model/gpt-image-2.5-sunburst) | $0.005 / $0.01 / $0.02 | GPT Image 2.5, heavier grain and brushwork; same price as Flare |
| [`nano-banana-2`](https://nezhagate.com/en/model/nano-banana-2) | $0.025 / $0.0375 / $0.0625 | Gemini 3.1 Flash Image, fast |
| [`nano-banana-pro`](https://nezhagate.com/en/model/nano-banana-pro) | $0.040 / $0.060 / $0.100 | Gemini 3 Pro Image, flagship quality |

`size` takes an aspect ratio (`1:1`, `3:4`, `2:3`, `9:16`, `4:3`, `3:2`, `16:9`) rendered natively, or a pixel size such as `1024x1536`. For image-to-image add `image` (public URL, `data:` URI or base64) — or call `/images/edits`; `images` takes several references at once.

### Video (`/v1/videos/generations`, async jobs)

| Model | Price | Duration | Resolutions | Notes |
| --- | --- | --- | --- | --- |
| [`seedance-2.5`](https://nezhagate.com/en/model/seedance-2.5) | $0.158 / s | 4–30 s | 480P, 720P | native audio (switchable), up to 9 reference images |
| [`seedance-2.5-30s`](https://nezhagate.com/en/model/seedance-2.5-30s) | $1.50 / clip | fixed 30 s | 720P | long take in one clip, up to 9 reference images |
| [`seedance-2.0`](https://nezhagate.com/en/model/seedance-2.0) | $0.12 (480P) / $0.15 (720P) per s | 5–15 s | 480P, 720P | standard tier; 1080P coming soon |
| [`seedance-2.0-fast`](https://nezhagate.com/en/model/seedance-2.0-fast) | $0.075 / s | 5–15 s | 720P | fastest, cheapest Seedance |
| [`wan3.0-video`](https://nezhagate.com/en/model/wan3.0-video) | $0.09 / $0.12 / $0.16 per s | 2–30 s | 480P, 720P, 1080P | text / first frame / first+last / up to 10 references / video rewrite |
| [`wan3.0-video-prime`](https://nezhagate.com/en/model/wan3.0-video-prime) | $0.12 / $0.16 / $0.20 per s | 2–30 s | 480P, 720P, 1080P | same model, faster queue |
| [`minimax-h3`](https://nezhagate.com/en/model/minimax-h3) | $0.036 / s | 5–15 s | 1080P | native audio always on, cheapest per second |
| [`grok-imagine-video-1.5`](https://nezhagate.com/en/model/grok-imagine-video-1.5) | $0.30 (480P) / $0.40 (720P) per clip | 4–15 s | 480P, 720P | up to 7 reference images (2+ cap the clip at 10 s) |

Per-second models bill `rate × duration` (Wan 3.0 also adds the declared length of any reference video). Failed or timed-out jobs are refunded in full.

### Coming soon and retired

- **Coming soon**: [`veo-3.1`](https://nezhagate.com/en/model/veo-3.1) (video) and the 1080P tier of `seedance-2.0` have pages and API references but are not callable yet: the request is rejected with HTTP 400 `model_coming_soon` and nothing is charged.
- **Retired**: `gemini-3.5-flash` (use `gemini-3.7-flash`) and `seedance-2.0-mini` (use `seedance-2.0-fast`) now return HTTP 400 `model_disabled`. Full history in [CHANGELOG.md](CHANGELOG.md).

## Claude through the native Anthropic API

```bash
export ANTHROPIC_BASE_URL=https://nezhagate.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # the same NezhaGate key
# models: claude-opus-5 / claude-fable-5 / claude-sonnet-4-6
```

That is all Claude Code needs. With the Anthropic SDK see [`examples/claude_native.py`](examples/claude_native.py) (`POST /anthropic/v1/messages`, `max_tokens` required). Thinking, tool use and prompt caching pass through unchanged; a cache read bills at 1/10 of the input rate.

## Async jobs (images and video)

`POST /v1/images/generations`, `POST /v1/images/edits` and `POST /v1/videos/generations` return **HTTP 202** with a job id right away:

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

Poll `GET /v1/images/jobs/{id}` (or `/v1/videos/jobs/{id}`) every few seconds until `status` is `succeeded`, then read `data[0].url`. Images take seconds, clips one to a few minutes (long clips longer). Never read `data` straight after submitting; a `failed` job is not billed.

**Download your results.** Generated images and videos (and any reference images you upload) are kept on `img.nezhagate.com` for **60 days**, then deleted; after that the link stops working. Copy anything you need long-term to your own storage.

## Errors

Every error uses one envelope. `code` is stable and machine-readable — branch on it, never on the message text:

```json
{"error": {"message": "human readable", "type": "invalid_request_error", "code": "model_not_found", "param": "model"}}
```

| HTTP | `code` | Meaning |
| --- | --- | --- |
| 401 | `missing_api_key`, `invalid_api_key` | no key, or the key is invalid or disabled |
| 402 | `insufficient_quota` | balance too low, or the key is over its cap |
| 400 | `model_not_found`, `model_disabled`, `model_coming_soon` | unknown id, retired model, or listed but not open yet |
| 400 | `invalid_messages`, `invalid_role`, `invalid_max_tokens`, `missing_prompt`, `invalid_json` | request rejected before anything is billed |
| 400 | `max_tokens_too_small` | a thinking model spent the whole budget before answering — raise `max_tokens` (512+); not billed |
| 404 | `job_not_found` | no such job, or it belongs to another key |
| 429 | `rate_limit_exceeded` | rate limited or every line is at capacity — retry after `Retry-After` |
| 502 | `empty_completion`, `upstream_error` | the upstream returned nothing or failed — not billed, safe to retry |

## Check your balance

Any key can read its own balance and spend, no console login needed:

```bash
curl https://nezhagate.com/v1/usage -H "Authorization: Bearer $NEZHAGATE_API_KEY"
```

The OpenAI-style `GET /v1/dashboard/billing/credit_grants` works too, so balance widgets in third-party clients pick it up.

## Examples in this repo

| File | What it shows |
| --- | --- |
| [`examples/chat.sh`](examples/chat.sh) | curl: chat, streaming, `reasoning_effort`; GPT, Claude, Gemini, DeepSeek and Grok through the same endpoint |
| [`examples/chat_python.py`](examples/chat_python.py) | Python `openai` SDK: chat, reasoning effort + reasoning summary, switching DeepSeek thinking off, streaming, vision input |
| [`examples/chat_node.mjs`](examples/chat_node.mjs) | Node.js `openai` SDK: chat, reasoning effort, streaming |
| [`examples/responses_api.py`](examples/responses_api.py) | the OpenAI Responses API (`/v1/responses`) on GPT-6 with a reasoning summary |
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

**How long are generated images and videos kept?** 60 days on `img.nezhagate.com`, then they are deleted and the link stops working — download what you want to keep. The text content in your call logs is kept for 15 days.

**How do I see balance and usage?** The console shows the live balance, per-key usage and a per-call log (model, time, tokens, cost); `GET /v1/usage` returns the same balance to any key. Model pages also show a public 24-hour success-rate bar computed from real gateway traffic.

More: [nezhagate.com/en/faq](https://nezhagate.com/en/faq)

## Links

- Home: <https://nezhagate.com/en/> — also in [中文](https://nezhagate.com/), [Español](https://nezhagate.com/es/), [日本語](https://nezhagate.com/ja/) and [한국어](https://nezhagate.com/ko/)
- Models: <https://nezhagate.com/en/market>
- Pricing: <https://nezhagate.com/en/pricing>
- Integration guide: <https://nezhagate.com/en/docs-guide>
- FAQ: <https://nezhagate.com/en/faq>
- llms.txt for AI tools: <https://nezhagate.com/en/llms.txt> · [llms-full.txt](https://nezhagate.com/llms-full.txt)
- Changelog of the model catalogue: [CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
