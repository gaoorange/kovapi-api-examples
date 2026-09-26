# Changelog — NezhaGate model catalogue and this repo

Dates are the day a change went live on [nezhagate.com](https://nezhagate.com/en/). Prices in the README are a snapshot; the [pricing page](https://nezhagate.com/en/pricing) is authoritative.

## 2026-09-26

- Repo refreshed: README + README.zh-CN price snapshot of 2026-09-26 with GPT-6, Grok, DeepSeek, GLM, Kimi and Qwen, the error codes, the balance endpoint and a Responses API example; the chat examples now show reasoning summaries and the DeepSeek thinking switch.
- Site: generated images and videos (and uploaded reference images) are kept for **60 days**, then deleted; the text content of call logs is kept for 15 days. Download results you want to keep.
- Site: the `seedance-2.5-30s` page shows a live status badge (running / busy / paused). While it is paused, new orders are refused with `model_coming_soon` and never billed.

## 2026-09-25

- `seedance-2.5-30s` back on sale: $1.50 per 30-second 720P clip, up to 9 reference images.
- A thinking model that spends its whole `max_tokens` budget before answering now returns HTTP 400 `max_tokens_too_small` (not billed) instead of an empty reply.

## 2026-09-24

- GPT-6 family: `gpt-6-sol` and `gpt-6-luna` launched next to `gpt-6-astra`.
- GPT chat models repriced to about 1/10 of the official list: `gpt-6-astra` $1.00 / $5.00, `gpt-6-sol` $0.20 / $1.00, `gpt-5.6-sol` $0.40 / $2.00, `gpt-5.6-terra` $0.20 / $1.20, `gpt-5.5` $0.50 / $3.00; both Luna models $0.07 / $0.40.
- New chat models: `deepseek-v4.1-flash`, `deepseek-v4-flash-0731`, `glm-5.3`, `glm-5.3-flash`, `kimi-k3` and `qwen3.7-max`.
- `grok-4.7` (xAI) launched at $0.30 / $0.90.

## 2026-09-23

- `seedance-2.0-mini` retired; use `seedance-2.0-fast`.

## 2026-09-17

- GPT image prices cut: `gpt-image-2`, `gpt-image-2.5-flare` and `gpt-image-2.5-sunburst` now cost $0.005 / $0.01 / $0.02 per image (1K / 2K / 4K).

## 2026-09-16

- One error envelope on every endpoint, `{"error": {"message", "type", "code", "param"}}`, with stable `code` values. Malformed requests (bad `max_tokens`, `messages` or `role`, a missing `prompt`) are rejected before anything is billed.
- `gemini-3.5-flash` retired (use `gemini-3.7-flash`); retired ids return HTTP 400 `model_disabled`.

## 2026-09-12

- Site in Spanish (`/es`) and Japanese (`/ja`).

## 2026-09-11

- GPT Image 2.5 launched as two style branches, `gpt-image-2.5-flare` and `gpt-image-2.5-sunburst` (there is no bare `gpt-image-2.5` id), at the GPT Image 2 price.
- Site in Korean (`/ko`).
- `seedance-2.5-30s` paused when its upstream went away; back on 2026-09-25.

## 2026-09-10

- Repo refreshed for the current catalogue: README (English) + README.zh-CN, per-kind examples in Python / Node / curl, a native-Anthropic example, this changelog and a syntax-check CI.
- Site: `gpt-6`, `gpt-image-2.5` and `veo-3.1` listed as **coming soon** (pages and API references live; calls are rejected and never billed).
- `gpt-6-astra` (GPT-6) launched later the same day, at $2.80 / $14.00 (see 2026-09-24). The `gpt-6` placeholder id keeps working as an alias.
- `minimax-h3` price halved to $0.036 per second.
- Site: every model page now shows a public 24-hour status bar computed from real gateway traffic.
- Site: English pages fully English (model cards, market blurbs, docs); `x-default` now points at the English pages.

## 2026-09-08

- `wan3.0-video` and `wan3.0-video-prime` (Alibaba Wan 3.0) launched: 2–30 s, 480P / 720P / 1080P, text / first-frame / first+last-frame / multi-image / video-rewrite on one endpoint, billed per second.
- Seedance family reorganised: `seedance-2.5` (4–30 s), `seedance-2.0` (5–15 s, 480P–1080P), `seedance-2.0-fast`, `seedance-2.0-mini`, plus the fixed-length `seedance-2.5-30s` clip tier.

## 2026-09-06

- `grok-imagine-video-1.5` launched — the first per-clip video model ($0.30 at 480P / $0.40 at 720P, 4–15 s).

## 2026-09-04

- `gemini-3.8-flash` and `gemini-3.7-flash` launched at $0.60 / $3.60 per 1M tokens.

## 2026-08-09

- `minimax-h3` (Hailuo 03) launched: 1080P, native audio, 5–15 s, billed per second.

## 2026-08-08

- `claude-opus-5` and `claude-fable-5` launched, with the native Anthropic Messages API at `/anthropic`.

## 2026-07-28

- `gemini-3.6-flash` family launched (Medium / High / Low / Tiered thinking budgets, same price).
- `claude-opus-4-8` and `claude-haiku-4-5` retired.

## 2026-07-23

- `gpt-5.4` and `gpt-5.4-mini` retired.

## 2026-07-16

- `gpt-5.6-sol` / `gpt-5.6-terra` / `gpt-5.6-luna` launched.

## 2026-07-05

- Initial release of this repository.
