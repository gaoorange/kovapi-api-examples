"""The OpenAI Responses API (POST /v1/responses) -- served for the GPT and Gemini models.

Same key and base_url as chat. For a reasoning model, `reasoning` sets the effort and asks for a short summary of
the thinking, which comes back as a `reasoning` item in `output`, separate from the answer.

    pip install openai
    export KOVAPI_API_KEY=sk-xxxx
    python examples/responses_api.py
"""
import os

from openai import OpenAI

API_KEY = os.environ.get("KOVAPI_API_KEY") or os.environ.get("NEZHAGATE_API_KEY")  # the old name still works
if not API_KEY:
    raise SystemExit("export KOVAPI_API_KEY=sk-... first (create a key at https://kovapi.com/keys)")

client = OpenAI(api_key=API_KEY, base_url="https://kovapi.com/v1")

resp = client.responses.create(
    model="gpt-6-astra",                        # or gpt-6.1-sol / gpt-6-sol / gpt-5.6-luna ...
    input="Is 1000003 prime? Answer yes or no, then explain briefly.",
    reasoning={"effort": "medium", "summary": "auto"},
)

for item in resp.output:
    if item.type == "reasoning":
        for part in item.summary or []:
            print("reasoning:", part.text)

print("answer:", resp.output_text)
print("usage:", resp.usage)
