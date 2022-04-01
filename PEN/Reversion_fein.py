from turtle import filling
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import math


X_START =[4.5,49.5]
Y_START =[1760,1745]
X_END = [13,54]
Y_END = [1840,1840]
TITEL = "Reversionspendel"
Y_LABEL = r"Periodendauer in ms"
X_LABEL = r"Abstand zu ersten Befestigung cm"
X_ERROR = 0.02
Y_ERROR = 2  #ms
X_MAJOR_TICK = 1
Y_MAJOR_TICK =10
X_MINOR_TICK =0.2
Y_MINOR_TICK = 2
SAVE_AS = "PEN\Reversion_fein.pdf"
POINT_STYLE = ["o","^","x"]
COLOR_STYLE =["red","blue","C3"]
ESTIMATE=[20,45]
#                 s1,ERR1,ERR2
ANNOTATE_POINTS=[[[9.5,1810],[5.5,1780],[8,1767]],[[52,1767],[50,1820],[50,1750]]]


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

fig, ax = plt.subplots(ncols=2)

fig.set_size_inches(8,4)
for J,col in enumerate(ax):

    col.grid()
    popt=[[],[]]
    perr =[[],[]]
    sc=[[],[]]
    aus=[[],[]]
    err=[[],[]]
    for i in range(len(x)):

        sc[i]=col.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10)
        popt[i],perr[i] = optimize.curve_fit(polynom,x[i],y[i])
        xp,yp=genDataFromFunktion(100,X_START[J],X_END[J],popt[i])
        aus[i],=col.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i])

    



    errorLines=[[[],[]],[[],[]]]
    for i in range(len(x)):
        popt[i][0]+=Y_ERROR
        errorLines[i][0] = popt[i].copy()
        xp,yp=genDataFromFunktion(100,X_START[J],X_END[J],popt[i])
        err[i],=col.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i],linestyle="dotted")
        popt[i][0]-= 2*Y_ERROR
        errorLines[i][1] = popt[i].copy()
        xp,yp=genDataFromFunktion(100,X_START[J],X_END[J],popt[i])
        col.plot(xp,yp,linewidth=0.8,color=COLOR_STYLE[i],linestyle="dotted")
        popt[i][0]+= Y_ERROR

    

    def difPol(x):
        return differenceOfPolynoms(x,popt)
    s1=optimize.fsolve(difPol,ESTIMATE[J])
    def difErr1(x):
        return differenceOfPolynoms(x,[errorLines[0][1],errorLines[1][0]])
    sErr1=optimize.fsolve(difErr1,ESTIMATE[J])
    def difErr2(x):
        return differenceOfPolynoms(x,[errorLines[0][0],errorLines[1][1]])
    sErr2=optimize.fsolve(difErr2,ESTIMATE[J])

    def annotate(x,y,annotatePoints):
        col.annotate(f"({round(x,2)} , {round(y,2)})",[x,y],xytext=annotatePoints,
        arrowprops=dict(arrowstyle="->",linewidth=1))
        col.scatter(x,y,s=40,facecolors="none",edgecolors="purple",linewidths=1.5)
        

    annotate(s1[0],polynomByArray(s1[0],popt[0]),ANNOTATE_POINTS[J][0])
    annotate(sErr1[0],polynomByArray(sErr1[0],errorLines[0][1]),ANNOTATE_POINTS[J][1])
    annotate(sErr2[0],polynomByArray(sErr2[0],errorLines[1][1]),ANNOTATE_POINTS[J][2])





    col.set(xlabel=X_LABEL, ylabel=Y_LABEL)
    #plt.title(TITEL,y=1.02)
    #col.scatter(x,y,marker='x',color="C0")
    #col.plot([X_START,X_END],[reg.intercept,intercept+X_END*slope],color="red",linewidth=0.8)


    col.set_xlim(X_START[J],X_END[J])
    col.set_ylim(Y_START[J],Y_END[J])


    # For the minor ticks, use no labels; default NullFormatter.
    col.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
    col.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
    col.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
    col.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
fig.legend([sc[0],aus[0],err[0],sc[1],aus[1],err[1]],["festes Gewicht oben", "Fit Polynom von Ordnung 6",r"Unsicherheit $\pm 2 ms$",
    "loses Gewicht oben", "Fit Polynom von Ordnung 6",r"Unsicherheit $\pm 2 ms$"],loc='upper center', bbox_to_anchor=(0.5, 0.17),
          ncol=3, fancybox=True, shadow=True)
fig.tight_layout()
plt.subplots_adjust(bottom=0.3)
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

