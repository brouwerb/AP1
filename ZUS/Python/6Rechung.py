from uncertainties import unumpy  
import numpy 
from roundwitherror import *

   
 

n = 0.002613
un =0.000016
Vk = (265.21e-6)*n
print(Vk)
uVk =75e-6
pk = 3.51e6
upk = 0.25e6
Av = 6.02214e23

n=unumpy.uarray(n, un)
Vk=unumpy.uarray(Vk, uVk)
pk=unumpy.uarray(pk, upk)
Av =  unumpy.uarray(Av,0)

b = Vk/(3*n)
a = 27*b**2*pk


print('b', float(unumpy.nominal_values(b)), float(unumpy.std_devs(b))) 
print('a', round_err(float(unumpy.nominal_values(a)), float(unumpy.std_devs(a))))

a = 27*b**2*pk/Av
b = Vk/(3*n)/Av
print('b', float(unumpy.nominal_values(b)), float(unumpy.std_devs(b)))
print('a', float(unumpy.nominal_values(a)), float(unumpy.std_devs(a)))