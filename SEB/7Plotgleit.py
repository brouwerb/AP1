
from decimal import Inexact
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
from roundwitherror import round_err
import math

X_START =0
Y_START =0
X_END = 45
Y_END = 0.5
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$a/g$"
X_LABEL = r"Winkel der schiefen Ebene in $°$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 5
Y_MAJOR_TICK =0.1
X_MINOR_TICK =1
Y_MINOR_TICK = 0.02
SAVE_AS = "./SEB/7Plotgleit.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]


indizes = [[[10, 44], [18, 54], [16, 47]], [[12, 36], [16, 41], [19, 36]], [[5, 23], [6, 24], [6, 24]], [[5, 29], [10, 30], 
[5, 25]]]
Hyp =120.0
g=9.807

def getData(path):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(i!=0 and i!=len(buf)-1):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content

def getPlotable(rData):
    data=[[],[]]
    for i,I in enumerate(rData):
        data[0].append(I[0])
        data[1].append(I[1])
    return data

def getDataVonBis(path,von,bis):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(von<=i and i<bis):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content

def parabel(x,a,b,c):
    return 0.5*a*(x+b)**2+c

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

def theorieFunk(x,mu):
    return math.sin(np.deg2rad(x))-math.cos(np.deg2rad(x))*mu
def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y

angles=[27.5,37.4,48.4,44.4]
for i in range(len(angles)):
    angles[i]= np.rad2deg(np.arcsin(angles[i]/Hyp))

besch =[]
beschErrs =[]
beschGew =[]
beschGewErr =[]
mu =[]
mu=[]
for angle in range(4):
    besch.append([])
    beschErrs.append([])
    for durch in range(3):
        data = getDataVonBis(f"./SEB/Raw_data/{angle+1}#{durch+1}.txt",indizes[angle][durch][0],indizes[angle][durch][1])
        data = getPlotable(data)
        params, errs = optimize.curve_fit(parabel,data[0],data[1])
        besch[angle].append(params[0])
        beschErrs[angle].append(np.sqrt(np.diag(errs))[0])
        print(besch[angle])
        print(beschErrs[angle])
    beschGew.append(gewichteterMittelwert(besch[angle],beschErrs[angle])/g)
    #print(intExtFehler(besch[angle],beschErrs[angle]))
    beschGewErr.append(np.sqrt(intExtFehler(besch[angle],beschErrs[angle])**2/g**2))
    mu.append((math.tan(np.deg2rad(angles[angle]))-beschGew[angle]/math.cos(np.deg2rad(angles[angle]))))
    
    mu.append(np.sqrt(1/np.cos(angles[angle])**2 * beschGewErr[angle]**2))

mures = gewichteterMittelwert(mu,mu)

muresErr = intExtFehler(mu,mu)


fig, ax = plt.subplots()
ax.grid()
errorsOfSlope = []
err1=[[],[]]
sc=[[],[]]
theo = [[],[]]
print(angles)

xy = genDataFromFunktion(100,X_START,X_END,mures,theorieFunk)
xyErr1 = genDataFromFunktion(100,X_START,X_END,mures+muresErr,theorieFunk)
xyErr2 = genDataFromFunktion(100,X_START,X_END,mures-muresErr,theorieFunk)


i=0
a=ax.errorbar(angles,beschGew,fmt=".",yerr=beschGewErr, ecolor="black",color="blue",elinewidth=1,capsize=5,capthick=1)
#ax.plot([X_START,X_END],[reg[i].intercept,reg[i].intercept+X_END*reg[i].slope],linewidth=0.8,color=COLOR_STYLE[i])
#ax.scatter(angles,beschGew,marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=15,linewidths=1,edgecolors="black",zorder=10)
b,=ax.plot(xy[0],xy[1],color="red",linestyle ="dotted")
c=ax.fill_between(xyErr1[0],xyErr1[1],xyErr2[1],color="orange",alpha=0.4)
ax.legend([a,b,c],[r"Messdaten mit Fehler",r"Fit $sin(\alpha)-\mu_{G}*cos(\alpha)$  mit $\mu_{G}=0.17(13)$",r"Fehler des Fits"])

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


plt.show()

