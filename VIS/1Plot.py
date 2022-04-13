import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import math
import roundwitherror as re

X_START =0
Y_START =0
X_END = 2
Y_END = 200
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
X_LABEL = r"Stromstärke i in $\frac{m^3}{s}$"
Y_LABEL = r"Druck $p$ in Pa"
X_ERROR = 20
Y_ERROR = 2
X_MAJOR_TICK = 0.5
Y_MAJOR_TICK =50
X_MINOR_TICK =0.1
Y_MINOR_TICK = 10
SAVE_AS = "./VIS/1Plot.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

dichteW = 0.997952 *1000
t = 60
g =9.807232


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

def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(float(part1(vals)**2*err1**2+part2(vals)**2*err2**2))


def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y
def Gerade(x,a,b):
    return a*x+b
def GeradeArr(x,a):
    return Gerade(x,a[0],a[1])
def StromI(arr,Dichte,t):
    return [arr[i]*0.001/Dichte/t *10e6 for i in range(len(arr))]
def druck (arr,Dichte,g):
    return [arr[i]*0.01*Dichte*g * 10e-3 for i in range(len(arr))]




y=[druck(re.getAxis(1,6,6,"./VIS/Daten.xls","v1"),dichteW,g),druck(re.getAxis(9,6,15,"./VIS/Daten.xls","v1"),dichteW,g)]
x =[StromI(re.getAxis(1,4,6,"./VIS/Daten.xls","v1"),dichteW,t),StromI(re.getAxis(9,4,15,"./VIS/Daten.xls","v1"),dichteW,t)]
print(x,y)
popt=[[],[]]
perr=[[],[]]
xy =[[],[]]
for i in range(len(x)):
    popt[i],perr[i] = optimize.curve_fit(Gerade,x[i],y[i])
    perr[i]=np.sqrt(np.diag(perr[i]))
    xy[i] =genDataFromFunktion(1000,X_START,X_END,popt[i],GeradeArr)
print(popt,perr)




#test

plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]
sc = [[],[]]
theo =[[],[]]
for i in range(len(x)):
    # sc = ax.errorbar(x, y,fmt=".",yerr = errorsY,xerr=errorsX, ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8,
    #     color=COLOR_STYLE[0])
    sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=8,linewidths=1,edgecolors="black",zorder=10)
    theo[i],=ax.plot(xy[i][0],xy[i][1],color= COLOR_STYLE[i],linestyle="dotted")
ax.legend([sc[0], theo[0],sc[1], theo[1]],[r"Kanüle mit d=0,317(11)",r"Ausgleichsgerade $W*x+b$"+"\n"+r"mit $W=$"+re.round_err(popt[0][0],perr[0][0])+r" $\frac{pa~s}{mm^3}$",
                                        r"Kanüle mit d=0,365(11)",r"Ausgleichsgerade $W*x+b$"+"\n"+r"mit $W=$"+re.round_err(popt[1][0],perr[1][0])+r" $\frac{pa~s}{mm^3}$"],loc=4)
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

