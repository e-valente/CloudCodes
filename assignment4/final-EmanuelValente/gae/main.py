from flask import Flask
from flask import abort, redirect, render_template, request, session, url_for
import urllib3
import dropbox
from hashlib import sha256
import hmac
import threading
import ConfigParser
from pprint import pprint
from dropbox.rest import ErrorResponse
from google.appengine.api import taskqueue
import datetime
import boto.sqs
from boto.sqs.message import Message

#parsing our token
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
access_token = config.get('Dropbox', 'token')
APP_SECRET = config.get('Dropbox', 'secret')

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



app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
"""
Frontend that processes HTTP requests from users. Simply queues a message (task)
with the backend. The default queue for this app is used, hence the name is not
specified.
"""


@app.route('/webhook', methods=['GET'])
def verify():

        '''Respond to the webhook verification (GET request) by echoing back the challenge parameter.'''
        return request.args.get('challenge')

@app.route('/webhook', methods=['POST'])
def Frontend():
     # Make sure this is a valid request from Dropbox
    signature = request.headers.get('X-Dropbox-Signature')
    if signature != hmac.new(APP_SECRET, request.data, sha256).hexdigest():
        abort(403)

    taskqueue.add(url='/deltaprocessing')    

    return " "
    
@app.route('/deltaprocessing', methods=['POST'])
def DeltaProcessing():
    if request.headers.get('X-AppEngine-QueueName') is None:
        # Ignore if not from AppEngine
        abort(403)
    client = dropbox.client.DropboxClient(access_token)

    try:    
        dropbox_file  = client.get_file('/.cursor')
        cursor = dropbox_file.read()
        delta = client.delta(cursor)
    except: #ErrorResponse
        cursor = None
        delta = client.delta(cursor)

    entries = delta['entries']
    

    #if there is only the cursor in delta
    if(len(entries) == 1 and ".cursor" in entries[0][0]):
        update_cursor_file = False

    #garantees that we have real(s) files
    else:
        conn = boto.sqs.connect_to_region(AWS_REGION, \
        aws_access_key_id = AWS_ACCESS_KEY_ID, \
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        #pprint(delta)
        #emulating do-while
        condition = True
        while condition == True:
            for i in range(len(entries)):
                metadata = client.metadata(entries[i][0])
                #print("File for process: ", entries[i][0])
                if(".cursor" not in entries[i][0] \
                    and entries[i][1] != None \
                    and entries[i][0].endswith(".gz") == False \
                    and metadata['is_dir'] == False):
                    q = conn.get_queue(AWS_QUEUE)
                    m = Message()
                    m.set_body(entries[i][0].decode('ascii'))
                    q.write(m)
            cursor = delta['cursor']
            delta = client.delta(cursor)
            entries = delta['entries']
            condition = delta['has_more']
            update_cursor_file = True

    
    if update_cursor_file:
        client.put_file('/.cursor', cursor, overwrite=True)

    return " " 
    
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
