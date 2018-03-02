###############################################################################
# Implementation of a simplified version of the OTR protocol,                 #
# utilizing Diffie-Hellman key exchange and SMP for mutual authentication.    #
###############################################################################

import socket
import random
import sys
import hashlib

def xor(msg, key):
    msg_bytes = bytes.fromhex(msg)
    msg_int = int.from_bytes(msg_bytes, 'big')
    return hex( msg_int ^ key )


def mod_inv(l, p):
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

    d = (p + calc_list[index])%p

    return d

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("eitn41.eit.lth.se", 1337))

g = 2
g1 = 2
p = int('FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF', 16)

# # # # # # # # # #
#D-H Key Exchange #
# # # # # # # # # #

print('\n--- Initializing D-H Key Exchange ---\n')

#receive g^x1
g_x1 = soc.recv(4096).decode('utf8').strip()
#convert to int
g_x1 = int(g_x1, 16)

x2 = random.randint(1,p-1)
g_x2 = pow(g, x2, p)
#convert to hex
g_x2_str = format(g_x2, 'x')

#send g_x2
soc.send(g_x2_str.encode('utf8'))

#receive ack/nak
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on g^x2')
    sys.exit(0);

key = pow(g_x1, x2, p)
print('--- D-H Key Exchange Complete ---\n')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#Socialist Millionaire Problem for mutual authentication#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print('--- Initializing SMP Handshake ---\n')

#receive g1^a2
g1_a2 = soc.recv(4096).decode('utf8').strip()
g1_a2 = int(g1_a2, 16)

#compute and send g1_b2
b2 = random.randint(1,p-1)
g1_b2 = pow(g1, b2, p)
g1_b2_str = format(g1_b2, 'x')
soc.send(g1_b2_str.encode('utf8'))

#receive ack/nak on g1_b2
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on g1^b2')
    sys.exit(0);

#Calculate g2
g2 = pow(g1_a2, b2, p)

#receive g1^a3
g1_a3 = soc.recv(4096).decode('utf8').strip()
g1_a3 = int(g1_a3, 16)

#compute and send g1_b3
b3 = random.randint(1,p-1)
g1_b3 = pow(g1, b3, p)
g1_b3_str = format(g1_b3, 'x')
soc.send(g1_b3_str.encode('utf8'))

#receive ack/nak on g1_b3
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on g1^b3')
    sys.exit(0);

#Calculate g3
g3 = pow(g1_a3, b3, p)

#receive Pa (g3^a)
pa = soc.recv(4096).decode('utf8').strip()
pa = int(pa, 16)

#compute and send Pb
b = random.randint(1,p-1)
pb = pow(g3, b, p)
pb_str = format(pb, 'x')
soc.send(pb_str.encode('utf8'))

#receive ack/nak on Pb
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on Pb')
    sys.exit(0);

#receive Qa (g1^a * g2^x)
qa = soc.recv(4096).decode('utf8').strip()
qa = int(qa, 16)

#compute and send Qb (g1^b * g2^y), where y is the hash of the key concatenated with the shared pass
key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')
pass_bytes = bytes('eitn41 <3', 'utf-8')
y = hashlib.sha1(key_bytes + pass_bytes).hexdigest()
y = int(y, 16)
qb = (pow(g1, b, p) * pow(g2, y, p)) % p
qb_str = format(qb, 'x')
soc.send(qb_str.encode('utf8'))

#receive ack/nak on Qb
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on Qb')
    sys.exit(0);

#receive Ra (Qa * Qb^-1)^a3
ra = soc.recv(4096).decode('utf8').strip()
ra = int(ra, 16)

#send Rb (Qa * Qb^-1)^b3
qb_inv = mod_inv(qb, p)
rb = pow(qa*qb_inv, b3, p)
rb_str = format(rb, 'x')
soc.send(rb_str.encode('utf8'))

#receive ack/nak on Rb
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('Received nak on Rb')
    sys.exit(0);

#receive ack/nak on authentication
response = soc.recv(4096).decode('utf8').strip()
if(response != 'ack'):
    print('*** Authentication failed ***\n')
    sys.exit(0);

print('--- SMP Handshake Complete ---\n')

# # # # # # #
#Secure Chat#
# # # # # # #
print('--- Initializing Secure Chat ---\n')

msg = 'fdc0a50f5a4c9485b34dcb00714d0cebf053b316' # <-- change message
enc_msg = xor(msg, key)
soc.send(enc_msg.encode('utf8'))
print('Sending Message:', msg)

response = soc.recv(4096).decode('utf8').strip()
print('Message Response:', response, '\n')
