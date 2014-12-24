#!/usr/bin/env python

import dropbox
import ConfigParser
from pprint import pprint
#import pprint

config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')

print token

client = dropbox.client.DropboxClient(token)

print 'linked account: ', client.account_info()


f, metadata = client.get_file_and_metadata('/hello.txt')
pprint(metadata)
print metadata
print f.read()
cursor = None
while True:
    while True:
        delta = client.delta(cursor)
        pprint(delta)
        cursor = delta['cursor']
        if delta['has_more'] is False:
            break
    raw_input('Press return to continue:')
