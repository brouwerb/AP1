import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import roundwitherror as re
from uncertainties import unumpy


X_START =0.22
Y_START =5.5
X_END = 0.52
Y_END = 6.3
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$p*V$   in   $pa*m^3$"
X_LABEL = r"$\frac{1}{V}$    in    $\frac{1}{cm^3}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 0.05
Y_MAJOR_TICK = 0.2
X_MINOR_TICK =0.01
Y_MINOR_TICK = 0.05
SAVE_AS = "./ZUS/Plots/3Plot_g3.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./ZUS/Data/G1.xls')
worksheet = workbook.sheet_by_name('Daten')



x=re.getAxis(26,8,46,'./ZUS/Data/G3.xls','Daten')
y = re.getAxis(26,9,46,'./ZUS/Data/G3.xls','Daten')
y = [y[i] *x[i]*0.1 for i in range(len(y))]
x = [1/(x[i])for i in range(len(x))]


plt.style.use("./AKU/AP1_style.mplstyle")

def Gerade (x,a,b):
    return a*x+b

def GeradeArr(x,p):
    return Gerade(x,p[0],p[1])

fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]

popt,perr=optimize.curve_fit(Gerade,x,y)
perr = np.sqrt(np.diag(perr))
print(popt)
xy = re.genDataFromFunktion(200,X_START,X_END,popt,GeradeArr)

sc=ax.scatter(x,y,marker=POINT_STYLE[0],color=COLOR_STYLE[0],s=10,linewidths=1,edgecolors="black",zorder=10)
theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1],linestyle="dotted")
ax.legend([sc,theo],[r"Messdaten",r"Fit : $ax+b$ mit"+"\n"+f"a={re.round_err(popt[0],perr[0])} , b={re.round_err(popt[1],perr[1])}"])
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
temp = unumpy.uarray(273.15+52.5,0.1)
val = unumpy.uarray(popt[1],perr[1])
R=8.314462618

res = val/(temp*R)
print(re.round_err(float(unumpy.nominal_values(res))*1000, float(unumpy.std_devs(res))*1000), "mmol")


