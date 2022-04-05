import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
from roundwitherror import round_err

X_START =0
Y_START =0
X_END = 16
Y_END = 3
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$F_{Haft}$ in $N$"
X_LABEL = r"$F_{N}$ in $N$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 2
Y_MAJOR_TICK =0.5
X_MINOR_TICK =0.5
Y_MINOR_TICK = 0.1
SAVE_AS = "./SEB/6Haftreib.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

workbook = xlrd.open_workbook('./SEB/SEB.xls')
worksheet = workbook.sheet_by_name('Haftreibung')






def getAxis(row1,collumn1,row2):
    data = []
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return np.array(data)

def getRow(collumn1,row1,collumn2):
    data = []
    for i in range(collumn1,collumn2):
        data.append(worksheet.cell(row1, i).value)    
    return np.array(data)



def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(part1(vals)**2*err1**2+part2(vals)**2*err2**2)



def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y

def studentT(t,n,fehler):
    return t*fehler/np.sqrt(n)
def average(arr):
    buf=0
    for i in range(len(arr)):
        buf+=arr[i]
    return buf/len(arr)
def linreg(x,a,b):
    return a+b*x
def Dreiecksvert(a):
    return a/(2*np.sqrt(6))

def partOben(vals):
    return 1/vals[1]
def partUnten(vals):
    return -1*vals[0]/vals[1]**2
def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(part1(vals)**2*err1**2+part2(vals)**2*err2**2)
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
    return np.sqrt(buf1/(len(vals)-1)*buf2)
def intExtFehler(errs,vals):
    return max([internerFehler(errs),externerFehler(vals,errs)])



Gewicht = np.array(getRow(1,1,4)) * 0.01
Gewichtsfehler = 0.01
KraftmesserF= getRow(1,20,4)
print(KraftmesserF)
x=[Gewicht]
y=[[average(getAxis(2,1,16)),average(getAxis(2,2,16)),average(getAxis(2,3,16))]]
yErr=[[studentT(1.05,15,Dreiecksvert(KraftmesserF[0])),studentT(1.05,15,Dreiecksvert(KraftmesserF[1])),studentT(1.05,15,Dreiecksvert(KraftmesserF[2]))]]
valsmu = [y[0][i]/x[0][i] for i in range(len(y[0]))]
errsmu = [FehlerFort(partOben,partUnten,yErr[0][i],Gewichtsfehler,[y[0][i],x[0][i]]) for i in range(len (y[0]))]
gewmu = gewichteterMittelwert(valsmu,errsmu)
errmu = intExtFehler(valsmu,errsmu)
print(gewmu)
print(errmu)
plt.style.use("./AKU/AP1_style.mplstyle")


reg,err= optimize.curve_fit(linreg,x[0],y[0])
err= np.sqrt(np.diag(err))


fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]
for i in range(len(x)):
    
    ax.errorbar(x[i], y[i],fmt="x",yerr = yErr[i], ecolor = 'black',
        elinewidth=0.5,
        capsize=2,
        capthick=0.5
        )
    sc[i]=ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10,linewidths=1,edgecolors="black",zorder=10)
    theo[i],=ax.plot([X_START,X_END],[reg[0],X_END*reg[1]+reg[0]],color= COLOR_STYLE[i],linestyle="dotted")
ax.legend([sc[0],theo[0]],[r"$F_{H}/F_{g}$",f"fit (a+bx) mit \na= {round_err(reg[0],err[0])} und b= {round_err(reg[1],err[1])}"])
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

