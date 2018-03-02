##################################################################################
# Implentation of the disclosure attack on Mixes, used to disclose IP addresses  #
##################################################################################

from pcapfile import savefile
from ipaddress import IPv4Address

cap = open('cia.log.2.pcap', 'rb')
capfile = savefile.load_savefile(cap, layers=2, verbose=True)

mix_IP = '15.24.22.93'
target_IP = '245.221.13.37'
m = 9

#Learning Phase
batches = []
curr_batch = []
target_flag = 0

#Separate batches, by checking that the that the target is part of the batch
#and that the outgoing source is the mix
for packet in capfile.packets:
    src = packet.packet.payload.src.decode('UTF8')
    dst = packet.packet.payload.dst.decode('UTF8')

    if(src == target_IP):
        target_flag = 1

    if(src == mix_IP and target_flag == 1):
        curr_batch.append(dst)
    elif(src != mix_IP and len(curr_batch) != 0):
        batches.append(curr_batch)
        curr_batch = []
        target_flag = 0

Rj = batches[0]
learn_sets = []
learn_sets.append(Rj)
index = 0

#Separate m mutually disjoint sets
while(len(learn_sets) < m):
    index +=1
    Ri = batches[index]
    intersect = []

    for R in learn_sets:
        intersect += set(Ri).intersection(R)

    if(len(intersect) == 0):
        learn_sets.append(Ri)


#Excluding Phase
index = 0
finished = 0
while(finished == 0):
    index += 1
    R = batches[index]
    R_col = 0
    collision = 0
    R_index = 0

    for Ri in learn_sets:
        if(len(set(R).intersection(Ri)) != 0):
            collision +=1
            Rcol = R_index
        R_index += 1

    if(collision == 1):
        learn_sets[Rcol] = set(learn_sets[Rcol]).intersection(R)

        finished = 1
        for Ri in learn_sets:
            if(len(Ri) > 1):
                finished = 0

print(learn_sets)

sum = 0
for R in learn_sets:
    sum += int(IPv4Address(list(R)[0]))
print (sum)
