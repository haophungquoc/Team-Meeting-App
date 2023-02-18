import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.app.created', 
        'https://www.googleapis.com/auth/calendar.readonly', 
        'https://www.googleapis.com/auth/calendar']


def create_event(data_frame):
    #Ask for some info
    summary = input("What is the event's name ?? ")
    location = input("Where you gonna meet (Optional)?? ")
    desc = input("What's the event about (Optional)?? ")

    #Ask for time info
    print("When does the event start ?? Please enter specific date below")
    date = int(input("Date: "))
    month = int(input("Month: "))
    year = int(input("Year: "))
    print("What time does the meeting start ?? Please enter specific time below")
    hour = int(input("Hour: "))
    minute = int(input("Minute: "))
    time = datetime.datetime(year, month, date, hour, minute)

    numOfPeople = input("How many other people will join the meeting ?? ")
    attendees = []
    for i in range(1, int(numOfPeople)+1):
        email = input(f"Attendee {i} email: ")
        attendees.append({'email': email})

    #For each activity in agenda, create an event, then add it to Google Calendar, make them continuous time blocks
    for id, row in data_frame.iterrows():
        added_time = datetime.timedelta(0, row['Durations (in seconds)'])
        #This is just resource info, check it out here: https://developers.google.com/calendar/api/v3/reference/events#resource
        event = {
            'summary': summary,
            'location': location,
            'description': desc + f"\n\nThis event is for activity {id+1}, which is {row['Task']}. This activity is about {row['Description']}",
            'start': {
                'dateTime': time.isoformat(),
                'timeZone': 'Australia/Adelaide',
            },
            'end': {
                'dateTime': (time + added_time).isoformat(),
                'timeZone': 'Australia/Adelaide',
            },
            'attendees': attendees,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
            'conferenceData': {
                'createRequest': {
                    'requestID': 'randomID',
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet',
                    },
                },
            }
        }
        add_new_event(event)
        time = time + added_time


def add_new_event(event):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        #Build a resource for interacting with Google Calendar API using above credential
        service = build('calendar', 'v3', credentials=creds)

        #Insert the event to Google Calendar
        event = service.events().insert(calendarId='primary', sendNotifications=True, body=event, conferenceDataVersion=1).execute()
        print('New event is successfully created, here is the link to the event: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)
