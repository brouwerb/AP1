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
X_END = 2
Y_END = 1
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$a/g$"
X_LABEL = r"Winkel der schiefen Ebene in $°$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 0.5
Y_MAJOR_TICK =0.2
X_MINOR_TICK =0.1
Y_MINOR_TICK = 0.02
SAVE_AS = "./SEB/multiple.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green","black"]


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
def parabelFromArr(x,vals):
    return parabel(x,vals[0],vals[1],vals[2])

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
def average(arr,ind):
    buf=0
    for i in range(len(arr)):
        buf+=arr[i][ind]
    return buf/len(arr)

angles=[27.5,37.4,48.4,44.4]
for i in range(len(angles)):
    angles[i]= np.rad2deg(np.arcsin(angles[i]/Hyp))

besch =[]
beschErrs =[]
beschGew =[]
beschGewErr =[]
mu =[]
muErr=[]
data=[]
params=[]
for angle in range(4):
    data.append([])
    besch.append([])
    beschErrs.append([])
    params.append([])
    for durch in range(3):
        params[angle].append([])
        dat = getDataVonBis(f"./SEB/Raw_data/{angle+1}#{durch+1}.txt",indizes[angle][durch][0],indizes[angle][durch][1])
        data[angle].append(getPlotable(dat))
        params[angle][durch], errs = optimize.curve_fit(parabel,data[angle][durch][0],data[angle][durch][1])
        besch[angle].append(params[angle][durch][0])
        beschErrs[angle].append(np.sqrt(np.diag(errs))[0])
        print(besch[angle])
        print(beschErrs[angle])
    beschGew.append(gewichteterMittelwert(besch[angle],beschErrs[angle])/g)
    #print(intExtFehler(besch[angle],beschErrs[angle]))
    beschGewErr.append(np.sqrt(intExtFehler(besch[angle],beschErrs[angle])**2/g**2))
    mu.append((math.tan(np.deg2rad(angles[angle]))-beschGew[angle]/math.cos(np.deg2rad(angles[angle]))))
    
    muErr.append(np.sqrt(1/np.cos(angles[angle])**2 * beschGewErr[angle]**2))

mures = gewichteterMittelwert(mu,muErr)

muresErr = intExtFehler(mu,muErr)


fig, ax = plt.subplots()
ax.grid()
errorsOfSlope = []
err1=[[],[]]
sc=[[],[]]
theo = [[],[]]


xy =[]
for i in range(len(angles)):
    
    params[i] = [average(params[i],0),average(params[i],1),average(params[i],2)]
    
    xy.append(genDataFromFunktion(100,X_START,X_END,params[i],parabelFromArr))
    
        


i=0
b=[[],[],[],[]]
for i in range(len(angles)):
    b[i],=ax.plot(xy[i][0],xy[i][1],color=COLOR_STYLE[i])
    for j in range(3):
        a =ax.scatter(data[i][j][0],data[i][j][1],color=COLOR_STYLE[i],marker=POINT_STYLE[j],s=5,alpha=0.7)

ax.legend([b[0],b[1],b[2],b[3]],[f"Winkel = {round(angles[0],2)}",f"Winkel = {round(angles[1],2)}",f"Winkel = {round(angles[2],2)}",f"Winkel = {round(angles[3],2)}"],loc=2)

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

