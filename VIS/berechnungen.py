import sympy
from sympy import *
from sympy.abc import i
#  Variablen
#x = symarray("x", 5)

x = IndexedBase("x")
u = IndexedBase("u")

r, s, m, t, rhof, rhok, v, g = symbols('r s m t rho_f rho_k v g')
ur, us, um, ut, urho = symbols('u_r u_s u_m u_t u_rho')




rhok = m/(sympy.Rational(4, 3)*r**3*sympy.pi)
v = s/t
init_printing(use_unicode=True)

nabla = ((2*(r**2)*g)/(9*v))*(rhok - rhof)

print(nabla)

gausserr = sqrt((diff(nabla, r)**2 * ur**2) + (diff(nabla, s)**2 * us**2) + (diff(nabla, m)**2 * um**2) + (diff(nabla, t)**2 * ut**2) + (diff(nabla, rhof)**2 * urho**2))

print(latex(simplify(gausserr)))

nab = lambdify([x[0], x[1], x[2], x[3], x[4]], nabla)
gauss = lambdify([x[0], x[1], x[2], x[3], x[4], u[0], u[1], u[2], u[3], u[4]], gausserr)

print(u)

r = 0.0039975 #0
s = 0.35 #1
m = 0.0008445/10 #2
g = 9.807232
t = 3.838235 #3
rhof = 1222 #4

ur = 0.000017
us = 0.00021
um = 0.0000005
ut = 0.14425
urho = 0.0000021

print(nab(r, s, m, t, rhof))
print(gauss(r, s, m, t, rhof, ur, us, um, ut, urho))