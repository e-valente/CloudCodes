#!/usr/bin/env python

import ConfigParser
"""
Receives messages via AWS SQS 'demo' queue. Runs forever,
so you will have to use ^C to kill it.

NOTE: make sure you have a ~/.boto file containing
your AWS credentials.
"""

import boto.sqs
from boto.sqs.message import Message

#parsing our token
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")

AWS_REGION = config.get('AWS', 'region')
AWS_ACCESS_KEY_ID = config.get('AWS', 'access_key_id')
AWS_SECRET_ACCESS_KEY = config.get('AWS', 'secret_access_key')
AWS_QUEUE = config.get('AWS', 'queue')


#Put here the aws region (eg., "us-west-1"),
#acces_key_id and secret key if you want to
#override configs from settings.cfg
'''
AWS_REGION = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_QUEUE = ""
'''

conn = boto.sqs.connect_to_region(AWS_REGION)
q = conn.get_queue(AWS_QUEUE)
while True:
    m = q.read(wait_time_seconds = 3) # wait up to 3 seconds for message
    if m is None:
        print "NO MESSAGE"
    else:
        print m.get_body()
        q.delete_message(m)
