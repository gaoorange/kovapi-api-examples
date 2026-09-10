# NezhaGate API 示例 — 一个 OpenAI 兼容接口调用 GPT / Claude / Gemini / 图像 / 视频模型

[![examples check](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml)
[English README](README.md)

> **[NezhaGate](https://nezhagate.com)** 是 OpenAI 兼容的 AI 模型网关：把 `base_url` 换成 `https://nezhagate.com/v1`，官方 `openai` SDK 一行业务代码不改，用一个接口、一把 Key 调用 GPT-5.6、GPT-5.5、Claude Opus 5、Gemini 3.8 Flash、图像模型（GPT Image 2、Nano Banana）与视频模型（Seedance、通义万相 3.0、MiniMax H3、Grok Imagine）。按量计费，**请求失败不扣费**，图像 / 视频任务失败全额退。

## 30 秒上手

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://nezhagate.com/v1")
resp = client.chat.completions.create(
    model="gpt-5.6-terra",            # 换模型只改这一个字段
    messages=[{"role": "user", "content": "用一句话解释什么是 OpenAI 兼容网关。"}],
)
print(resp.choices[0].message.content)
```

```bash
curl https://nezhagate.com/v1/chat/completions \
  -H "Authorization: Bearer $NEZHAGATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "claude-opus-5", "messages": [{"role": "user", "content": "你好"}]}'
```

- **Base URL**：`https://nezhagate.com/v1` —— 对话 `/chat/completions` 与 `/responses`，图像 `/images/generations` 与 `/images/edits`，视频 `/videos/generations`，路径与 OpenAI 一致。
- **API Key**：[nezhagate.com](https://nezhagate.com) 注册 → 控制台创建。
- **原生 Claude 口径**：`https://nezhagate.com/anthropic` 同时提供 Anthropic Messages API（见下文），Claude Code 与 Anthropic SDK 无需改动。

## 模型

价格为 **2026-09-10 快照（USD）**，实时价格以 [定价页](https://nezhagate.com/pricing) 与 [llms.txt](https://nezhagate.com/llms.txt) 为准。每个模型 ID 都链到它的页面：参数、在线试用、24 小时状态条。

### 对话（`/v1/chat/completions`、`/v1/responses`）—— 每百万 token，输入 / 输出

| 模型 | NezhaGate | 官方标价 | 说明 |
| --- | --- | --- | --- |
| [`gpt-5.6-sol`](https://nezhagate.com/model/gpt-5.6-sol) | $2.00 / $12.00 | $8 / $48 | 前沿旗舰，Agentic 编程，支持 `reasoning_effort` |
| [`gpt-5.6-terra`](https://nezhagate.com/model/gpt-5.6-terra) | $1.20 / $7.00 | $5 / $30 | 日常均衡款 |
| [`gpt-5.6-luna`](https://nezhagate.com/model/gpt-5.6-luna) | $0.80 / $4.80 | $2.5 / $15 | 快而省 |
| [`gpt-5.5`](https://nezhagate.com/model/gpt-5.5) | $0.70 / $4.20 | $5 / $30 | 旗舰对话与推理 |
| [`claude-opus-5`](https://nezhagate.com/model/claude-opus-5) | $4.00 / $20.00 | — | 自适应思考、工具调用、图片理解、提示缓存（缓存读 $0.40） |
| [`claude-fable-5`](https://nezhagate.com/model/claude-fable-5) | $8.00 / $40.00 | — | Fable 系列，叙事与长文写作 |
| [`claude-sonnet-4-6`](https://nezhagate.com/model/claude-sonnet-4-6) | $1.50 / $7.50 | $3 / $15 | 均衡的对话与代码 |
| [`gemini-3.1-pro`](https://nezhagate.com/model/gemini-3.1-pro) | $0.50 / $3.00 | $2 / $12 | 默认低推理档；`reasoning_effort=high` → $0.50 / $3.20 |
| [`gemini-3.8-flash`](https://nezhagate.com/model/gemini-3.8-flash) | $0.60 / $3.60 | $0.75 / $3.75 | 最新 Flash，1M 上下文，动态思考 |
| [`gemini-3.7-flash`](https://nezhagate.com/model/gemini-3.7-flash) | $0.60 / $3.60 | $0.75 / $3.75 | 上一代 Flash，同价 |
| [`gemini-3.6-flash`](https://nezhagate.com/model/gemini-3.6-flash) | $0.60 / $3.60 | — | 四档思考预算 `-high` / `-low` / `-tiered`，同价 |
| [`gemini-3.5-flash`](https://nezhagate.com/model/gemini-3.5-flash) | $0.45 / $2.70 | $1.5 / $9 | 高速思考模型 |
| [`gemini-3-flash-preview`](https://nezhagate.com/model/gemini-3-flash-preview) | $0.30 / $1.20 | $0.5 / $3 | 高吞吐 |
| [`gemini-2.5-flash`](https://nezhagate.com/model/gemini-2.5-flash) | $0.30 / $1.20 | $0.3 / $2.5 | 多模态输入 |

### 图像（`/v1/images/generations`、`/v1/images/edits`）—— 每张，1K / 2K / 4K

| 模型 | NezhaGate | 说明 |
| --- | --- | --- |
| [`gpt-image-2`](https://nezhagate.com/model/gpt-image-2) | $0.015 / $0.025 / $0.040 | 文生图 + 图生图 |
| [`nano-banana-2`](https://nezhagate.com/model/nano-banana-2) | $0.025 / $0.0375 / $0.0625 | Gemini 3.1 Flash Image，出图快 |
| [`nano-banana-pro`](https://nezhagate.com/model/nano-banana-pro) | $0.040 / $0.060 / $0.100 | Gemini 3 Pro Image，旗舰画质 |

### 视频（`/v1/videos/generations`，异步任务）

| 模型 | 计费 | 时长 | 分辨率 | 说明 |
| --- | --- | --- | --- | --- |
| [`seedance-2.5`](https://nezhagate.com/model/seedance-2.5) | $0.158 / 秒 | 4–30 秒 | 480P、720P | 原生音轨，最多 9 张参考图 |
| [`seedance-2.5-30s`](https://nezhagate.com/model/seedance-2.5-30s) | $1.50 / 条 | 固定 30 秒 | 720P | 长片档 |
| [`seedance-2.0`](https://nezhagate.com/model/seedance-2.0) | $0.15 / 秒 | 5–15 秒 | 480P、720P、1080P | 标准档 |
| [`seedance-2.0-fast`](https://nezhagate.com/model/seedance-2.0-fast) | $0.10 / 秒 | 5–15 秒 | 480P、720P | 最快最省的 Seedance |
| [`seedance-2.0-mini`](https://nezhagate.com/model/seedance-2.0-mini) | $0.066 / 秒 | 5–15 秒 | 720P | 入门档 |
| [`wan3.0-video`](https://nezhagate.com/model/wan3.0-video) | $0.12 / 秒（720P） | 2–30 秒 | 480P、720P、1080P | 文生 / 首帧 / 首尾帧 / 多图参考 / 视频改写 |
| [`wan3.0-video-prime`](https://nezhagate.com/model/wan3.0-video-prime) | $0.16 / 秒（720P） | 2–30 秒 | 480P、720P、1080P | 同模型，更快队列 |
| [`minimax-h3`](https://nezhagate.com/model/minimax-h3) | $0.072 / 秒 | 5–15 秒 | 1080P | 固定生成原生音频 |
| [`grok-imagine-video-1.5`](https://nezhagate.com/model/grok-imagine-video-1.5) | $0.30（480P）/ $0.40（720P）每条 | 4–15 秒 | 480P、720P | 站内最便宜的视频 |

按秒模型的费用 = 单价 × 时长（万相 3.0 另加参考视频的声明时长）。失败或超时的任务全额退款。

### 即将上线

[`gpt-6`](https://nezhagate.com/model/gpt-6)（对话）、[`gpt-image-2.5`](https://nezhagate.com/model/gpt-image-2.5)（图像）、[`veo-3.1`](https://nezhagate.com/model/veo-3.1)（视频）已有模型页与 API 文档，但暂未开放调用：请求会被拒绝（HTTP 400）且不产生任何扣费。

## 用原生 Anthropic 接口调 Claude

```bash
export ANTHROPIC_BASE_URL=https://nezhagate.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # 就是 NezhaGate 的 Key
# 模型：claude-opus-5 / claude-fable-5 / claude-sonnet-4-6
```

Claude Code 只需要这两行环境变量。用 Anthropic SDK 见 [`examples/claude_native.py`](examples/claude_native.py)（`POST /anthropic/v1/messages`，`max_tokens` 必填）。

## 异步任务（图像与视频）

`POST /v1/images/generations`、`POST /v1/images/edits`、`POST /v1/videos/generations` 会立刻返回 **HTTP 202** 与任务号：

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

每隔几秒轮询 `GET /v1/images/jobs/{id}`（或 `/v1/videos/jobs/{id}`），直到 `status` 为 `succeeded`，再读取 `data[0].url`（重托管的稳定直链）。图片几秒钟，视频一到几分钟（长片更久）。不要在提交后直接读 `data`；`failed` 的任务不计费。

## 本仓库示例

| 文件 | 说明 |
| --- | --- |
| [`examples/chat.sh`](examples/chat.sh) | curl：对话、流式、`reasoning_effort`，同一接口调 Claude 与 Gemini |
| [`examples/chat_python.py`](examples/chat_python.py) | Python `openai` SDK：对话、流式、推理强度、图片输入 |
| [`examples/chat_node.mjs`](examples/chat_node.mjs) | Node.js `openai` SDK：对话与流式 |
| [`examples/claude_native.py`](examples/claude_native.py) | Anthropic SDK 直连 `/anthropic`（Claude Code 的走法） |
| [`examples/image_generation.py`](examples/image_generation.py) | 文生图与图生图：提交 → 轮询 → 直链 |
| [`examples/image_generation.mjs`](examples/image_generation.mjs) | 同上，Node.js |
| [`examples/image_generation.sh`](examples/image_generation.sh) | 同上，curl |
| [`examples/video_generation.py`](examples/video_generation.py) | Seedance / 万相 3.0 / MiniMax H3 / Grok Imagine：提交 → 轮询 → mp4 直链，文生与图生 |
| [`examples/video_generation.mjs`](examples/video_generation.mjs) | 同上，Node.js |
| [`examples/video_generation.sh`](examples/video_generation.sh) | 同上，curl |
| [`examples/langchain_chat.py`](examples/langchain_chat.py) | LangChain `ChatOpenAI` 改 `base_url` |

```bash
export NEZHAGATE_API_KEY=sk-xxxx      # 或复制 .env.example 为 .env
python examples/chat_python.py
```

示例只依赖 `openai` / `anthropic` / `requests`（Python）或 `openai`（Node）。CI 对每个文件做语法检查；仓库里永远不会出现任何 Key。

## 生态兼容

任何支持自定义 OpenAI Base URL 的工具都能直接接入：**Cursor、Claude Code、Codex、n8n、Dify、LangChain、Open WebUI、LobeChat、Cherry Studio、ChatBox** 等——Base URL 填 `https://nezhagate.com/v1`，API Key 填控制台创建的 Key。

## FAQ 精选

**请求失败会扣费吗？** 不会。只有成功返回的调用才按实际用量结算，上游报错或超时不产生费用；图像 / 视频任务失败全额退。

**和官方 API 有什么区别？** 一个接口、一把 Key、一张账单覆盖所有模型，请求形状与 OpenAI 一致，多数对话模型价格低于官方标价（见上表）。

**怎么看余额和用量？** 控制台有实时余额、每个 Key 的用量和逐条调用日志（模型、时间、token、花费）。每个模型页都有一条按真实网关流量计算的 24 小时状态条。

更多：[nezhagate.com/faq](https://nezhagate.com/faq)

## 链接

- 官网：<https://nezhagate.com>
- 模型市场：<https://nezhagate.com/market>
- 定价：<https://nezhagate.com/pricing>
- 接入文档：<https://nezhagate.com/docs-guide>
- FAQ：<https://nezhagate.com/faq>
- 给 AI 工具读的站点索引：<https://nezhagate.com/llms.txt> · [llms-full.txt](https://nezhagate.com/llms-full.txt)
- 模型目录变更记录：[CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
