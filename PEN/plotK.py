from matplotlib.markers import MarkerStyle
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
     
SchFits =[[[[0.21649635036496342,3.2628175485390445,1.3461548783367518,0.04760948905109491,-29.525716261522128,2.2583133943300515],[0.005476556946792009,0.02230598971075557,0.5076961961290818,0.022353509835514276,1.6641814977427751,0.0054805959642909964]],
            [[0.2026277372262774,3.374378782852423,1.1649504106560689,0.1581430503428508,10.108509229298317,2.190801574923289],[0.0058225549224565605,0.022673496475120375,0.44629586792851794,0.022645801648268554,1.3190436470638096,0.005822415578657265]],
            [[0.18472222222222226,3.5388913387244387,0.4403108421678987,0.3235657761548786,6.026517822670712,2.1538988985110303],[0.005609111226857138,0.01199122174347601,0.2473286833504709,0.012010667250596234,0.7507352984194634,0.005606198984892457]]],
            [[[0.10527518248175179,3.272481751824818,0.7269662437770732,0.06490401555714932,23.927329130554444,2.2297585208948685],[0.0031017101261111174,0.029033838364517332,0.6170354454064232,0.028920733199566746,1.8109881555104446,0.00310020447147233]],
            [[0.15901468830323023,3.433010840015915,1.100060996276056,0.2162683868505843,36.39884178693499,2.152305712687213],[0.005005204986371087,0.019556098784130376,0.38570286351853933,0.01958160257391233,1.1399776385313052,0.005009316025187682]],
            [[0.1591292733109368,3.6519713202127058,0.6401773448791633,0.44172262773722637,31.022496111625767,2.120123885088057],[0.005180576723701646,0.031098500579630685,0.643607057747196,0.031451815986358364,2.120139252401137,0.005188249414532787]]]]


notchAbstand=[28.3,53.2,78.2]


X_START =20
Y_START =0
X_END = 85
Y_END = 0.30
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Kopplungsgrad K"
X_LABEL = r"Kopplungsradius $r$ in cm"
X_ERROR = 0.02
Y_ERROR = 1
X_MAJOR_TICK = 10
Y_MAJOR_TICK =0.05
X_MINOR_TICK =2
Y_MINOR_TICK = 0.01
SAVE_AS = "AKU\Test.pdf"
POINT_STYLE = ["o","^","x","s"]
COLOR_STYLE =["blue","red"]

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
    return np.sqrt(part1(val1)**2*err1**2+part2(val2)**2*err2**2)


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
            print(errors[typ][fed][notch][2])


#Wgeg -------------------------------------------Wgl
file = open("./PEN/KdataTabel.txt","w")
Kval1_ = [[],[]]
Wgeg1_ =[[],[]]
Wgl1_ =[[],[]]
for fed in range(2):
    arrCollector =[[],[],[],[],[],[]]
    for notch in range(3):
        Wgeg = Fits[0][fed][notch][2]
        Wgl = Fits[1][fed][notch][2]
        WgegErr = errors[0][fed][notch][2]
        WglErr = errors[1][fed][notch][2]
        K = CalK(Wgeg,Wgl)
        Kerr= FehlerFort(partGeg,partGl,WgegErr,WglErr,[Wgeg,Wgl],[Wgeg,Wgl])
        arrCollector[0].append(K)
        arrCollector[1].append(Kerr)
        arrCollector[2].append(Wgeg)
        arrCollector[3].append(WgegErr)
        arrCollector[4].append(Wgl)
        arrCollector[5].append(WglErr)
        file.write(f"{fed+1} & {notchAbstand[notch]} & {roundwitherror.round_err(Wgeg,WgegErr)} & {roundwitherror.round_err(Wgl,WglErr)} & {roundwitherror.round_err(K,Kerr)} \\\\ \n")
        print(f"{fed+1} & {notchAbstand[notch]} & {roundwitherror.round_err(Wgeg,WgegErr)} & {roundwitherror.round_err(Wgl,WglErr)} & {roundwitherror.round_err(K,Kerr)} \\\\")
    Kval1_[fed].append(arrCollector[0])
    Kval1_[fed].append(arrCollector[1])
    Wgeg1_[fed].append(arrCollector[2])
    Wgeg1_[fed].append(arrCollector[3])
    Wgl1_[fed].append(arrCollector[4])
    Wgl1_[fed].append(arrCollector[5])
