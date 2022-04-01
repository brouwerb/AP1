
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
        


Feder=2
notch=3
#"./PEN/Rawdata/f1gegn1#1.txt"
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

def sine(x,a,b,c,d):
    return a+b*np.sin(c*(x+d))

def polynom(x,a,b,c,d,e,f,g):
    return a+b*x+c*x**2+d*x**3+e*x**4+f*x**5+g*x**6
    
def polynomByArray(x,popt):
    return polynom(x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6])

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

xy=getPlotable(getData(f"./PEN/Rawdata/f{Feder}gln{notch}#1.txt"))
fig, ax = plt.subplots()



ax.grid()
def change(von,bis):
    popt, perr= optimize.curve_fit(sine,xy[0],xy[1],bounds=((-np.inf,0.2,von,-np.inf),(np.inf,np.inf,bis,np.inf)))
    print(popt)
    xs,ys=genDataFromFunktion(1000,0,60,popt,sineArr)
    return ys


popt, perr= optimize.curve_fit(sine,xy[0],xy[1],bounds=((-np.inf,0.3,3,-np.inf),(np.inf,np.inf,3.2,np.inf)))
print(popt)
xs,ys=genDataFromFunktion(1000,0,60,popt,sineArr)
ax.scatter(xy[0],xy[1],marker=".")
[line] =ax.plot(xs,ys,color ="r")

von_ax  = fig.add_axes([0.25, 0.05, 0.5, 0.03])
vonSl = Slider(von_ax, 'von', 0.1, 5)
bis_ax  = fig.add_axes([0.25, 0, 0.5, 0.03])
bisSl = Slider(bis_ax, 'bis', 0.1, 5)

def sliders_on_changed(val):
    line.set_ydata(change(vonSl.val,bisSl.val))
    fig.canvas.draw_idle()
vonSl.on_changed(sliders_on_changed)
bisSl.on_changed(sliders_on_changed)

fig.set_size_inches(15,6)
plt.show()
