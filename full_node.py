############################################################################################
# A program that takes an integer index i, another integer index j, and a set of leaves,   #
# (l(0), l(1), l(2), . . . , l(n − 1)), in a Merkle tree.                                  #
# The program provides:                                                                    #
# The Merkle path for leaf l(i), starting with the sibling of l(i).                        #
# The Merkle path node at a given depth j.                                                 #
# The resulting Merkle root.                                                               #
############################################################################################

import hashlib

f = open('full_node_test.txt', 'r')
lines = f.read().splitlines()
f.close()

leaves = []
last_leaf = ''

#append leaves to list
for line in lines[2:]:
    last_leaf = bytes.fromhex(line)
    leaves.append(last_leaf)
print('Appended ', len(leaves), ' leaves.')

levels = []
level = leaves
levels.append(level)

#create new layers while not at root
while(len(level) > 1):
    if(len(level)%2 != 0):
        level.append(level[len(level) - 1])
        print('Odd number of nodes on depth ', len(level) - 1, ', added copy of last node.')

    pre_level = level
    level = []

    #sum up all nodes in pairs of two and append the resulting hash to a new level
    for i in range(len(pre_level)):
        if(i%2 == 0):
            new_node = bytes.fromhex(hashlib.sha1(pre_level[i] + pre_level[i+1]).hexdigest())
            level.append(new_node)

    levels.append(level)
    print('Appended ', len(level), ' nodes to level ', len(levels))


root = bytes.hex(level[0])
print('Root calculated as ', root)

i = int(lines[0])
j = int(lines[1]) -1

path = []
index = i

#create markle path for leaf at index i
for level in levels[:-1]:
    if(index % 2 == 0):
        path.append('R' + bytes.hex(level[index + 1]))
    else:
        path.append('L' + bytes.hex(level[index - 1]))
    print('Appended element to merklepath at level ', len(path))
    index = index // 2


path = path[::-1]
node_path = path[j]

print(node_path + root)
