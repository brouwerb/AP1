import uncertainties.unumpy as unumpy  
import numpy 
from roundwitherror import *

   
 

g = 9.807232

   
"""  
 Now any operation that you carry on xerr and yerr will   
 automatically propagate the associated errors, as long  
 as you use the methods provided with uncertainties.unumpy  
 instead of using the numpy methods.  
   
 Let's for instance define z as   
 z = log10(x+y**2)  
 and estimate errz.  
 """  



v = 200/3.6
m = 80
rhof = 1
r = 0.4

rhok = m/((4/3)*(r**3)*numpy.pi)

nabla = ((2*(r**2)*g)/(9*v))*(rhok - rhof)
Re = (r*rhof*v)/nabla


# Print the propagated error errz  

print('eta nach (11)', nabla) 

print('Reynold', Re)
