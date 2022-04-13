import sympy

def error(f, err_vars=None):
    from sympy import Symbol, latex
    s = 0
    latex_names = dict()
    
    if err_vars == None:
        err_vars = f.free_symbols
        
    for v in err_vars:
        err = Symbol('latex_std_' + v.name)
        s += f.diff(v)**2 * err**2
        latex_names[err] = '\\sigma_{' + latex(v) + '}'
        
    return latex(sympy.sqrt(s), symbol_names=latex_names)

r, s, m, t, rhof, rhok, v = sympy.var('r s m t rho_f, rho_k, v')

rhok = m/(4/3*r**3*sympy.pi)
v = s/t


nabla = ((2*(r**2)*9.81)/(9*v))*(rhok - rhof)
print(error(nabla))