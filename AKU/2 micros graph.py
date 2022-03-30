import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


X_START =0
Y_START =0
X_END = 90
Y_END = 2500
TITEL = "Zeitdifferenz in Bezug zum Abstand der Mikrophone"
Y_LABEL = r"Zeitdifferenz in $\mu s$"
X_LABEL = r"Abstand in $cm$"
X_ERROR = 0.02887
Y_ERROR = 20
X_MAJOR_TICK = 10
Y_MAJOR_TICK =500
X_MINOR_TICK =2
Y_MINOR_TICK = 100
SAVE_AS = "./AKU/2Mikros.pdf"

workbook = xlrd.open_workbook('./AKU/Testergebnisse.xls')
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

def makeErrorBoxes(xdata,ydata,xerror,yerror,fc='k',ec='None',alpha=0.5):

    # Create list for all the error patches
    errorboxes = []

    # Loop over data points; create box from errors at each point
    for i in range(len(xdata)):
        rect = Rectangle([xdata[i],ydata[i]],xerror,yerror)
        errorboxes.append(rect)

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(errorboxes,facecolor=fc,alpha=alpha,edgecolor=ec)

    # Add collection to axes
    ax.add_collection(pc)



x=getAxis(1,0,13)
y=getAxis(1,1,13)
#test

plt.style.use("./AKU/AP1_style.mplstyle")


slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

fig, ax = plt.subplots()
ax.grid()

ax.errorbar(x, y, yerr = Y_ERROR,fmt='x', ecolor = 'black',color="C0",
    capsize=4,
    capthick=0.5)
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL,title=TITEL)
#makeErrorBoxes(x,y,X_ERROR,Y_ERROR)
#ax.scatter(x,y,marker='x',color="C0")
ax.plot([X_START,X_END],[intercept,intercept+X_END*slope],color="red",linewidth=0.8)


ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)


# For the minor ticks, use no labels; default NullFormatter.
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

plt.legend(("Daten", f"Ausgleichsgerade $a +bx$ \nmit $a={round(intercept,2)}$ und $b={round(slope,2)}$"), loc=4)
print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

