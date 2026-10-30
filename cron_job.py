import os
import requests
from dotenv import load_dotenv
from datetime import datetime

from google_calendar_service import get_calendar_service

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    return response.status_code == 200


def get_today_events():
    service = get_calendar_service()
    today = datetime.now().date()
    events = service.fetch_events(str(today), str(today))
    return events


def run_daily_digets():
    try:
        events = get_today_events()

        if not events or (isinstance(events, dict) and "error" in events):
            message = "No events scheduled for today!"
        else:
            message = "Today's Schedule:\n\n"
            for event in events:
                message += f"• {event.get('title', 'No Title')}\n"
                if event.get('start') and event.get('end'):
                    start = format_time(event['start'])
                    end = format_time(event['end']).split(', ')[1]  # Get just time part
                    message += f"  ⏰ {start} - {end}\n"
                if event.get('location'):
                    message += f"  📍 {event['location']}\n"
                message += "\n"

        send_telegram_message(message)
        print(f"✓ Digest sent at {datetime.now()}")
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        send_telegram_message(error_msg)
        print(error_msg)

def format_time(iso_time: str) -> str:
    """Convert ISO time to humanized format (Option C)."""
    if not iso_time:
        return "Time not specified"
    
    try:
        # Parse ISO format: "2026-10-30T14:30:00Z"
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        
        # Format as: "Today, 2:30 PM"
        time_str = dt.strftime("%I:%M %p").lstrip('0')
        return f"Today, {time_str}"
    except:
        return iso_time


if __name__ == "__main__":
    run_daily_digets()
