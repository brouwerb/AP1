import math
from sympy import *
from sympy.abc import i
#  Variablen
x = symarray("x", 5)

x = IndexedBase("x")
uerr = IndexedBase("ui")

r, s, m, t, rhof, rhok, v = symbols('r s m t rho_f, rho_k, v')

g = 9.807232


rhok = x[2]/(4/3*x[0]**3*pi)
v = x[1]/x[3]
init_printing(use_unicode=True)

nabla = ((2*(x[0]**2)*g)/(9*v))*(rhok - x[4])

print(nabla)

gausserr = sqrt(Sum((diff(nabla, x[i])**2*uerr[i]**2), (i, 0, 4)))

print(latex(gausserr))

nab = lambdify([x[0], x[1], x[2], x[3], x[4]], nabla)
gauss = lambdify([x[0], x[1], x[2], x[3], x[4], uerr[0], uerr[1], uerr [2], uerr[3], uerr [4]], gausserr)

r = 0.0039975 #0
s = 0.35 #1
m = 0.0008445/10 #2
g = 9.807232
t = 3.838235 #3
rhof = 0.001222 #4

ur = 0.000017
us = 0.00021
um = 0.0000005
ut = 0.14425
urho = 0.0000021

print(nab(r, s, m, t, rhof))
print(gauss(r, s, m, t, rhof, ur, us, um, ut, urho))