from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pytz
import cmsc_calendar
import secret

"""
Modified quickstart code
"""

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
CAL_ID = ""

def main():
    # Get creds to use api
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Get event log
    with open('event_log.txt', 'a+') as f:
        f.close()
    with open('event_log.txt', 'r+') as f:
        event_log = set(f.read().split("\n"))

    # Set google calendar
    if CAL_ID == "":
        # make google calendar
        calendar = {
            'summary': 'CMSC Undergrad Events',
            'timeZone': 'America/New_York'
        }
        goog_cal = service.calendars().insert(body=calendar).execute()
    else:
        goog_cal = service.calendarList().get(calendarId=CAL_ID).execute()

    # get cmsc calendar
    c = cmsc_calendar.Calendar()
    c.connect()

    # add events
    est = pytz.timezone("US/Eastern")
    for e in c.events:
        # skip if logged
        if e.href in event_log:
            continue
        # add event to google calendar
        event = {
            'summary':e.title,
            'description':e.content,
            'start':{
                'dateTime':e.get_start()+('-04:00' if bool(est.localize(e.start_time).dst()) else '-05:00'),
                'timeZone':'America/New_York'
            },
            'end':{
                'dateTime':e.get_end()+('-04:00' if bool(est.localize(e.end_time).dst()) else '-05:00'),
                'timeZone':'America/New_York'
            }
        }
        event = service.events().insert(calendarId=goog_cal['id'], body=event).execute()

        # append to event log
        with open('event_log.txt', 'a') as f:
            f.write(e.href+"\n")
            f.close()
        
if __name__ == '__main__':
    CAL_ID = secret.CAL_ID
    main()
