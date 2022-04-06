import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats
import math

X_START =0
Y_START =0
X_END = 45
Y_END = 1
TITEL = ""
Y_LABEL = r"Kraft Qutienten"
X_LABEL = r"Winkel $\alpha$ in $°$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 5
Y_MAJOR_TICK =0.1
X_MINOR_TICK =1
Y_MINOR_TICK = 0.02
SAVE_AS = "./SEB/5Kraftzer.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./POR/Daten.xls')
worksheet = workbook.sheet_by_name('v1')




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

def quotientArray(oben,unten):
    buf=[]
    for i in range(len(oben)):
        buf.append(float(oben[i])/float(unten[i]))
    return buf

def wichtungsFaktor(err):
    return 1/err**2
def gewichteterMittelwert(vals,errs):
    buf =0
    for i in range(len(vals)):
        buf+= vals[i]*wichtungsFaktor(errs[i])
    buf2 =0 
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return buf/buf2
def internerFehler(errs):
    buf=0
    for i in range(len(errs)):
        buf+=wichtungsFaktor(errs[i])
    return np.sqrt(1/buf)
def externerFehler(vals,errs):
    buf1=0
    gewAvg = gewichteterMittelwert(vals,errs)
    for i in range(len(vals)):
        buf1+=wichtungsFaktor(errs[i])*(vals[i]-gewAvg)**2
    buf2 =0
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return np.sqrt(buf1/((len(vals)-1)*buf2))
def intExtFehler(errs,vals):
    return max(internerFehler(errs),externerFehler(vals,errs))


def partOben(vals):
    return 1/vals[1]
def partUnten(vals):
    return -1*vals[0]/vals[1]**2

def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(float(part1(vals)**2*err1**2+part2(vals)**2*err2**2))

def sine(x,buf):
    return np.sin(np.deg2rad(x))
def cos (x,buf):
    return np.cos(np.deg2rad(x))
def tan (x,buf):
    return np.tan(x/180*np.pi)

def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y



Winkel = getAxis(1,0,5)
Zeit = getAxis(1,7,5)
Hangab = getAxis(1,8,5)
NormalF = getAxis(1,9,5)
HangabF = getAxis(1,10,5)
Gewichts = getAxis(1,17,5)
GewichtsF= getAxis(1,18,5)
print(Hangab)
print(Gewichts)
print(HangabF)
print(GewichtsF)

x=[Winkel,Winkel,Winkel]
y =[quotientArray(Hangab,Gewichts),quotientArray(Normal,Gewichts),quotientArray(Hangab,Normal)]
errorsY =[FehlerFort(partOben,partUnten,HangabF[i],GewichtsF[i],[Hangab[i],Gewichts[i]])for i in range(3)]
theoXY = [genDataFromFunktion(100,X_START,X_END,[],sine),genDataFromFunktion(100,X_START,X_END,[],cos),genDataFromFunktion(100,X_START,X_END,[],tan)]
print(tan(10,[]))

#test

plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]
for i in range(len(x)):
    
    ax.errorbar(x[i], y[i],fmt="x",yerr = errorsY[i],xerr =X_ERROR, ecolor = 'black',
        elinewidth=0.5,
        capsize=2,
        capthick=0.5
        )
    sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10,linewidths=1,edgecolors="black",zorder=10)
    theo[i],=ax.plot(theoXY[i][0],theoXY[i][1],color= COLOR_STYLE[i],linestyle="dotted")
ax.legend([sc[0],theo[0],sc[1],theo[1],sc[2],theo[2]],[r"$F_{H}/F_{g}$",r"$sin(\alpha)$",r"$F_{N}/F_{g}$",r"$cos(\alpha)$",r"$F_{H}/F_{N}$",r"$tan(\alpha)$"])
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

