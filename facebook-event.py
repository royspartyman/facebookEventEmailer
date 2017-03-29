#!/usr/bin/env python3

import argparse
import json
import dateutil.parser as dateparser
from datetime import datetime
from facepy import GraphAPI
import smtplib
import keys
# Importing Twilio so we can text my phone
from twilio.rest import TwilioRestClient

class FacebookEvent():
    """
    Grabs the count of people going to a FB event and emails the specified person in our keys.py file
    """
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
        """
        Grab's the event info(count) and tells it to to email
        :param eventId: the FB event ID for today
        :param email: The email we're sending from
        :param password: The password to our email(gmail)
        :return:
        """
        details, guests = ({}, {})

        event = self.graph.get(eventId)

        # All the people attending our event
        event_people = self.graph.get(eventId,
                                      fields='attending_count, interested_count')
        # The number of people interested and attending our fb event
        people_count = event_people['attending_count'] + event_people['interested_count']
        send_email(people_count, email, password)

    def events(self, pageId, email, password):
        details, guests = ({}, {})

        page = self.graph.get(pageId)
        events = self.graph.get(pageId + '/events')
        for event in events['data']:
            event_date = convertTime(event['start_time']).date()
            if event_date == datetime.today().date():
                self.event_info(event['id'], email, password)

def send_email(people_count, email, password):
    """
    Uses the smtplib/Gmail to send emails
    :param people_count:
    :param email:
    :param password:
    :return:
    """
    to = keys.PERSON_WERE_EMAILING
    gmail_user = email
    gmail_pwd = password
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Event Pizza Order \n'
    msg = header + "Hi Lori, \n\nSpartanHackers is throwing a workshop today at 7pm at 1345 Engineering Building with an expected " +  str(people_count + 10)  +\
                  " people. You can contact me at 616-238-3511.\n\nThanks,\nJosh Benner"
    smtpserver.sendmail(gmail_user, to, msg)
    textMessage(msg)
    smtpserver.close()

'''
Twilio function to text our phone
:param msg: Message we're texting to our phone
:return:
'''
def textMessage(msg):

    # Find these values at https://twilio.com/user/account
    account_sid = keys.ACCOUNT_SID
    auth_token = keys.AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    twilio_phone_number = "(616) 920-6564"
    message = client.messages.create(to=keys.USER_PHONE_NUMBER, from_=twilio_phone_number,
                                 body=msg)

def urlId(url):
    return url.rstrip('/').rsplit('/', 1)[-1]


def convertTime(dtStr):
    """
    Converts the event day FB gives us into a datetime object
    :param dtStr:
    :return:
    """
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

    config = readConfig('/Users/joshbenner/Personal-Website/projects/facebookEventEmailer/config.json')
    facebookEvent = FacebookEvent(config['accessToken'])

    if args.id:
        args.id = urlId(args.id)
    if args.action == 'details':
        print(facebookEvent.details(args.id))
    if args.action == 'events' and args.email and args.password:
        print(facebookEvent.events(args.id, args.email, args.password))
