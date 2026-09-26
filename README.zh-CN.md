# NezhaGate API 示例 — 一个 OpenAI 兼容接口调用 GPT / Claude / Gemini / Grok / DeepSeek / Kimi / GLM / Qwen / 图像 / 视频模型

[![examples check](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/gaoorange/nezhagate-api-examples/actions/workflows/ci.yml)
[English README](README.md)

> **[NezhaGate](https://nezhagate.com)** 是 OpenAI 兼容的 AI 模型网关：把 `base_url` 换成 `https://nezhagate.com/v1`，官方 `openai` SDK 一行业务代码不改，用一个接口、一把 Key 调用 GPT-6、GPT-5.6、Claude Opus 5、Gemini 3.8 Flash、Grok 4.7、DeepSeek V4.1 Flash、Kimi K3、GLM-5.3、Qwen3.7 Max、图像模型（GPT Image 2 / 2.5、Nano Banana）与视频模型（Seedance、通义万相 3.0、MiniMax H3、Grok Imagine）。按量计费，**请求失败不扣费**，图像 / 视频任务失败全额退。

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

- **Base URL**：`https://nezhagate.com/v1` —— 对话 `/chat/completions`（所有对话模型）与 `/responses`（GPT 与 Gemini 模型），图像 `/images/generations` 与 `/images/edits`，视频 `/videos/generations`，路径与 OpenAI 一致。
- **API Key**：[nezhagate.com](https://nezhagate.com) 注册 → 控制台创建。
- **原生 Claude 口径**：`https://nezhagate.com/anthropic` 同时提供 Anthropic Messages API（见下文），Claude Code 与 Anthropic SDK 无需改动。

## 模型

价格为 **2026-09-26 快照（USD）**，实时价格以 [定价页](https://nezhagate.com/pricing) 与 [llms.txt](https://nezhagate.com/llms.txt) 为准。每个模型 ID 都链到它的页面：参数说明与在线试用。

### 对话（`/v1/chat/completions`）—— 每百万 token，输入 / 输出

| 模型 | 厂商 | NezhaGate | 官方标价 | 说明 |
| --- | --- | --- | --- | --- |
| [`gpt-6-astra`](https://nezhagate.com/model/gpt-6-astra) | OpenAI | $1.00 / $5.00 | $10 / $50 | GPT-6 旗舰：105 万上下文、最高 12.8 万输出，`reasoning_effort` 从 low 到 max |
| [`gpt-6-sol`](https://nezhagate.com/model/gpt-6-sol) | OpenAI | $0.20 / $1.00 | $2 / $10 | 复杂编码与 Agentic 工作流 |
| [`gpt-6-luna`](https://nezhagate.com/model/gpt-6-luna) | OpenAI | $0.07 / $0.40 | $0.1 / $0.5 | 大批量、低延迟 |
| [`gpt-5.6-sol`](https://nezhagate.com/model/gpt-5.6-sol) | OpenAI | $0.40 / $2.00 | $4 / $20 | 前沿推理，Agentic 编程 |
| [`gpt-5.6-terra`](https://nezhagate.com/model/gpt-5.6-terra) | OpenAI | $0.20 / $1.20 | $2 / $12 | 日常均衡款 |
| [`gpt-5.6-luna`](https://nezhagate.com/model/gpt-5.6-luna) | OpenAI | $0.07 / $0.40 | $0.2 / $1.2 | 快而省 |
| [`gpt-5.5`](https://nezhagate.com/model/gpt-5.5) | OpenAI | $0.50 / $3.00 | $5 / $30 | 对话与推理 |
| [`claude-opus-5`](https://nezhagate.com/model/claude-opus-5) | Anthropic | $4.00 / $20.00 | — | 自适应思考、工具调用、图片理解、提示缓存（缓存读 $0.40） |
| [`claude-fable-5`](https://nezhagate.com/model/claude-fable-5) | Anthropic | $8.00 / $40.00 | — | Fable 系列，叙事与长文写作 |
| [`claude-sonnet-4-6`](https://nezhagate.com/model/claude-sonnet-4-6) | Anthropic | $1.50 / $7.50 | $3 / $15 | 均衡的对话与代码 |
| [`gemini-3.1-pro`](https://nezhagate.com/model/gemini-3.1-pro) | Google | $0.50 / $3.00 | $2 / $12 | 默认低推理档；`reasoning_effort=high` → $0.50 / $3.20 |
| [`gemini-3.8-flash`](https://nezhagate.com/model/gemini-3.8-flash) | Google | $0.60 / $3.60 | $0.75 / $3.75 | 最新 Flash，1M 上下文，动态思考 |
| [`gemini-3.7-flash`](https://nezhagate.com/model/gemini-3.7-flash) | Google | $0.60 / $3.60 | $0.75 / $3.75 | 上一代 Flash，同价 |
| [`gemini-3.6-flash`](https://nezhagate.com/model/gemini-3.6-flash) | Google | $0.60 / $3.60 | — | 四档思考预算 `-high` / `-low` / `-tiered`，同价 |
| [`gemini-3-flash-preview`](https://nezhagate.com/model/gemini-3-flash-preview) | Google | $0.30 / $1.20 | $0.5 / $3 | 高吞吐 |
| [`gemini-2.5-flash`](https://nezhagate.com/model/gemini-2.5-flash) | Google | $0.30 / $1.20 | $0.3 / $2.5 | 多模态输入 |
| [`grok-4.7`](https://nezhagate.com/model/grok-4.7) | xAI | $0.30 / $0.90 | $2 / $6 | 始终思考；工具调用、JSON Schema、识图；不支持 `stop` |
| [`deepseek-v4.1-flash`](https://nezhagate.com/model/deepseek-v4.1-flash) | DeepSeek | $0.09 / $0.36 | $0.15 / $0.6 | 默认开启思考，传 `thinking: {"type": "disabled"}` 关闭 |
| [`deepseek-v4-flash-0731`](https://nezhagate.com/model/deepseek-v4-flash-0731) | DeepSeek | $0.045 / $0.18 | $0.15 / $0.6 | 固定 0731 版本，站内最便宜的对话模型 |
| [`glm-5.3`](https://nezhagate.com/model/glm-5.3) | 智谱 Z.ai | $0.34 / $1.25 | $1.4 / $4.4 | 编码、Agent、中英文写作 |
| [`glm-5.3-flash`](https://nezhagate.com/model/glm-5.3-flash) | 智谱 Z.ai | $0.072 / $0.25 | $0.15 / $0.5 | 大批量分类、抽取、改写 |
| [`kimi-k3`](https://nezhagate.com/model/kimi-k3) | 月之暗面 Moonshot | $1.80 / $9.00 | $3 / $15 | 长文档、多文档分析、Agent |
| [`qwen3.7-max`](https://nezhagate.com/model/qwen3.7-max) | 阿里云 | $1.65 / $4.85 | $2.5 / $7.5 | 推理、编码、Agent、长上下文 |

- **`/v1/responses`** 支持 GPT 与 Gemini 模型；其余模型只走 `/v1/chat/completions`（Claude 另有原生 `/anthropic`）。缓存读价格见 [定价页](https://nezhagate.com/pricing)。
- **思考**：`reasoning_effort` 对 GPT、Claude 与 `gemini-3.1-pro` 生效。GPT-6、Grok、DeepSeek、GLM、Kimi、Qwen 会在 `message.reasoning_content` 返回思考内容；思考 token 按输出价计费，计入 `usage.completion_tokens`。
- **会被忽略的参数**：GPT 模型不接受 `temperature`、`top_p`、`max_tokens` / `max_completion_tokens` 与两个 penalty 参数（静默忽略、不报错）——用 `reasoning_effort` 控制思考深度、用提示词约束长度；图片输入请用 base64 `data:` URI。Claude Opus 5 会丢弃 `temperature` / `top_p` / `top_k`；Kimi K3 的温度由模型固定。

### 图像（`/v1/images/generations`、`/v1/images/edits`）—— 每张，1K / 2K / 4K

| 模型 | NezhaGate | 说明 |
| --- | --- | --- |
| [`gpt-image-2`](https://nezhagate.com/model/gpt-image-2) | $0.005 / $0.01 / $0.02 | 文生图 + 图生图，7 种比例原生出图 |
| [`gpt-image-2.5-flare`](https://nezhagate.com/model/gpt-image-2.5-flare) | $0.005 / $0.01 / $0.02 | GPT Image 2.5 干净平滑风格分支，带 C2PA 内容凭证 |
| [`gpt-image-2.5-sunburst`](https://nezhagate.com/model/gpt-image-2.5-sunburst) | $0.005 / $0.01 / $0.02 | GPT Image 2.5 颗粒与笔触更重的风格分支，与 Flare 同价 |
| [`nano-banana-2`](https://nezhagate.com/model/nano-banana-2) | $0.025 / $0.0375 / $0.0625 | Gemini 3.1 Flash Image，出图快 |
| [`nano-banana-pro`](https://nezhagate.com/model/nano-banana-pro) | $0.040 / $0.060 / $0.100 | Gemini 3 Pro Image，旗舰画质 |

`size` 传比例（`1:1`、`3:4`、`2:3`、`9:16`、`4:3`、`3:2`、`16:9`）即按该比例原生出图，也接受 `1024x1536` 这类像素尺寸。图生图：请求里加 `image`（公网 URL、`data:` URI 或 base64），或直接调 `/images/edits`；`images` 可一次传多张参考图。

### 视频（`/v1/videos/generations`，异步任务）

| 模型 | 计费 | 时长 | 分辨率 | 说明 |
| --- | --- | --- | --- | --- |
| [`seedance-2.5`](https://nezhagate.com/model/seedance-2.5) | $0.158 / 秒 | 4–30 秒 | 480P、720P | 原生音轨（可关），最多 9 张参考图 |
| [`seedance-2.5-30s`](https://nezhagate.com/model/seedance-2.5-30s) | $1.50 / 条 | 固定 30 秒 | 720P | 一条出 30 秒长镜头，最多 9 张参考图 |
| [`seedance-2.0`](https://nezhagate.com/model/seedance-2.0) | $0.12（480P）/ $0.15（720P）每秒 | 5–15 秒 | 480P、720P | 标准档；1080P 即将开放 |
| [`seedance-2.0-fast`](https://nezhagate.com/model/seedance-2.0-fast) | $0.075 / 秒 | 5–15 秒 | 720P | 最快最省的 Seedance |
| [`wan3.0-video`](https://nezhagate.com/model/wan3.0-video) | $0.09 / $0.12 / $0.16 每秒 | 2–30 秒 | 480P、720P、1080P | 文生 / 首帧 / 首尾帧 / 最多 10 张参考图 / 视频改写 |
| [`wan3.0-video-prime`](https://nezhagate.com/model/wan3.0-video-prime) | $0.12 / $0.16 / $0.20 每秒 | 2–30 秒 | 480P、720P、1080P | 同模型，更快队列 |
| [`minimax-h3`](https://nezhagate.com/model/minimax-h3) | $0.036 / 秒 | 5–15 秒 | 1080P | 固定生成原生音频，按秒最便宜 |
| [`grok-imagine-video-1.5`](https://nezhagate.com/model/grok-imagine-video-1.5) | $0.30（480P）/ $0.40（720P）每条 | 4–15 秒 | 480P、720P | 最多 7 张参考图（2 张及以上时最长 10 秒） |

按秒模型的费用 = 单价 × 时长（万相 3.0 另加参考视频的声明时长）。失败或超时的任务全额退款。

### 即将上线与已下架

- **即将上线**：[`veo-3.1`](https://nezhagate.com/model/veo-3.1)（视频）与 `seedance-2.0` 的 1080P 档已有页面与 API 文档，但暂未开放调用：请求会被拒绝（HTTP 400 `model_coming_soon`），不产生任何扣费。
- **已下架**：`gemini-3.5-flash`（请改用 `gemini-3.7-flash`）与 `seedance-2.0-mini`（请改用 `seedance-2.0-fast`），调用返回 HTTP 400 `model_disabled`。完整记录见 [CHANGELOG.md](CHANGELOG.md)。

## 用原生 Anthropic 接口调 Claude

```bash
export ANTHROPIC_BASE_URL=https://nezhagate.com/anthropic
export ANTHROPIC_API_KEY=YOUR_API_KEY        # 就是 NezhaGate 的 Key
# 模型：claude-opus-5 / claude-fable-5 / claude-sonnet-4-6
```

Claude Code 只需要这两行环境变量。用 Anthropic SDK 见 [`examples/claude_native.py`](examples/claude_native.py)（`POST /anthropic/v1/messages`，`max_tokens` 必填）。思考、工具调用与提示缓存原样透传；缓存命中按输入价的 1/10 计费。

## 异步任务（图像与视频）

`POST /v1/images/generations`、`POST /v1/images/edits`、`POST /v1/videos/generations` 会立刻返回 **HTTP 202** 与任务号：

```json
{"id": "img_3f9a...", "object": "image.generation.job", "status": "queued"}
```

每隔几秒轮询 `GET /v1/images/jobs/{id}`（或 `/v1/videos/jobs/{id}`），直到 `status` 为 `succeeded`，再读取 `data[0].url`。图片几秒钟，视频一到几分钟（长片更久）。不要在提交后直接读 `data`；`failed` 的任务不计费。

**记得下载结果。** 生成的图片、视频（以及你上传的参考图）在 `img.nezhagate.com` 保留 **60 天**，之后自动删除、链接失效。需要长期使用的请转存到你自己的存储。

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
| 429 | `rate_limit_exceeded` | 限流，或所有线路并发已满——按 `Retry-After` 重试 |
| 502 | `empty_completion`、`upstream_error` | 上游返回空响应或失败——不计费，可直接重试 |

## 查余额

任何 Key 都能查自己的余额与消费，无需登录控制台：

```bash
curl https://nezhagate.com/v1/usage -H "Authorization: Bearer $NEZHAGATE_API_KEY"
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
export NEZHAGATE_API_KEY=sk-xxxx      # 或复制 .env.example 为 .env
python examples/chat_python.py
```

示例只依赖 `openai` / `anthropic` / `requests`（Python）或 `openai`（Node）。CI 对每个文件做语法检查；仓库里永远不会出现任何 Key。

## 生态兼容

任何支持自定义 OpenAI Base URL 的工具都能直接接入：**Cursor、Claude Code、Codex、n8n、Dify、LangChain、Open WebUI、LobeChat、Cherry Studio、ChatBox** 等——Base URL 填 `https://nezhagate.com/v1`，API Key 填控制台创建的 Key。

## FAQ 精选

**请求失败会扣费吗？** 不会。只有成功返回的调用才按实际用量结算，上游报错或超时不产生费用；图像 / 视频任务失败全额退。

**和官方 API 有什么区别？** 一个接口、一把 Key、一张账单覆盖所有模型，请求形状与 OpenAI 一致，多数对话模型价格低于官方标价（见上表）。

**生成的图片和视频能保存多久？** 在 `img.nezhagate.com` 保留 60 天，之后自动删除、链接失效——想留的请及时下载。调用日志里的文字内容保留 15 天。

**怎么看余额和用量？** 控制台有实时余额、每个 Key 的用量和逐条调用日志（模型、时间、token、花费）；任何 Key 调 `GET /v1/usage` 也能拿到同样的余额。模型页还有一条按真实网关流量计算的 24 小时成功率状态条。

更多：[nezhagate.com/faq](https://nezhagate.com/faq)

## 链接

- 官网：<https://nezhagate.com> —— 另有 [English](https://nezhagate.com/en/)、[Español](https://nezhagate.com/es/)、[日本語](https://nezhagate.com/ja/)、[한국어](https://nezhagate.com/ko/)
- 模型市场：<https://nezhagate.com/market>
- 定价：<https://nezhagate.com/pricing>
- 接入文档：<https://nezhagate.com/docs-guide>
- FAQ：<https://nezhagate.com/faq>
- 给 AI 工具读的站点索引：<https://nezhagate.com/llms.txt> · [llms-full.txt](https://nezhagate.com/llms-full.txt)
- 模型目录变更记录：[CHANGELOG.md](CHANGELOG.md)

## License

[MIT](LICENSE)
