from uncertainties import unumpy  
import numpy 
from roundwitherror import *

   
 

n1 = 0.002613
un1 =0.000016
n2 = 0.0025813
un2 =0.0000006
un2 =0.000016
Vk = (265.21e-6)*n1
print(Vk)
uVk = (75e-6)*n1
pk = 3.51e6
upk = 0.25e6
Av = 6.02214e23
Mm = 0.14606


n1=unumpy.uarray(n1, un1)
n2=unumpy.uarray(n2, un2)
Vk=unumpy.uarray(Vk, uVk)
pk=unumpy.uarray(pk, upk)
Av =  unumpy.uarray(Av,0)
Mm = unumpy.uarray(Mm,0)

b = Vk/(3*n1)
a = 27*b**2*pk
rho1 = n1*Mm/Vk
rho2 = n2*Mm/Vk

print('b', float(unumpy.nominal_values(b)), float(unumpy.std_devs(b))) 
print('a', round_err(float(unumpy.nominal_values(a)), float(unumpy.std_devs(a))))
print('rho_krit1',round_err(float(unumpy.nominal_values(rho1)), float(unumpy.std_devs(rho1))))
print('rho_krit2',round_err(float(unumpy.nominal_values(rho2)), float(unumpy.std_devs(rho2))))
b = Vk/(3*n1)/Av
a = 27*b**2*pk
b = Vk/(3*n1)/Av
print('b', float(unumpy.nominal_values(b)), float(unumpy.std_devs(b)))
print('a', float(unumpy.nominal_values(a)), float(unumpy.std_devs(a)))



