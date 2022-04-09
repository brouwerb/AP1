import math
from sympy import *
from sympy.abc import i
#  Variablen

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

nab = lambdify([x[0], s, m, g, t, rhof], nabla)

r = 0.0039975 #0
s = 0.35 #1
m = 0.0008445/10 #2
g = 9.807232
t = 3.838235 #3
rhof = 0.001222 #4

ur = 0.0017

print(nab(r, s, m, g, t, rhof))