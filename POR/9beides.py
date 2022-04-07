from signal import signal
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize, signal
from roundwitherror import *
import math

X_START =0
Y_START =-20
X_END = 100
Y_END = 20
TITEL = ""
Y_LABEL = r"Kraft Qutienten"
X_LABEL = r"Winkel $\alpha$ in $°$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 5
Y_MAJOR_TICK =0.1
X_MINOR_TICK =1
Y_MINOR_TICK = 0.02
SAVE_AS = "./POR/8comp.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./POR/Daten.xls')
worksheet = workbook.sheet_by_name('v1')

def getAxis(row1,collumn1,row2):
    data = []
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return data

def getRow(collumn1,row1,collumn2):
    data = []
    for i in range(collumn1,collumn2):
        data.append(worksheet.cell(row1, i).value)    
    return np.array(data)

xy = getPlotable(getData("./POR/Raw_data/A3#1.txt"))


# Frequez
def expSin(x,phi,lam,om,be):
    return phi*np.exp(-1*lam*x)*np.cos(om*x+be)


def getomega(xyn):
    for i in range(len(xy[1])):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind = i
            break
    for i in range(ind + 5, len(xy[1])):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind2 = i
            break
    print(xy[0][ind2]-xy[0][ind])
    return (3.1415*2)/(xy[0][ind2]-xy[0][ind])





def expSinArr(x,params):
    return expSin(x,params[0],params[1],params[2],params[3])

def ehoch(x,phi,lam):
    return phi*np.exp(-1*lam*x)
def ehochar(x,params):
    return ehoch(x, params[0], params[1])




#test
xyn = [[], []]
plt.style.use("./AKU/AP1_style.mplstyle")
n = cut(xy)

xyn[0] = xy[0][n:]
xyn[1] = xy[1][n:]
print(getomega(xyn))
#print(xyn)

peaks  = signal.find_peaks(xyn[1], height = 1)
print(peaks[0])
peaks = peaks[0]
xpeak = []
ypeak = []
for i in peaks:
    xpeak.append(xyn[0][i])
    ypeak.append(xyn[1][i])

evar, eerr = optimize.curve_fit(ehoch, xpeak, ypeak)

popt, pconv= optimize.curve_fit(expSin,xyn[0],xyn[1], bounds=((evar[0]*0.8,evar[1]*0.9,getomega(xyn)*0.8,0),(evar[0]*1.2,evar[1]*1.2,getomega(xyn)*1.15,7)))
print(popt, pconv)
err = np.sqrt(np.diag(pconv))
eerr = np.sqrt(np.diag(eerr))
fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]


xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
exs,eys=genDataFromFunktion(1000,0,100,evar,ehochar)

# for i in range(len(x)):
    
#     ax.errorbar(x[i], y[i],fmt="x",yerr = errorsY[i],xerr =X_ERROR, ecolor = 'black',
#         elinewidth=0.5,
#         capsize=2,
#         capthick=0.5
#         )
#     sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10,linewidths=1,edgecolors="black",zorder=10)
#     theo[i],=ax.plot(theoXY[i][0],theoXY[i][1],color= COLOR_STYLE[i],linestyle="dotted")

# ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)

#ax.scatter(xpeak,ypeak,marker='o',color="green", s=100)
#ax.scatter(xy[0][cut(xy)],xy[1][cut(xy)],marker='x',color="orange", s=100)
dat, = ax.plot(xyn[0],xyn[1],color="blue",linewidth=0.8)
theo, = ax.plot(xs,ys,color="red",linewidth=0.8)
expf, = ax.plot(exs,eys,color="purple",linewidth=0.8)
ax.legend([dat,theo, expf],[r"Messdaten",f"Theoriekurve mit $\omega = {round_err(popt[2], err[2])} $", f"einhüllende Expontentialfunktion $ \\varphi = {round_err(evar[0], eerr[0])} \cdot exp({round_err(evar[1], eerr[1])} \cdot x)$"])

ax.set_xlim(xyn[0][0],xyn[0][-1])
ax.set_ylim(0.1,100)
ax.set_yscale('log')


# For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")




# For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
#fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  
# For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
#fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  
plt.show()
#fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

