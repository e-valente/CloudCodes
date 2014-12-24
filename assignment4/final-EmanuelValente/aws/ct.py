#!/usr/bin/python
import dropbox
import ConfigParser
from pprint import pprint
import gzip
import boto.sqs
from boto.sqs.message import Message
import os

#parsing our token
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
access_token = config.get('Dropbox', 'token')
APP_SECRET = config.get('Dropbox', 'secret')

AWS_REGION = config.get('AWS', 'region')
AWS_ACCESS_KEY_ID = config.get('AWS', 'access_key_id')
AWS_SECRET_ACCESS_KEY = config.get('AWS', 'secret_access_key')
AWS_QUEUE = config.get('AWS', 'queue')

client = dropbox.client.DropboxClient(access_token)

def compress_from_dropbox(target_file):

    global client

    full_target_name = target_file
    tmplist = target_file.split('/')
    target_file = tmplist[-1].strip()

    try:
        dropbox_file  = client.get_file(full_target_name)
        content_dropbox_file = dropbox_file.read()
    except: #ErrorResponse
        print "Fail - opening file " + full_target_name + " in dropbox"
        return False

    #Open file on Dropbox to compress and write on disk locally
    myfile = open(target_file, 'wb')
    myfile.write(content_dropbox_file)
    myfile.close()

    #set file name
    zipfilename = target_file + ".gz"
    zipfilename_to_dropbox = full_target_name + ".gz"

    #Open locally and compress
    f_in = open(target_file, 'rb')
    f_out = gzip.open(zipfilename, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()

    #Send to dropbox
    target_file_content = open(zipfilename, "rb")
    client.put_file(zipfilename_to_dropbox, target_file_content, overwrite=True)

    #delete files on disk
    os.remove(target_file)
    os.remove(zipfilename)
    #print "done"


#Fetch Messages
conn = boto.sqs.connect_to_region(AWS_REGION)
q = conn.get_queue(AWS_QUEUE)
while True:
    m = q.read(wait_time_seconds = 3) # wait up to 3 seconds for message
    if m is None:
        print "NO MESSAGE"
    else:
        #print m.get_body()
        print "sending", m.get_body(), " to compress"
        file_target = m.get_body()
        #removes first slash /
	q.delete_message(m)
        compress_from_dropbox(file_target)

