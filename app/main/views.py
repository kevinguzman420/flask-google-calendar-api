import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#
from flask import Blueprint, request, jsonify

main_bp = Blueprint("main", __name__)

SCOPES = ["https://www.googleapis.com/auth/calendar"]


@main_bp.route("/calendar", methods=["GET"])
def get_events():

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("credentials.json expired but refreshing...")
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"

        # Getting the upcoming 10 events
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found")
            return

        return jsonify(events=events)

    except HttpError as error:
        return {"message": f"There's a server error {error}"}


@main_bp.route("/calendar", methods=["POST"])
def create_events():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            'summary': request.json["summary"],
            # 'location': 'Online',
            'description': request.json["description"],
            'start': {
                'dateTime': '2024-02-14T09:00:00-06:00',  # custom this
                'timeZone': 'America/Guatemala',  # custom this
            },
            'end': {
                'dateTime': '2024-02-14T13:00:00-06:00',  # custom this
                'timeZone': 'America/Guatemala',  # custom this
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': 'hangoutsMeet',  # if you want to set a Google Meet link
                },
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'  # if the event will repet
            ],
            'attendees': [{"email": request.json["email"]}],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    # {'method': 'email', 'minutes': 24 * 60}, # if you want to set a reminder one day before
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        event = service.events().insert(calendarId='primary',
                                        body=event, sendUpdates="all", conferenceDataVersion=1).execute()
        return jsonify(event=event)
    except HttpError as error:
        return {"message": f"There's a server error {error}"}
