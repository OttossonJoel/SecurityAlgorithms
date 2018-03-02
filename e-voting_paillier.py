# ############################################################
# Implementation of an electronic-voting system based on     #
# the homomorphic property of the Paillier cryptosystem      #
##############################################################

from math import gcd
from math import floor

#Input
f = open('e-voting_paillier_votes.txt', 'r')
votes = f.read().splitlines()
f.close()

p = 1117 #<--
q = 1471 #<--
g = 652534095028 #<--

#Functions
def lcm(x,y):
    return (x*y) / gcd(x,y)

def L(x):
    return floor((x-1)/n)

def my(l):
    a = n
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

    d = (n + calc_list[index])%n

    return d

def decrypt(c):
    return (L( pow(c, lamb, (n**2)) ) * my) % n


#Calculations
n = p * q
lamb = int(lcm(p-1, q-1))

result_L = L(pow(g, lamb, (n**2)))
my = my(result_L)

#homomorphic property of paillier, multiplication of ciphertext results in summation of plaintext
sum_votes = 1
for vote in votes:
    sum_votes *= int(vote)%(n**2)

sum_votes = sum_votes % (n**2)
print("sum_votes", sum_votes)
result = decrypt(sum_votes) % n

if(result > len(votes)):
    result -= n

print("Result:",result)
