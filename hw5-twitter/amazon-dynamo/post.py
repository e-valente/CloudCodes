#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2 import connect_to_region
import time, sys, inspect, ConfigParser
from pprint import *

def PrintItem(item):
    #pprint(item)
    print("--------------")
    for (field, val) in item.items():
        print "%s: %s" % (field, val)
def parsePost(msg):
    wordlist = msg.split()
    result = []
    for word in wordlist:
        if word.startswith("#"):
            result.append(word)
    return result    

def makeItem():
    item = Item(twitter, data={ \
        'user_type': "standard_user",
        'post_time': time.ctime(), \
        'username': sys.argv[1][0:10], \
        #messages must have 140 char
        'post': sys.argv[2][0:140],
        'hashtaglist': set(hashtaglist)} \
        )  
    return item              

    

#parsing our access
config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
aws_access_key_id = config.get('Twitter', 'aws_access_key_id')
aws_secret_access_key = config.get('Twitter', 'aws_secret_access_key')
region = config.get("Twitter", 'region')
local = config.get('Twitter', 'local')


########### Connect to DynamoDB
if local == 'True':
    # Connect to DynamoDB Local
    conn = DynamoDBConnection(
        host='localhost',
        port=8000,
        aws_secret_access_key='foo',
        is_secure=False)
else:
    conn = connect_to_region(region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)    

#############################################

###########Try to connect in our table. Otherwise, it creates one#######
tables = conn.list_tables()
#print tables
if 'twitter' not in tables['TableNames']:
    # Create table of employees
    twitter = Table.create('twitter',
        schema = [HashKey('username'), RangeKey('post_time')],
        #global_indexes = [GlobalAllIndex('HashtagIndex', parts = [ HashKey('user_type'), RangeKey('post')])],
        #connection = conn)
        global_indexes = [GlobalAllIndex('HashtagIndex', parts = [ HashKey('user_type'), RangeKey('post')]),
            GlobalAllIndex('UsernameIndex', parts = [ HashKey('user_type'), RangeKey('username')])],
        connection = conn)
        
    
else:
    twitter = Table('twitter', connection=conn)


##############Parse input data#####################    

if (len(sys.argv) is not 3):
    print("Usage:\n%s <user> <msg>" % (sys.argv[0]))
    sys.exit(1)



hashtaglist = parsePost(sys.argv[2][0:140])
if hashtaglist == None:
    hashtaglist = []
    hashtaglist.append("None")


#our Item
item = makeItem()  
res = item.save()

#We are handling with concurrency
#if it fails, it will generates 
#another ctime() string -> rangekey
while res is False:
    item = makeItem()  
    item.save()
