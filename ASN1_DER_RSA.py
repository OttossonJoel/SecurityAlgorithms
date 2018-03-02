#################################################
# Implementation of function for DER-encoding   #
#################################################

import math
import codecs

def mod_inv(e, p):
    a = p
    b = e
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

#input int
def DER_encode(nbr):
    nbr = int(nbr)
    der = '02'
    nbr_hex = format(nbr, 'x')
    if(len(nbr_hex) % 2 != 0):
        nbr_hex = '0' + nbr_hex

    nbr_hex_bin = "{0:b}".format(int(nbr_hex, 16)).zfill(len(nbr_hex)*4)
    if(nbr_hex_bin[0] == '1'):
        nbr_hex = '00' + nbr_hex

    nbr_len = math.ceil(len(nbr_hex)/2)

    if(nbr_len < 128):

        if(nbr_len < 16):
            der += '0'
        der += format(nbr_len, 'x')
        der += nbr_hex
        return der

    if(nbr_len < 256):
        der += '81'
        der += format(nbr_len, 'x')

    else:
        der += '82'
        if(nbr_len < 4096):
            der += '0'
        der += format(nbr_len, 'x')

    der += nbr_hex
    return der

def RSA_priv_key(p, q):
    version = 0
    e = 65537
    n = p*q
    d = mod_inv(e, (p-1)*(q-1))
    exp1 = d % (p-1)
    exp2 = d % (q-1)
    coef = mod_inv(q, p)

    version = DER_encode(version)
    p = DER_encode(p)
    q = DER_encode(q)
    e = DER_encode(e)
    n = DER_encode(n)
    d = DER_encode(d)
    exp1 = DER_encode(exp1)
    exp2 = DER_encode(exp2)
    coef = DER_encode(coef)

    value = version + n + e + d + p + q + exp1 + exp2 + coef

    value_len = math.ceil(len(value)/2)
    key = '30'

    value_len_hex = format(value_len, 'x')
    if(len(value_len_hex) % 2 != 0):
        value_len_hex = '0' + value_len_hex

    if(value_len < 128):
        key += value_len_hex + value

    else:

        v_len_b = "{0:b}".format(int(len(value_len_hex)/2)).zfill(7)
        v_len_b = '1' + v_len_b
        v_len_b = format(int(v_len_b, 2), 'x')

        if(len(v_len_b) % 2 != 0):
            v_len_b = '0' + v_len_b

        key += v_len_b + value_len_hex + value

    key_base64 = codecs.encode(codecs.decode(key, 'hex'), 'base64').decode()
    return key_base64.replace('\n', '')

#print(DER_encode(104851514188320469851842535897414994825804027352948170823042398663518292867483790970524047257311797943710610482484351309372618495147668788150083166439602199707493246001700413688376623257599044916616943143249661425431940796248852456221265915221633767805203223240532685954755240004577691036186545403012573876059))

print(RSA_priv_key(164114594813800307418447673273331457802487402173218084522602279570759004943271059687980245867351587073874764332560761774240994382474441220210511471982863169720786223197663189087845453185199410925726140702115909207384343131130632724527137836874094130746865061867165444262600737519305143603065906576556601467253, 138860036995238526080367240083285286681635555273154650324671981431526392420382863540566294084899239184605154847615665762977423503412412956533905723990024164641959322001637368919248262573746614094591422079709594652645576162813156700232309643462640201858941733810450453809169981262133674178293379602902911333927))
