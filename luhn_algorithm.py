file = open('luhn_algorithm_test.txt', 'r')
lines = file.read().splitlines()
file.close

sumtot = ''

for line in lines:
    line = line[::-1]
    sumline = 0
    var = 1
    xvar = 1

    for char in line:

        var +=1
        mulfactor = 1 + var%2
        if(char == 'X'):
            xvar = mulfactor
        else:
            char = int(char, 10)
            char *= mulfactor
            if(char > 9):
                char -= 9
            sumline += char

    i = (10-(sumline % 10))
    if(i == 10):
        i = 0
    elif(i%2 != 0 and xvar == 2):
        i = (10 + (i - 1))/2
    else:
        i /= xvar

    sumtot += str(int(i))

print(sumtot)
