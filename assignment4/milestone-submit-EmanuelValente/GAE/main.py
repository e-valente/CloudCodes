from flask import Flask
from flask import abort, redirect, render_template, request, session, url_for
import urllib3
import dropbox
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

@app.route('/')
def Frontend():

    mytime = {}
    mytime['now'] = datetime.datetime.now()
    taskqueue.add(url='/deltaprocessing', params=mytime)
    return ''

"""
Backend that is called when a message is delivered (pushed) from the queue. The
message is delivered via an HTTP POST request.
"""

@app.route('/deltaprocessing', methods=['POST'])
def DeltaProcessing():
    if request.headers.get('X-AppEngine-QueueName') is None:
        # Ignore if not from AppEngine
        abort(403)
    mynow = request.form.get('now') # parameter example
    #print 'Current time is "%s"' % mynow

    conn = boto.sqs.connect_to_region(AWS_REGION, \
        aws_access_key_id = AWS_ACCESS_KEY_ID, \
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

    q = conn.get_queue(AWS_QUEUE)
    m = Message()
    m.set_body(mynow)
    q.write(m)

    return ''
'''
@app.route('/')
def hello():

    """Return a friendly HTTP greeting."""
    return 'Hello World!'
'''
@app.route('/<path:name>')
def process(name):
    client = dropbox.client.DropboxClient(access_token)
    try:
        metadata = client.metadata(name)

        #in this point we know that
        #the file (or dir) exists
        if metadata['is_dir'] == False:
            f = client.get_file(name)
            return f.read()
        else:
            f = client.get_file(name + "/index.html")
            return f.read()

    except ErrorResponse:
        result = "<html><title>Error</title><body><pre>"
        result += "<br><br><br><br><center>a<img src=\"http://speckycdn.sdm.netdna-cdn.com/wp-content/uploads/2010/03/four-oh-four_08.jpg\">"
        result+="</center></pre></body></html>"

        return result

        #return "error 404"


@app.route('/webhook', methods=['GET'])
def verify():

        '''Respond to the webhook verification (GET request) by echoing back the challenge parameter.'''
        return request.args.get('challenge')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
