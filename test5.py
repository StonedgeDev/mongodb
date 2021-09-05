import datetime
import time

import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://king:kingqueen@cluster0.opj1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster['myFirstDatabase']
machines = db['Machines']
users = db['Users']
payments = db['Payments']
fillings = db['Fillings']
machine_id = 'pad_office'

machine_data = {
    "_id": machine_id,
    "Machine Type": "Sanitary Pad Vending Machine",
    "Machine Code": 'office',
    'Items': {
        'Size1': 'Medium',
        'Size2': 'Large'
    },
    'Current_Quantity': {
        'Size1': '25',
        'Size2': '5'
    },
    'Price': {
        'Brand1_single': '10',
        'Brand2_single': '15'
    },
    'users': [
        {'user_id': 'Ramesh90'},
        {'user_id': 'Suresh80'}
    ]
}


#machines.insert_one(machine_data)

'''
user_data = {
    '_id': 'Ramesh90',
    'First Name': 'Ramesh',
    'Last Name': 'Suresh',
    'Phone Number': '1234567890',
    'Contact': {
        'email': 'ramesh@suresh.com',
        'Address': 'Plot 2, Kings Street, Uppal, Hyderabad',
        'City': 'Hyderabad',
        'State': 'Telengana',
        'Country': 'India',
    },
    'Password': 'FirstMachine',
    'Machines': [
        machine_id
    ]
}

users.insert_one(user_data)
'''

'''
payment_data = {
    '_id': 'ad',
    'Date': "11-07-2021",
    "Machine_id": machine_id,
    "Time": "11:07:58",
    'Purchase': ['One:5', 'Two:6']
}

payments.insert_one(payment_data)
'''


filling_data = {
    'Date': time.localtime(),
    "Time": "11:07:58",
    "Machine_id": machine_id,
    "fillings":['One:20', 'Two:0']
}
fillings.insert_one(filling_data)