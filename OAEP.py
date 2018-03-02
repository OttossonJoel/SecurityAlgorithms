#########################################################################
# Implementation of OAEP according to specification found in RFC 8017   #
#########################################################################

import math
import hashlib

def XOR(a, b):
    return '{0:04x}'.format( int(a, 16) ^ int(b, 16) ).zfill(len(a))

#converts a nonnegative integer to an octet string (byte string) of a specified length
def I2OSP(x, x_len):
    if(x < 0):
        print("Invalid input, negative value.")
        return None

    if(x >= 256**x_len):
        print("Integer too large")
        return None

    return x.to_bytes(x_len, 'big')

#mgf_seed in hex, mask_len number of bytes
def MGF1(mgf_seed, mask_len):
    h_len = 20
    length = math.ceil((mask_len/h_len)) - 1
    t = ''

    if(mask_len > 2**32 * h_len):
        print("Mask too long!")
        return None

    for counter in range(length + 1):
        c = I2OSP(counter, 4)
        mgf_concat = mgf_seed + bytes.hex(c)
        t += hashlib.sha1(bytes.fromhex(mgf_concat)).hexdigest()

    #truncate to 30 bytes -> include 60 digits in hex form
    return t[:mask_len*2]

def OAEP_encode(m, seed):
    k = 128 #RSA encryption length in bytes, 1028 bit
    h_len = 20 #sha1 output in bytes
    m_len = len(m) #message length
    l = ''

    if(m_len > (k - 2*h_len -2)):
        print("Message too long")
        return None

    lhash = hashlib.sha1(bytes.fromhex(l)).hexdigest()

    ps_len = k - int(m_len/2) - 2*h_len - 2
    ps = '00'*ps_len

    db = lhash + ps + '01' + m
    db_mask = MGF1(seed, k - h_len - 1)
    masked_db = XOR(db, db_mask)
    seed_mask = MGF1(masked_db, h_len)
    masked_seed = XOR(seed, seed_mask)

    em = '00' + masked_seed + masked_db
    return em

def OAEP_decode(em):
    k = 128 #RSA encryption length in bytes, 1028 bit
    h_len = 20 #sha1 output in bytes
    l = ''
    lhash = hashlib.sha1(bytes.fromhex(l)).hexdigest()

    y = em[0:2]
    if(y != '00'):
        print("Decryption error 1")
        return None

    masked_seed = em[2: 2 + h_len*2]
    masked_db = em[2 + h_len*2 : 2 + h_len*2 + (k - h_len -1)*2]

    seed_mask = MGF1(masked_db, h_len)
    seed = XOR(masked_seed, seed_mask)
    db_mask = MGF1(seed, k - h_len - 1)
    db = XOR(masked_db, db_mask)

    lhash_d = db[:h_len*2]
    if(lhash != lhash_d):
        print("Decryption error 2")
        return None

    m_index = db.find('01', h_len*2)
    if(m_index == -1):
        print("Decryption error 3")
        return None

    return db[m_index + 2:]


print('MGF1:',MGF1('601c47ea27444ce24417a1526c8c65ca8c3191f9877343c202', 25))
print('Encode:',OAEP_encode('0d4413b8823db607b594f3d7e86c4db168a4a17eb4fffd97bb71', 'e1683401d63da920ccced24b47c53cca7479f0ec'))
print('Decode:',OAEP_decode('00b2f73d91326091417ed768c1bab03bdf7d32cb15d2345866989457444e4884695e81d6241ec8130c631733247498de28d4b5acfa50496127730f60b29cfad2157ca073fc373e40305f7eaeadcd30a7d591185f84876ca9e9d417f8441127dfb137ff4faf8437bd955e5dc03ed9094e6ea8429fa67e15173c42b2839afbd156'))
