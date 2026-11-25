# KovAPI API 示例 —— 一个 OpenAI 兼容接口调用对话、图像和视频模型

[![examples check](https://github.com/gaoorange/kovapi-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/gaoorange/kovapi-api-examples/actions/workflows/ci.yml)
[![DevHunt](https://img.shields.io/badge/DevHunt-KovAPI-orange)](https://devhunt.org/tool/kovapi)
[English README](README.md)

> KovAPI 是 NezhaGate 的新名字（2026-10-31 起）。原来的 API Key、余额和 `nezhagate.com` 的 API 地址都照常可用；没设 `KOVAPI_API_KEY` 时仍会读取 `NEZHAGATE_API_KEY`。

> **[KovAPI](https://kovapi.com/zh/)** 是 OpenAI 兼容的 AI 模型 API：一把 Key 调用 Claude、GPT、Gemini、DeepSeek、Grok 对话模型，以及 Seedance、Veo、可灵、Nano Banana、GPT Image 等图像和视频模型。把 `base_url` 换成 `https://kovapi.com/v1`，官方 `openai` SDK 照用。多数模型低于官方标价；按量计费，**请求失败不扣费**，图像 / 视频任务失败全额退。

## 30 秒上手

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://kovapi.com/v1")
resp = client.chat.completions.create(
    model="gpt-5.6-luna",             # 换模型只改这一个字段
    messages=[{"role": "user", "content": "用一句话解释什么是 OpenAI 兼容网关。"}],
)
print(resp.choices[0].message.content)
```

```bash
curl https://kovapi.com/v1/chat/completions \
  -H "Authorization: Bearer $KOVAPI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4-6", "messages": [{"role": "user", "content": "你好"}]}'
```

- **Base URL**：`https://kovapi.com/v1` —— 对话 `/chat/completions`（所有对话模型）与 `/responses`（GPT 模型），图像 `/images/generations` 与 `/images/edits`，视频 `/videos/generations`，路径与 OpenAI 一致。
- **API Key**：[kovapi.com](https://kovapi.com/zh/) 注册 → 控制台创建。
- **原生 Claude 口径**：`https://kovapi.com/anthropic` 同时提供 Anthropic Messages API（见下文），Claude Code 与 Anthropic SDK 无需改动。

## 模型

价格会变，所以这里不抄价格。实时价格看 [定价页](https://kovapi.com/zh/pricing)、[llms.txt](https://kovapi.com/zh/llms.txt) 或 JSON 接口 [`/api/pricing`](https://kovapi.com/api/pricing)；和官方价的逐项对比（每个价格都写了核对日期）在 [kovapi.com/zh/compare](https://kovapi.com/zh/compare)。下面每个模型 ID 都链到它的页面：参数、价格和在线试用。这里只列常用的，完整目录见 [模型市场](https://kovapi.com/zh/market)。

### 对话（`/v1/chat/completions`）

| 厂商 | 模型 ID |
| --- | --- |
| OpenAI | [`gpt-6-astra`](https://kovapi.com/zh/model/gpt-6-astra), [`gpt-6.1-sol`](https://kovapi.com/zh/model/gpt-6.1-sol), [`gpt-6-sol`](https://kovapi.com/zh/model/gpt-6-sol), [`gpt-5.6-luna`](https://kovapi.com/zh/model/gpt-5.6-luna) |
| Anthropic | [`claude-sonnet-4-6`](https://kovapi.com/zh/model/claude-sonnet-4-6), [`claude-opus-5-5`](https://kovapi.com/zh/model/claude-opus-5-5), [`claude-haiku-5-5`](https://kovapi.com/zh/model/claude-haiku-5-5), [`claude-fable-5-2`](https://kovapi.com/zh/model/claude-fable-5-2) |
| Google | [`gemini-3.8-flash`](https://kovapi.com/zh/model/gemini-3.8-flash), [`gemini-4-hydrogen`](https://kovapi.com/zh/model/gemini-4-hydrogen) |
| xAI | [`grok-4.7`](https://kovapi.com/zh/model/grok-4.7) |
| DeepSeek | [`deepseek-v4.1-flash`](https://kovapi.com/zh/model/deepseek-v4.1-flash) |

### 图像（`/v1/images/generations`、`/v1/images/edits`，异步任务）

| 厂商 | 模型 ID |
| --- | --- |
| OpenAI | [`gpt-image-2`](https://kovapi.com/zh/model/gpt-image-2), [`gpt-image-2.6-flare`](https://kovapi.com/zh/model/gpt-image-2.6-flare), [`gpt-image-2.6-sunburst`](https://kovapi.com/zh/model/gpt-image-2.6-sunburst) |
| Google | [`nano-banana-2.1`](https://kovapi.com/zh/model/nano-banana-2.1), [`nano-banana-pro`](https://kovapi.com/zh/model/nano-banana-pro), [`nano-banana-2`](https://kovapi.com/zh/model/nano-banana-2) |
| 字节跳动 | [`seedream-5.5`](https://kovapi.com/zh/model/seedream-5.5) |
| 快手 | [`kling-image-4.0`](https://kovapi.com/zh/model/kling-image-4.0) |
| Midjourney | [`midjourney`](https://kovapi.com/zh/model/midjourney) |

### 视频（`/v1/videos/generations`，异步任务）

| 厂商 | 模型 ID |
| --- | --- |
| 字节跳动 | [`seedance-2.5`](https://kovapi.com/zh/model/seedance-2.5), [`seedance-2.5-flash`](https://kovapi.com/zh/model/seedance-2.5-flash), [`seedance-2.0`](https://kovapi.com/zh/model/seedance-2.0) |
| Google | [`veo-3.1`](https://kovapi.com/zh/model/veo-3.1), [`gemini-omni-1.2-flash`](https://kovapi.com/zh/model/gemini-omni-1.2-flash) |
| 阿里巴巴 | [`wan3.0-video`](https://kovapi.com/zh/model/wan3.0-video) |
| MiniMax | [`minimax-h3`](https://kovapi.com/zh/model/minimax-h3) |
| xAI | [`grok-imagine-video-1.5`](https://kovapi.com/zh/model/grok-imagine-video-1.5) |

- `/v1/responses` 支持 GPT 模型；Claude 另有原生 `/anthropic` 接口（见下文）。
- 每个模型自己的参数（思考档位、思考开关、尺寸、时长、参考素材上限）写在 [docs.kovapi.com](https://docs.kovapi.com/zh/) 上它的文档页。
- 按秒计费的视频模型：费用 = 单价 × 时长，部分模型还会计入参考视频的时长，以模型页为准。图像 / 视频任务失败或超时全额退。
- 已下架的模型 ID 返回 HTTP 400 `model_disabled`，不扣费。新模型和调价见 [kovapi.com/zh/new](https://kovapi.com/zh/new)。

## 用原生 Anthropic 接口调 Claude

```bash
export ANTHROPIC_BASE_URL=https://kovapi.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # 就是 KovAPI 的 Key
# 模型：claude-sonnet-4-6 / claude-opus-5-5 / claude-haiku-5-5 / claude-fable-5-2 等
```

Claude Code 只需要这两行环境变量。用 Anthropic SDK 见 [`examples/claude_native.py`](examples/claude_native.py)（`POST /anthropic/v1/messages`，`max_tokens` 必填）。思考、工具调用与提示缓存原样透传；缓存读写按模型页上写的缓存价计费。

## 异步任务（图像与视频）

`POST /v1/images/generations`、`POST /v1/images/edits`、`POST /v1/videos/generations` 会立刻返回 **HTTP 202** 与任务号：

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

每隔几秒轮询 `GET /v1/images/jobs/{id}`（或 `/v1/videos/jobs/{id}`），直到 `status` 为 `succeeded`，再读取 `data[0].url`。图片几秒钟，视频一到几分钟（长片更久）。不要在提交后直接读 `data`；`failed` 的任务不计费。

**记得下载结果。** 生成的图片、视频（以及你上传的参考图）在 `img.kovapi.com` 保留 **7 天**，之后自动删除、链接失效。需要长期使用的请转存到你自己的存储。

## 错误格式

所有错误都是同一个信封。`code` 是稳定的机器可读标识——请按 `code` 分支，不要匹配 message 文本：

```json
{"error": {"message": "human readable", "type": "invalid_request_error", "code": "model_not_found", "param": "model"}}
```

| HTTP | `code` | 含义 |
| --- | --- | --- |
| 401 | `missing_api_key`、`invalid_api_key` | 没带 Key，或 Key 无效 / 已停用 |
| 402 | `insufficient_quota` | 余额不足，或 Key 超出限额 |
| 400 | `model_not_found`、`model_disabled`、`model_coming_soon` | 模型不存在、已下架、或已上架但尚未开放 |
| 400 | `invalid_messages`、`invalid_role`、`invalid_max_tokens`、`missing_prompt`、`invalid_json` | 请求在计费之前就被拒绝 |
| 400 | `max_tokens_too_small` | 思考模型在写出答案前就用完了预算——调大 `max_tokens`（建议 512 以上），本次不计费 |
| 404 | `job_not_found` | 任务号不存在，或不属于这把 Key |
| 429 | `rate_limit_exceeded` | 限流，或上游都已满载——按 `Retry-After` 重试 |
| 502 | `empty_completion`、`upstream_error` | 上游返回空响应或失败——不计费，可直接重试 |

## 查余额

任何 Key 都能查自己的余额与消费，无需登录控制台：

```bash
curl https://kovapi.com/v1/usage -H "Authorization: Bearer $KOVAPI_API_KEY"
```

也兼容 OpenAI 风格的 `GET /v1/dashboard/billing/credit_grants`，第三方客户端的余额显示可以直接读到。

## 本仓库示例

| 文件 | 说明 |
| --- | --- |
| [`examples/chat.sh`](examples/chat.sh) | curl：对话、流式、`reasoning_effort`，同一接口调 GPT、Claude、Gemini、DeepSeek、Grok |
| [`examples/chat_python.py`](examples/chat_python.py) | Python `openai` SDK：对话、推理强度与思考摘要、关闭 DeepSeek 思考、流式、图片输入 |
| [`examples/chat_node.mjs`](examples/chat_node.mjs) | Node.js `openai` SDK：对话、推理强度、流式 |
| [`examples/responses_api.py`](examples/responses_api.py) | OpenAI Responses API（`/v1/responses`）调 GPT-6，带思考摘要 |
| [`examples/claude_native.py`](examples/claude_native.py) | Anthropic SDK 直连 `/anthropic`（Claude Code 的走法） |
| [`examples/image_generation.py`](examples/image_generation.py) | 文生图与图生图：提交 → 轮询 → 直链 |
| [`examples/image_generation.mjs`](examples/image_generation.mjs) | 同上，Node.js |
| [`examples/image_generation.sh`](examples/image_generation.sh) | 同上，curl |
| [`examples/video_generation.py`](examples/video_generation.py) | Seedance / 万相 3.0 / MiniMax H3 / Grok Imagine：提交 → 轮询 → mp4 直链，文生与图生 |
| [`examples/video_generation.mjs`](examples/video_generation.mjs) | 同上，Node.js |
| [`examples/video_generation.sh`](examples/video_generation.sh) | 同上，curl |
| [`examples/langchain_chat.py`](examples/langchain_chat.py) | LangChain `ChatOpenAI` 改 `base_url` |

```bash
export KOVAPI_API_KEY=sk-xxxx      # 或复制 .env.example 为 .env
python examples/chat_python.py
```

示例只依赖 `openai` / `anthropic` / `requests`（Python）或 `openai`（Node）。CI 对每个文件做语法检查；仓库里永远不会出现任何 Key。

## 生态兼容

任何支持自定义 OpenAI Base URL 的工具都能直接接入：**Cursor、Claude Code、Codex、n8n、Dify、LangChain、Open WebUI、LobeChat、Cherry Studio、ChatBox** 等——Base URL 填 `https://kovapi.com/v1`，API Key 填控制台创建的 Key。

## FAQ 精选

**请求失败会扣费吗？** 不会。只有成功返回的调用才按实际用量结算，上游报错或超时不产生费用；图像 / 视频任务失败全额退。

**和官方 API 有什么区别？** 一个接口、一把 Key、一张账单覆盖所有模型，请求形状与 OpenAI 一致，多数模型价格低于官方标价（逐项对比见 [kovapi.com/zh/compare](https://kovapi.com/zh/compare)）。

**生成的图片和视频能保存多久？** 在 `img.kovapi.com` 保留 7 天，之后自动删除、链接失效——想留的请及时下载。调用日志里的文字内容保留 30 天。

**怎么看余额和用量？** 控制台有实时余额、每个 Key 的用量和逐条调用日志（模型、时间、token、花费）；任何 Key 调 `GET /v1/usage` 也能拿到同样的余额。模型页还有一条按真实网关流量计算的 24 小时成功率状态条。

更多：[kovapi.com/zh/faq](https://kovapi.com/zh/faq)

## 链接

- 官网：<https://kovapi.com/zh/> —— 另有 [English](https://kovapi.com/)、[Español](https://kovapi.com/es/)、[日本語](https://kovapi.com/ja/)、[한국어](https://kovapi.com/ko/)、[Русский](https://kovapi.com/ru/)
- 模型市场：<https://kovapi.com/zh/market>
- 定价：<https://kovapi.com/zh/pricing> · 比价：<https://kovapi.com/zh/compare>
- 文档：<https://docs.kovapi.com/zh/>
- FAQ：<https://kovapi.com/zh/faq>
- 给 AI 工具读的站点索引：<https://kovapi.com/zh/llms.txt> · [llms-full.txt](https://kovapi.com/llms-full.txt)
- 文档 MCP 服务器（只读、免 Key）：`https://kovapi.com/mcp`
- 本仓库的模型目录变更记录：[CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
