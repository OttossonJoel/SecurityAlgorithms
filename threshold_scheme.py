# ##############################################
# Implementation of a (k,n) threshold scheme   #
################################################

import sys
import numpy as np

# Parameters that needs to be changed manually are marked with: <--

par_nbr = 1 #<-- participant number
n = 5   #<--
k = 3   #<--
polynom = np.poly1d([14, 4, 16]) #<-- participant's private polynom (in descending order, largest first)

if(n > 8 or k < 3 or k >= n):
    sys.exit("Invalid parameters")

#sum of participant's polynom and collaborates results for the participant's number
par_sum = polynom(par_nbr) + 45 + 57 + 30 + 39  #<--

col_sum = [0] * n
col_sum[par_nbr - 1] = par_sum
col_sum[2 - 1] = 471   #<--
col_sum[4 - 1] = 1381  #<--
#col_sum[5 - 1] = 50751  #<--
#col_sum[6 - 1] = 101700 #<--

#Calculations

tot_sum = 0

for i in range(n):
    if(col_sum[i] != 0):

        num = 1
        for j in range(n):
            if(col_sum[j] != 0 and i != j):
                num *= j+1

        dem = 1
        for j in range(n):
            if(col_sum[j] != 0 and i != j):
                dem *= ((j+1) - (i+1))

        tot_sum += (num/dem) * col_sum[i]

print(tot_sum)
