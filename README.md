# KovAPI API Examples — one OpenAI-compatible endpoint for chat, image and video models

[![examples check](https://github.com/gaoorange/kovapi-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/gaoorange/kovapi-api-examples/actions/workflows/ci.yml)
[![DevHunt](https://img.shields.io/badge/DevHunt-KovAPI-orange)](https://devhunt.org/tool/kovapi)
[中文说明 / Chinese README](README.zh-CN.md)

> KovAPI is the new name of NezhaGate (since 2026-10-31). API keys, balances and the `nezhagate.com` API address keep working, and `NEZHAGATE_API_KEY` is still read when `KOVAPI_API_KEY` is not set.

> **[KovAPI](https://kovapi.com/)** is an OpenAI-compatible API for AI models: one key for Claude, GPT, Gemini, DeepSeek and Grok chat, plus image and video models such as Seedance, Veo, Kling, Nano Banana and GPT Image. Point `base_url` at `https://kovapi.com/v1` and keep the official `openai` SDK. Most models cost less than the official list price; pay as you go; **failed requests are never billed**, and image and video jobs that fail are refunded in full.

## 30-second quickstart

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://kovapi.com/v1")
resp = client.chat.completions.create(
    model="gpt-5.6-luna",             # switching models = changing this one string
    messages=[{"role": "user", "content": "Explain OpenAI-compatible gateways in one sentence."}],
)
print(resp.choices[0].message.content)
```

```bash
curl https://kovapi.com/v1/chat/completions \
  -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "Hello"}]}'
```

- **Base URL**: `https://kovapi.com/v1` — chat `/chat/completions` (every chat model) and `/responses` (GPT models), images `/images/generations` and `/images/edits`, video `/videos/generations`; paths match OpenAI.
- **API key**: sign up at [kovapi.com](https://kovapi.com/) → console → create a key.
- **Claude natively**: the Anthropic Messages API is also served at `https://kovapi.com/anthropic` (see below), so Claude Code and the Anthropic SDK work unchanged.

## Models

Prices change, so this README does not copy them. Live prices are on the [pricing page](https://kovapi.com/pricing), in [llms.txt](https://kovapi.com/llms.txt) and as JSON at [`/api/pricing`](https://kovapi.com/api/pricing); official list prices next to ours, each with the date it was checked, are at [kovapi.com/compare](https://kovapi.com/compare). Each id below links to its page with parameters, prices and a playground. This is a selection: the full catalogue is on the [model market](https://kovapi.com/market).

### Chat (`/v1/chat/completions`)

| Vendor | Model ids |
| --- | --- |
| OpenAI | [`gpt-6-astra`](https://kovapi.com/model/gpt-6-astra), [`gpt-6.1-sol`](https://kovapi.com/model/gpt-6.1-sol), [`gpt-6-sol`](https://kovapi.com/model/gpt-6-sol), [`gpt-5.6-luna`](https://kovapi.com/model/gpt-5.6-luna) |
| Anthropic | [`claude-sonnet-4-6`](https://kovapi.com/model/claude-sonnet-4-6), [`claude-opus-5-5`](https://kovapi.com/model/claude-opus-5-5), [`claude-haiku-5-5`](https://kovapi.com/model/claude-haiku-5-5), [`claude-fable-5-2`](https://kovapi.com/model/claude-fable-5-2) |
| Google | [`gemini-3.8-flash`](https://kovapi.com/model/gemini-3.8-flash), [`gemini-4-hydrogen`](https://kovapi.com/model/gemini-4-hydrogen) |
| xAI | [`grok-4.7`](https://kovapi.com/model/grok-4.7) |
| DeepSeek | [`deepseek-v4.1-flash`](https://kovapi.com/model/deepseek-v4.1-flash) |

### Images (`/v1/images/generations`, `/v1/images/edits`, async jobs)

| Vendor | Model ids |
| --- | --- |
| OpenAI | [`gpt-image-2`](https://kovapi.com/model/gpt-image-2), [`gpt-image-2.6-flare`](https://kovapi.com/model/gpt-image-2.6-flare), [`gpt-image-2.6-sunburst`](https://kovapi.com/model/gpt-image-2.6-sunburst) |
| Google | [`nano-banana-2.1`](https://kovapi.com/model/nano-banana-2.1), [`nano-banana-pro`](https://kovapi.com/model/nano-banana-pro), [`nano-banana-2`](https://kovapi.com/model/nano-banana-2) |
| ByteDance | [`seedream-5.5`](https://kovapi.com/model/seedream-5.5) |
| Kuaishou | [`kling-image-4.0`](https://kovapi.com/model/kling-image-4.0) |
| Midjourney | [`midjourney`](https://kovapi.com/model/midjourney) |

### Video (`/v1/videos/generations`, async jobs)

| Vendor | Model ids |
| --- | --- |
| ByteDance | [`seedance-2.5`](https://kovapi.com/model/seedance-2.5), [`seedance-2.5-flash`](https://kovapi.com/model/seedance-2.5-flash), [`seedance-2.0`](https://kovapi.com/model/seedance-2.0) |
| Google | [`veo-3.1`](https://kovapi.com/model/veo-3.1), [`gemini-omni-1.2-flash`](https://kovapi.com/model/gemini-omni-1.2-flash) |
| Alibaba | [`wan3.0-video`](https://kovapi.com/model/wan3.0-video) |
| MiniMax | [`minimax-h3`](https://kovapi.com/model/minimax-h3) |
| xAI | [`grok-imagine-video-1.5`](https://kovapi.com/model/grok-imagine-video-1.5) |

- `/v1/responses` serves the GPT models; Claude is also native at `/anthropic` (see below).
- Model-specific parameters (reasoning effort levels, thinking switches, sizes, durations, reference limits) are on each model's docs page at [docs.kovapi.com](https://docs.kovapi.com/).
- Per-second video models bill rate × duration, and some also bill the length of reference videos; the model page says which. Failed or timed-out image and video jobs are refunded in full.
- A retired model id returns HTTP 400 `model_disabled` and is never billed. New models and price changes: [kovapi.com/new](https://kovapi.com/new).

## Claude through the native Anthropic API

```bash
export ANTHROPIC_BASE_URL=https://kovapi.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # the same KovAPI key
# models: claude-sonnet-4-6 / claude-opus-5-5 / claude-haiku-5-5 / claude-fable-5-2 ...
```

That is all Claude Code needs. With the Anthropic SDK see [`examples/claude_native.py`](examples/claude_native.py) (`POST /anthropic/v1/messages`, `max_tokens` required). Thinking, tool use and prompt caching pass through unchanged; cache reads and writes bill at the model's cache rates shown on its page.

## Async jobs (images and video)

`POST /v1/images/generations`, `POST /v1/images/edits` and `POST /v1/videos/generations` return **HTTP 202** with a job id right away:

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

Poll `GET /v1/images/jobs/{id}` (or `/v1/videos/jobs/{id}`) every few seconds until `status` is `succeeded`, then read `data[0].url`. Images take seconds, clips one to a few minutes (long clips longer). Never read `data` straight after submitting; a `failed` job is not billed.

**Download your results.** Generated images and videos (and any reference images you upload) are kept on `img.kovapi.com` for **7 days**, then deleted; after that the link stops working. Copy anything you need long-term to your own storage.

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
| 429 | `rate_limit_exceeded` | rate limited, or every upstream is at capacity — retry after `Retry-After` |
| 502 | `empty_completion`, `upstream_error` | the upstream returned nothing or failed — not billed, safe to retry |

## Check your balance

Any key can read its own balance and spend, no console login needed:

```bash
curl https://kovapi.com/v1/usage -H "Authorization: Bearer $KOVAPI_API_KEY"
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
export KOVAPI_API_KEY=sk-xxxx      # or copy .env.example to .env
python examples/chat_python.py
```

The examples only need `openai` / `anthropic` / `requests` (Python) or `openai` (Node). CI runs a syntax check on every file; no key is ever stored in this repository.

## Works with

Anything that lets you set an OpenAI base URL: **Cursor, Claude Code, Codex, n8n, Dify, LangChain, Open WebUI, LobeChat, Cherry Studio, ChatBox** and more — set Base URL to `https://kovapi.com/v1` and paste a key from the console.

## FAQ highlights

**Am I charged for failed requests?** No. Only calls that return successfully are settled on actual usage; upstream errors and timeouts cost nothing, and failed image or video jobs are refunded in full.

**How is this different from the official APIs?** One endpoint, one key, one bill for every model, with OpenAI-compatible request shapes, and prices below the official list for most models ([kovapi.com/compare](https://kovapi.com/compare)).

**How long are generated images and videos kept?** 7 days on `img.kovapi.com`, then they are deleted and the link stops working — download what you want to keep. The text content in your call logs is kept for 30 days.

**How do I see balance and usage?** The console shows the live balance, per-key usage and a per-call log (model, time, tokens, cost); `GET /v1/usage` returns the same balance to any key. Model pages also show a public 24-hour success-rate bar computed from real gateway traffic.

More: [kovapi.com/faq](https://kovapi.com/faq)

## Links

- Home: <https://kovapi.com/> — also in [中文](https://kovapi.com/zh/), [Español](https://kovapi.com/es/), [日本語](https://kovapi.com/ja/), [한국어](https://kovapi.com/ko/) and [Русский](https://kovapi.com/ru/)
- Models: <https://kovapi.com/market>
- Pricing: <https://kovapi.com/pricing> · price comparison: <https://kovapi.com/compare>
- Docs: <https://docs.kovapi.com/>
- FAQ: <https://kovapi.com/faq>
- llms.txt for AI tools: <https://kovapi.com/llms.txt> · [llms-full.txt](https://kovapi.com/llms-full.txt)
- Docs MCP server (read-only, no key): `https://kovapi.com/mcp`
- Catalogue changes for this repo: [CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
