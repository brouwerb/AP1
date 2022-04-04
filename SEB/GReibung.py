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

X_START =20
Y_START =3.15
X_END = 85
Y_END = 4.2
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Winkelgeschwindigkeit $\omega$ rad/s"
X_LABEL = r"Kopplungsradius $r$ in cm"
X_ERROR = 0.02
Y_ERROR = 1
X_MAJOR_TICK = 10
Y_MAJOR_TICK =0.2
X_MINOR_TICK =2
Y_MINOR_TICK = 0.05
SAVE_AS = "./SEB/plotW.pdf"
POINT_STYLE = [4,5,"x","s"]
COLOR_STYLE =["blue","red","green","purple"]

path1 = './SEB/Raw_data/1#1.txt'

def getData(path):
    content=""
    with open (path) as f:
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


fig, ax = plt.subplots()
ax.plot(getPlotable(getData(path1))[0], getPlotable(getData(path1))[1], picker=3)
# plt.show()


# 3, for example, is tolerance for picker i.e, how far a mouse click from
# the plotted point can be registered to select nearby data point/points.

def on_pick(event):
    global points
    line = event.artist
    xdata, ydata = line.get_data()
    print('selected point is:',np.array([xdata[ind], ydata[ind]]).T)

cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()