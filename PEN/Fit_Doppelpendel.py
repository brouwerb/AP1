
from matplotlib.widgets import Slider
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
import math



Fits =[[[[2.25217312, 0.15    ,   3.31242126 ,0.08173956],[2.18692843 ,0.17566002, 3.53409045, 0.94868202],[2.15121613 ,0.1954903 , 3.86274606, 1.9238661 ]],
        [[2.22778397, 0.16340497 ,3.34592159 ,0.94466359],[2.15304351, 0.15956641, 3.64871821, 2.08355101],[2.12151143 ,0.1640976,  4.08609582 ,1.32476386]]],
        [[[2.25285776, 0.31898153, 3.21498939 ,1.54816277],[2.1859024 , 0.2   ,     3.21621283 ,1.15465449],[2.15143556 ,0.25900279, 3.21602224, 2.50805166]],
        [[ 2.22645115 , 0.36652452 , 3.21525205, -0.46575825],[2.15302248 ,0.37370468 ,3.21634713, 0.04223042],[2.1219952,  0.27536607, 3.21664702, 1.19240415]]]]

SchFits =[[0.21649635036496342,3.2628175485390445,1.3461548783367518,0.04760948905109491,-29.525716261522128,2.2583133943300515],[0.005476556946792009,0.02230598971075557,0.5076961961290818,0.022353509835514276,1.6641814977427751,0.0054805959642909964]]


Feder=1
notch=1
vonsch=0.04
bissch=0.05
vonamp=100
bisamp=101

#"./PEN/Rawdata/f1gegn1#1.txt"
def getData(path):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if i==len(buf)/2:
            break
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

def sine(x,a,b,c,d):
    return a+b*np.sin(c*(x+d))

def dualSine(x,a,b,c,d,e,f):
    return 2* a *np.sin(b*(x+c))*np.sin(d*(x+e))+f

def dualSineArr(x,a):
    return dualSine(x,a[0],a[1],a[2],a[3],a[4],a[5])


def sineArr(x,params):
    return sine(x,params[0],params[1],params[2],params[3])
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
        if i !=len(arr):
            string+=str(I)+","
        else:
            string+=str(I)
    return string



xy=getPlotable(getData(f"./PEN/Rawdata/f{Feder}schn{notch}#1.txt"))
fig, ax = plt.subplots()



ax.grid()
def change(von,bis,von2,bis2,ampvon,ampbis):
    popt, perr= optimize.curve_fit(dualSine,xy[0],xy[1],bounds=((ampvon,von,-np.inf,von2,-np.inf,-np.inf),(ampbis,bis,np.inf,bis2,np.inf,np.inf)))
    print("["+arrToStrin(popt)+","+arrToStrin( np.sqrt(np.diag(pconv)) )+"]")
    xs,ys=genDataFromFunktion(1000,0,100,popt,dualSineArr)
    return ys


popt, pconv= optimize.curve_fit(dualSine,xy[0],xy[1],bounds=((0,2,-np.inf,-np.inf,-np.inf,-np.inf),(0.1,np.inf,np.inf,np.inf,np.inf,np.inf)))

xs,ys=genDataFromFunktion(1000,0,100,popt,sineArr)
ax.scatter(xy[0],xy[1],marker=".")
[line] =ax.plot(xs,ys,color ="r")

von_ax1  = fig.add_axes([0.25, 0.175, 0.5, 0.03])
vonSl1 = Slider(von_ax1, 'f von', 0.1, 5)
bis_ax1  = fig.add_axes([0.25, 0.15, 0.5, 0.03])
bisSl1 = Slider(bis_ax1, 'f bis', 0.1, 5)

von_ax2  = fig.add_axes([0.25, 0.125, 0.5, 0.03])
vonSl2 = Slider(von_ax2, 'f von Sch', 0.001,0.1)
bis_ax2  = fig.add_axes([0.25, 0.1, 0.5, 0.03])
bisSl2 = Slider(bis_ax2, 'f bis Sch', 0.001, 0.1)

von_ax3  = fig.add_axes([0.25, 0.075, 0.5, 0.03])
vonSl3 = Slider(von_ax3, 'amp von', 0.1, 2)
bis_ax3  = fig.add_axes([0.25, 0.05, 0.5, 0.03])
bisSl3 = Slider(bis_ax3, 'amp bis', 0.1, 2)

def sliders_on_changed(val):
    line.set_ydata(change(vonSl1.val,bisSl1.val,vonSl2.val,bisSl2.val,vonSl3.val,bisSl3.val))
    fig.canvas.draw_idle()
vonSl1.on_changed(sliders_on_changed)
bisSl1.on_changed(sliders_on_changed)
vonSl2.on_changed(sliders_on_changed)
bisSl2.on_changed(sliders_on_changed)
vonSl3.on_changed(sliders_on_changed)
bisSl3.on_changed(sliders_on_changed)

fig.set_size_inches(15,6)
plt.subplots_adjust(bottom=0.2)
plt.show()
