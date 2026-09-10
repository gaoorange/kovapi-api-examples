"""Claude through the native Anthropic Messages API -- the same thing Claude Code does with two env vars:

    export ANTHROPIC_BASE_URL=https://nezhagate.com/anthropic
    export ANTHROPIC_API_KEY=$NEZHAGATE_API_KEY

With the SDK:
    pip install anthropic
    export NEZHAGATE_API_KEY=sk-xxxx
    python examples/claude_native.py

Models: claude-opus-5 / claude-fable-5 / claude-sonnet-4-6. max_tokens is required by the Messages API.
"""
import os

import anthropic

client = anthropic.Anthropic(
    api_key=os.environ["NEZHAGATE_API_KEY"],
    base_url="https://nezhagate.com/anthropic",
)

msg = client.messages.create(
    model="claude-opus-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain, in three sentences, why an API gateway is useful."}],
)
print(msg.content[0].text)

# streaming works the same way
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
