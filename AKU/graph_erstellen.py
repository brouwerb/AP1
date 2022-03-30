import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats


X_START =0
Y_START =0
X_END = 90
Y_END = 2500
TITEL = "Titel"
Y_LABEL = r"Zeitdifferenz in $\mu m$"
X_LABEL = r"Abstand in $cm$"
X_ERROR = 0.02
Y_ERROR = 20
X_MAJOR_TICK = 10
Y_MAJOR_TICK =500
X_MINOR_TICK =2
Y_MINOR_TICK = 100
SAVE_AS = "AKU\Test.pdf"

workbook = xlrd.open_workbook('AKU\Testergebnisse.xls')
worksheet = workbook.sheet_by_name('2 mikros')

def getData(row1,collumn1,row2,collumn2):
    data = []
    for j in range(collumn1,collumn2+1):
        data.append([])
        for i in range(row1,row2):
            data[j].append(worksheet.cell(i, j).value)
        
    return data

def getAxis(row1,collumn1,row2):
    data = []
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return np.array(data)

x=getAxis(1,0,13)
y=getAxis(1,1,13)


plt.style.use("./AKU/AP1_style.mplstyle")


reg = stats.linregress(x,y)

fig, ax = plt.subplots()
ax.grid()

#ax.errorbar(x, y, xerr = X_ERROR, yerr = Y_ERROR,fmt='x', ecolor = 'black',color="C0")
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL,title=TITEL)
ax.scatter(x,y,marker='x',color="C0")
ax.plot([X_START,X_END],[reg.intercept,reg.intercept+X_END*reg.slope],color="red",linewidth=0.8)


ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)


# For the minor ticks, use no labels; default NullFormatter.
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

plt.legend(("Daten", f"Ausgleichsgerade $a +bx$ \nmit $a={round(reg.intercept,2)}$ und $b={round(reg.slope,2)}$"), loc=4)
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

