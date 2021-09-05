import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://king:kingqueen@cluster0.opj1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster['test']
collection = db['test']

