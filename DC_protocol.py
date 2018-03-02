################################################################################################
# Implementation of the Dining Cryptographers-protocol, but instead of sending a single bit,   #
# we are sending 16-bit anonymous messages at the same time.                                   #
################################################################################################

SA = '5259'
SB = '0A14'
DA = 'D9FB'
DB = '1820'
M = '07BD'
b = '0'

def XOR(a, b):
    in_a = int(a, 16)
    in_b = int(b, 16)
    return '{0:04x}'.format(in_a^in_b)

if(int(b, 16) == 0):
    result = XOR(SA,SB) + XOR(XOR(SA,SB), XOR(DA,DB))
    print(result)

elif(int(b, 16) == 1):
    result = XOR(XOR(SA,SB), M)
    print(result)
