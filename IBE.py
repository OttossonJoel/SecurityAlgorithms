################################################################################################
# Implementation of an IBE (Identity Based Encryption) system with Cock’s encryption scheme    #
################################################################################################

import hashlib

def jacobi (a, m):
	j = 1
	a %= m
	while a:
		t = 0
		while not a & 1:
			a = a >> 1
			t += 1
		if t&1 and m%8 in (3, 5):
			j = -j
		if (a % 4 == m % 4 == 3):
			j = -j
		a, m = m % a, a
	return j if m == 1 else 0

#returns hexadecimal private key
def PKG(p, q, m, identity):
    a = int(hashlib.sha1(bytes(identity, 'utf-8')).hexdigest(), 16)

    while(jacobi(a,m) != 1):
        a = int(hashlib.sha1(a.to_bytes((a.bit_length() + 7) // 8, 'big')).hexdigest(), 16)

    exp = (m + 5 - int(p,16) - int(q,16))//8

    r = pow(a, exp, m)
    return format(r, 'x')

def decrypt(m, r, msg):
    message = ''

    for s in msg:
        message += '0' if(jacobi(int(s, 16)+2*r, m) == -1) else '1'

    return int(message, 2)


identity = 'faythe@crypto.sec' #<--
p = '9240633d434a8b71a013b5b00513323f' #<--
q = 'f870cfcd47e6d5a0598fc1eb7e999d1b' #<--

f = open('encrypted_bits.txt', 'r') #<--
encrypted_msg = f.read().splitlines()
f.close()

m = int(p, 16) * int(q, 16)

key = PKG(p, q, m, identity)
print('r:',key)

msg = decrypt(m, int(key, 16), encrypted_msg)
print('Decrypted message:', msg)
