from openai import OpenAI
import json

from tools import fetch_calendar_events

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
      tools=[
        {
          "type": "function",
          "function": {
            "name": "fetch_calendar_events",
            "description": "Fetch calendar events within a date range",
            "parameters": {
              "type": "object",
              "properties": {
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"}
              },
              "required": ["start_date", "end_date"]
            }
          }
        }
      ]
    )
    
    message = response.choices[0].message
    messages.append(message)
    
    if message.tool_calls is None:
      return message.content

    for tool_call in message.tool_calls:
      if tool_call.function.name == "fetch_calendar_events":
        arguments = json.loads(tool_call.function.arguments)
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")

        events = fetch_calendar_events(start_date=start_date, end_date=end_date)
        messages.append({
          "role": "tool",
          "id": tool_call.id,
          "content": json.dumps(events)
        })

  return "Unable to generate a response."


