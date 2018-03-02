##########################################################################################
# The probability of breaking the concealing property of a commitment scheme x = h(v,k)  #
##########################################################################################

from random import randint
import hashlib

def int_to_bytes(int):
    return int.to_bytes((int.bit_length() + 7) // 8, byteorder='big')

X_bits = 160

k = (bin(randint(0,2**17))[2:]).zfill(17) #random 17 bit (convert from int to bits), omits the '0b'

k_bytes = int_to_bytes(int(k, 2)) #Convert the concatenated string to bytes

x = hashlib.sha1(k_bytes).hexdigest() #Hash the bytes and returns hex representation
x_bin = (bin(int(x, 16))[2:]).zfill(160) # Convert to bin

x_first = x_bin[:X_bits]

print("Original hash truncated to:", x_first, "(", X_bits, "bits)")

collision = 0
iterations = 0

while(collision == 0):
    iterations += 1

    k = (bin(randint(0,2**17))[2:]).zfill(17)

    k_bytes = int_to_bytes(int(k, 2))

    x = hashlib.sha1(k_bytes).hexdigest()
    x_bin = (bin(int(x, 16))[2:]).zfill(160)

    x_cut = x_bin[:X_bits]

    if(x_first == x_cut):
        collision = 1

print("Number of iterations before collision:", iterations)
