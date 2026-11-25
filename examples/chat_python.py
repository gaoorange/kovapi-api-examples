"""KovAPI chat with the official OpenAI SDK -- only base_url and api_key change.

    pip install openai
    export KOVAPI_API_KEY=sk-xxxx
    python examples/chat_python.py
"""
import os

from openai import OpenAI

API_KEY = os.environ.get("KOVAPI_API_KEY") or os.environ.get("NEZHAGATE_API_KEY")  # the old name still works
if not API_KEY:
    raise SystemExit("export KOVAPI_API_KEY=sk-... first (create a key at https://kovapi.com/keys)")

client = OpenAI(api_key=API_KEY, base_url="https://kovapi.com/v1")

# 1) basic chat -- switch models by changing one string:
#    gpt-6-astra / gpt-6.1-sol / gpt-6-sol / gpt-5.6-luna / claude-sonnet-4-6 / claude-opus-5-5 /
#    gemini-3.8-flash / grok-4.7 / deepseek-v4.1-flash ... (full list: https://kovapi.com/market)
resp = client.chat.completions.create(
    model="gpt-5.6-luna",
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)
print(resp.choices[0].message.content)

# 2) reasoning effort (GPT models; other models: see their docs page): low / medium / high -- more thinking, more output tokens.
#    Thinking models also return their reasoning in message.reasoning_content, separate from the answer.
resp = client.chat.completions.create(
    model="gpt-6-astra",
    messages=[{"role": "user", "content": "Is 1000003 prime? Answer yes or no, then explain briefly."}],
    extra_body={"reasoning_effort": "high"},
)
msg = resp.choices[0].message
print("reasoning:", getattr(msg, "reasoning_content", None))
print("answer:", msg.content)

# 3) DeepSeek thinks by default; switch it off for a faster, cheaper direct answer
resp = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "Translate 'good morning' into French, Japanese and Korean."}],
    extra_body={"thinking": {"type": "disabled"}},
)
print(resp.choices[0].message.content)

# 4) streaming
stream = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()

# 5) vision input -- a public image URL is fine here; for GPT models send the image as a base64 data: URI
resp = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "What is in this picture?"},
        {"type": "image_url", "image_url": {"url": "https://kovapi.com/static/img/logo-mark.png"}},
    ]}],
)
print(resp.choices[0].message.content)

# Usage and cost come back on every response; failed calls are never billed.
print("usage:", resp.usage)
