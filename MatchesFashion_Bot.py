import requests
import json
from bs4 import BeautifulSoup
import datetime
import time

from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

# Set proxy to use
proxies = {
    'xxx'
}

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        "upgrade-insecure-requests" : "1",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "en-US,en;q=0.9",
        "cache-control" : "max-age=0",
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }

# Create the session and set the proxies.
s = requests.Session()
# s.proxies = proxies


# CRSF Token
print(str(datetime.datetime.now()) + " Retrieving CRSF Token")
r = s.get(url = 'https://www.matchesfashion.com/intl/login', headers = headers)
soup = BeautifulSoup(r.content, "html.parser")


token = soup.find('input', {'name':'CSRFToken'})['value']
print(str(datetime.datetime.now()) + " CRSF token : " + token)
print("===========================================================================")

# Login Process
print(str(datetime.datetime.now()) + " Logging In")
login = {
    'j_username': 'XXX',
    'j_password': 'XXX',
    'CSRFToken': ''
}
login['CSRFToken'] = token
l = s.post(url = 'https://www.matchesfashion.com/intl/login/j_spring_security_check', headers = headers, cookies = r.cookies, data = login)
print(l)

print("===========================================================================")

# ATC Process
print(str(datetime.datetime.now()) + " ATC Process Started")
ATC = {
    'qty': '1',
    'productCodePost': 'XXX',
    'CSRFToken': '',
    'stockcontext': 'web'
}
ATC['CSRFToken'] = token
a = s.post(url = 'https://www.matchesfashion.com/intl/cart/add', headers = headers, cookies = l.cookies, data = ATC)
atc_data = a.json()
if atc_data['cartData']['StockError'] == "":
    print(str(datetime.datetime.now()) + Fore.GREEN + " Successfully Added to Cart")
else:
    print(str(datetime.datetime.now()) + Fore.GREEN + " Item out of stock")
print(atc_data)

print("===========================================================================")

# Apply Coupon
print(str(datetime.datetime.now()) + " Applying Voucher : NEW15")
voucher = {
    'voucherCode': 'NEW15',
    'CSRFToken': ''
}
voucher['CSRFToken'] = token
v = s.post(url = 'https://www.matchesfashion.com/ajax/checkout/voucher/redeem', cookies = a.cookies, headers = headers, data = voucher)
v1 = v.json()
if v1['status'] == "SUCCESS":
    print(Fore.GREEN + "SUCCESSFULLY applied voucher")
else:
    print(Fore.GREEN + "FAILED to apply voucher")
print(v1)

print("===========================================================================")

# Set Billing Address
print(str(datetime.datetime.now()) + " Setting Billing Address")
billing = {
    'addressId': 'XXX',
    'CSRFToken' : ""
}
billing['CSRFToken'] = token
b = s.post(url = 'https://www.matchesfashion.com/ajax/checkout/billingAddress/set', cookies = v.cookies, headers = headers, data = billing)
b1 = b.json()
if b1['status'] == "SUCCESS":
    print(Fore.GREEN + "SUCCESSFULLY set billing address")
else:
    print(Fore.GREEN + "FAILED to set billing address")
print(b1)

print("===========================================================================")

checkout = s.get(url = 'https://www.matchesfashion.com/intl/checkout/review-and-pay', headers = headers)
#soup1 = BeautifulSoup(checkout.content, "html.parser")
#token2 = soup1.find('input', {'class':'hidden edq-config'})['value']
#print(str(datetime.datetime.now()) + " CRSF token : " + token2)

print("===========================================================================")

# Add Card + Place Order
print(str(datetime.datetime.now()) + " Adding Card")
card = {
    'cardType':'visa',
    'cardNumber': 'XXX',
    'cardName':'Chen Yongjin',
    'expireMonth':'XXX',
    'expireYear':'XXX',
    'securityCode':'XXX',
    'saveCardAsDefault':'on',
    'CSRFToken':""
}
card['CSRFToken'] = token

p = s.post(url = 'https://www.matchesfashion.com/ajax/checkout/cardDetails/add', cookies = checkout.cookies, headers = headers, data = json.dumps(card))
p1 = p.json()
print(p1)
c = s.post(url = 'https://www.matchesfashion.com/ajax/checkout/placeOrder', cookies = p.cookies, headers = headers, data = card)
c1 = c.json()
print(c1)
