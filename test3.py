from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://king:kingqueen@cluster0.opj1s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster['db']
fillings = db['Fillings']
payments = db['Payments']
users = db['Users']
machines = db['Machines']

# Quantity Update
'''
collections.update_one(
    {"_id": '34'},
    {'$set': { "Current_Quantity.Brand1_single": '4'},
     '$currentDate': {'lastModified': True}}
)'''

# Fillings
'''
collections.update_one(
    {'_id': 'a34'},
    {'$push': {
        'Fillings': {
            '$each': [{
                'Date': "12-06-2021",
                "Time": "11:07:58",
                'Brand1_single': '20',
                'Brand2_single': '20',
                'Brand3_single': '20',
                'Brand4_single': '20',
                'Brand1_box': '20',
                'Brand2_box': '20',
                'Brand3_box': '20',
                'Brand4_box': '20'
            }]
        }
    }}
)
'''


machine_id = 'a34'
# Getting the Quantity of the items
'''query = machines.find_one(
    {'_id': machine_id}
)

print(query['Current_Quantity'])
'''

def get_quantity():
    query = machines.find_one(
        {'_id': machine_id}
    )
    return query['Current_Quantity']

quantity = get_quantity()
print(quantity)