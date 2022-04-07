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
Y_LABEL = r"Auslenkung in Grad"
X_LABEL = r"Zeit in Sekunden"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 10
Y_MAJOR_TICK =50
X_MINOR_TICK =1
Y_MINOR_TICK = 10
SAVE_AS = "./POR/8comp.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./POR/Daten.xls')
worksheet = workbook.sheet_by_name('v2')

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

xy = getPlotable(getData("./POR/Raw_data/A5#3#1.txt"))


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


faktor =  19/76.96*90/12
add = -0.7

#test
hdata = [[], [], []]
for i in range(3):
    hdata[i] = [i*(90/12) for i in getAxis(1, i+1, 18) if i != '']
print(hdata)



xyn = [[], []]
xynrad = [[], []]
plt.style.use("./AKU/AP1_style.mplstyle")
n = cut(xy)

xyn[0] = xy[0][n:]
xynrad = xy[1][n:]

for i in xynrad:
    xyn[1].append(-i*faktor + add)
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

hdatax = [[], [], []]

for j, J in enumerate(hdata):
    for i, I in enumerate(J):
        hdatax[j].append(xpeak[0] + i*(2*math.pi)/popt[2])



hvar, herr = optimize.curve_fit(ehoch, hdatax[0] + hdatax[1] + hdatax[2], hdata[0] + hdata[1] + hdata[2])


err = np.sqrt(np.diag(pconv))
eerr = np.sqrt(np.diag(eerr))
herr = np.sqrt(np.diag(herr))





fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]


xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
exs,eys=genDataFromFunktion(1000,0,100,evar,ehochar)
hxs,hys=genDataFromFunktion(1000,0,100,hvar,ehochar)

# for i in range(len(x)):
    
errorbar = ax.errorbar(hdatax[0], hdata[0],fmt="x",yerr = 36/12, ecolor = 'black',
    elinewidth=0.5,
    capsize=2,
    capthick=0.5
    )
#     sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10,linewidths=1,edgecolors="black",zorder=10)
#     theo[i],=ax.plot(theoXY[i][0],theoXY[i][1],color= COLOR_STYLE[i],linestyle="dotted")

ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)

#ax.scatter(xpeak,ypeak,marker='o',color="green", s=100)
#ax.scatter(xy[0][cut(xy)],xy[1][cut(xy)],marker='x',color="orange", s=100)
mess1 = ax.scatter(hdatax[0],hdata[0],marker='o',color="green", s=10)
mess2 = ax.scatter(hdatax[1],hdata[1],marker='o',color="red", s=10)
mess3 = ax.scatter(hdatax[2],hdata[2],marker='o',color="blue", s=10)
dat, = ax.plot(xyn[0],xyn[1],color="blue",linewidth=0.8)
theo, = ax.plot(xs,ys,color="red",linewidth=0.8)
expf, = ax.plot(exs,eys,color="purple",linewidth=0.8)
htheo, = ax.plot(hxs,hys,color="orange",linewidth=0.8)
ax.legend([dat,theo, expf, mess1, errorbar, mess2, mess3, htheo],[r"Messdaten Computer", f"Theoriekurve mit $\\varphi = {round_err(popt[2], err[2])} rad \, s^{{-1}}$",
    f"einhüllende Expontentialfunktion Computer $ \\varphi = \\varphi_0 \cdot exp(\lambda t)$" + "\n" + 
    f"mit $\\varphi_0 = {round_err(evar[0], eerr[0])}^{{\circ}}$ und $\lambda = {round_err(evar[1], eerr[1])} rad \, s^{{-1}}$",
    r"händische Messreihe 1", r"Unsicherheit händische Messreihe 1", r"händische Messreihe 2", r"händische Messreihe 3",
    f"einhüllende Expontentialfunktion Hand mit" + "\n" + f"$ \\varphi_0 = {round_err(hvar[0], herr[0])}$ und $ \lambda = {round_err(hvar[1], herr[1])} rad \, s^{{-1}}$"])

ax.set_xlim(xyn[0][0],xyn[0][-1])
ax.set_ylim(-ehochar(xyn[0][0], evar), ehochar(xyn[0][0], evar))
#ax.set_yscale('log')


# For the minor ticks, use no labels; default NullFormatter.
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")




# For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  
# For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

\
# worksheet.cell(0, 0).value  

