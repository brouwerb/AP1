
from matplotlib.widgets import Slider
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
import math

index =1

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


xy=getPlotable(getData(f"./POR/Raw_data/A5{index+1}#1.txt"))
fig, ax = plt.subplots()




ax.grid()
def change(von,bis,von2,bis2,ampvon,ampbis,phasevon,phasebis):
    popt,perr= optimize.curve_fit(expSin,xy[0],xy[1],bounds=((ampvon,von,-np.inf,von2,phasevon,-np.inf),(ampbis,bis,np.inf,bis2,phasebis,np.inf)))
    print("["+arrToStrin(popt)+","+arrToStrin( np.sqrt(np.diag(pconv)) )+"]")
    print(np.sqrt(np.diag(perr)))
    xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
    return ys


popt, pconv= optimize.curve_fit(expSin,xy[0],xy[1],bounds=((0,2,-np.inf,-np.inf,-np.inf,2),(0.1,np.inf,np.inf,np.inf,np.inf,np.inf)))

xs,ys=genDataFromFunktion(1000,0,100,popt,expSinArr)
ax.scatter(xy[0],xy[1],marker=".")
[line] =ax.plot(xs,ys,color ="r")

von_ax1  = fig.add_axes([0.25, 0.175, 0.5, 0.03])
vonSl1 = Slider(von_ax1, 'f von', 0.1, 5)
bis_ax1  = fig.add_axes([0.25, 0.15, 0.5, 0.03])
bisSl1 = Slider(bis_ax1, 'f bis', 0.1, 5)

von_ax2  = fig.add_axes([0.25, 0.125, 0.5, 0.03])
vonSl2 = Slider(von_ax2, 'f von Sch', 0.001,0.5)
bis_ax2  = fig.add_axes([0.25, 0.1, 0.5, 0.03])
bisSl2 = Slider(bis_ax2, 'f bis Sch', 0.001, 0.5)

von_ax3  = fig.add_axes([0.25, 0.075, 0.5, 0.03])
vonSl3 = Slider(von_ax3, 'amp von', 0.001, 1)
bis_ax3  = fig.add_axes([0.25, 0.05, 0.5, 0.03])
bisSl3 = Slider(bis_ax3, 'amp bis', 0.1, 2)

von_ax4  = fig.add_axes([0.25, 0.025, 0.5, 0.03])
vonSl4 = Slider(von_ax4, 'Phaseschw von', 0.1, 100)
bis_ax4  = fig.add_axes([0.25, 0, 0.5, 0.03])
bisSl4 = Slider(bis_ax4, 'Phaseschw bis', 0.1, 100)
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


fig.set_size_inches(15,6)
plt.subplots_adjust(bottom=0.2)
plt.show()
