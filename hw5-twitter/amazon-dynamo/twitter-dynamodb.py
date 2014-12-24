#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
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
if 'twitter' not in tables['TableNames']:
    # Create table of employees
    twitter = Table.create('twitter',
        schema = [HashKey('post_time'), RangeKey('username')],
        #secondary global
        indexes = [AllIndex('PostIndex', parts = [
            HashKey('post_time'),
            RangeKey('post')])],
            connection = conn)
else:
    twitter = Table('twitter', connection=conn)


##############Parse input data#####################    

if (len(sys.argv) is not 3 or sys.argv[1][0] is not '@'):
    print("Usage:\n./%s @<user> <msg>" % (sys.argv[0]))
    sys.exit(1)


########## Handling our post - IT DOESN'T SAVE ON Dynamo
item = Item(twitter, data={ \
    'post_time': time.ctime(), \
    'username': sys.argv[1], \
    #messages must have 140 char
    'msg': sys.argv[2][0:140]} \
    )

####UPLOAD TO DYNAMODB
item.save()

#print by scan order
for emp in twitter.scan():
    PrintItem(emp)

