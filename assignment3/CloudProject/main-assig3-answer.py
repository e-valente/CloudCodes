from flask import Flask
from flask import abort, redirect, render_template, request, session, url_for
import urllib3
import dropbox
import ConfigParser
from pprint import pprint
from dropbox.rest import ErrorResponse

#parsing our token
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
access_token = config.get('Dropbox', 'token')



app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def hello():

    """Return a friendly HTTP greeting."""
    return 'Hello World!'

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



@app.route('/changes.txt')
def process_changes():
    client = dropbox.client.DropboxClient(access_token)

    result = "<html><title>Changes on Dropbox Folder</title><body><pre>"

    cursor = None
    delta = client.delta(cursor)
    delta_bk = delta

    while delta['has_more']:
        cursor = delta['cursor']
        delta_bk = delta
        delta = client.delta(cursor)

    entries = delta['entries']
    entries_reverse = entries[::-1]


    if(len(entries_reverse) >=20):
        for i in range(20):
            result+=entries_reverse[i][1]['modified'][0:25]+ "\t" + entries_reverse[i][0] +  "\t" + "Modified\n"
    else:
        entries2 = delta_bk['entries']
        entries2_reverse = entries[::-1]
        diff = 20 - len(entries_reverse)
        for i in range(diff):
            result+=entries2_reverse[i][1]['modified'][0:25]+ "\t" + entries2_reverse[i][0] +  "\t" + "Modified\n"

        for i in range(len(entries_reverse) - diff):
            result+=entries_reverse[i][1]['modified'][0:25]+ "\t" + entries_reverse[i][0] +  "\t" + "Modified\n"
    result+="</pre></body></html>"
    return result

@app.route('/webhook', methods=['GET'])
def verify():

        '''Respond to the webhook verification (GET request) by echoing back the challenge parameter.'''
        return request.args.get('challenge')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
