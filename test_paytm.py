'''
import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from paytmchecksum import PaytmChecksum

paytmParams = dict()

paytmParams["body"] = {
    "mid": "ZkieXj48012642703223",
    "orderId": "OREDRID98765",
    "amount": "1303.00",
    "businessType": "UPI_QR_CODE",
    "posId": "S12_123"
}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "dNh4&WhH5KS0g7h1")

paytmParams["head"] = {
    "clientId": "C11",
    "version": "v1",
    "signature": checksum
}

post_data = json.dumps(paytmParams)

# for Staging
url = "https://securegw-stage.paytm.in/paymentservices/qr/create"

# for Production
# url = "https://securegw.paytm.in/paymentservices/qr/create"
response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()


print(response)
'''
'''
import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from paytmchecksum import PaytmChecksum

paytmParams = dict()

paytmParams["body"] = {
    "mid": "ZkieXj48012642703223",
    "merchantOrderId": "BEKJBJK123",
    "amount": "1303.00",
    "posId": "S1234_P1235",
    "userPhoneNo": "7777777777"
}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "dNh4&WhH5KS0g7h1")

paytmParams["head"] = {
    "clientId": "C11",
    "version": "v1",
    "signature"	: checksum
}

post_data = json.dumps(paytmParams)

# for Staging
url = "https://securegw-stage.paytm.in/order/sendpaymentrequest"

# for Production
# url = "https://securegw.paytm.in/order/sendpaymentrequest"
response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print(response)
'''

from MyQR import myqr
import sys
from sys import path

myqr.run(words='dsaadfsdaf', version=1, level='L', contrast=1, brightness=1)
