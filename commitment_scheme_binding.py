########################################################################################
# The probability of breaking the binding property of a commitment scheme x = h(v,k)   #
########################################################################################

from random import randint
import hashlib

def int_to_bytes(int):
    return int.to_bytes((int.bit_length() + 7) // 8, byteorder='big')

X_bits = 40
iterations = 10000000

v = '0' #vote
k = (bin(randint(0,65535))[2:]).zfill(16) #random 16 bit (convert from int to bits), omits the '0b'

con_string = v + k # Concatenates v and k
con_bytes = int_to_bytes(int(con_string, 2)) #Convert the concatenated string to bytes

x = hashlib.sha1(con_bytes).hexdigest() #Hash the bytes and returns hex representation
x_bin = (bin(int(x, 16))[2:]).zfill(160) # Convert to bin

x_first = x_bin[:X_bits]

print("Original hash truncated to:", x_first, "(", X_bits, "bits)")

nbr_collision = 0
v = '1'
for i in range(iterations):
    k = (bin(randint(0,65535))[2:]).zfill(16)

    con_string = v + k
    con_bytes = int_to_bytes(int(con_string, 2))

    x = hashlib.sha1(con_bytes).hexdigest()
    x_bin = (bin(int(x, 16))[2:]).zfill(160)

    x_cut = x_bin[:X_bits]

    if(x_first == x_cut):
        nbr_collision += 1

print("Number of collisions:", nbr_collision)
print("Probability:", (nbr_collision/iterations)*100, "%")
