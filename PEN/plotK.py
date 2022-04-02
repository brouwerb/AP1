from tkinter import W
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats
from scipy import optimize
import math
import roundwitherror

Fits =[[[[2.25217312, 0.15    ,   3.31242126 ,0.08173956],[2.18692843 ,0.17566002, 3.53409045, 0.94868202],[2.15121613 ,0.1954903 , 3.86274606, 1.9238661 ]],
        [[2.22778397, 0.16340497 ,3.34592159 ,0.94466359],[2.15304351, 0.15956641, 3.64871821, 2.08355101],[2.12151143 ,0.1640976,  4.08609582 ,1.32476386]]],
        [[[2.25285776, 0.31898153, 3.21498939 ,1.54816277],[2.1859024 , 0.2   ,     3.21621283 ,1.15465449],[2.15143556 ,0.25900279, 3.21602224, 2.50805166]],
        [[ 2.22645115 , 0.36652452 , 3.21525205, -0.46575825],[2.15302248 ,0.37370468 ,3.21634713, 0.04223042],[2.1219952,  0.27536607, 3.21664702, 1.19240415]]]]
     





X_START =0
Y_START =0
X_END = 3.5
Y_END = 0.25
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Länge der Röhre in $cm$"
X_LABEL = "Ordnung der Maxima"
X_ERROR = 0.02
Y_ERROR = 1
X_MAJOR_TICK = 1
Y_MAJOR_TICK =0.05
X_MINOR_TICK =1
Y_MINOR_TICK = 0.01
SAVE_AS = "AKU\Test.pdf"
POINT_STYLE = ["o","^","x"]
COLOR_STYLE =["blue","red","C3"]

workbook = xlrd.open_workbook('./AKU/Testergebnisse.xls')
worksheet = workbook.sheet_by_name('stehende welle')

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



def CalK(wge,wgl):
    return (wge**2-wgl**2)/(wge**2+wgl**2)

def getKData(i):
    K=[]
    for j in range(len(Fits[0][0])):
        wge=Fits[0][i][j][2]
        wgl=Fits[1][i][j][2]
        K.append(CalK(wge,wgl))
    return K

def sine(x,a,b,c,d):
    return a+b*np.sin(c*(x+d))


def getErrorsOfFit(xy,data):
    v=0.001
    popt, pconv=optimize.curve_fit(sine,xy[0],xy[1],bounds=((data[0]-v,data[1]-v,data[2]-v,data[3]-v),(data[0]+v,data[1]+v,data[2]+v,data[3]+v)))
    return np.sqrt(np.diag(pconv))

def partGeg(par):
    return (2*par[0])/(par[0]**2+par[1]**2)-(par[0]**2-par[1]**2)/(par[0]**2+par[1]**2)**2 *2*par[0]
def partGl(par):
    return (-2*par[1])/(par[1]**2+par[0]**2)-2*par[1]*(par[0]**2-par[0]**2)/(par[1]**2+par[0]**2)**2

def FehlerFort(part1,part2,err1,err2,val1,val2):
    return np.sqrt(part1(val1)**2*err1**2+part2(val2)**2+err2**2)


x=[[1,2,3],[1,2,3]]
y=[getKData(0),getKData(1)]

xy=[]
errors=[]
Typen=["gegn","gln"]

for typ in range(2):
    errors.append([])
    for fed in range(2):
        errors[typ].append([])
        xy.append([])
        for notch in range(3):
            errors[typ][fed].append([])
            xy[fed].append(getPlotable(getData(f"./PEN/Rawdata/f{fed+1}{Typen[typ]}{notch+1}#1.txt")))
            errors[typ][fed][notch]=getErrorsOfFit(xy[fed][notch],Fits[typ][fed][notch])
#print(errors)
file = open("./PEN/KdataTabel.txt","w")
for fed in range(2):
    for notch in range(3):
        Wgeg = Fits[0][fed][notch][2]
        Wgl = Fits[1][fed][notch][2]
        WgegErr = errors[0][fed][notch][2]
        WglErr = errors[0][fed][notch][2]
        K = CalK(Wgeg,Wgl)
        Kerr= FehlerFort(partGeg,partGl,WgegErr,WglErr,[Wgeg,Wgl],[Wgeg,Wgl])
        file.write(f"{fed+1} & {notch+1} & {roundwitherror.round_err(Wgeg,WgegErr)} & {roundwitherror.round_err(Wgl,WglErr)} & {roundwitherror.round_err(K,Kerr)} // \n")

file.close()



#test

plt.style.use("./AKU/AP1_style.mplstyle")


reg= [stats.linregress(x[0],y[0]),stats.linregress(x[1],y[1])]

#print(reg[0])
fig, ax = plt.subplots()
ax.grid()
errorsOfSlope = []
for i in range(2):
    ax.scatter(x[i],y[i],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=10)
    ax.plot([X_START,X_END],[reg[i].intercept,reg[i].intercept+X_END*reg[i].slope],linewidth=0.8,color=COLOR_STYLE[i])
plt.legend((f"2 $kHz$",f"$a={round(reg[0].intercept,3)}$ und $b={round(reg[0].slope,2)}(31)$"
            ,f"0,5 $kHz$",f"$a={round(reg[1].intercept,2)}$ und $b={round(reg[1].slope,2)}(1.2)$"
            ),loc=4)

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

