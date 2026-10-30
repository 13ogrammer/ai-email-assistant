from tools import fetch_calendar_events

TOOLS_REGISTRY = {
  "fetch_calendar_events": {
    "function": fetch_calendar_events,
    "schema": {
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
  }
}