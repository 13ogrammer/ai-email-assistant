from openai import OpenAI
import json
from tools_registry import TOOLS_REGISTRY

MODEL = 'gpt-5-nano'

def run_agent(prompt: str):
  client = OpenAI()

  messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]

  for _ in range(3):
    response = client.chat.completions.create(
      model=MODEL,
      messages=messages,
      tools=[tool_config['schema'] for tool_config in TOOLS_REGISTRY.values()]
    )
    
    message = response.choices[0].message
    messages.append(message)
    
    if message.tool_calls is None:
      return message.content

    for tool_call in message.tool_calls:
      tool_name = tool_call.function.name

      if tool_name in TOOLS_REGISTRY:
        tool_func = TOOLS_REGISTRY[tool_name]['function']
        arguments = json.loads(tool_call.function.arguments)
        result = tool_func(**arguments)

        messages.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "content": json.dumps(result)
        })
      else:
        messages.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "content": json.dumps({"error": f"Tool '{tool_name}' not found"})
        })

  return "Unable to generate a response."

