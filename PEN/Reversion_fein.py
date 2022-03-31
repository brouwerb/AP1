from turtle import filling
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import math


X_START =2.5
Y_START =1750
X_END = 6.5
Y_END = 1840
TITEL = "Reversionspendel"
Y_LABEL = r"Periodendauer in $ms$"
X_LABEL = r"Befestigungsstellen des losen Gewichts"
X_ERROR = 0.02
Y_ERROR = 2  #ms
X_MAJOR_TICK = 1
Y_MAJOR_TICK =20
X_MINOR_TICK =0.2
Y_MINOR_TICK = 5
SAVE_AS = "PEN\Reversion_fein.pdf"
POINT_STYLE = ["o","^","x"]
COLOR_STYLE =["red","blue","C3"]

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
sc=[[],[]]
aus=[[],[]]
err=[[],[]]
for i in range(len(x)):

    sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10)
    popt[i],perr[i] = optimize.curve_fit(polynom,x[i],y[i])
    xp,yp=genDataFromFunktion(100,X_START,X_END,popt[i])
    aus[i],=ax.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i])

plt.legend(("festes Gewicht oben", "Fit Polynom von Ordnung 6","festes Gewicht oben", "Fit Polynom von Ordnung 6"),loc=1)




errorLines=[[[],[]],[[],[]]]
for i in range(len(x)):
    popt[i][0]+=Y_ERROR
    errorLines[i][0] = popt[i].copy()
    xp,yp=genDataFromFunktion(100,X_START,X_END,popt[i])
    err[i],=ax.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i],linestyle="dotted")
    popt[i][0]-= 2*Y_ERROR
    errorLines[i][1] = popt[i].copy()
    xp,yp=genDataFromFunktion(100,X_START,X_END,popt[i])
    ax.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i],linestyle="dotted")
    popt[i][0]+= Y_ERROR

plt.legend([sc[0],aus[0],err[0],sc[1],aus[1],err[1]],["festes Gewicht oben", "Fit Polynom von Ordnung 6",r"Unsicherheit $\pm 2 ms$",
"festes Gewicht oben", "Fit Polynom von Ordnung 6",r"Unsicherheit $\pm 2 ms$"],loc=1)


def difPol(x):
    return differenceOfPolynoms(x,popt)
s1=optimize.fsolve(difPol,5)
def difErr1(x):
    return differenceOfPolynoms(x,[errorLines[0][1],errorLines[1][0]])
sErr1=optimize.fsolve(difErr1,5)
def difErr2(x):
    return differenceOfPolynoms(x,[errorLines[0][0],errorLines[1][1]])
sErr2=optimize.fsolve(difErr2,5)

def annotate(x,y,tx,ty):
    plt.annotate(f"({round(x,2)} , {round(y,2)})",[x,y],xytext=[tx,ty],
    arrowprops=dict(arrowstyle="->",linewidth=1))
    plt.scatter(x,y,s=40,facecolors="none",edgecolors="purple",linewidths=1.5)
    

annotate(s1[0],polynomByArray(s1[0],popt[0]),5,1800)
annotate(sErr1[0],polynomByArray(sErr1[0],errorLines[0][1]),3.2,1787)
annotate(sErr2[0],polynomByArray(sErr2[0],errorLines[1][1]),4.3,1767)





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

