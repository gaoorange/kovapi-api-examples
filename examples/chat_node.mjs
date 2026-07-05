// NezhaGate chat with the official OpenAI Node SDK — only baseURL/apiKey change.
//   npm i openai
//   NEZHAGATE_API_KEY=sk-xxxx node chat_node.mjs
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.NEZHAGATE_API_KEY,
  baseURL: "https://nezhagate.com/v1",
});

// basic chat — switch model by changing one string
const resp = await client.chat.completions.create({
  model: "gemini-3.5-flash",
  messages: [{ role: "user", content: "用一句话介绍你自己" }],
});
console.log(resp.choices[0].message.content);

// streaming
const stream = await client.chat.completions.create({
  model: "claude-sonnet-4-6",
  messages: [{ role: "user", content: "数到 5" }],
  stream: true,
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
process.stdout.write("\n");
