'''
import requests

url = "https://mercury-uat.phonepe.com/v4/debit/"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-CALLBACK-URL": "https://www.demoMerchant.com/callback"
}

response = requests.request("POST", url, headers=headers)

print(response.text)'''

import requests
headers = {
    'content-type': 'application/json',
}

data = '{ "amount": 1000, "currency": "INR" }'

response = requests.post('https://api.razorpay.com/v1/payments/pay_29QQoUBi66xm2f/capture', headers=headers, data=data, auth=('rzp_live_UWXAYIsDlrNTHV', '74QOlK0dc1uk81nAuX40zmyf'))
for i in response:
    print(i)


