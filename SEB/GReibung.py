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
from matplotlib.lines import Line2D

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




def onpick1(event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            if ind in selectedpoints:
                selectedpoints.remove(ind)
            else:
                selectedpoints.append(ind)
            selectedpoints.sort()
            
            for i in selectedpoints:
                buff[0].append(getPlotable(getData(path1))[0][ind[0]])
                buff[1].append(getPlotable(getData(path1))[1][ind[0]])

            
            ax.clear() #Funktioniert noch nicht soll eigendlich durch nochmal clicken wieder löschen
            ax.plot(getPlotable(getData(path1))[0], getPlotable(getData(path1))[1], picker=True, pickradius=5)
            ax.scatter(buff[0], buff[1], color=COLOR_STYLE[0])
            print('onpick1 line:', np.column_stack([xdata[ind], ydata[ind]]), ind, buff)
            if len(buff[0]) >= 2:
                pass     
            plt.draw()

fig, ax = plt.subplots()
fig.canvas.mpl_connect('pick_event', onpick1)


# 3, for example, is tolerance for picker i.e, how far a mouse click from
# the plotted point can be registered to select nearby data point/points.

def on_pick(event):
    global points
    line = event.artist
    xdata, ydata = line.get_data()
    print('selected point is:',np.array([xdata[ind], ydata[ind]]).T)

# cid = fig.canvas.mpl_connect('pick_event', on_pick)
#Schleife Funzt nicht, ka wie plt.show() funktioniert, jedenfalls nicht wie ich will
for i in range(4):
    for j in range(3):

        buff = [[], []]

        path1 = f'./SEB/Raw_data/{i+1}#{j+1}.txt'
        ax.plot(getPlotable(getData(path1))[0], getPlotable(getData(path1))[1], picker=True, pickradius=5)
        # plt.show()
        selectedpoints = []
        fig.canvas.mpl_connect('pick_event', onpick1)
        #plt.ioff()
        plt.show()

