##############################################################################################
# A local simulation of coin withdrawal with 2k quadruples in an untraceable e-cash scheme   #
# based on blind signatures.                                                                 #
##############################################################################################

from random  import randint
from random import sample
from fractions import gcd
import hashlib
import sys


#concatenates values
#takes byte input, returns byte
def h(a, b):
    ab = a + b
    return hashlib.sha1(ab).digest()

#concatenate values
#takes byte input, returns int
def f(a, b):
    ab = a + b
    return int.from_bytes(hashlib.sha1(ab).digest(), byteorder = 'big')

def mod_inv(l,p):
    a = p
    b = l
    c = a % b
    stored = []
    calc_list = []
    index = 0

    while(c > 1):
        stored.append(a)
        a = b
        b = c
        c = a % b
    stored.append(a)
    stored.append(b)
    stored.append(c)

    stored = stored[::-1]
    calc_list = [0]*len(stored)
    calc_list[0] = 1

    while (index < len(calc_list)-2):
        calc_list[index + 2] += calc_list[index]
        calc_list[index + 1] -= (stored[index + 2] // stored[index + 1]) * calc_list[index]
        calc_list[index] = 0
        index += 1

    d = (p + calc_list[index]) % p

    return d

#RSA calculation for the Bank
e = 7
p = 76079
q = 104393
n = p*q
phi = (p-1)*(q-1)

a = phi
b = e
c = a % b
stored = []
calc_list = []
index = 0

while (c > 1):
    stored.append(a)
    a = b
    b = c
    c = a % b
stored.append(a)
stored.append(b)
stored.append(c)

stored = stored[::-1]
calc_list = [0] * len(stored)
calc_list[0] = 1

while (index < len(calc_list) - 2):
    calc_list[index + 2] += calc_list[index]
    calc_list[index + 1] -= (stored[index + 2] // stored[index + 1])*calc_list[index]
    calc_list[index] = 0
    index += 1

d = phi + calc_list[index]
print("Private key calculated as:",d)

#Alice is provided with an ID stored as a byte
ID = 1

#Alice selects 2k quadruples of random integers, caluculates stuff
k = randint(10,50)
quad_values = []
x_values = []
y_values = []
b_values = []

for i in range(2*k):
    #calculates random values
    a = randint(1,100000)
    c = randint(1,100000)
    d = randint(1,100000)
    r = randint(1,100000)

    while(gcd(r,n) != 1):
        r = randint(1,100000)

    #converts to bytes and calculates x, y and b
    a_byte = a.to_bytes((a.bit_length() + 7) // 8, 'big')
    c_byte = c.to_bytes((c.bit_length() + 7) // 8, 'big')
    d_byte = d.to_bytes((d.bit_length() + 7) // 8, 'big')
    XOR = a^ID
    XOR = XOR.to_bytes((XOR.bit_length() + 7) // 8, 'big')
    x = h(a_byte, c_byte)
    y = h(XOR, d_byte)
    b = ((r**e) * f(x,y)) % n

    #appends values to vectors
    quad_values.append([a, c, d, r])
    x_values.append(x)
    y_values.append(y)
    b_values.append(b)

#Bank receieves B vector, selects half of values and sends them back to Alice
return_set = sample(range(len(b_values)), len(b_values)//2)

#Alice receives return_set. Sends variables a,c,d,r for chosen b values.
sample_values = []
for i in return_set:
    sample_values.append(quad_values[i])

#Bank receives the values a,c,d,r for chosen b values.
counter = 0
for i in sample_values:
    a = i[0]
    c = i[1]
    d = i[2]
    r = i[3]

    a_byte = a.to_bytes((a.bit_length() + 7) // 8, 'big')
    c_byte = c.to_bytes((c.bit_length() + 7) // 8, 'big')
    d_byte = d.to_bytes((d.bit_length() + 7) // 8, 'big')
    XOR = a^ID
    XOR = XOR.to_bytes((XOR.bit_length() + 7) // 8, 'big')
    x = h(a_byte, c_byte)
    y = h(XOR, d_byte)
    b = ((r**e) * f(x,y)) % n

    if(b != b_values[return_set[counter]]):
        print("Error, b value not correct! Invalid ID")
        sys.exit()

    counter += 1

print("ID:s are valid, proceeding with coin computation")

#Bank computes the remaining set of b values and the blind signature
calc_set = list(b_values)
for i in return_set:
        calc_set.remove(b_values[i])

signature = 1

for b in calc_set:
    signature *= b**d % n

#Alice also extracts the set of quad_values for the remaining indexes
#The blind signature is sent to Alice, for Alice to extract the signature
calc_values = []
for i in quad_values:
    if(i not in sample_values):
        calc_values.append(i)

r_values = 1
for i in calc_values:
    r_values *= i[3]

print("signature value is: ", signature)
print("r-value is :", r_values)

r_values_inv = mod_inv(r_values, n)
print("r-value mod:", r_values_inv)

coin = signature * r_values_inv
print("Coin computed with signature:", coin)
