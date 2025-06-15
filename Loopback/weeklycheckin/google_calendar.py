from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_user_google_service(profile):
    creds = Credentials.from_authorized_user_info(profile.google_credentials)
    return build('calendar', 'v3', credentials=creds)

def fetch_events(profile, time_min=None, time_max=None):
    service = get_user_google_service(profile)
    kwargs = {
        "calendarId": "primary",
        "singleEvents": True,
        "orderBy": "startTime",
    }
    if time_min:
        kwargs["timeMin"] = time_min
    if time_max:
        kwargs["timeMax"] = time_max
    return service.events().list(**kwargs).execute().get('items', [])