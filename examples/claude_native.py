"""Claude through the native Anthropic Messages API -- the same thing Claude Code does with two env vars:

    export ANTHROPIC_BASE_URL=https://kovapi.com/anthropic
    export ANTHROPIC_API_KEY=$KOVAPI_API_KEY

With the SDK:
    pip install anthropic
    export KOVAPI_API_KEY=sk-xxxx
    python examples/claude_native.py

Models: claude-opus-5 / claude-fable-5 / claude-sonnet-4-6. max_tokens is required by the Messages API.
"""
import os

import anthropic

API_KEY = os.environ.get("KOVAPI_API_KEY") or os.environ.get("NEZHAGATE_API_KEY")  # the old name still works
if not API_KEY:
    raise SystemExit("export KOVAPI_API_KEY=sk-... first (create a key at https://kovapi.com/keys)")

client = anthropic.Anthropic(
    api_key=API_KEY,
    base_url="https://kovapi.com/anthropic",
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
