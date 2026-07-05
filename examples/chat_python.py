"""NezhaGate chat with the official OpenAI SDK — only base_url/api_key change.

    pip install openai
    export NEZHAGATE_API_KEY=sk-xxxx
    python chat_python.py
"""
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["NEZHAGATE_API_KEY"],
    base_url="https://nezhagate.com/v1",
)

# 1) basic chat — switch model by changing one string:
#    gpt-5.5 / claude-opus-4-8 / claude-sonnet-4-6 / gemini-3.5-flash ...
resp = client.chat.completions.create(
    model="claude-opus-4-8",
    messages=[{"role": "user", "content": "用一句话介绍你自己"}],
)
print(resp.choices[0].message.content)

# 2) streaming
stream = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "数到 5"}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
print()
