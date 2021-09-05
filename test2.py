import pymongo
from pymongo import MongoClient

# Machine ID
machine_id = 'pad_office'

# DataBase
cluster = MongoClient(
    "mongodb+srv://king:kingqueen@cluster0.opj1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster['test']
fillings = db['Fillings']
payments = db['Payments']
users = db['Users']
machines = db['Machines']

'''
# Adding new Machine to the User
users.update_one(
    {'_id': 'Ramesh90'},
    {'$push': {
        'Machines': 'machine 2'
        }
    }
)
'''
