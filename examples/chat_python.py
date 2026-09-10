"""NezhaGate chat with the official OpenAI SDK -- only base_url and api_key change.

    pip install openai
    export NEZHAGATE_API_KEY=sk-xxxx
    python examples/chat_python.py
"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["NEZHAGATE_API_KEY"], base_url="https://nezhagate.com/v1")

# 1) basic chat -- switch models by changing one string:
#    gpt-5.6-sol / gpt-5.6-terra / gpt-5.6-luna / gpt-5.5 / claude-opus-5 / claude-fable-5 /
#    claude-sonnet-4-6 / gemini-3.1-pro / gemini-3.8-flash / gemini-3.6-flash ...
resp = client.chat.completions.create(
    model="gpt-5.6-terra",
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)
print(resp.choices[0].message.content)

# 2) reasoning effort (GPT-5.x and gemini-3.1-pro): low / medium / high -- more thinking, more output tokens
resp = client.chat.completions.create(
    model="claude-opus-5",
    messages=[{"role": "user", "content": "Is 1000003 prime? Answer yes or no, then explain briefly."}],
    extra_body={"reasoning_effort": "high"},
)
print(resp.choices[0].message.content)

# 3) streaming
stream = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()

# 4) vision input (any model that accepts images: claude-opus-5, gemini-3.x, gpt-5.x)
resp = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "What is in this picture?"},
        {"type": "image_url", "image_url": {"url": "https://nezhagate.com/static/img/logo-mark.png"}},
    ]}],
)
print(resp.choices[0].message.content)

# Usage and cost come back on every response; failed calls are never billed.
print("usage:", resp.usage)
