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
        global_indexes = [GlobalAllIndex('HashtagIndex', parts = [ HashKey('user_type'), RangeKey('post')]),\
            GlobalAllIndex('UsernameIndex', parts = [ HashKey('user_type'), RangeKey('username')])],
        connection = conn)
        
    
else:
    twitter = Table('twitter', connection=conn)


##############Parse input data#####################    

if (len(sys.argv) < 2):
    print("Usage:\n%s <#keyword|@user>" % (sys.argv[0]))
    sys.exit(1)

mykeyword = sys.argv[1]
mylimit = -1
res = None

if(len(sys.argv) > 2):
    mylimit = int(sys.argv[2])

if mykeyword.startswith("#"):
    res = twitter.query_2(user_type__eq='standard_user', \
        query_filter={'hashtaglist__contains': mykeyword}, index='HashtagIndex', 
        limit=mylimit, reverse=True)
elif mykeyword.startswith("@"):
    res = twitter.query_2(user_type__eq='standard_user', username__eq=mykeyword[1:], 
        index='UsernameIndex', limit=mylimit)

#print posts
if(res is not None):
    for r in res:
        print("%s\t%s\t%s" % (r['username'], r['post_time'], r['post'])) 



