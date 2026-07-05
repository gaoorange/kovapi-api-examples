# NezhaGate API Examples — 一个 OpenAI 兼容接口调用 Claude / GPT / Gemini / Nano Banana / Veo

> **NezhaGate**（[nezhagate.com](https://nezhagate.com)）是 OpenAI 兼容的 AI 模型网关：把 `base_url` 换成 `https://nezhagate.com/v1`，官方 `openai` SDK 一行业务代码不改，就能统一调用 Claude Opus 4.8、GPT-5.5、Gemini 3.5、Nano Banana Pro（图像）、Veo 3.1（视频）。按量计费、请求失败不扣费、支持微信支付充值。
>
> **NezhaGate** is an OpenAI-compatible AI model gateway: point `base_url` at `https://nezhagate.com/v1` and call Claude, GPT, Gemini, image and video models through the official OpenAI SDK — one endpoint, one API key. Pay-as-you-go; failed requests are never billed.

## 30 秒上手 / 30-second quickstart

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY", base_url="https://nezhagate.com/v1")
resp = client.chat.completions.create(
    model="claude-opus-4-8",          # 换模型只改这一个字段
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

- **Base URL**: `https://nezhagate.com/v1`（对话 `/chat/completions`、图像 `/images/generations`、视频 `/videos/generations`，路径与 OpenAI 一致）
- **API Key**: [nezhagate.com](https://nezhagate.com) 注册 → 控制台创建
- 换模型 = 只改 `model` 字段：`gpt-5.5` / `claude-opus-4-8` / `gemini-3.5-flash` / `nano-banana-pro` / `veo-3.1` …

## 支持的模型与价格 / Models & Pricing

价格快照（2026-07-05，USD）；**实时价格以 [pricing 页](https://nezhagate.com/pricing) 与 [llms.txt](https://nezhagate.com/llms.txt) 为准**：

| 模型 ID | 类型 | NezhaGate 价 | 官方价 | 提供方 |
| --- | --- | --- | --- | --- |
| `gpt-5.5` | 对话 | $0.7 / $4.2 每百万 token | $5 / $30 | OpenAI |
| `gpt-5.4` | 对话 | $0.5 / $3 | $1.25 / $10 | OpenAI |
| `gpt-5.4-mini` | 对话 | $0.15 / $1 | $0.25 / $2 | OpenAI |
| `claude-opus-4-8` | 对话 | $4 / $20 | $5 / $25 | Anthropic |
| `claude-sonnet-4-6` | 对话 | $1.5 / $7.5 | $3 / $15 | Anthropic |
| `claude-haiku-4-5` | 对话 | $0.5 / $2.5 | $1 / $5 | Anthropic |
| `gemini-3.1-pro-preview` | 对话 | $0.7 / $3.5 | $2 / $12 | Google |
| `gemini-3.5-flash` | 对话 | $0.45 / $2.7 | $1.5 / $9 | Google |
| `gemini-3-flash-preview` | 对话 | $0.3 / $1.2 | $0.5 / $3 | Google |
| `gpt-image-2` | 图像 | $0.015–$0.04 / 张（1K–4K） | — | OpenAI |
| `nano-banana-2` | 图像 | $0.02–$0.05 / 张（1K–4K） | — | Google |
| `nano-banana-pro` | 图像 | $0.04–$0.1 / 张（1K–4K） | — | Google |
| `veo-3.1` | 视频 | 按条计费（档位/分辨率定价），失败全额退 | — | Google |

对话按输入 / 输出 token 分开计价；图像按张（1K / 2K / 4K 分辨率不同价）；视频按条。**请求失败不扣费**：超时、报错不产生费用。

## 本仓库示例 / Examples

| 文件 | 说明 |
| --- | --- |
| [`examples/chat.sh`](examples/chat.sh) | curl：对话 + 流式输出 |
| [`examples/chat_python.py`](examples/chat_python.py) | Python `openai` SDK：对话 + 流式 |
| [`examples/chat_node.mjs`](examples/chat_node.mjs) | Node.js `openai` SDK |
| [`examples/image_generation.py`](examples/image_generation.py) | Nano Banana Pro 文生图 / 图生图（异步任务：提交 → 轮询） |
| [`examples/veo_video.py`](examples/veo_video.py) | Veo 3.1 文生 / 图生视频（异步任务：提交 → 轮询 → mp4 直链） |
| [`examples/langchain_chat.py`](examples/langchain_chat.py) | LangChain 接入（`ChatOpenAI` 改 `base_url`） |

运行前：

```bash
export NEZHAGATE_API_KEY=sk-xxxx   # 或复制 .env.example 为 .env
```

## 生态兼容 / Works with

任何支持自定义 OpenAI Base URL 的工具都能直接接入：**n8n、Dify、LangChain、Open WebUI、LobeChat、Cherry Studio、ChatBox、Cursor、Claude Code、Codex** 等——在工具设置里把 Base URL 填 `https://nezhagate.com/v1`、API Key 填控制台创建的 Key 即可。

## FAQ 精选

**请求失败会扣费吗？** 不会。只有成功返回的调用才按实际用量结算，超时 / 报错不产生费用；视频生成失败全额退。

**和官方 API 有什么区别？** 官方按单家模型直连提供，适合有官方账号和独立结算的团队；NezhaGate 是统一模型网关，解决多模型统一接入、OpenAI 兼容调用、计费管理和开发效率问题，价格低于官方（见上表）。

**图像 / 视频怎么调？** 异步任务模式：`POST /v1/images/generations`（或 `/v1/videos/generations`）提交后返回 202 与任务号，轮询 `GET /v1/images/jobs/{id}`（或 `/v1/videos/jobs/{id}`）直到 `status=succeeded`，结果在 `data[0].url`（重托管稳定直链）。见本仓库示例。

**怎么看余额和用量？** 控制台有实时余额、每个 Key 的用量和逐条调用日志（模型、时间、token、花费）。

更多（26 条完整 FAQ）：[nezhagate.com/faq](https://nezhagate.com/faq)

## 链接 / Links

- 官网 / Home: <https://nezhagate.com>
- 模型市场 / Models: <https://nezhagate.com/market>
- 定价 / Pricing: <https://nezhagate.com/pricing>
- 接入文档 / Docs: <https://nezhagate.com/docs-guide>
- FAQ: <https://nezhagate.com/faq>
- llms.txt（给 AI 工具读的站点索引）: <https://nezhagate.com/llms.txt> · [llms-full.txt](https://nezhagate.com/llms-full.txt)
- English pages: <https://nezhagate.com/en/>

## License

[MIT](LICENSE)
