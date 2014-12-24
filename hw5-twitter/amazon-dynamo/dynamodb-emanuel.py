#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
from pprint import *
import inspect

def PrintItem(item):
    pprint(item)
    for (field, val) in item.items():
        print "%s: %s" % (field, val)

# Connect to DynamoDB Local
conn = DynamoDBConnection(
    host='localhost',
    port=8000,
    aws_secret_access_key='foo',
    is_secure=False)

tables = conn.list_tables()

print tables

if 'employees' not in tables['TableNames']:
    # Create table of employees
    employees = Table.create('employees',
                             schema = [HashKey('etype'), RangeKey('id')],
                             indexes = [AllIndex('TitleIndex', parts = [
                                            HashKey('etype'),
                                            RangeKey('title')])],
                             connection = conn
                            )
else:
    employees = Table('employees', connection=conn)

print employees

for data in [{'etype' : 'E', 'first_name' : 'John', 'last_name': 'Doe', 'id' : '123456789',
             'title' : 'Head Bottle Washer', 'hiredate' : 'June 5 1986'},
            {'etype' : 'E', 'first_name' : 'Alice', 'last_name': 'Kramden', 'id' : '007',
             'title' : 'Assistant Bottle Washer', 'hiredate' : 'July 1 1950'},
            {'etype' : 'E', 'first_name' : 'Bob', 'last_name': 'Dylan', 'id' : '42',
             'title' : 'Assistant Bottle Washer', 'hiredate' : 'January 1 1970'}]:

    employees.put_item(data=data, overwrite=True)

print 'XXXXX'

#print inspect.getsource(employees.query_2)

emp = employees.get_item(etype='E', id='123456789')

PrintItem(emp)
'''
emps = employees.query_2(etype__eq='E', title__eq='Assistant Bottle Washer', index='TitleIndex')
for emp in emps:
    PrintItem(emp)

emp = employees.get_item(etype='E', id='123456789')
emp2 = employees.get_item(etype='E', id='123456789')
emp['first_name'] = 'Jane'
emp.save()

emp2['first_name'] = 'Joe'
print emp2.save()

print '*****'
for emp in employees.scan():
    PrintItem(emp)
'''
