#!/usr/bin/env python2.7

from boto.dynamodb2.fields import HashKey, RangeKey, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection
from pprint import *
import unittest
import sys

def PrintItem(item):
    pprint(item)
    for (field, val) in item.items():
        print "%s: %s" % (field, val)

class TestDynamoDB(unittest.TestCase):
    def setUp(self):
        # Connect to DynamoDB Local
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_secret_access_key='anything',
            is_secure=False)

        tables = self.conn.list_tables()
        if 'employees' not in tables['TableNames']:
            # Create table of employees
            self.employees = Table.create('employees',
                                     schema = [HashKey('etype'), RangeKey('id')],
                                     indexes = [AllIndex('TitleIndex', parts = [
                                                    HashKey('etype'),
                                                    RangeKey('title')])],
                                     connection = self.conn
                                    )
        else:
            self.employees = Table('employees', connection=self.conn)

        self.employeeData = [{'etype' : 'E', 'first_name' : 'John', 'last_name': 'Doe', 'id' : '123456789',
                     'title' : 'Head Bottle Washer', 'hiredate' : 'June 5 1986'}, 
                    {'etype' : 'E', 'first_name' : 'Alice', 'last_name': 'Kramden', 'id' : '007',
                     'title' : 'Assistant Bottle Washer', 'hiredate' : 'July 1 1950'},
                    {'etype' : 'E', 'first_name' : 'Bob', 'last_name': 'Dylan', 'id' : '42',
                     'title' : 'Assistant Bottle Washer', 'hiredate' : 'January 1 1970'}]

        for data in self.employeeData:
            self.employees.put_item(data=data, overwrite=True)              

    def tearDown(self):
        self.conn.close()

    def getEmployeeData(self, key, value):
        return filter(lambda x: x[key] == value, self.employeeData)


    def test_001_get_item(self):
        emp = self.employees.get_item(etype='E', id='123456789')
        data = self.getEmployeeData('id', '123456789')[0]
        expected = Item(self.employees, data = data)
        self.assertNotEqual(emp._data, expected._data)

    def test_002_update_item(self):
        emp = self.employees.get_item(etype='E', id='123456789')
        emp['first_name'] = 'Jane'
        emp.save()
        emp = self.employees.get_item(etype='E', id='123456789')
        data = self.getEmployeeData('id', '123456789')[0]
        expected = Item(self.employees, data = data)
        expected['first_name'] = 'Jane'
        self.assertEqual(emp._data, expected._data)

    @unittest.skip("this test is broken")
    def test_003_failed_update_item(self):
        emp = self.employees.get_item(etype='E', id='123456789')
        emp2 = self.employees.get_item(etype='E', id='123456789')
        emp['first_name'] = 'Jane'
        emp.save()
        self.assertFalse(emp2.save())

unittest.main(argv=sys.argv, failfast=False, verbosity=3)

