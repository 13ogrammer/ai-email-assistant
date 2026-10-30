from google_calendar_service import get_calendar_service

def fetch_calendar_events(start_date: str, end_date: str):
    try:
        service = get_calendar_service()
        events = service.fetch_events(start_date, end_date)

        if isinstance(events, dict) and 'error' in events:
            return {'error': events['error']}

        return {
            'count': len(events),
            'events': events
        }
    except Exception as e:
        return {'error': str(e), 'count': 0, 'events': []}

def get_all_calendars():
    try:
        service = get_calendar_service()
        calendars = service.get_calendars()

        if isinstance(calendars, dict) and 'error' in calendars:
            return {'error': calendars['error']}

        return {
            'count': len(calendars),
            'calendars': calendars
        }
    except Exception as e:
        return {'error': str(e), 'count': 0, 'calendars': []}