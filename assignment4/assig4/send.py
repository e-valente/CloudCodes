#!/usr/bin/env python

"""
Sends 10 messages via AWS SQS 'demo' queue.

NOTE: make sure you have a ~/.boto file containing
your AWS credentials.
"""

import boto.sqs
from boto.sqs.message import Message

conn = boto.sqs.connect_to_region("us-west-1")
q = conn.create_queue('myqueue2', 10) # 10-second message visibility
for i in xrange(0,10):
    m = Message()
    m.set_body("Message %d" % i)
    q.write(m)

