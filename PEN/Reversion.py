import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import math

X_START =0
Y_START =1600
X_END = 60
Y_END = 2300
TITEL = "Reversionspendel"
Y_LABEL = r"Periodendauer in $ms$"
X_LABEL = r"Befestigungsstellen des losen Gewichts"
X_ERROR = 0.02
Y_ERROR = 2  #ms
X_MAJOR_TICK = 5
Y_MAJOR_TICK =100
X_MINOR_TICK =1
Y_MINOR_TICK = 10
SAVE_AS = "PEN\Reversion_grob.pdf"
POINT_STYLE = ["o","^","x"]
COLOR_STYLE =["red","blue","C3"]
ANNOTATE_TEXT_PREV =["S1","S2"]

workbook = xlrd.open_workbook('./PEN/Reversion.xls')
worksheet = workbook.sheet_by_name('Reversionspendel')

def polynom(x,a,b,c,d,e,f,g):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5+g*x**6
    
def polynomByArray(x,popt):
    return polynom(x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6])

def differenceOfPolynoms(x,popt):
    return polynomByArray(x,popt[0])-polynomByArray(x,popt[1])


def genDataFromFunktion(amount,von,bis,params):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(polynom(x[i],params[0],params[1],params[2],params[3],params[4],params[5],params[6]))

    return x,y


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

x=[getAxis(1,0,26),getAxis(1,0,26)]
y=[getAxis(1,1,26),getAxis(1,2,26)]




plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
popt=[[],[]]
perr =[[],[]]
for i in range(len(x)):

    ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10)
    popt[i],perr[i] = optimize.curve_fit(polynom,x[i],y[i])
    xp,yp=genDataFromFunktion(100,X_START,X_END,popt[i])
    ax.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i])

plt.legend(("festes Gewicht oben", "Fit Polynom von Ordnung 6","loses Gewicht oben", "Fit Polynom von Ordnung 6"),loc=2)
def difPol(x):
    return differenceOfPolynoms(x,popt)
s1=optimize.fsolve(difPol,10)
s2=optimize.fsolve(difPol,45)
plt.annotate(f"{ANNOTATE_TEXT_PREV[0]} = ({round(s1[0],2)} , {round(polynomByArray(s1,popt[0])[0],2)})",[s1,polynomByArray(s1,popt[0])],xytext=[5,1940],
arrowprops=dict(arrowstyle="->",linewidth=1))

plt.annotate(f"{ANNOTATE_TEXT_PREV[1]} = ({round(s2[0],2)} , {round(polynomByArray(s2,popt[0])[0],2)})",[s2,polynomByArray(s2,popt[0])],xytext=[35,1940],
arrowprops=dict(arrowstyle="->",linewidth=1))
#print(perr)

# for i in range(len(x)):
#     popt[i][0]+=Y_ERROR
#     xp,yp=genDataFromFunktion(100,X_START,X_END,popt[i])
#     ax.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i],linestyle="dotted")

ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
plt.title(TITEL,y=1.02)
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

