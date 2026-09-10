// NezhaGate chat with the official OpenAI Node SDK -- only baseURL and apiKey change.
//   npm i openai
//   export NEZHAGATE_API_KEY=sk-xxxx
//   node examples/chat_node.mjs
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.NEZHAGATE_API_KEY,
  baseURL: "https://nezhagate.com/v1",
});

// 1) basic chat -- switch models by changing one string
const res = await client.chat.completions.create({
  model: "gpt-5.6-terra",
  messages: [{ role: "user", content: "Introduce yourself in one sentence." }],
});
console.log(res.choices[0].message.content);

// 2) reasoning effort on a Claude model (low / medium / high)
const deep = await client.chat.completions.create({
  model: "claude-opus-5",
  messages: [{ role: "user", content: "Is 1000003 prime? Answer yes or no, then explain briefly." }],
  reasoning_effort: "high",
});
console.log(deep.choices[0].message.content);

// 3) streaming
const stream = await client.chat.completions.create({
  model: "gemini-3.8-flash",
  messages: [{ role: "user", content: "Count from 1 to 5." }],
  stream: true,
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
}
process.stdout.write("\n");
