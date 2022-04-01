from math import *

def round_err(num, err,  sig=2):
    posof1digit = floor(log10(abs(err)))
    rnum = round(num, sig-int(floor(log10(abs(err))))-1)
    srnum = str(rnum)
    if posof1digit <= 0:
        abrerr = err*10**(-int(floor(log10(abs(err))))+1)
        while len(srnum.split('.')[1]) <= -posof1digit:
            srnum += '0'
    
    else:
        abrerr = round(err, sig-int(floor(log10(abs(err))))-1)
        srnum = str(int(rnum))
    

    return(srnum + '(' + str(ceil(abrerr)) + ')')

print(round_err(float(input()), float(input())))