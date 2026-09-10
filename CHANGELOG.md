# Changelog — NezhaGate model catalogue and this repo

Dates are the day a change went live on [nezhagate.com](https://nezhagate.com/en/). Prices in the README are a snapshot; the [pricing page](https://nezhagate.com/en/pricing) is authoritative.

## 2026-09-10

- Repo refreshed for the current catalogue: README (English) + README.zh-CN, per-kind examples in Python / Node / curl, a native-Anthropic example, this changelog and a syntax-check CI.
- Site: `gpt-6`, `gpt-image-2.5` and `veo-3.1` listed as **coming soon** (pages and API references live; calls are rejected and never billed).
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
