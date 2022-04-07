
from matplotlib.widgets import Slider
from scipy import optimize ,signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from roundwitherror import *
import math

X_START =0
Y_START =-20
X_END = 100
Y_END = 20
TITEL = ""
Y_LABEL = r"Auslenkung in Grad"
X_LABEL = r"Z"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 5
Y_MAJOR_TICK =0.1
X_MINOR_TICK =1
Y_MINOR_TICK = 0.02
SAVE_AS = "./POR/6fits.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]


indizes = [[90, 1445], [111, 941], [80, 628], [81, 474], [110, 385], [76, 301], [77, 261], [65, 199], [50, 177], [44, 146], [56, 143], [60, 153], [62, 140], [66, 136]]
add = -0.7
faktor =  19/76.96*90/12
print(faktor)
index=12
Fits = [[[154.73762436048682,0.054849598148885875,3.1244232702381853,1.1237581053180126],[1.1906612521705262,0.000592763399204044,0.0006032663507882536,0.007959084129265772]],
        [[154.06736169609215,0.0976611030188857,3.1189030986975985,1.6705252524059255],[0.9030079316745859,0.0007720520228019844,0.000769605919820482,0.005809387722812539]],
        [[170.13702766589137,0.15730574337486858,3.1132535829739156,6.512355833013279],[0.8674664779521798,0.000976957584033556,0.0009789145848029602,0.005092613100903107]],
        [[151.73675851164128,0.23333744669494982,3.1033208715415923,2.585950190456993],[0.48975802557397086,0.0011018852083055101,0.0011862314447617598,0.003722834872722351]],
        [[168.07790999122776,0.33413142667857243,3.088093440723531,1.7919778383794045],[0.5545392151292429,0.0013305956145231058,0.0013606825061372098,0.0033807009684542868]],
        [[213.020716663584,0.4398206873769744,3.067804559130612,6.6759730055131685],[0.6776219502470506,0.0015133300014171433,0.0017370609777783515,0.004078417858929789]],
        [[226.41162418809674,0.5627287239985566,3.097942740691568,6.746199999999998],[2.065890765261605,0.004888053347870577,0.005636702963130184,0.011452384089130338]],
        [[196.0310030652458,0.7096034899707016,2.98232703423731,1.7963411830032212],[0.7933172780371239,0.0038828377049788133,0.0047294183324168935,0.006202418714617093]],
        [[221.5315662413464,0.8611120207219007,2.9423666652131306,1.5778706251561552],[0.8765780226390761,0.003522411503545466,0.004654092488409345,0.0062600834021884315]],
        [[197.89592666934797,1.0302340126925784,2.8910017312650864,2.0784164695636957],[0.7250538117159945,0.005264451147023591,0.006889985553048954,0.006835843432172548]],
        [[455.61741683142964,1.2296041339111183,2.8215497259623334,0.2947010683673322],[3.5994598042781285,0.006726008302795229,0.008119454195382028,0.011919347124249545]],
        [[708.6957999999998,1.429859926596756,2.7531237629103837,6.097415340856622],[7.338739252343618,0.007825952680400577,0.00905219281605659,0.014637138131361664]],
        [[191.73865182443848,1.7041179204817645,2.633596782770586,2.3745193959617974],[0.8521530387775128,0.01099087950372315,0.012157060578385998,0.008964106999388531]],
        [[400.000000000001,2.0635102673910115,2.4899514909277727,1.5282992734461642],[5.913181368979814,0.02167248635941091,0.012639088708100672,0.011877718035721031]],
        ]



#"./PEN/Rawdata/f1gegn1#1.txt"
def getData(path):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if i==len(buf)/1:
            break
        if(i!=0 and i!=len(buf)-1):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content


def getDataVonBisCalcY(path,von,bis,factor,add):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    s = float(buf[von][0])
    for i,I in enumerate(buf):
        if(von<=i and i<=bis):
            buffer=I.split("\t")
            buffer2=[]
            for n,N in enumerate(buffer): 
                
                if n ==1:       
                    buffer2.append((float(N)-add)*factor)
                else:
                    buffer2.append(float(N)-s)
            content.append(buffer2)
    return content

def getPlotable(rData):
    data=[[],[]]
    for i,I in enumerate(rData):
        data[0].append(I[0])
        data[1].append(I[1])
    return data


def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y

def arrToStrin(arr):
    string="["
    for i,I in enumerate(arr):
        if i !=len(arr)-1:
            string+=str(I)+","
        else:
            string+=str(I) +"]"
    return string
def expSin(x,phi,lam,om,be):
    return phi*np.exp(-1*lam*x)*np.cos(om*x+be)
def expSinArr(x,params):
    return expSin(x,params[0],params[1],params[2],params[3])

def getomega(xyn):
    for i in range(len(xy[1])):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind = i
            break
    for i in range(ind + 5, len(xy[1])):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind2 = i
            break
    print(xy[0][ind2]-xy[0][ind])
    return (3.1415*2)/(xy[0][ind2]-xy[0][ind])

