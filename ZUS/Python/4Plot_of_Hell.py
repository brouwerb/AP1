import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import roundwitherror as re
import string

X_START =0.22
Y_START =55
X_END = 0.49
Y_END = 63
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$p*V$   in   $hpa*mm^3$"
X_LABEL = r"$\frac{1}{V}$    in    $\frac{1}{cm^3}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 0.05
Y_MAJOR_TICK = 2
X_MINOR_TICK =0.01
Y_MINOR_TICK = 0.5
SAVE_AS = "./ZUS/Plots/4Plot_of_Hell.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

def Alind(String):
    return [string.ascii_uppercase.index(String[0]),int(String[1]-1)]

def getValFromCell(Cell,path,sheet):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    return worksheet.cell(Alind(Cell)[1], Alind(Cell)[0]).value

Temps = [["B1","B53","B103"],["A1","C1","E1"],["A1","E1","I1"]]
Axis = [[[["A3","A25"],["A29","A51"]],[["A54","A76"],["A80","A101"]],[["A105","A141"],["A148","A171"]]],[[["A3","A25"],["A3","A25"]],[["C3","C25"],["C3","C25"]],[["E3","E23"],["E3","E23"]]],[[["A3","A25"],["A29","A51"]],[["E3","E25"],["E29","E51"]],[["I3","I23"],["I26","I58"]]]]


for i in range(3):
    path = f"./ZUS/Data/G{i+1}.xls"
    for j in range(len(Temps[0])):
        







fig, ax = plt.subplots()
ax.grid()
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

# worksheet.cell(0, 0).value  