import uncertainties.unumpy as unumpy  
import numpy 
from roundwitherror import *

   
 

r = 0.0039975 #0
s = 0.35 #1
m = 0.00008445 #2
g = 9.807232
t = 3.838235 #3
rhof = 1222 #4
r2 = 0.0533 #5

ur = 0.000017
us = 0.00021
um = 0.0000005/10
ut = 0.14425
urho = 2.1 
ur2 = 0.0006

r=unumpy.uarray(r, ur)
s=unumpy.uarray(s, us)
m=unumpy.uarray(m, um)
t=unumpy.uarray(t, ut)
rhof = unumpy.uarray(rhof, urho)
r2=unumpy.uarray(r2, ur2)
   
"""  
 Now any operation that you carry on xerr and yerr will   
 automatically propagate the associated errors, as long  
 as you use the methods provided with uncertainties.unumpy  
 instead of using the numpy methods.  
   
 Let's for instance define z as   
 z = log10(x+y**2)  
 and estimate errz.  
 """  

rhok = m/(4/3*r**3*numpy.pi)
print(numpy.pi)
print(rhok)
v = s/t

nabla2 = ((2*(r**2)*g)/(9*v*(1 + 2.4*(r/r2))))*(rhok - rhof)
nabla = ((2*(r**2)*g)/(9*v))*(rhok - rhof)
Re = (r*rhof*v)/nabla2


# Print the propagated error errz  

print('eta nach (11)', round_err(float(unumpy.nominal_values(nabla)), float(unumpy.std_devs(nabla)))) 
print('eta nach (12)', round_err(float(unumpy.nominal_values(nabla2)), float(unumpy.std_devs(nabla2))))
print('Reynold', round_err(float(unumpy.nominal_values(Re)), float(unumpy.std_devs(Re))))
print(Re)