file.close()
#Wm--------------------------------------------Ws
Kval_ = [[],[]]
Wgeg_ =[[],[]]
Wgl_ =[[],[]]
file = open("./PEN/SchwdataTabel.txt","w")
for fed in range(2):
    arrCollector =[[],[],[],[],[],[]]
    for notch in range(3):
        Wm = SchFits[fed][notch][0][1]
        Ws = SchFits[fed][notch][0][3]
        WmErr = SchFits[fed][notch][1][1]
        WsErr = SchFits[fed][notch][1][3]
        Wgeg = Wm+Ws
        Wgl= Wm-Ws
        WgegErr = np.sqrt(WmErr**2+WsErr**2)
        WglErr = np.sqrt(WmErr**2+WsErr**2)
        K = CalK(Wgeg,Wgl)
        Kerr= FehlerFort(partGeg,partGl,WgegErr,WglErr,[Wgeg,Wgl],[Wgeg,Wgl])
        arrCollector[0].append(K)
        arrCollector[1].append(Kerr)
        arrCollector[2].append(Wgeg)
        arrCollector[3].append(WgegErr)
        arrCollector[4].append(Wgl)
        arrCollector[5].append(WglErr)
        
        file.write(f"{fed+1} & {notchAbstand[notch]} & {roundwitherror.round_err(Wgeg,WgegErr)} & {roundwitherror.round_err(Wgl,WglErr)} & {roundwitherror.round_err(K,Kerr)} \\\\ \n")
        print(f"{fed+1} & {notchAbstand[notch]}& {roundwitherror.round_err(Wm,WmErr)} & {roundwitherror.round_err(Ws,WsErr)} & {roundwitherror.round_err(Wgeg,WgegErr)} & {roundwitherror.round_err(Wgl,WglErr)} & {roundwitherror.round_err(K,Kerr)}\\\\ //")
    Kval_[fed].append(arrCollector[0])
    Kval_[fed].append(arrCollector[1])
    Wgeg_[fed].append(arrCollector[2])
    Wgeg_[fed].append(arrCollector[3])
    Wgl_[fed].append(arrCollector[4])
    Wgl_[fed].append(arrCollector[5])
file.close()




#test

plt.style.use("./AKU/AP1_style.mplstyle")


#reg= [stats.linregress(x[0],y[0]),stats.linregress(x[1],y[1])]

#print(reg[0])
fig, ax = plt.subplots()
ax.grid()
errorsOfSlope = []
err1=[[],[]]
sc=[[],[]]
for i in range(2):
    print(notchAbstand)
    print(Kval_[i][1])

    
    err2 =ax.errorbar(notchAbstand,Kval_[i][0],fmt="x",yerr=Kval_[i][1], ecolor = 'black',elinewidth=0.5,capsize=2,capthick=0.5)
    #ax.scatter(notchAbstand,Kval1_[i][0],marker=POINT_STYLE[i+2],color=COLOR_STYLE[i],s=10)
    err1[i]=ax.errorbar(notchAbstand,Kval1_[i][0],fmt="x",yerr=Kval1_[i][1], ecolor=COLOR_STYLE[i],elinewidth=1,capsize=5,capthick=1)
    #ax.plot([X_START,X_END],[reg[i].intercept,reg[i].intercept+X_END*reg[i].slope],linewidth=0.8,color=COLOR_STYLE[i])
    sc[i]=ax.scatter(notchAbstand,Kval_[i][0],marker=POINT_STYLE[i],color=COLOR_STYLE[i],s=15,linewidths=1,edgecolors="black",zorder=10)
plt.legend([sc[0],err1[0],sc[1],err1[1],err2],(r"$K$ Feder1 aus Auf.12 ",r"$K$ Feder1 aus Auf.11 mit Fehler",
                                            r"$K$ Feder2 aus Auf.12",r"$K$ Feder2 aus Auf.11 mit Fehler","Fehlerbalken der von K aus Schwebung"),loc=2)

ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
#plt.title(TITEL,y=1.02)
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

