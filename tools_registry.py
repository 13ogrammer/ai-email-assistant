from tools import fetch_calendar_events, get_all_calendars

TOOLS_REGISTRY = {
    "fetch_calendar_events": {
        "function": fetch_calendar_events,
        "schema": {
            "type": "function",
            "function": {
                "name": "fetch_calendar_events",
                "description": "Fetch calendar events from Google Calendar within a date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Start date in YYYY-MM-DD format",
                        },
                        "end_date": {
                            "type": "string",
                            "format": "date",
                            "description": "End date in YYYY-MM-DD format",
                        },
                    },
                    "required": ["start_date", "end_date"],
                },
            },
        },
    },
    "get_all_calendars": {
        "function": get_all_calendars,
        "schema": {
            "type": "function",
            "function": {
                "name": "get_all_calendars",
                "description": "Get list of all available calendars for the user",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        },
    },
}
