from uncertainties import unumpy  
import numpy 
from roundwitherror import *

def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = numpy.average(values, weights=weights)
    # Fast and numerically precise:
    variance = numpy.average((values-average)**2, weights=weights)
    return (average, numpy.sqrt(variance))  
 

d1 = 0.000315
d2 = 0.000365 #0
l1 = 0.03105 #1
l2 = 0.03155
#m = 0.00012
W1 = 129*10**9 #2
W2 = 90.3*10**9


ud = 0.00001
ul = 0.0001
uW1 = 10*10**9
uW2 = 2.9*10**9



d1 = unumpy.uarray(d1, ud)
d2 = unumpy.uarray(d2, ud)
l1 = unumpy.uarray(l1, ul)
l2 = unumpy.uarray(l2, ul)
W1 = unumpy.uarray(W1, uW1)
W2 = unumpy.uarray(W2, uW2)
   
"""  
 Now any operation that you carry on xerr and yerr will   
 automatically propagate the associated errors, as long  
 as you use the methods provided with uncertainties.unumpy  
 instead of using the numpy methods.  
   
 Let's for instance define z as   
 z = log10(x+y**2)  
 and estimate errz.  
 """  

eta1 = (numpy.pi*W1*(d1/2)**4)/(8*l1)
eta2 = (numpy.pi*W2*(d2/2)**4)/(8*l2)




# Print the propagated error errz  

print('eta 1', round_err(float(unumpy.nominal_values(eta1)), float(unumpy.std_devs(eta1)))) 
print('eta 2', round_err(float(unumpy.nominal_values(eta2)), float(unumpy.std_devs(eta2))))

av = gewichteterMittelwert([float(unumpy.nominal_values(eta1)), float(unumpy.nominal_values(eta2))], [unumpy.std_devs(eta1), unumpy.std_devs(eta2)])
averr = intExtFehler([float(unumpy.nominal_values(eta1)), float(unumpy.nominal_values(eta2))], [unumpy.std_devs(eta1), unumpy.std_devs(eta2)])

print('etagesamt', round_err(av, averr))