from openai import OpenAI
import json
from tools_registry import TOOLS_REGISTRY

MODEL = "gpt-5-nano"


def run_agent(prompt: str):
    if not is_calendar_related(prompt):
        return "I can only help with calendar and email queries. Please ask me something like 'What events do I have tomorrow?' or 'Show me my schedule for next week.'"

    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful calendar assistant to let users know about their events based on the requested date range. For any other queries, you should respond that you only handle calendar-related requests.",
        },
        {"role": "user", "content": prompt},
    ]

    for _ in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[tool_config["schema"] for tool_config in TOOLS_REGISTRY.values()],
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls is None:
            return message.content

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            if tool_name in TOOLS_REGISTRY:
                tool_func = TOOLS_REGISTRY[tool_name]["function"]
                arguments = json.loads(tool_call.function.arguments)
                result = tool_func(**arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )
            else:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            {"error": f"Tool '{tool_name}' not found"}
                        ),
                    }
                )

    return "Unable to generate a response."


def is_calendar_related(prompt: str) -> bool:
    """Check if the prompt is calendar/email related."""
    keywords = [
        "calendar",
        "event",
        "meeting",
        "schedule",
        "appointment",
        "time",
        "when",
        "what time",
        "email",
        "message",
        "send",
        "compose",
        "reminder",
        "busy",
        "free",
        "available",
    ]

    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in keywords)
