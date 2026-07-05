"""NezhaGate + LangChain — ChatOpenAI works as-is with a custom base_url.

    pip install langchain-openai
    export NEZHAGATE_API_KEY=sk-xxxx
    python langchain_chat.py

Same pattern works for n8n / Dify / Open WebUI / LobeChat / Cherry Studio / ChatBox:
set the OpenAI-compatible Base URL to https://nezhagate.com/v1 and paste your key.
"""
import os

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="claude-sonnet-4-6",
    api_key=os.environ["NEZHAGATE_API_KEY"],
    base_url="https://nezhagate.com/v1",
)
print(llm.invoke("用一句话介绍你自己").content)