def ehoch(x,phi,lam):
    return phi*np.exp(-1*lam*x)
def ehochar(x,params):
    return ehoch(x, params[0], params[1])
popts=[]

    
xy=getPlotable(getDataVonBisCalcY(f"./POR/Raw_data/A5#{index+1}#1.txt",indizes[index-1][0],indizes[index-1][1],faktor,add))
peaks  = signal.find_peaks(xy[1], height = 1)
print(peaks[0])
peaks = peaks[0]
xpeak = []
ypeak = []
for i in peaks:
    xpeak.append(xy[0][i])
    ypeak.append(xy[1][i])
try:
    evar, eerr = optimize.curve_fit(ehoch, xpeak, ypeak)
except:
    evar=[500,1.3]
try:
    omega = getomega(xy)
except:
    omega=3

popt, pconv= optimize.curve_fit(expSin,xy[0],xy[1], bounds=((evar[0]*0.8,evar[1]*0.9,omega*0.8,0),(evar[0]*1.2,evar[1]*1.2,omega*1.15,7)))



err = np.sqrt(np.diag(pconv))
print(popt, err)
popts.append([popt, err])

fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]
xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
exs,eys=genDataFromFunktion(1000,0,100,evar,ehochar)

def change(lamvon,lambis,omvon,ombis,phivon,phibis,bevon,bebis):
    popt,perr= optimize.curve_fit(expSin,xy[0],xy[1],bounds=((phivon,lamvon,omvon,bevon),(phibis,lambis,ombis,bebis)))
    print("["+arrToStrin(popt)+","+arrToStrin( np.sqrt(np.diag(perr)) )+"]")

    xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
    return ys



xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
ax.scatter(xy[0],xy[1],marker=".")
[line] =ax.plot(xs,ys,color ="r")

von_ax1  = fig.add_axes([0.25, 0.175, 0.5, 0.03])
vonSl1 = Slider(von_ax1, 'lam von', 0.01, 10,evar[1]*0.9)
bis_ax1  = fig.add_axes([0.25, 0.15, 0.5, 0.03])
bisSl1 = Slider(bis_ax1, 'lam bis', 0.01, 10,evar[1]*1.1)

von_ax2  = fig.add_axes([0.25, 0.125, 0.5, 0.03])
vonSl2 = Slider(von_ax2, 'f von', 0.001,10,valinit=omega*0.8)
bis_ax2  = fig.add_axes([0.25, 0.1, 0.5, 0.03])
bisSl2 = Slider(bis_ax2, 'f bis ', 0.001, 10,valinit=omega*1.2)

von_ax3  = fig.add_axes([0.25, 0.075, 0.5, 0.03])
vonSl3 = Slider(von_ax3, 'Phi von', 0.001, 1000,evar[0]*0.8)
bis_ax3  = fig.add_axes([0.25, 0.05, 0.5, 0.03])
bisSl3 = Slider(bis_ax3, 'Phi bis', 0.1, 1000,evar[0]*1.2)

von_ax4  = fig.add_axes([0.25, 0.025, 0.5, 0.03])
vonSl4 = Slider(von_ax4, 'be von', 0.1, 10,valinit=0)
bis_ax4  = fig.add_axes([0.25, 0, 0.5, 0.03])
bisSl4 = Slider(bis_ax4, 'be bis', 0.1, 10,valinit=7)
def sliders_on_changed(val):
    line.set_ydata(change(vonSl1.val,bisSl1.val,vonSl2.val,bisSl2.val,vonSl3.val,bisSl3.val,vonSl4.val,bisSl4.val))
    fig.canvas.draw_idle()
vonSl1.on_changed(sliders_on_changed)
bisSl1.on_changed(sliders_on_changed)
vonSl2.on_changed(sliders_on_changed)
bisSl2.on_changed(sliders_on_changed)
vonSl3.on_changed(sliders_on_changed)
bisSl3.on_changed(sliders_on_changed)
vonSl4.on_changed(sliders_on_changed)
bisSl4.on_changed(sliders_on_changed)





ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)

#ax.scatter(xpeak,ypeak,marker='o',color="green", s=100)
#ax.scatter(xy[0][cut(xy)],xy[1][cut(xy)],marker='x',color="orange", s=100)
dat, = ax.plot(xy[0],xy[1],color="blue",linewidth=0.8)
#theo, = ax.plot(xs,ys,color="red",linewidth=0.8)
expf, = ax.plot(exs,eys,color="purple",linewidth=0.8)
#ax.legend([dat,theo, expf],[r"Messdaten",f"Theoriekurve mit $\omega = {round_err(popt[2], err[2])} $", f"einhüllende Expontentialfunktion $ \\varphi = {round_err(evar[0], eerr[0])} \cdot exp({round_err(evar[1], eerr[1])} \cdot x)$"])

ax.set_xlim(xy[0][0],xy[0][-1])
ax.set_ylim(-ehochar(xy[0][0], evar), ehochar(xy[0][0], evar))







fig.set_size_inches(15,6)
plt.subplots_adjust(bottom=0.2)
plt.show()


