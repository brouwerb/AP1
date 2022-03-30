import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats


X_START =0
Y_START =0
X_END = 10
Y_END = 100
TITEL = "Titel"
Y_LABEL = r"Länge der Röhre in $cm$"
X_LABEL = "Ordnung der Maxima"
X_ERROR = 0.02
Y_ERROR = 1
X_MAJOR_TICK = 1
Y_MAJOR_TICK =10
X_MINOR_TICK =10
Y_MINOR_TICK = 2
SAVE_AS = "AKU\Test.pdf"
POINT_STYLE = [".","1","x"]
COLOR_STYLE =["C0","C1","C3"]

workbook = xlrd.open_workbook('./AKU/Testergebnisse.xls')
worksheet = workbook.sheet_by_name('stehende welle')

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

x=[getAxis(12,0,22),getAxis(8,0,11),getAxis(2,0,7)]
y=[getAxis(12,1,22),getAxis(8,1,11),getAxis(2,1,7)]


#test

plt.style.use("./AKU/AP1_style.mplstyle")


reg= [stats.linregress(x[0],y[0]),stats.linregress(x[1],y[1]),stats.linregress(x[2],y[2])]
#print(reg[0])
fig, ax = plt.subplots()
ax.grid()
for i in range(2+1):
    ax.errorbar(x[i], y[i],fmt="x",yerr = Y_ERROR, ecolor = 'black',
        elinewidth=0.5,
        capsize=2,
        capthick=0.5
        )
    ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i])
    ax.plot([X_START,X_END],[reg[i].intercept,reg[i].intercept+X_END*reg[i].slope],linewidth=0.8,color=COLOR_STYLE[i])
plt.legend((f"2 $kHz$",f"$a={round(reg[0].intercept,2)}$ und $b={round(reg[0].slope,2)}$"
            ,f"0,5 $kHz$",f"$a={round(reg[1].intercept,2)}$ und $b={round(reg[1].slope,2)}$"
            ,f"1 $kHz$",f"$a={round(reg[2].intercept,2)}$ und $b={round(reg[2].slope,2)}$" ),title = f"fits mit $y=a+bx$" ,loc=4)

ax.set(xlabel=X_LABEL, ylabel=Y_LABEL,title=TITEL)
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

