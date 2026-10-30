import os
from dotenv import load_dotenv

load_dotenv()  # This loads your .env file
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.__initialise_service()

    def __initialise_service(self):
        if not os.path.exists("service_account_key.json"):
            raise FileNotFoundError("Service account key file not found.")

        creds = Credentials.from_service_account_file(
            "service_account_key.json", scopes=SCOPES
        )
        self.service = build("calendar", "v3", credentials=creds)

    def fetch_events(self, start_date: str, end_date: str):
        try:
            start_time = f"{start_date}T00:00:00Z"
            end_time = f"{end_date}T23:59:59Z"

            events_result = (
                self.service.events()
                .list(
                    calendarId=os.getenv("PRIMARY_CALENDAR_ID"),
                    timeMin=start_time,
                    timeMax=end_time,
                    singleEvents=True,
                    orderBy="startTime",
                    fields="items(id,summary,description,start,end,location)",
                )
                .execute()
            )

            events = events_result.get("items", [])

            formatted_events = []
            for event in events:
                start = event.get("start", {})
                end = event.get("end", {})

                formatted_event = {
                    "id": event.get("id"),
                    "summary": event.get("summary", "No title"),
                    "description": event.get("description", ""),
                    "location": event.get("location", ""),
                    "start": start.get("dateTime") or start.get("date"),
                    "end": end.get("dateTime") or end.get("date"),
                }
                formatted_events.append(formatted_event)

            return formatted_events

        except Exception as e:
            return {"error": str(e), "events": []}

    def get_calendars(self):
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get("items", [])

            formatted_calendars = []

            for cal in calendars:
                formatted_calendars.append(
                    {
                        "id": cal.get("id"),
                        "name": cal.get("summary", "No title"),
                        "description": cal.get("description", ""),
                    }
                )

            return formatted_calendars

        except Exception as e:
            return {"error": str(e), "calendars": []}


_service_instance = None


def get_calendar_service():
    global _service_instance
    if _service_instance is None:
        _service_instance = GoogleCalendarService()
    return _service_instance
