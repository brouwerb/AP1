from uncertainties import unumpy  
import numpy 
from roundwitherror import *

   
 

d1 = 0.0039975/2 #0
l1 = 31.05 #1
l2 = 31.55
#m = 0.00012
W = 129 #2
W2 = 903


ud = 0.01
ul = 0.1
uW = 10
uW2 = 2.9



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

rhok = m/((4/3)*(r**3)*numpy.pi)
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