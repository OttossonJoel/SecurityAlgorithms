###########################################################################################
# A program that simulates the time needed to generate MicroMint coins                    #
# as described in                                                                         #
# R. L. Rivest and A. Shamir - PayWord and MicroMint: Two simple micropayment schemes     #
###########################################################################################

import sys
import math
from random import randint

def simulation(u, k, c):
    b = 2**u #number of bins
    iterations = 0
    coins = 0
    current_bin = 0
    bins = [0 for i in range(b)]

    while(coins < c):
        iterations += 1

        #throw a ball into a randomly selected bin
        current_bin = randint(0, b-1)
        bins[current_bin] += 1
        if(bins[current_bin] == k):
            coins += 1

    return iterations

#
# Main
#
u = int(sys.argv[1]) #number of bits used for identifying the bin
k = int(sys.argv[2]) #the number of collisions (balls in the same bin) needed to make a coin
c = int(sys.argv[3]) #number of coins to generate
conf_width = (int(sys.argv[4])-1)/2
lam = 3.66

sum_x = 0
nbr_of_simulations = 0
x_values = []
mean_dev = 0
mean_x = 0

x = simulation(u,k,c)
x_values.append(x)
sum_x +=  x
nbr_of_simulations +=1
mean_x = sum_x/nbr_of_simulations
mean_dev = 0


while(True):
    x = simulation(u,k,c)
    x_values.append(x)
    sum_x +=  x
    nbr_of_simulations +=1
    mean_x = sum_x/nbr_of_simulations

    for val in x_values:
        mean_dev += (val - mean_x) ** 2
    mean_dev = math.sqrt(mean_dev)/nbr_of_simulations

    if(lam*mean_dev < conf_width):
        break

print(mean_x)
