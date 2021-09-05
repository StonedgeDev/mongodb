import datetime

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
def sales_data(month, year):
    query = payments.find(
        {'Machine_id': machine_id}
    )
    send = []
    for i in query:
        if i['Date'].split('-')[2] == year and i['Date'].split('-')[1] == month:
            send.append(i)
    return send

a = sales_data('07', '2021')


''''''
date = list(range(1, 32))
list_s1, list_s2 = [], []
for i in date:
    q_date = str(i) + '-' +  str(datetime.datetime.now().strftime('%m')) + '-' +  str(datetime.datetime.now().strftime('%Y'))
    print(q_date)
    q = payments.find(
        {'$and': [
            {'Machine_id': machine_id},
            {'Date': q_date}
        ]}
    )
    print(list(q))
'''



def sales_data(mode, month, year):
    query1 = eval('''mode.find(
        {'$and':[
            {'Machine_id': machine_id},
            {'Date': {'$regex': '{}-{}'.format(month, year)}}
        ]}
    )''')

    date = list(range(1, 32))
    sale_list = []
    for i in query1:
        for j in date:
            kk = {'One': 0, 'Two': 0}
            if i['Date'].split('-')[0] == str(j):
                for k in i['Purchase']:
                    kk[k.split(':')[0]] += int(k.split(':')[1])
            sale_list.append(kk)
    return query1, sale_list

"""
def sales_data1(mode, month, year):
    query1 = eval('''mode.find(
        {'$and':[
            {'Machine_id': machine_id},
            {'Date': {'$regex': '{}-{}'.format(month, year)}}
        ]}
    )''')
    return query1


now = datetime.datetime.now()
a = sales_data1(payments, now.strftime('%m'), now.strftime('%Y'))

print(a)

for i in a:
    print(i)
"""

'''def fillings_data(month, year):
    query = fillings.find(
        {'Date': {'$regex': '{}-{}'.format(month, year)}}
    )
    return query

a = fillings_data('06', '2021')
for i in a:
    print(i)'''

'''
# Gmail Credentials
sender = "stonedgetechmachines@gmail.com"
receiver = "justtotry1006@gmail.com"
password = "StonEdge$123"

import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


msg = MIMEMultipart('alternative')
msg['Subject'] = "Remainder for the refilling of Vending Machine"
msg['From'] = sender
msg['To'] = receiver

text = "Hi"
html = """\
            <html>
              <head></head>
              <body>
                <p>Hi!</p>
                <b>This is a remainder for the Slot {0}</b><br>
                <p>The quantity remaining are {1}</p>
                <p>You can log into your dashboard <a href="www.google.com">here</a></p>
              </body>
            </html>
            """

filename = 'a.csv'
file = open(filename, 'rb')


part1 = MIMEText(text, 'text')
part2 = MIMEText(html, 'html')
part3 = MIMEApplication(file.read(), Name=filename)

msg.attach(part1)
msg.attach(part2)
msg.attach(part3)

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login(sender, password)
mail.sendmail(sender, receiver, msg.as_string())
mail.quit()

'''

'''
from pandas import DataFrame
query1 = fillings.find()

print(query1)
for i in query1:
    print(i['Date'].strftime('%Y'))

'''

month = datetime.datetime.now().strftime('%m-%Y')
s_date = datetime.datetime.strptime('1-'+month, '%d-%m-%Y')
e_date = datetime.datetime.strptime('31-'+month, '%d-%m-%Y')

query = payments.find(
    {'$and':[
        {'Machine_id': machine_id},
        {'Date': {'$gte': s_date}},
        {'Date': {'$lte': e_date}}
    ]}
)

aa = (e_date-s_date).days
'''
for i in range(aa):
    day = s_month + datetime.timedelta(days=i)
'''

'''
q = payments.aggregate([
    {'$match': {
        'Date': {'$lte': e_month, '$gte': s_month},
        'Machine_id': machine_id
    }},
    {'$group': {
        '_id': {"Date": '$Date', 'purchase': '$Purchase'},
        'Revenue': {'$sum': '$Amount'}
    }
}])

for i in q:
    revenue[i['_id']['Date'].strftime('%d-%m')] = i['Revenue']
    print(i)

'''

'''
days = []

for i in range(aa):
    day = s_date + datetime.timedelta(days=i)
    days.append(day.strftime('%d-%m'))
'''

query1 = eval('''payments.find(
    {'$and':[
        {'Machine_id': machine_id},
        {'Date': {'$gte': s_date}},
        {'Date': {'$lte': e_date}}
    ]}
)''')
'''
m = [(s_date + datetime.timedelta(days=i)).strftime('%d-%m') for i in range(aa) ]
print(m)

revenue_One = [0] * 31
revenue_Two = [0] * 31
sale_One = [0] * 31
sale_Two = [0] * 31

for i in query1:
    print(i)
    if i['Date'].strftime('%d-%m') in m:
        index = m.index(i['Date'].strftime('%d-%m'))
        for j in i['Purchase']:
            exec('revenue_{0}[index] = revenue_{0}[index] + i["Amount"]'.format(j.split(':')[0]))
            exec('sale_{0}[index] = sale_{0}[index] + {1}'.format(j.split(':')[0], int(j.split(':')[1])))



print(revenue_One)
print(revenue_Two)
'''


import datetime
from dateutil.rrule import rrule, MONTHLY, DAILY

from math import ceil
def line_graph(mode, s_date, e_date, type):
    a = {DAILY: '%d-%m', MONTHLY: '%B %y'}


    query1 = eval('''mode.find(
        {'$and':[
            {'Machine_id': machine_id},
            {'Date': {'$gte': s_date}},
            {'Date': {'$lte': e_date}}
        ]}
    )''')

    dates = [dt.strftime(a[type]) for dt in rrule(type, dtstart=s_date, until=e_date)]

    revenue_One = [0] * len(dates)
    revenue_Two = [0] * len(dates)
    sale_One = [0] * len(dates)
    sale_Two = [0] * len(dates)


    for i in query1:
        if i['Date'].strftime(a[type]) in dates:
            index = dates.index(i['Date'].strftime(a[type]))
            for indx, j in enumerate(i['Purchase']):
                exec('sale_{0}[index] = sale_{0}[index] + {1}'.format(j, i['Purchase'][j]))
                exec('revenue_{0}[index] = revenue_{0}[index] + {1}'.format(j, int(i['Amount_breakout'].split(';')[indx])))

    return dates, revenue_One, revenue_Two, sale_One, sale_Two


now_month = datetime.datetime.now().strftime('%m%Y')
now_year = datetime.datetime.now().strftime('%Y')

a = sales_data(payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
b = sales_data(fillings, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
c = sales_data(fillings, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'))
d, e, f, g, h = line_graph(payments, datetime.datetime.strptime('01'+now_month, '%d%m%Y'),  datetime.datetime.strptime('31'+now_month, '%d%m%Y'), DAILY)


print(d)
print(e)
print(f)
#print(g)
#print(h)



