from pickletools import optimize
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize, signal
import math
import roundwitherror as re
import sympy as sp

X_START =0
Y_START =0
X_END = 10
Y_END = 70
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Amplittude in $°$"
X_LABEL = r"Winkelgeschwindigkeit $\omega$ in $\frac{Rad}{s}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 2
Y_MAJOR_TICK =10
X_MINOR_TICK =0.5
Y_MINOR_TICK = 2
SAVE_AS = "./POR/10Plot.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./POR/Daten.xls')
worksheet = workbook.sheet_by_name('v4')

def xErr(x):
    return np.sqrt(((0.025* x)/np.sqrt(3))**2 + 0.0101/3)
def quotientArray(oben,unten):
    buf=[]
    for i in range(len(oben)):
        buf.append(float(oben[i])/float(unten[i]))
    return buf

def partOben(vals):
    return 1/vals[1]
def partUnten(vals):
    return -1*vals[0]/vals[1]**2

def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y
def theoKurv(x,om0,lam,Mom):
    return Mom/np.sqrt((om0**2-x**2)**2+4*lam**2*x**2)
def theoKurvArr(x,p):
    return theoKurv(x,p[0],p[1],p[2])
def findExtremums(func, arg):
  dy = func.diff(arg)
  ddy = dy.diff(arg)
  return sp.solve(dy, arg)





x=re.getAxis(1,3,34,"./POR/Daten.xls","v4")
y =re.getAxis(1,6,34,'./POR/Daten.xls',"v4")

popt,perr = optimize.curve_fit(theoKurv,x,y,bounds=[[0,0,0],[np.inf,np.inf,np.inf]])
perr = np.sqrt(np.diag(perr))


xy =genDataFromFunktion(1000,X_START,X_END,popt,theoKurvArr)
var = sp.symbols("var")
expr = popt[2]/sp.sqrt((popt[0]**2-var**2)**2+4*popt[1]**2*var**2)
Extremum =findExtremums(expr,var)[2]
schnittpunkte = sp.solve(expr-theoKurvArr(float(str(Extremum)),popt)/sp.sqrt(2),var)
print(schnittpunkte)
#test

plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]
y
def annotate(x,y,x1,y1):
    ax.annotate(f"({round(x,3)} , {round(y,3)})",[x,y],xytext=[x1,y1],
    arrowprops=dict(arrowstyle="->",linewidth=1))
    
        
print(theoKurvArr(float(str(Extremum)),popt))
annotate(Extremum,theoKurvArr(float(str(Extremum)),popt),0.5,60)
annotate(schnittpunkte[2],theoKurvArr(float(str(schnittpunkte[2])),popt),0.5,30)
annotate(schnittpunkte[3],theoKurvArr(float(str(schnittpunkte[3])),popt),4,30)
sc=ax.scatter(x,y,marker=POINT_STYLE[0],color=COLOR_STYLE[0],s=8,linewidths=1,edgecolors="black",zorder=10)
theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1])
ax.plot([0,schnittpunkte[3]],[theoKurvArr(float(str(schnittpunkte[2])),popt),theoKurvArr(float(str(schnittpunkte[3])),popt)],color="green",linestyle="dotted")
ax.plot([schnittpunkte[2],schnittpunkte[2]],[theoKurvArr(float(str(schnittpunkte[2])),popt),0],color="green",linestyle="dotted")
ax.plot([schnittpunkte[3],schnittpunkte[3]],[theoKurvArr(float(str(schnittpunkte[3])),popt),0],color="green",linestyle="dotted")

re.round_err(popt[2],perr[2])
ax.legend([sc, theo],[r"Messdaten",r"Theoriekurve (5) mit"+"\n"+r"$\frac{M_0}{\theta}$="+re.round_err(popt[2],perr[2])+r" $\omega_0=$"+re.round_err(popt[0],perr[0])+"\n"+r"$\lambda=$"+re.round_err(popt[1],perr[1])])
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
#ax.scatter(x,y,marker='x',color="C0")
#ax.plot([X_START,X_END],[reg.intercept,intercept+X_END*slope],color="red",linewidth=0.8)


ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)


# For the minor ticks, use no labels; default NullFormatter.
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

