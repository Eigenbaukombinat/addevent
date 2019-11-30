import caldav
from caldav.elements import dav, cdav
from datetime import datetime
import sys
from configparser import ConfigParser
import uuid

config = ConfigParser()
config.read('config.ini')
CALENDAR_URL = config['DEFAULT']['calendar_url']
CALENDAR_UUID = config['DEFAULT']['calendar_uuid']

VCAL_TEMPLATE = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Eigenbaukombinat//CalDAV Client//DE
BEGIN:VTIMEZONE
TZID:Europe/Berlin
BEGIN:STANDARD
DTSTART:20001029T040000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10
TZNAME:CET
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:20000326T020000
RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3
TZNAME:CEST
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
END:DAYLIGHT
END:VTIMEZONE
BEGIN:VEVENT
UID:{uuid}
DTSTAMP:{timestamp}
DTSTART;TZID=Europe/Berlin:{start}
DTEND;TZID=Europe/Berlin:{end}
SUMMARY:{summary}
DESCRIPTION:{description}
CLASS:{klass}
END:VEVENT
END:VCALENDAR
"""


def tfmt(dt):
    return dt.strftime('%Y%m%dT%H%M%S')


def add_event(title, start, end, description='', public=True):
    """Adds an event.
    title..the Summary of the event
    start..Start of the event. Format: YYYY-MM-DD HH:MM
    end..End of the event. Format see above
    description..Description
    public..True/False
    """
    client = caldav.DAVClient(CALENDAR_URL)
    principal = client.principal()
    calendars = principal.calendars()

    for calendar in calendars:
        if CALENDAR_UUID in str(calendar.url):
            break
    
    vcal = VCAL_TEMPLATE.format(
        uuid=uuid.uuid4(),
        timestamp=tfmt(datetime.now()),
        start=tfmt(start),
        end=tfmt(end),
        summary=title,
        description=description,
        klass='PUBLIC' if public else 'PRIVATE',)
    event = calendar.add_event(vcal)
    return event


"""
ev1 = add_event('Testtermin1',
    '2019-06-01 13:30',
    '2019-06-01 14:50')
ev2 = add_event('Testtermin2',
    '2019-06-01 15:30',
    '2019-06-01 17:00',
    'Beschreibung', False)
"""

