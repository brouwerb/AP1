import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
from roundwitherror import round_err

X_START =0
Y_START =0
X_END = 0.1
Y_END = 4
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$Dampfdruck$ in $MPa$"
X_LABEL = r"$Kehrwert$ $t$ in $\frac{1}{^{\circ} C}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 2
Y_MAJOR_TICK =0.5
X_MINOR_TICK =0.5
Y_MINOR_TICK = 0.1
SAVE_AS = "./ZUS/Plots/dampf.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]




Temp = np.array([20, 30, 40])
Druck = np.array([2.108, 2.66, 3.31])

def exp(t, a, c):
    return c * np.exp(-a / t)




plt.style.use("./AKU/AP1_style.mplstyle")


reg,err= optimize.curve_fit(exp,Temp,Druck)
err= np.sqrt(np.diag(err))

ex = np.linspace(0, 100, 100)
ey = exp(ex, reg[0], reg[1])

fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]

sc=ax.scatter(1/Temp,Druck,)
theo,=ax.plot(1/ex,ey, linestyle="dotted")
ax.legend([sc,theo],[r"Messwerte",f"fit ($c \cdot e^{{\\frac{{A}}{{T}}}}$) mit \nA= {round_err(reg[0],err[0])} und c= {round_err(reg[1],err[1])}"])
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
#ax.scatter(x,y,marker='x',color="C0")
#ax.plot([X_START,X_END],[reg.intercept,intercept+X_END*slope],color="red",linewidth=0.8)


ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)


# # For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

