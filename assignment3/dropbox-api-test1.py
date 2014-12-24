#!/usr/bin/python
import dropbox
import ConfigParser
from pprint import pprint
#url https://www.dropbox.com/developers/core/start/python

app_key = 'f79yomf3e3mv5yj'
app_secret = 'k15eayfnufpe84e'


#builds a DropboxOAuth2FlowNoRedirect object
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

#Have the user sign in and authorize this token
#generates the url to the user click and authorize
authorize_url = flow.start() 

print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()


#Once the user has delivered the authorization code to our app,
# we can exchange that code for an access token via finish:
access_token, user_id = flow.finish(code)


#The access token is all you'll need to make API requests 
#on behalf of this user, so you should store 
#it away for safe-keeping (even though we don't for this tutorial).

#Now that the hard part is done, all we need to do to authorize 
#our API calls is to to pass the access token to DropboxClient. 
#To test that we have got access to the Core API, let's try calling 
#account_info, which will return 
#a dictionary with information about the user's linked account:
client = dropbox.client.DropboxClient(access_token)

print 'linked account: ', client.account_info()


#code.txt is a local file
f = open('code.txt', 'rb')

#put_file -> upload the file to our 
#root app directory (it isn't the user dropbox)
#The variable response will be a dictionary containing 
#the metadata of the newly uploaded file. 

#response = client.put_file('/vaiii.txt', f)
#print "uploades: ", response

#folder_metadata = client.metadata('/')
#print "metadata:", folder_metadata

f, metadata = client.get_file_and_metadata('/teste.txt')
pprint(metadata)
print metadata
print f.read()#cursor ->What's changed since you gave me this cursor?
cursor = None 
while True:
    while True:
        delta = client.delta(cursor)
        pprint(delta)
        cursor = delta['cursor']
        if delta['has_more'] is False:
            break
    raw_input('Press return to continue:')
