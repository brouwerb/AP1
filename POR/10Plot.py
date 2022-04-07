from pickletools import optimize
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize, signal
import math
import roundwitherror as re
from sympy import *

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




x=re.getAxis(1,3,34,"./POR/Daten.xls","v4")
y =re.getAxis(1,6,34,'./POR/Daten.xls',"v4")
print(x,y)
popt,perr = optimize.curve_fit(theoKurv,x,y)
perr = np.sqrt(np.diag(perr))
print(popt,perr)

xy =genDataFromFunktion(1000,X_START,X_END,popt,theoKurvArr)


#test

plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]

    

sc=ax.scatter(x,y,marker=POINT_STYLE[0],color=COLOR_STYLE[0],s=8,linewidths=1,edgecolors="black",zorder=10)
theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1])
#ax.legend([sc, theo],[r"Dämpfungskonstante $\lambda$ mit Fehler",r"Theoriekurve $\lambda=k*I^2$ mit $k=$0.89653(30)"])
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

