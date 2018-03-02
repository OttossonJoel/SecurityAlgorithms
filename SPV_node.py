#######################################################################################################
# A program that takes a file with a leaf node L, given as a hexadecimal string,                      #
# and a Merkle path as input, with each node in the path on a separate line.                          #
# The Merkle path nodes are given in the order of highest depth first, i.e., the leaf node sibling.   #
# Each string representing nodes in the Merkle path is preceded by the letter ’L’ or ’R’,             #
# indicating if the sibling node in the path is a Left or Right node.                                 #
# The program outputs the Merkle root as a hexadecimal string.                                        #
#######################################################################################################
import hashlib

f = open('SPV_node_test.txt', 'r')
lines = f.read().splitlines()
f.close

byte = ''

for line in lines:
    first_char = line[0]

    if(first_char == 'L'):
        line = line[1:]
        byte = bytes.fromhex(line) + byte
        byte = bytes.fromhex(hashlib.sha1(byte).hexdigest())

    elif(first_char == 'R'):
        line = line[1:]
        byte += bytes.fromhex(line)
        byte = bytes.fromhex(hashlib.sha1(byte).hexdigest())

    else:
        byte = bytes.fromhex(line)

print(bytes.hex(byte))
