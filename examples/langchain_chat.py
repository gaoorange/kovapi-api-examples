"""NezhaGate with LangChain -- ChatOpenAI with a custom base_url; every chat model works the same way.

    pip install langchain-openai
    export NEZHAGATE_API_KEY=sk-xxxx
    python examples/langchain_chat.py
"""
import os

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-5.6-terra",            # or claude-opus-5 / gemini-3.8-flash / deepseek-v4.1-flash / grok-4.7 ...
    api_key=os.environ["NEZHAGATE_API_KEY"],
    base_url="https://nezhagate.com/v1",
    # GPT models ignore temperature / top_p / max_tokens (no error); each model page lists what it accepts
)

print(llm.invoke("Give me three names for a cat cafe, one per line.").content)

# streaming
for chunk in llm.stream("Count from 1 to 5."):
    print(chunk.content, end="", flush=True)
print()
