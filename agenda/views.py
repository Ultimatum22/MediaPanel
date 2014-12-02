import pytz
from agenda.models import Event

import google_calendar

import datetime

from django.utils import timezone
from dateutil.parser import parse
from dateutil.relativedelta import *

from itertools import groupby

from django.http import HttpResponse


def index(request):
    max_events = 2

    get_events('dave.nieuwenhuijzen@gmail.com')
    get_events('qv5nr1cqmt4tlut05old032en9g3h6id@import.calendar.google.com')

    events_html = '<table id="events_table"><tbody><tr>'

    now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    all_events = Event.objects.order_by('start_date')
    for start_date, events in groupby(all_events, key=extract_date):
        events = list(events)

        last_event = events[-1]
        if last_event.start_date >= now:
            events_html += '<td>'
            events_html += '<div class="day">' + ('Today' if start_date.strftime("%Y-%d-%m") == now.strftime("%Y-%d-%m") else start_date.strftime("%A, %d/%m")) + '</div>'
            events_html += '<ul>'

        for event in events[:max_events]:
            if event.start_date >= now:
                events_html += '<li><span class="bright">%s</span> <span class="bright semi_bold">%s</span></li>' % (event.start_date.strftime("%H:%M"),  event.summary)

        events_html += '</ul>'
        events_html += '</td>'

    events_html += '</tr></tbody></table>'

    return HttpResponse(events_html)


def extract_date(event):
    return event.start_date.date()


def get_events(calendar_id):
    print 'CalendarId:', calendar_id

    today = datetime.datetime.today()
    today -= relativedelta(days=+1)
    end_date = today + relativedelta(days=+5)

    events = google_calendar.service.events().list(
        calendarId=calendar_id,
        singleEvents=True,
        maxResults=50,
        orderBy='startTime',
        timeMin='%s-%s-%s' % (today.year, today.month, today.day) +'T00:00:00-23:29',
        timeMax='%s-%s-%s' % (end_date.year, end_date.month, end_date.day) +'T00:00:00-23:29',
        ).execute()

    for event in events['items']:
        if 'dateTime' in event['start']:
            start_date_event = event['start']['dateTime']
        else:
            start_date_event = event['start']['date']

        if 'dateTime' in event['end']:
            end_date_event = event['end']['dateTime']
        else:
            end_date_event = event['end']['date']

        #print 'SD: %s - ED: %s - S: %s' % (start_date_event, end_date_event, event['summary'])

        Event(id=event['id'], summary=event['summary'], start_date=parse(start_date_event).replace(tzinfo=pytz.utc), end_date=parse(end_date_event).replace(tzinfo=pytz.utc)).save()

    return events