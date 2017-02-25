#!/usr/bin/env python3

import argparse
import json
import dateutil.parser as dateparser
from datetime import datetime
from dateutil.tz import tzlocal
from facepy import GraphAPI
import smtplib

class FacebookEvent():
    '''API documentation:
    https://developers.facebook.com/docs/reference/api/event/
    '''

    def __init__(self, accessToken):
        self.graph = GraphAPI(accessToken, version=2.8)

    def update(self, eventId, **params):
        fields = {}
        for param in params:
            if params[param]:
                fields[param] = params[param]
        return self.graph.post(eventId, **fields)

    def details(self, eventId):
        details, guests = ({}, {})

        event = self.graph.get(eventId)
        rsvps = self.graph.get(eventId + '/attending',
                               fields='email,name')

        details['title'] = event['name']
        if 'description' in event:
            details['desc'] = event['description']
        for rsvp in rsvps['data']:
            if 'email' in rsvp:
                guests[rsvp['email']] = rsvp['name']
            elif 'username' in rsvp:
                guests[rsvp['username'] + '@facebook.com'] = rsvp['name']
            else:
                guests[rsvp['id']] = rsvp['name']
        details['guests'] = guests

        return details

    def event_info(self, eventId, email, password):
        details, guests = ({}, {})

        event = self.graph.get(eventId)
        event_people = self.graph.get(eventId,
                                      fields='attending_count, interested_count')
        people_count = event_people['attending_count'] + event_people['interested_count']
        send_email(people_count, email, password)

    def events(self, pageId, email, password):
        details, guests = ({}, {})

        page = self.graph.get(pageId)
        events = self.graph.get(pageId + '/events')

        for event in events['data']:
            event_date = convertTime(event['start_time'])
            if event_date <= datetime.today():
                if event['id'] == "293157527751045":
                    self.event_info(event['id'], email, password)

def send_email(people_count, email, password):
    to = 'perrym23@msu.edu'
    gmail_user = email
    gmail_pwd = password
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Event Pizza Order \n'
    msg = header + '\n There are ' + str(people_count) + ' people coming to the event today!\n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()

def urlId(url):
    return url.rstrip('/').rsplit('/', 1)[-1]


def convertTime(dtStr):
    dt = dateparser.parse(dtStr)
    dt = dt.replace(tzinfo=None)
    return dt


def readConfig(filePath):
    with open(filePath, 'r') as configFile:
        return json.loads(configFile.read())


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('action', choices=('details', 'events'),
                           help='''use "create" to create a new event,
                           "update" to update an event and
                           "details" to get the event info''')
    argParser.add_argument('--id', help='Page id')
    argParser.add_argument('--email', help='from email')
    argParser.add_argument('--password', help='email password')
    args = argParser.parse_args()

    config = readConfig('config.json')
    facebookEvent = FacebookEvent(config['accessToken'])

    if args.id:
        args.id = urlId(args.id)
    if args.action == 'details':
        print(facebookEvent.details(args.id))
    if args.action == 'events' and args.email and args.password:
        print(facebookEvent.events(args.id, args.email, args.password))
